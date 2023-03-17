from cadCAD_tools.types import Signal, VariableUpdate
from consensus_pledge_model.params import YEAR
from collections import defaultdict
from copy import copy, deepcopy
from consensus_pledge_model.types import *
import scipy.stats as st

# ## Time Tracking


def p_evolve_time(params: ConsensusPledgeParams,
                  _2,
                  _3,
                  _4) -> Signal:
    """Update the timesteps in the day

    Args:
        params (ConsensusPledgeParams): System parameters
        _2 
        _3 
        _4 

    Returns:
        Signal: The number of days that are added in the epoch
    """
    return {'delta_in_days': params['timestep_in_days']}


def s_days_passed(_1,
                  _2,
                  _3,
                  state: ConsensusPledgeDemoState,
                  signal: Signal) -> VariableUpdate:
    """State update for the number of days passed

    Args:
        _1
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: The updates to the days passed variable
    """
    # Simply add the delta days to current days passed
    value = state['days_passed'] + signal['delta_in_days']
    return ('days_passed', value)


def s_delta_days(_1,
                 _2,
                 _3,
                 state: ConsensusPledgeDemoState,
                 signal: Signal) -> VariableUpdate:
    """Simple state update to keep track of delta days assumption

    Args:
        _1
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: The updates to the delta_in_days variable
    """

    value = signal['delta_in_days']
    return ('delta_days', value)


def s_behaviour(params: ConsensusPledgeParams,
                _2,
                _3,
                state: ConsensusPledgeDemoState,
                signal: Signal) -> VariableUpdate:
    """State update for what the current behavior is

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: The update to the behaviour variable
    """

    # Pull out behavioural_params from params
    behaviour_params = params['behavioural_params']

    # Filter behaviors to only be ones where the key is greater than days passed
    filtered_params = {
        k: v for k, v in behaviour_params.items() if k >= state['days_passed']}

    # Grab the first element (latest relevant behavior where key > days_passed)
    value = list(filtered_params.values())[0]

    return ('behaviour', value)

# ## Network


def s_power_qa(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState,
               signal: Signal) -> VariableUpdate:
    """State update for the current quality adjusted power

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: The update to the power_qa variable
    """
    value = sum(s.power_qa for s in state['aggregate_sectors'])
    return ('power_qa', value)


def s_power_rb(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState,
               signal: Signal) -> VariableUpdate:
    """State update for the current power

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: The update to the power_rb variable
    """
    value = sum(s.power_rb for s in state['aggregate_sectors'])
    return ('power_rb', value)


def s_baseline(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState,
               signal: Signal) -> VariableUpdate:
    """Function to update the current baseline

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: Update for the current baseline
    """
    # Get the number of baseline years
    days_passed = state['days_passed']
    DAYS_TO_YEARS = 1 / 365.25
    baseline_years = days_passed * DAYS_TO_YEARS

    # Find the baseline value at the current number of baseline years
    value = params['baseline_mechanism'].baseline_function(
        baseline_years)
    return ('baseline', value)


def s_cumm_capped_power(params: ConsensusPledgeParams,
                        _2,
                        _3,
                        state: ConsensusPledgeDemoState,
                        signal: Signal) -> VariableUpdate:
    """Function for finding the cummulative capped power

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: The cumm_capped_power variable update
    """
    DAYS_TO_YEARS = 1 / YEAR
    dt = params['timestep_in_days'] * DAYS_TO_YEARS
    current_power = state['power_rb']

    # If the baseline_activated then capped_power is bounded to be the baseline
    if params['baseline_activated'] is True:
        capped_power = min(current_power, state['baseline'])
    else:
        capped_power = state['baseline']

    # Add the capped_power over the time delta to the cummulative
    cumm_capped_power_differential = capped_power * dt
    new_cumm_capped_power = state['cumm_capped_power'] + \
        cumm_capped_power_differential
    return ('cumm_capped_power', new_cumm_capped_power)


def s_effective_network_time(params: ConsensusPledgeParams,
                             _2,
                             history: list[list[ConsensusPledgeDemoState]],
                             state: ConsensusPledgeDemoState,
                             signal: Signal) -> VariableUpdate:
    """The update function for effective network time

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        history (list[list[ConsensusPledgeDemoState]]): History of the states of the system
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: Variable update for effective_network_time
    """
    # Calculate through the baseline mechanism parameter
    value = params['baseline_mechanism'].effective_network_time(
        state['cumm_capped_power'])

    return ('effective_network_time', value)


def s_reward(params: ConsensusPledgeParams,
             _2,
             history: list[list[ConsensusPledgeDemoState]],
             state: ConsensusPledgeDemoState,
             signal: Signal) -> VariableUpdate:
    """Function which updates the reward

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        history (list[list[ConsensusPledgeDemoState]]): History of the states of the system
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: Variable update for the reward
    """
    # Simple Minting
    simple_mechanism = params['simple_mechanism']
    t_i = history[-1][-1]['days_passed'] / YEAR
    t_f = state['days_passed'] / YEAR

    simple_issuance_start = simple_mechanism.issuance(t_i)
    simple_issuance_end = simple_mechanism.issuance(t_f)
    simple_reward = simple_issuance_end - simple_issuance_start

    # Baseline Minting
    baseline_mechanism = params['baseline_mechanism']
    eff_t_i = history[-1][-1]['effective_network_time']
    eff_t_f = state['effective_network_time']

    baseline_issuance_start = baseline_mechanism.issuance(eff_t_i)
    baseline_issuance_end = baseline_mechanism.issuance(eff_t_f)
    baseline_reward = baseline_issuance_end - baseline_issuance_start

    # Wrap everything together
    reward = Reward(simple_reward, baseline_reward)
    return ('reward', reward)


def s_consensus_pledge_per_new_qa_power(params: ConsensusPledgeParams,
                                        _2,
                                        _3,
                                        state: ConsensusPledgeDemoState,
                                        _5) -> VariableUpdate:
    """Function which updates consensus_pledge_per_new_qa_power

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        _5

    Returns:
        VariableUpdate: Variable update for the consensus_pledge_per_new_qa_power
    """

    # Find total locked supply
    value = params['target_locked_supply']
    value *= state['token_distribution'].circulating

    # Find locked supply per quality adjusted power
    value /= max(state['baseline'], state['power_qa'])
    return ('consensus_pledge_per_new_qa_power', value)


def s_storage_pledge_per_new_qa_power(params: ConsensusPledgeParams,
                                      _2,
                                      history: dict[list, dict[list, ConsensusPledgeDemoState]],
                                      state: ConsensusPledgeDemoState, _5) -> VariableUpdate:
    """SP per Sector = Estimated 20 days of daily BR for the Sector
    SP this round = OnboardingNetworkQAP * 20 * DailyBR / ExistingNetworkQAP
    What should be returned: 20 * DailyBR / CurrentNetworkQAP

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        history (dict[list, dict[list, ConsensusPledgeDemoState]]): History of the states of the system
        state (ConsensusPledgeDemoState): The current state of the system
        _5

    Returns:
        VariableUpdate: Variable update for the storage_pledge_per_new_qa_power
    """

    # Find estimate of daily rewards
    current_reward = state["reward"].block_reward
    dt = state['delta_days']
    daily_reward_estimate = current_reward / dt

    # Find 20D daily reward divided by power_qa
    value = daily_reward_estimate
    value *= 20.0
    value /= state["power_qa"]

    return ('storage_pledge_per_new_qa_power', value)


def s_sectors_onboard(params: ConsensusPledgeParams,
                      _2,
                      _3,
                      state: ConsensusPledgeDemoState,
                      signal: Signal) -> VariableUpdate:
    """Onboard sectors

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: VariableUpdate for aggregate_sectors
    """

    current_sectors_list = state['aggregate_sectors'].copy()

    # Sector Properties
    power_rb_new = state['behaviour'].new_sector_rb_onboarding_rate * \
        state['delta_days']
    power_qa_new = power_rb_new * state['behaviour'].new_sector_quality_factor

    if power_rb_new > 0.0:
        # Find what the pledges should be
        storage_pledge = state['storage_pledge_per_new_qa_power'] * power_qa_new
        consensus_pledge = state['consensus_pledge_per_new_qa_power'] * power_qa_new
        # Create new aggregate sector
        reward_schedule = {}
        new_sectors = AggregateSector(power_rb=power_rb_new,
                                      power_qa=power_qa_new,
                                      remaining_days=state['behaviour'].new_sector_lifetime,
                                      storage_pledge=storage_pledge,
                                      consensus_pledge=consensus_pledge,
                                      reward_schedule=reward_schedule)
        current_sectors_list.append(new_sectors)
    else:
        pass

    return ('aggregate_sectors', current_sectors_list)


def s_sectors_renew(params,
                    _2,
                    _3,
                    state: ConsensusPledgeDemoState,
                    signal: Signal) -> VariableUpdate:
    """Function to take care of sector renewals

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: VariableUpdate for aggregate_sectors
    """

    # Find share of renewals

    # Assumption: Sectors are going to perform a `delta_days` amount of
    # independent trials when renewing. It is possible that a sector
    # renews more than 1x on a given timestep.
    #renew_share = state['behaviour'].daily_renewal_probability * state['delta_days']

    # Assumption: Sectors are going to attempt to renew daily until they're successful.
    # No more attempts through the timestep will be done after that.
    renew_share = st.binom.pmf(k=1, n=state['delta_days'], p=state['behaviour'].daily_renewal_probability)
    current_sectors_list = state['aggregate_sectors'].copy()

    if renew_share > 0:
        power_rb_renew: PiB = 0.0
        power_qa_renew: QA_PiB = 0.0
        reward_schedule_renew = defaultdict(FIL)

        for _, aggregate_sector in enumerate(current_sectors_list):
            # Retrieve renew values
            sector_power_rb_renew = aggregate_sector.power_rb * renew_share
            sector_power_qa_renew = aggregate_sector.power_qa * renew_share
            sector_storage_pledge_renew = aggregate_sector.storage_pledge * renew_share
            sector_consensus_pledge_renew = aggregate_sector.consensus_pledge * renew_share
            sector_schedule_renew = {k: v * renew_share
                                     for k, v
                                     in aggregate_sector.reward_schedule.items()}

            # Assign values to the new renewed sectors
            power_rb_renew += sector_power_rb_renew
            power_qa_renew += sector_power_qa_renew

            # Subtract values from the non-renewed sectors
            aggregate_sector.power_rb -= sector_power_rb_renew
            aggregate_sector.power_qa -= sector_power_qa_renew
            aggregate_sector.storage_pledge -= sector_storage_pledge_renew
            aggregate_sector.consensus_pledge -= sector_consensus_pledge_renew

            # Storage & Consensus Pledge are going to be recomputed
            # after the for-loop
            for k, v in sector_schedule_renew.items():
                reward_schedule_renew[k] += v
                aggregate_sector.reward_schedule[k] -= v

        # Compute Pledges
        storage_pledge_renew = 0.0
        consensus_pledge_renew = 0.0

        storage_pledge_renew = state['storage_pledge_per_new_qa_power']
        storage_pledge_renew *= power_qa_renew

        consensus_pledge_renew = state['consensus_pledge_per_new_qa_power']
        consensus_pledge_renew *= power_qa_renew

        reward_schedule_renew = dict(reward_schedule_renew)

        # Create new sector representing the Renewed Sectors
        new_sectors = AggregateSector(power_rb=power_rb_renew,
                                      power_qa=power_qa_renew,
                                      remaining_days=state['behaviour'].renewal_lifetime,
                                      storage_pledge=storage_pledge_renew,
                                      consensus_pledge=consensus_pledge_renew,
                                      reward_schedule=reward_schedule_renew)
        current_sectors_list.append(new_sectors)
    else:
        pass

    return ('aggregate_sectors', current_sectors_list)


def s_sectors_expire(_1,
                     _2,
                     _3,
                     state: ConsensusPledgeDemoState,
                     signal: Signal) -> VariableUpdate:
    """Function which updates for sectors expiring. The assumption is that that locked rewards are going to be released.

    Args:
        _1
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: VariableUpdate for aggregate_sectors
    """

    current_sectors_list = state['aggregate_sectors'].copy()
    expired_sectors_indices = []

    # If remaining days are below zero, get their index for removing from the
    # active sectors list. Else, reduce their lifetime
    for i, aggregate_sector in enumerate(current_sectors_list):
        if aggregate_sector.remaining_days < 0:
            expired_sectors_indices.append(i)
        else:
            aggregate_sector.remaining_days -= state['delta_days']

    # Expire them
    for i_expired in sorted(expired_sectors_indices, reverse=True):
        current_sectors_list.pop(i_expired)
        # Implicit action: Locked Rewards & Collaterals enter Circulating Supply

    return ('aggregate_sectors', current_sectors_list)


def s_sectors_rewards(params: ConsensusPledgeParams,
                      _2,
                      _3,
                      state: ConsensusPledgeDemoState,
                      signal: Signal) -> VariableUpdate:
    """Function for computing the sector rewards

    Parts for what this SUF represents for each AggregateSector Schedule:
    Part 1 - Unlock Current Rewards. eg. {0: 5, 1: 10, 2: 20} -> {1: 10, 2: 20}
    NOTE: Unlocking only adds them back to circulating. Can remove item at index 0, since
    we must update at every timestep anyways, and new rewards are only added from the timestep forward
    Part 2 - Shift Reward Schedule. eg. {1: 10, 2: 20} -> {0: 10, 1: 20}
    Part 3 - Lock New Rewards. eg. {0: 10, 1: 20} -> {0: 15, 1: 25, 2: 5}

    1. Retrieve the Total Rewards during this timestep
    2. Iterate across the `AggregateSectors`
    3. Get their share of the Network QA Power: this is the % of the total reward
    due to them.
    4. For the Sector Total Reward, modify the reward schedule so that it incorporates them

    Eg. LINEAR_DURATION = 180 days means that the Total Reward should be split
    between 180 days. For 1 Timestep = 1 Day, that's 180 ts.

    Suppose LINEAR_DURATION = 3 days
    & sector_reward = 15 <=> sector_reward_per_day = 5
    & reward_schedule_init = {0: 20, 1: 30, 2: 40, 3: 50}
    then
    reward_schedule_final = {0: 20 + 5, 1: 30 + 5, 2: 40 + 5, 3: 50}

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: VariableUpdate for aggregate_sectors
    """

    # Retrieve total rewards
    total_reward = state["reward"].block_reward
    linear_duration = params["linear_duration"]
    current_sector_list = state["aggregate_sectors"].copy()
    total_qa = state["power_qa"]
    immediate_release = params["immediate_release_fraction"]
    days_passed = state['days_passed']

    for agg_sector in current_sector_list:
        reward_schedule = agg_sector.reward_schedule
        # get share of total reward
        sector_qa = agg_sector.power_qa
        share_qa = sector_qa / total_qa
        available_reward = total_reward * (1.0 - immediate_release)
        share_reward = share_qa * available_reward
        daily_reward = share_reward / linear_duration
        # create new reward schedule dict to be merged
        today_reward_schedule = {k + days_passed: daily_reward
                                 for k
                                 in range(linear_duration)}
        # new method of transforming the dict
        new_reward_schedule = {k: v
                               for k, v
                               in reward_schedule.items() if k > days_passed}

        # create new dict, and adds the values from shifted reward schedule and
        # newly created reward schedule
        reward_days = set(new_reward_schedule | today_reward_schedule)
        updated_reward_schedule = {unlock_day: new_reward_schedule.get(
            unlock_day, 0.0) + today_reward_schedule.get(unlock_day, 0.0)
            for unlock_day
            in reward_days}

        agg_sector.reward_schedule = updated_reward_schedule

    return ('aggregate_sectors', current_sector_list)


def p_vest_fil(params: ConsensusPledgeParams,
               _2,
               _3,
               state: ConsensusPledgeDemoState) -> VariableUpdate:
    """Function for computation of fil to vest

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system

    Returns:
        VariableUpdate: VariableUpdate for fil_to_vest
    """
    now = state['days_passed']
    value = params['vesting_schedule'].get(now, 0.0)
    return {'fil_to_vest': value}


def p_burn_fil(_1,
               _2,
               _3,
               state: ConsensusPledgeDemoState) -> VariableUpdate:
    """Function for finding fil to burn

    Args:
        _1
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system

    Returns:
        VariableUpdate: VariableUpdate for fil_to_burn
    """
    return {'fil_to_burn': 0.0}


def p_minted_fil(params: ConsensusPledgeParams,
                 _2,
                 _3,
                 state: ConsensusPledgeDemoState) -> VariableUpdate:
    """Function for finding fil to mint

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system

    Returns:
        VariableUpdate: VariableUpdate for fil_minted
    """

    value = params['simple_mechanism'].issuance(
        state['effective_network_time'])
    value += params['baseline_mechanism'].issuance(
        state['effective_network_time'])
    return {'fil_minted': value}


def s_token_distribution(params: ConsensusPledgeParams,
                         _2,
                         _3,
                         state: ConsensusPledgeDemoState,
                         signal: Signal) -> VariableUpdate:
    """Find the new token distribution

    Args:
        params (ConsensusPledgeParams): System parameters
        _2
        _3
        state (ConsensusPledgeDemoState): The current state of the system
        signal (Signal): The signal created from policies in this substep

    Returns:
        VariableUpdate: Update the token_distribution variable
    """
    distribution = copy(state["token_distribution"])
    rewards = state["reward"].block_reward
    aggregate_sectors = state["aggregate_sectors"]
    burn = signal.get('fil_to_burn', 0.0)
    today_vested = signal.get("fil_to_vest", 0.0)

    distribution.update_distribution(
        new_vested=today_vested,
        minted=signal.get('fil_minted', None),
        aggregate_sectors=aggregate_sectors,
        marginal_burn=burn)

    return ('token_distribution', distribution)
