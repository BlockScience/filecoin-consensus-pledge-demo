from collections import OrderedDict
import os
import streamlit as st

from chart import (
    NetworkPowerPlotlyChart,
    MiningUtilityPlotlyChart,
    EffectiveNetworkTimePlotlyChart,
    SimpleRewardPlotlyChart,
    BaselineRewardPlotlyChart,
)
from description import description
from glossary import glossary
from model import run_cadcad_model
from utils import load_constants


C = CONSTANTS = load_constants()


# Define layout

st.set_page_config(layout="wide")

_, image_container, _ = st.columns([1, 4, 1])

with image_container:
    st.image(os.path.join(os.path.dirname(__file__), "assets", "logo.png"), width=800)

st.markdown("# Description")
with st.expander("See description"):
    description()

st.markdown("# Graphs")
plot_container = st.container()

st.markdown("# Conclusions")
conclusions_container = st.container()

st.markdown("# Glossary")
glossary_container = st.container()
with glossary_container:
    with st.expander("See glossary"):
        glossary()

st.markdown("# Download")
download_container = st.container()

# Define sidebar

st.sidebar.markdown("# Simulator")

st.sidebar.markdown("## Network Power Parameters")

defaults = C["network_power"]["pessimistic"]

st.sidebar.text(
    """
The network power changes course.

For each change, we ask:

- When? (Years Since Prev. Change)
- How fast? (Frac. BaseFunc Growth)
"""
)

st.sidebar.markdown("### 1️⃣ Cross BaseFunc From Above")

fall_after_beginning = (
    st.sidebar.slider("When?", 0.0, 8.0, defaults["fall_after_beginning"] / C["days_per_year"], 0.25, key="fall")
    * C["days_per_year"]
)

growth_fall = st.sidebar.slider("How fast?", -0.2, 1.2, defaults["growth_fall"], 0.1, key="fall")

st.sidebar.markdown("### 2️⃣ Stabilize Below BaseFunc")

stable_after_fall = (
    st.sidebar.slider("When?", 0.0, 8.0, defaults["stable_after_fall"] / C["days_per_year"], 0.25, key="stable")
    * C["days_per_year"]
)

growth_stable = st.sidebar.slider("How fast?", -0.2, 1.2, defaults["growth_stable"], 0.1, key="stable")

st.sidebar.markdown("### 3️⃣ Recross BaseFunc from Below")

take_off_after_stable = (
    st.sidebar.slider("When?", 0.0, 8.0, defaults["take_off_after_stable"] / C["days_per_year"], 0.25, key="take_off")
    * C["days_per_year"]
)

growth_take_off = st.sidebar.slider("How fast?", -0.2, 8.0, defaults["growth_take_off"], 0.1, key="take_off")

st.sidebar.markdown("### 4️⃣ Stabilize Above BaseFunc")

steady_after_take_off = (
    st.sidebar.slider("When?", 0.0, 8.0, defaults["steady_after_take_off"] / C["days_per_year"], 0.25, key="steady")
    * C["days_per_year"]
)

growth_steady = st.sidebar.slider("How fast?", -0.2, 1.2, defaults["growth_steady"], 0.1, key="steady")

st.sidebar.markdown("## Compare Against")

SCENARIO2CHECKBOX = OrderedDict(
    {
        "user-baseline-deactivated": st.sidebar.checkbox("User + BaseFunc Deactivated Scenario"),
        "optimistic": st.sidebar.checkbox("Optimistic Scenario"),
        "baseline": st.sidebar.checkbox("BaseFunc Scenario"),
    }
)

# Run model

df = run_cadcad_model(
    fall_after_beginning=fall_after_beginning,
    growth_fall=growth_fall,
    stable_after_fall=stable_after_fall,
    growth_stable=growth_stable,
    take_off_after_stable=take_off_after_stable,
    growth_take_off=growth_take_off,
    steady_after_take_off=steady_after_take_off,
    growth_steady=growth_steady,
)
df = df[df["scenario"].isin(["user"] + [scenario for scenario, checked in SCENARIO2CHECKBOX.items() if checked])]

# Plot results

with plot_container:
    num_steps, = set(df['scenario'].value_counts())
    network_power_chart = NetworkPowerPlotlyChart.build(df, num_steps)
    mining_utility_chart = MiningUtilityPlotlyChart.build(df, num_steps)
    effective_network_time_chart = EffectiveNetworkTimePlotlyChart.build(df, num_steps)
    simple_reward_chart = SimpleRewardPlotlyChart.build(df, num_steps)
    baseline_reward_chart = BaselineRewardPlotlyChart.build(df, num_steps)

# Download data

@st.cache
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
