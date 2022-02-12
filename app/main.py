import os
import time
import numpy as np
import pandas as pd
import streamlit as st

from chart import (
    NetworkPowerAltairChart,
    MiningUtilityAltairChart
)
from description import description
from glossary import glossary
from stats import stat2meta
from utils import load_constants


C = CONSTANTS = load_constants()
SPEED2LATENCY = {
    "Slow": 1,
    "Medium": C["speed"],
    "Fast": .1
}

# Define layout

st.image(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))

st.markdown("## Description")
with st.expander("See description"):
    description()

st.markdown("## Stats")
stats_dboard = st.empty()

st.markdown("## Graphs")
plot_container = st.container()

st.markdown("## Conclusions")
conclusions_container = st.container()

st.markdown("## Glossary")
glossary_container = st.container()
with glossary_container:
    with st.expander("See glossary"):
        glossary()

st.markdown("## Download")
download_container = st.container()

# Define sidebar

st.sidebar.markdown("# Simulator")

run_simulation = st.sidebar.button("Run")

st.sidebar.markdown("## Progress")

progress_bar = st.sidebar.progress(0)
progress_text = st.sidebar.text("0.0% Complete")

st.sidebar.markdown("## Network Power Parameters")

defaults = C["network_power"]

st.sidebar.markdown("### Independent")

init_power__pib = st.sidebar.slider("Initial Power (PiB)", 0, 4000, defaults["initial_power__pib"], 500)

st.sidebar.markdown("### Chronological")

cross_basefunc_from_above__month = st.sidebar.slider("1️⃣ Cross BaseFunc From Above At (Month)", 0, 24, defaults["cross_basefunc_from_above__month"], 3)

stabilize_below_at__frac = st.sidebar.slider("2️⃣ Stabilize Below At (% of BaseFunc)", 0, 100, int(defaults["stabilize_below_at__frac"] * 100), 10) / 100

cross_basefunc_from_below__month = st.sidebar.slider("3️⃣ Recross BaseFunc From Below At (Month)", 0, 24, defaults["cross_basefunc_from_below__month"], 3)

stabilize_above__month = st.sidebar.slider("4️⃣ Stabilize Above At (Month)", 0, 24, defaults["stabilize_above__month"], 3)

stabilize_above_at__frac = st.sidebar.slider("5️⃣ Stabilize Above At (% of BaseFunc)", 0, 100, int(defaults["stabilize_above_at__frac"] * 100), 10) / 100

st.sidebar.markdown("## Compare Against")

compare_scenario_a = st.sidebar.checkbox('Scenario A')
compare_scenario_b = st.sidebar.checkbox('Scenario B')
compare_scenario_b_star = st.sidebar.checkbox('Scenario B*')

SCENARIO2CHECKBOX = {
    'A': compare_scenario_a,
    'B': compare_scenario_b,
    'B*': compare_scenario_b_star,
}

st.sidebar.markdown("## Speed")

simulation_speed = st.sidebar.selectbox("Simulation Speed", ("Medium", "Fast", "Slow"))

# TODO: parameter validation

# TODO: run simulation

num_steps = C['timesteps'] + 1

def run_dummy_sim(scenario):
    return pd.DataFrame({
        'years_passed': np.linspace(0, 6, num_steps),
        'consensus_power_in_zib': np.random.uniform(0, 100, num_steps),
        'block_reward_in_kfil': np.random.uniform(0, 100, num_steps),
        'marginal_reward_per_power_in_fil_per_pib': np.random.uniform(0, 100, num_steps),
        'utility': np.random.uniform(0, 100, num_steps),
        'scenario': scenario
    })

comparison_dfs = [run_dummy_sim(scenario) for scenario, checked in SCENARIO2CHECKBOX.items() if checked]
comparison_df = pd.concat(comparison_dfs) if comparison_dfs else pd.DataFrame()
df = run_dummy_sim("user")

# Simulate user scenario

prevrow = None

for i in range(num_steps if run_simulation else 1):
    row = df.iloc[[i]]
    # Update stats
    cols = stats_dboard.columns(len(stat2meta))
    for ((stat, meta), col) in zip(stat2meta.items(), cols):
        delta_func = meta.get("delta_func")
        value_func = meta.get("value_func", lambda x: x)
        format_func = meta.get("format_func", lambda x: x)
        if prevrow is not None and delta_func is not None:
            delta = delta_func(row[stat].item(), prevrow[stat].item())
            delta = meta.get("format_func", lambda x: x)(delta)
        else:
            delta = None
        value = format_func(value_func(row[stat]))
        with col:
            st.metric(label=meta["label"], value=value, delta=delta)
    # Update plots
    if i == 0:
        with plot_container:
            network_power_chart = NetworkPowerAltairChart.build(pd.concat([comparison_df, row]), num_steps)
            mining_utility_chart = MiningUtilityAltairChart.build(pd.concat([comparison_df, row]), num_steps)
    else:
        network_power_chart.add_rows(row)
        mining_utility_chart.add_rows(row)
    # Finally
    if run_simulation:
        frac_complete = (i + 1) / num_steps
        time.sleep(SPEED2LATENCY[simulation_speed])
        progress_bar.progress(frac_complete)
        progress_text.text(f"{(frac_complete * 100):.2f}% Complete")
        prevrow = row

# Download data

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


with download_container:
    csv = convert_df(pd.concat([df, comparison_df]))
    st.text("Download raw simulation results as .csv.")
    st.download_button(
        label="Download",
        data=csv,
        file_name='filecoin_basefunc_sim_results.csv',
        mime='text/csv',
    )
