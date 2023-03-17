# Model Spec

[Base Model: Filecoin Baseline Incentives](https://github.com/BlockScience/filecoin-baseline-incentives)

## Assumptions

- All Sectors are Capacity Commitments
- Quality Adjustment can also be applied to CC Sectors
- All sectors have an 6-month lifetime, renewable

## Model Parameters

- `target_locked_supply (%)`
- `storage_pledge_factor (Days)`
- `VestingSchedule (dict[Days, FIL])`
- Reward Schedule Params
    - `linear_duration (Days)`
    - `immediate_release_fraction (%)`
- Behavioural Params
    - `onboarding_rate (PiB/day)`
    - `onboarding_quality_factor ([1, 10])`
    - `daily_renewal_probability (%)`

## World State

- `days_passed (Days)`: Set-up initially to XXX days
- `delta_days (Days)`: Set-up initially to 1 day
- `aggregate_sectors (list[AggregateSector])`
    - `AggregateSector`
        - `rb_power (PiB)`
        - `qa_power (QA-PiB)`
        - `remaining_days (Days)`
        - `storage_pledge (FIL)`
        - `consensus_pledge (FIL)`
        - `collateral_in_fil (metric, FIL)`
        - `RewardSchedule (dict[Days, FIL])`
        - `locked_in_fil (metric, FIL)`
- `token_distribution (dataclass)`
    - `minted (FIL)`: (endogenous)
    - `vested (FIL)`: Set-up initially to XXXX kFIL
    - `collateral (FIL)`: (endogenous)
    - `locked_rewards (FIL)`: (endogenous)
    - `burnt (FIL)`: Set-up initially to XXXX kFIL
    - `locked (metric, FIL)`
    - `available (metric, FIL)`
    - `circulating = (metric, FIL)` 
- From Baseline Edu Calculator
    - `power_qa (QA-PiB)`: (endogenous)
    - `power_rb (PiB)`: (endogenous)
    - `baseline (PiB)`: (endogenous)
    - `cumm_capped_power (PiB*Days)`: (endogenous)
    - `effective_days_passed (Days)`: Set-up initially to XXXX years
    - `reward (tuple[FIL, FIL])`: (endogenous)

### Initializing the `aggregate_sectors` historical data


#### Assumptions
- Network QAP is held constant during the initialization phase
- Storage and Consensus Pledge per Sector is held constant during the initialization phase

#### Sequence

1. Create AggregateSectors with equal sizes and with lifetimes varying from 0 days to 180 days
2. Set-up their collaterals to be constant values
3. Retro-simulate their reward schedules by assuming an constant share of the Network QAP 


## Simulation Sequence

- Time Section
    - Pass Time
    - Evolve Sector Lifetime
- Collateral Metrics Section
    - Initial & Storage Pledge on this Round
- Sector Decisions Section
    - Sector Onboarding Decision
    - Sector Renewal Decision
    - Expire Sectors
- Baseline & Rewards Section
    - RB & QA Power from Sectors
    - Cummulative Capped Power
    - Effective Network Time
    - Reward
- Rewards & Vesting Section
    - Award & Lock Rewards
    - Unlock Scheduled Rewards
    - Vest FIL according to Schedule
- Token Supply Section
    - Compute Token Distribution

## Scenarios

- Standard Scenario
- User Scenario
    - Compared to the Standard Scenario, the TLS is user-provided
- Counterfactual Scenario
    - Compared to the Standard Scenario, the TLS is set to zero



# References

- [Reviewing the Target Locked Supply](/90MrWid8QHejWGAju9EaDw)