import os
import streamlit as st

from chart import *
from description import description
from glossary import glossary
from model import run_cadcad_model
from utils import load_constants
from consensus_pledge_model.types import BehaviouralParams
from copy import deepcopy
from dataclasses import dataclass
from dataclasses_json import dataclass_json
C = CONSTANTS = load_constants()
import json

# Define layout

st.set_page_config(
    page_title="Filecoin Consensus Pledge Educational Calculator",
    page_icon=os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
    layout="wide",
)

st.markdown("# Filecoin Consensus Pledge Educational Calculator")

st.markdown(
    """
This app allows you to **interactively understand Baseline Minting** through the lens of both mining incentives and **crossing the Baseline Function up or down**.

You have full control over the raw-bytes Network Power trajectory! That's the `user`, and by tweaking the `How long? (in years since last change)` and `rb-NP growth (as a fraction of the baseline growth)` fields for each stage, you can **observe its behavior, and compare to it to that of other baseline scenarios.**
"""
)

with st.expander("See description"):
    description()


st.markdown("## Graphs")
plot_container = st.container()

st.markdown("## Glossary")
glossary_container = st.container()
with glossary_container:
    with st.expander("See glossary"):
        glossary()

st.markdown("## Download")
download_container = st.container()

# Define sidebar
###############
_, image_container, _ = st.sidebar.columns([1, 2, 1])

with image_container:
    st.image(os.path.join(os.path.dirname(__file__), "assets", "icon.png"))

st.sidebar.markdown("""
## Table of Contents

- [Description](#filecoin-consensus-pledge-educational-calculator)
- [Network Power](#network-power)
- [Token Distribution & Supply](#token-distribution-supply)
- [Security](#security)
- [Sector Onboarding](#sector-onboarding)
- [Sector Reward](#sector-reward)
    """)

st.sidebar.markdown("## Sector Onboarding Configuration")

defaults = C


phase_defaults = defaults['phase_config']
phase_count = st.sidebar.slider(
    "Number of Phases", 1, len(phase_defaults), defaults["phase_count"], 1, key="phase_count"
)



def generate_default_phases():
    DEFAULT_PHASES = {}
    DEFAULT_PHASE_DURATIONS = {}
    for i in range(1, len(phase_defaults) + 1):
        phase_default = phase_defaults[i]
        DEFAULT_PHASE_DURATIONS[i] = phase_default['duration']
        params = BehaviouralParams(i, 
                                phase_default['rb_onboarding_rate'], 
                                phase_default['quality_factor'], 
                                phase_default['sector_lifetime'], 
                                phase_default['daily_renewal_probability'] / 100, 
                                phase_default['sector_lifetime'])
        DEFAULT_PHASES[i] = params
    return (DEFAULT_PHASES, DEFAULT_PHASE_DURATIONS)

if ('phases' not in st.session_state) or ('phase_durations' not in st.session_state):
    (phases, phase_durations) = generate_default_phases()
    st.session_state['phases'] = phases
    st.session_state['phase_durations'] = phase_durations
else:
    phases = st.session_state['phases']
    phase_durations = st.session_state['phase_durations']


st.sidebar.markdown(
"""### Phase Configuration""")

option = int(st.sidebar.selectbox(
    'Selected Phase',
    list(phases.keys()),
    label_visibility='visible',
    key='phase_select'))


# phases = deepcopy(phases)
#phase_durations = deepcopy(phase_durations)

phase_durations[option] = st.sidebar.number_input(
    "Duration in Years", 0.0, 4.0, phase_durations[option], 0.25, key=f"{option}_duration"
)

new_sector_onboarding_rate = st.sidebar.number_input(
    "RB Onboarding Rate (PiB)", 0.0, 1000.0, phases[option].new_sector_rb_onboarding_rate, 1.0, key=f"{option}_onboarding_rate"
)

new_sector_quality_factor = st.sidebar.number_input(
    "RB Onboarding QF", 1.0, 20.0, phases[option].new_sector_quality_factor, 0.1, key=f"{option}_quality_factor"
)

new_sector_lifetime = st.sidebar.number_input(
    "New Sector Lifetime", 180, 1200, phases[option].new_sector_lifetime, 1, key=f"{option}_lifetime"
)

monthly_renewal_probability = st.sidebar.number_input(
    "Monthly Renewal Probability (%)", 0.0, 20.0, phases[option].daily_renewal_probability * 100 * 30, 0.5, key=f"{option}_renewal")


renewal_lifetime = phases[option].new_sector_lifetime


label = phases[option].label
phases[option] = BehaviouralParams(label, 
                                   new_sector_onboarding_rate,
                                   new_sector_quality_factor,
                                   new_sector_lifetime,
                                   monthly_renewal_probability / (100 * 30),
                                   renewal_lifetime)

st.session_state['phases'] = phases
st.session_state['phase_durations'] = phase_durations

@dataclass_json
@dataclass
class CalculatorSimParams():
    phase_count: int
    phases: dict[int, BehaviouralParams]
    phase_durations: dict[int, float]

params = CalculatorSimParams(phase_count, phases, phase_durations)

st.sidebar.download_button(
    label="Download Parameters",
    data=params.to_json(),
    file_name="sim_params.json",
    mime="text/json",
)

uploaded_file = st.sidebar.file_uploader(
    label="Read Parameters",
    type=['json']
)

if uploaded_file is not None:
    params = CalculatorSimParams.from_json(uploaded_file.read())
    phase_count = params.phase_count
    phase_durations = params.phase_durations
    phases = params.phases
    st.session_state['phases'] = phases
    st.session_state['phase_durations'] = phase_durations

sim_phase_durations = {k: v for k, v in phase_durations.items() if k <= phase_count}

cumm_years = 0.0
for k, v in sim_phase_durations.items():
    cumm_years += v
    sim_phase_durations[k] = cumm_years
vlines = {f"Phase {k + 1}": v for k, v in sim_phase_durations.items()
          if k >= 1 and k < len(sim_phase_durations)}

sim_phases = {k: v for k, v in phases.items() if k <= phase_count}
# Run model
############

df = run_cadcad_model(sim_phase_durations, sim_phases)

# Plot results
##########

user_df = df.query("scenario == 'consensus_pledge_on'")
with plot_container:
    num_steps = df.timestep.nunique()
    vline = 0 / 365.25 # TODO
    st.markdown("### Network Power")
    network_power_chart = NetworkPowerPlotlyChart.build(user_df, num_steps, vlines)
    qa_power_chart = QAPowerPlotlyChart.build(user_df, num_steps, vlines)

    st.markdown("### Token Distribution & Supply")
    circulating_supply_chart = CirculatingSupplyPlotlyChart.build(df, num_steps, vlines)
    token_dist_chart = TokenDistributionPlotlyChart.build(df, num_steps, vlines)
    locked_token_dist_chart = TokenLockedDistributionPlotlyChart.build(df, num_steps, vlines)

    st.markdown("### Security")
    critical_cost_chart = CriticalCostPlotlyChart.build(df, num_steps, vlines)
    circulating_surplus_chart = CirculatingSurplusPlotlyChart.build(df, num_steps, vlines)

    st.markdown("### Sector Onboarding")
    onboarding_collateral_chart = OnboardingCollateralPlotlyChart.build(df, num_steps, vlines)
    rb_onboarding_collateral_chart = RBOnboardingCollateralPlotlyChart.build(df, num_steps, vlines)
    
    st.markdown("### Sector Reward")
    reward_chart = RewardPlotlyChart.build(user_df, num_steps, vlines)
    reward_per_power_chart = RewardPerPowerPlotlyChart.build(user_df, num_steps, vlines)
    
# Download data


@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")


with download_container:
    csv = convert_df(df)
    st.text("Download raw simulation results as .csv.")
    st.download_button(
        label="Download",
        data=csv,
        file_name="filecoin_basefunc_sim_results.csv",
        mime="text/csv",
    )
