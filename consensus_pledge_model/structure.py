from consensus_pledge_model.logic import *
from typing import Callable


def generic_policy(_1, _2, _3, _4) -> dict:
    """Function to generate pass through policy

    Args:
        _1
        _2
        _3
        _4

    Returns:
        dict: Empty dictionary
    """
    return {}


def generate_generic_suf(variable: str) -> Callable:
    """Creates generic function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, _5: (variable, state[variable])


# The partial state update blocks used in the simulation
CONSENSUS_PLEDGE_DEMO_BLOCKS = [
    {
        'label': 'Time Tracking',
        'ignore': True,
        'desc': 'Updates the time in the system',
        'policies': {
            'evolve_time': p_evolve_time
        },
        'variables': {
            'days_passed': s_days_passed,
            'delta_days': s_delta_days
        }
    },
    {
        'label': 'Select Behaviour Params',
        'ignore': True,
        'desc': 'Picks the behavior to be using in the current block',
        'policies': {
        },
        'variables': {
            'behaviour': s_behaviour
        }
    },
    {
        'label': 'Compute Collateral to be paid on this Round',
        'ignore': True,
        'desc': 'The consensus and storage pledge added in this timestep are recorded',
        'policies': {
        },
        'variables': {
            'consensus_pledge_per_new_qa_power': s_consensus_pledge_per_new_qa_power,
            'storage_pledge_per_new_qa_power': s_storage_pledge_per_new_qa_power
        }
    },
    {
        'label': 'Onboard Sectors',
        'desc': 'Adds a new `AggregateSector` to the list',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'aggregate_sectors': s_sectors_onboard
        }
    },
    {
        'label': 'Renew Sectors',
        'desc': 'Updates the Remaining Days to the Default Lifetime',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'aggregate_sectors': s_sectors_renew
        }
    },
    {
        'label': 'Expire Sectors',
        'desc': 'Evolve Sectors Lifetime & Expire them',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'aggregate_sectors': s_sectors_expire
        }
    },
    {
        'label': 'Compute Network Statistics',
        'desc': 'eg. compute QA / RB Network Power',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'power_qa': s_power_qa,
            'power_rb': s_power_rb,
            'baseline': s_baseline
        }
    },
    {
        'label': 'Cummulative Capped Power',
        'desc': 'Update the cummulative capped power from the baseline functions',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'cumm_capped_power': s_cumm_capped_power
        }
    },
    {
        'label': 'Effective Network Time',
        'desc': 'Update the effective network time as defined by baseline functions',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'effective_network_time': s_effective_network_time
        }
    },
    {
        'label': 'Compute Rewards',
        'desc': 'Compute the rewards of this timestep',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'reward': s_reward
        }
    },
    {
        'label': 'Lock / Unlock Rewards',
        'desc': 'Deal with any rewards being unlocked or locked based upon the current sector reward schedules',
        'ignore': True,
        'policies': {
        },
        'variables': {
            'aggregate_sectors': s_sectors_rewards
        }
    },
    {
        'label': 'Distribute Unlocked Rewards & Compute Token Distribution',
        'desc': 'Unlocked Reward = Immediate Rewards + Vested Rewards',
        'ignore': True,
        'policies': {
            'vest_fil': p_vest_fil,
            'burn_fil': p_burn_fil,
            'minted_fil': p_minted_fil
        },
        'variables': {
            'token_distribution': s_token_distribution
        }
    },
]


# CONSENSUS_PLEDGE_DEMO_BLOCKS = [block
#                                 for block
#                                 in CONSENSUS_PLEDGE_DEMO_BLOCKS
#                                 if block.get('ignore', False) == True]


for block in CONSENSUS_PLEDGE_DEMO_BLOCKS:
    # For each block, update the policies and state update variables to be pass through functions if none exist
    policies = block['policies']
    variables = block['variables']
    block['policies'] = {key: generic_policy if policy is None else policy
                         for key, policy in policies.items()}
    block['variables'] = {key: generate_generic_suf(key) if variable is None else variable
                          for key, variable in variables.items()}
