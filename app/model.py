
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from cadCAD_tools.execution import easy_run
from consensus_pledge_model.types import ConsensusPledgeSweepParams, BehaviouralParams
from consensus_pledge_model.params import INITIAL_STATE, SINGLE_RUN_PARAMS, TIMESTEP_IN_DAYS
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from utils import load_constants
from copy import deepcopy
from cadCAD_tools.preparation import sweep_cartesian_product
from joblib import Parallel, delayed
from math import inf
C = CONSTANTS = load_constants()
import streamlit as st

@st.cache_resource
def run_cadcad_model(duration_1,
                     new_sector_rb_onboarding_rate_1,
                     new_sector_quality_factor_1,
                     new_sector_lifetime_1,
                     renewal_probability_1,
                     new_sector_rb_onboarding_rate_2,
                     new_sector_quality_factor_2,
                     new_sector_lifetime_2,
                     renewal_probability_2,
                     days):
    
    def run_sim(tls):
        first_year = BehaviouralParams('first_year',
                                                new_sector_rb_onboarding_rate_1,
                                                new_sector_quality_factor_1,
                                                new_sector_lifetime_1,
                                                renewal_probability_1,
                                                new_sector_lifetime_1)
        second_year = BehaviouralParams('second_year',
                                                new_sector_rb_onboarding_rate_2,
                                                new_sector_quality_factor_2,
                                                new_sector_lifetime_2,
                                                renewal_probability_2,
                                                new_sector_lifetime_2)
        params = ConsensusPledgeSweepParams(**{k: [v] for k, v in SINGLE_RUN_PARAMS.items()})
        params['target_locked_supply'] = [tls]
        params["behavioural_params"] = [{duration_1: first_year,
                                        inf: second_year}]


        timesteps = int(days / TIMESTEP_IN_DAYS)
        RUN_ARGS = (deepcopy(INITIAL_STATE), sweep_cartesian_product(params), CONSENSUS_PLEDGE_DEMO_BLOCKS, timesteps, 1)
        
        return easy_run(*RUN_ARGS)

    dfs = Parallel(n_jobs=2)(delayed(run_sim)(i) for i in [0.3, 0.0])
    df = pd.concat(dfs).assign(scenario="").sort_values(['target_locked_supply', 'days_passed'], ascending=False)
    df.loc[df.target_locked_supply == 0.0, 'scenario'] = 'consensus_pledge_off'
    df.loc[df.target_locked_supply == 0.3, 'scenario'] = 'consensus_pledge_on'

    # Post-process results
    df = post_process_results(df)
    
    # Return relevant scenarios
    return df.query('timestep > 1')



def post_process_results(df):

    DROP_COLS = ["reward", 
                 "simple_mechanism", 
                 "baseline_mechanism", 
                 "token_distribution",
                 "aggregate_sectors",
                 "behavioural_params",
                 "vesting_schedule",
                 "behaviour"]

    df = (df
        .assign(initial_pledge_per_new_qa_power=lambda df: df.storage_pledge_per_new_qa_power + df.consensus_pledge_per_new_qa_power)
        .assign(storage_pledge_per_new_rb_power=lambda df: df.storage_pledge_per_new_qa_power * df.power_qa / df.power_rb)
        .assign(consensus_pledge_per_new_rb_power=lambda df: df.consensus_pledge_per_new_qa_power * df.power_qa / df.power_rb)
        .assign(initial_pledge_per_new_rb_power=lambda df: df.initial_pledge_per_new_qa_power * df.power_qa / df.power_rb)
        .assign(daily_simple_reward=lambda df: df.reward.map(lambda x: x.simple_reward)  / TIMESTEP_IN_DAYS)
        .assign(daily_baseline_reward=lambda df: df.reward.map(lambda x: x.baseline_reward) / TIMESTEP_IN_DAYS)
        .assign(fil_locked=lambda df: df.token_distribution.map(lambda x: x.locked))
        .assign(fil_collateral=lambda df: df.token_distribution.map(lambda x: x.collateral))
        .assign(fil_locked_reward=lambda df: df.token_distribution.map(lambda x: x.locked_rewards))
        .assign(fil_circulating=lambda df: df.token_distribution.map(lambda x: x.circulating))
        .assign(fil_available=lambda df: df.token_distribution.map(lambda x: x.available))
        .assign(fil_vested=lambda df: df.token_distribution.map(lambda x: x.vested))
        .assign(fil_minted=lambda df: df.token_distribution.map(lambda x: x.minted))
        .assign(years_passed=lambda x: x.days_passed / C["days_per_year"])
        .assign(critical_cost=lambda df: (df.power_qa * 0.33) * df.initial_pledge_per_new_qa_power)
        .assign(circulating_surplus=lambda df: df.fil_circulating / df.critical_cost)
        .assign(circulating_supply=lambda df: df.fil_circulating / df.fil_available)
        .assign(locked_supply=lambda df: df.fil_locked / df.fil_available)
        .assign(daily_reward=lambda df: df.daily_simple_reward + df.daily_baseline_reward)
        .assign(daily_reward_per_rbp=lambda df: df.daily_reward / df.power_rb)
        .assign(daily_reward_per_qap=lambda df: df.daily_reward / df.power_qa)
        .drop(columns=DROP_COLS)
    )
    return df
