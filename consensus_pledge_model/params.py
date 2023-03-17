from consensus_pledge_model.types import BaselineMinting, Reward, SimpleMinting

from consensus_pledge_model.types import ConsensusPledgeDemoState, ConsensusPledgeParams, ConsensusPledgeSweepParams
from consensus_pledge_model.types import QA_PiB, PiB, Days, FIL, FIL_per_QA_PiB
from consensus_pledge_model.types import TokenDistribution, BehaviouralParams, AggregateSector

# TODO: Upgrade to the Consensus Pledge Model
# TODO: pinpoint the sources for the numerical constants

# TODO: refactor
# DAYS_PER_TIMESTEP = 1
YEAR = 365.25
# SIMULATION_TIME_IN_YEARS = 6
TIMESTEP_IN_DAYS = 7
# TIMESTEPS = int(ceil(SIMULATION_TIME_IN_YEARS * YEAR) / DAYS_PER_TIMESTEP)
TIMESTEPS = int(800 / TIMESTEP_IN_DAYS)
#TIMESTEPS = 35

# BLOCKS_SINCE_LAUNCH = 2_563_129  # Block height used as an reference point
# DAYS_AFTER_LAUNCH = (BLOCKS_SINCE_LAUNCH * 30) / \
#     (60 * 60 * 24)  # Days after launch
# YEARS_AFTER_LAUNCH = DAYS_AFTER_LAUNCH / YEAR


INITIAL_POWER_RB = 16 * 1024
INITIAL_POWER_QA: QA_PiB = 18 * 1024

# Guess-estimate


# Guess-estimate
YEARS_AFTER_LAUNCH = 2
INITIAL_CUMM_CAPPED_POWER = INITIAL_POWER_RB * YEARS_AFTER_LAUNCH * 0.75

SIMPLE_MINTING_MECH = SimpleMinting(time_offset=YEARS_AFTER_LAUNCH)
BASELINE_MINTING_MECH = BaselineMinting(time_offset=YEARS_AFTER_LAUNCH)
INITIAL_EFFECTIVE_NETWORK_TIME: Days = BASELINE_MINTING_MECH.effective_network_time(
    INITIAL_CUMM_CAPPED_POWER)
INITIAL_BASELINE: PiB = BASELINE_MINTING_MECH.baseline_function(0.0)

INITIAL_SIMPLE_REWARD = SIMPLE_MINTING_MECH.issuance(
    0) - SIMPLE_MINTING_MECH.issuance(-1/365.25)
INITIAL_BASELINE_REWARD = BASELINE_MINTING_MECH.issuance(
    INITIAL_EFFECTIVE_NETWORK_TIME) - BASELINE_MINTING_MECH.issuance(INITIAL_EFFECTIVE_NETWORK_TIME - (1/365.25))

LINEAR_DURATION: Days = 180  # Source: Spec

SAMPLES = 1

"""
Note: the previous code from the Baseline Edu Calculator ends here.
"""

# TODO: move from `hack` definitions towards `guess` or `estimate` ones.
# INITIAL_AGGREGATE_SECTORS = AggregateSectorList([]) # Source: hack

INITIAL_COLLATERAL: FIL = 107_204_459.6
INITIAL_LOCKED_REWARDS: FIL = 14_385_576.42
INITIAL_STORAGE_PLEDGE: FIL = INITIAL_COLLATERAL * 0.10
INITIAL_CONSENSUS_PLEDGE: FIL = INITIAL_COLLATERAL * 0.85


MAX_SECTOR_LIFETIME = 360
avg_sector_power_rb = INITIAL_POWER_RB / MAX_SECTOR_LIFETIME
avg_sector_power_qa = INITIAL_POWER_QA / MAX_SECTOR_LIFETIME
avg_sector_storage_pledge = INITIAL_STORAGE_PLEDGE * \
    avg_sector_power_qa / INITIAL_POWER_QA
avg_sector_consensus_pledge = INITIAL_CONSENSUS_PLEDGE * \
    avg_sector_power_qa / INITIAL_POWER_QA


number_of_day_rewards = sum(min(LINEAR_DURATION, sector_lifetime)
                            for sector_lifetime
                            in range(MAX_SECTOR_LIFETIME))
avg_day_reward = INITIAL_LOCKED_REWARDS / number_of_day_rewards


def generate_demo_reward_schedule(sector_lifetime, reward):
    number_of_rewards = min(sector_lifetime, LINEAR_DURATION)
    return {i: reward for i in range(number_of_rewards)}


INITIAL_AGGREGATE_SECTORS = [AggregateSector(avg_sector_power_rb,
                                             avg_sector_power_qa,
                                             sector_lifetime,
                                             avg_sector_storage_pledge,
                                             avg_sector_consensus_pledge,
                                             generate_demo_reward_schedule(sector_lifetime, avg_day_reward))
                             for sector_lifetime in range(1, MAX_SECTOR_LIFETIME)]


INITIAL_TOKEN_DISTRIBUTION: TokenDistribution = TokenDistribution(
    minted=0.0,
    vested=0.0,
    collateral=0.0,
    locked_rewards=0.0,
    burnt=0.0
)

INITIAL_REWARDS: FIL = 0.0  # Source: hack
INITIAL_MINTED = BASELINE_MINTING_MECH.issuance(INITIAL_EFFECTIVE_NETWORK_TIME)
INITIAL_MINTED += SIMPLE_MINTING_MECH.issuance(0)
INITIAL_VESTED: FIL = 0.0  # Source: hack
INITIAL_BURNT: FIL = 0.0  # Source: hack
INITIAL_TOKEN_DISTRIBUTION.update_distribution(new_vested=INITIAL_VESTED,
                                               minted=INITIAL_MINTED,
                                               aggregate_sectors=INITIAL_AGGREGATE_SECTORS,
                                               marginal_burn=INITIAL_BURNT)

DEMO_VESTING_SCHEDULE: dict[Days, FIL] = {}  # TODO: fill in

INITIAL_ONBOARDING_CONSENSUS_PLEDGE: FIL_per_QA_PiB = 0.0  # Source: hack
INITIAL_ONBOARDING_STORAGE_PLEDGE: FIL_per_QA_PiB = 0.0  # Source: hack


INITIAL_BEHAVIOURAL_PARAMS = {
    180: BehaviouralParams('Initial Phase',
                           new_sector_rb_onboarding_rate=1.0,
                           new_sector_quality_factor=2.0,
                           new_sector_lifetime=180,
                           daily_renewal_probability=0.02,
                           renewal_lifetime=180),
    270: BehaviouralParams('Phase 2',
                           new_sector_rb_onboarding_rate=1.0,
                           new_sector_quality_factor=2.0,
                           new_sector_lifetime=360,
                           daily_renewal_probability=0.02,
                           renewal_lifetime=360),
    9999: BehaviouralParams('Phase 3',
                           new_sector_rb_onboarding_rate=50.0,
                           new_sector_quality_factor=2.0,
                           new_sector_lifetime=180,
                           daily_renewal_probability=0.02,
                           renewal_lifetime=180)
}

INITIAL_STATE = ConsensusPledgeDemoState(
    days_passed=0,
    delta_days=TIMESTEP_IN_DAYS,
    aggregate_sectors=INITIAL_AGGREGATE_SECTORS,
    token_distribution=INITIAL_TOKEN_DISTRIBUTION,
    power_qa=INITIAL_POWER_QA,
    power_rb=INITIAL_POWER_RB,
    baseline=INITIAL_BASELINE,
    cumm_capped_power=INITIAL_CUMM_CAPPED_POWER,
    effective_network_time=INITIAL_EFFECTIVE_NETWORK_TIME,
    reward=Reward(INITIAL_SIMPLE_REWARD, INITIAL_BASELINE_REWARD),
    storage_pledge_per_new_qa_power=INITIAL_ONBOARDING_CONSENSUS_PLEDGE,
    consensus_pledge_per_new_qa_power=INITIAL_ONBOARDING_STORAGE_PLEDGE,
    behaviour=None
)

SINGLE_RUN_PARAMS = ConsensusPledgeParams(
    timestep_in_days=TIMESTEP_IN_DAYS,
    vesting_schedule=DEMO_VESTING_SCHEDULE,  # Source: Guess
    target_locked_supply=0.3,  # Source: Spec
    storage_pledge_factor=20,  # Source: Spec
    simple_mechanism=SIMPLE_MINTING_MECH,
    baseline_mechanism=BASELINE_MINTING_MECH,
    baseline_activated=True,
    linear_duration=LINEAR_DURATION,
    immediate_release_fraction=0.25,  # Source: Spec
    behavioural_params=INITIAL_BEHAVIOURAL_PARAMS
)


MULTI_RUN_PARAMS = ConsensusPledgeSweepParams(
    **{k: [v] for k, v in SINGLE_RUN_PARAMS.items()})
MULTI_RUN_PARAMS['target_locked_supply'] = [0.3, 0.0]