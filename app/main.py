import os
import streamlit as st

from chart import *
from description import description
from glossary import glossary
from model import run_cadcad_model
from utils import load_constants
from consensus_pledge_model.types import BehaviouralParams
from copy import deepcopy
C = CONSTANTS = load_constants()

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

DEFAULT_PHASES = {}
DEFAULT_PHASE_DURATIONS = {}
for i in range(1, len(phase_defaults) + 1):
    phase_default = phase_defaults[i]
    DEFAULT_PHASE_DURATIONS[i] = phase_default['duration']
    params = BehaviouralParams(i, 
                               phase_default['rb_onboarding_rate'], 
                               phase_default['quality_factor'], 
                               phase_default['sector_lifetime'], 
                               phase_default['renewal_probability'], 
                               phase_default['sector_lifetime'])
    DEFAULT_PHASES[i] = params

if 'phases' not in vars():
    phases = deepcopy(DEFAULT_PHASES)
if 'phase_durations' not in vars():
    phase_durations = deepcopy(DEFAULT_PHASE_DURATIONS)

st.sidebar.markdown(
"""### Phase Configuration""")

option = int(st.sidebar.selectbox(
    'Selected Phase',
    list(phases.keys()),
    label_visibility='visible',
    key='phase_select'))


phases = deepcopy(phases)
phase_durations = deepcopy(phase_durations)

phase_durations[option] = st.sidebar.slider(
    "Duration in Years", 0.0, 4.0, phase_defaults[option]['duration'], 0.25, key=f"{option}_duration"
)

new_sector_onboarding_rate = st.sidebar.slider(
    "RB Onboarding Rate (PiB)", 0.0, 500.0, phase_defaults[option]['rb_onboarding_rate'], 0.1, key=f"{option}_onboarding_rate"
)

new_sector_quality_factor = st.sidebar.slider(
    "RB Onboarding QF", 1.0, 20.0, phase_defaults[option]['quality_factor'], 0.1, key=f"{option}_quality_factor"
)

new_sector_lifetime = st.sidebar.slider(
    "New Sector Lifetime", 180, 360, phase_defaults[option]['sector_lifetime'], 1, key=f"{option}_lifetime"
)
renewal_lifetime = phases[option].new_sector_lifetime

renewal_probability = st.sidebar.slider(
    "Daily Renewal Probability (%)", 0.0, 10.0, phase_defaults[option]['renewal_probability'], 0.1, key=f"{option}_renewal"
)

label = phases[option].label
phases[option] = BehaviouralParams(label, 
                                   new_sector_onboarding_rate,
                                   new_sector_quality_factor,
                                   new_sector_lifetime,
                                   renewal_probability,
                                   renewal_lifetime)

sim_phase_durations = {k: v for k, v in phase_durations.items() if k <= phase_count}
sim_phases = {k: v for k, v in phases.items() if k <= phase_count}

# Run model
############

df = run_cadcad_model(phase_durations, sim_phases)

# Plot results
##########

user_df = df.query("scenario == 'consensus_pledge_on'")
with plot_container:
    num_steps = df.timestep.nunique()
    vline = 0 / 365.25 # TODO
    st.markdown("### Network Power")
    network_power_chart = NetworkPowerPlotlyChart.build(user_df, num_steps, vline)
    qa_power_chart = QAPowerPlotlyChart.build(user_df, num_steps)

    st.markdown("### Token Distribution & Supply")
    circulating_supply_chart = CirculatingSupplyPlotlyChart.build(df, num_steps, vline)
    token_dist_chart = TokenDistributionPlotlyChart.build(df, num_steps, vline)
    locked_token_dist_chart = TokenLockedDistributionPlotlyChart.build(df, num_steps, vline)

    st.markdown("### Security")
    critical_cost_chart = CriticalCostPlotlyChart.build(df, num_steps, vline)
    circulating_surplus_chart = CirculatingSurplusPlotlyChart.build(df, num_steps, vline)

    st.markdown("### Sector Onboarding")
    onboarding_collateral_chart = OnboardingCollateralPlotlyChart.build(df, num_steps, vline)
    rb_onboarding_collateral_chart = RBOnboardingCollateralPlotlyChart.build(df, num_steps, vline)
    
    st.markdown("### Sector Reward")
    reward_chart = RewardPlotlyChart.build(user_df, num_steps, vline)
    reward_per_power_chart = RewardPerPowerPlotlyChart.build(user_df, num_steps, vline)
    
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
