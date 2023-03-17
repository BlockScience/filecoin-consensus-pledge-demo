import pandas as pd
from consensus_pledge_model.params import INITIAL_STATE
from consensus_pledge_model.params import SINGLE_RUN_PARAMS
from consensus_pledge_model.structure import CONSENSUS_PLEDGE_DEMO_BLOCKS
from cadCAD_tools import easy_run
from pandas import DataFrame


def standard_run() -> DataFrame:
    """Function which runs the cadCAD simulations

    Returns:
        DataFrame: A dataframe of simulation data
    """
    # The number of timesteps for each simulation to run
    N_timesteps = 360

    # The number of monte carlo runs per set of parameters tested
    N_samples = 1
    # %%
    # Get the sweep params in the form of single length arrays
    sweep_params = {k: [v] for k, v in SINGLE_RUN_PARAMS.items()}

    # Load simulation arguments
    sim_args = (INITIAL_STATE,
                sweep_params,
                CONSENSUS_PLEDGE_DEMO_BLOCKS,
                N_timesteps,
                N_samples)

    # Run simulation
    sim_df = easy_run(*sim_args)
    return sim_df
