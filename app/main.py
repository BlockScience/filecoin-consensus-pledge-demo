import os
import streamlit as st

from chart import *
from description import description
from glossary import glossary
from model import run_cadcad_model
from utils import load_constants

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

years = st.sidebar.slider(
    "Simulation Duration in Years", 0.0, 10.0, defaults["years"], 0.25, key="years"
)
days = years * 366

st.sidebar.markdown(
"""### Phase 1"""
)

duration_1_years = st.sidebar.slider(
    "Duration in Days", 0.0, years, defaults["duration_1"], 0.1, key="duration_1"
)
duration_1 = duration_1_years * 365.5

new_sector_rb_onboarding_rate_1 = st.sidebar.slider(
    "RB Onboarding Rate (PiB)", 0.0, 500.0, defaults["new_sector_rb_onboarding_rate_1"], 0.1, key="new_sector_rb_onboarding_rate_1"
)

new_sector_quality_factor_1 = st.sidebar.slider(
    "RB Onboarding QF", 1.0, 20.0, defaults["new_sector_quality_factor_1"], 0.1, key="new_sector_quality_factor_1"
)

new_sector_lifetime_1 = st.sidebar.slider(
    "New Sector Lifetime", 180, 360, defaults["new_sector_lifetime_1"], 1, key="new_sector_lifetime_1"
)

daily_renewal_probability_1 = st.sidebar.slider(
    "Daily Renewal Probability (%)", 0.0, 10.0, defaults["daily_renewal_probability_1"], 0.1, key="daily_renewal_probability_1"
)

st.sidebar.markdown(
"""### Phase 2"""
)

new_sector_rb_onboarding_rate_2 = st.sidebar.slider(
    "RB Onboarding Rate (PiB)", 0.0, 500.0, defaults["new_sector_rb_onboarding_rate_2"], 0.1, key="new_sector_rb_onboarding_rate_2"
)

new_sector_quality_factor_2 = st.sidebar.slider(
    "RB Onboarding QF", 1.0, 20.0, defaults["new_sector_quality_factor_2"], 0.1, key="new_sector_quality_factor_2"
)

new_sector_lifetime_2 = st.sidebar.slider(
    "New Sector Lifetime", 180, 360, defaults["new_sector_lifetime_2"], 1, key="new_sector_lifetime_2"
)

daily_renewal_probability_2 = st.sidebar.slider(
    "Daily Renewal Probability (%)", 0.0, 10.0, defaults["daily_renewal_probability_2"], 0.1, key="daily_renewal_probability_2"
)

# st.sidebar.markdown("## Compare Against")

# SCENARIO2CHECKBOX = OrderedDict(
#     {
#         "user-baseline-deactivated": st.sidebar.checkbox("User + BaseFunc Deactivated Scenario", value=True),
#         "optimistic": st.sidebar.checkbox("Optimistic Scenario", value=True),
#         "baseline": st.sidebar.checkbox("BaseFunc Scenario", value=True),
#     }
# )

# Run model
############

df = run_cadcad_model(duration_1, new_sector_rb_onboarding_rate_1, new_sector_quality_factor_1, new_sector_lifetime_1, daily_renewal_probability_1 / 100,
                      new_sector_rb_onboarding_rate_2, new_sector_quality_factor_2, new_sector_lifetime_2,
                       daily_renewal_probability_2 / 100, days)

# Plot results
##########

user_df = df.query("scenario == 'consensus_pledge_on'")
with plot_container:
    num_steps = df.timestep.nunique()
    vline = duration_1 / 365.25
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
