from typing import Annotated, TypedDict, Union
from math import exp, log, nan
from dataclasses import dataclass

# TODO: Upgrade to the Consensus Pledge Model

# Units
Days = Annotated[float, 'days']
FIL = Annotated[float, "FIL"]
FILYear = Annotated[float, "FIL * Year"] # TODO: check if this is right
PerYear = Annotated[float, "1/year"]
Year = Annotated[float, "year"]
PiB = Annotated[float, "PiB (QA)"]
QA_PiB = Annotated[float, "PiB (QA)"]
PiB_per_Day = Annotated[float, "PiB per Day"]
FIL_per_QA_PiB = Annotated[float, "PiB per Day"]


@dataclass
class Reward():
    simple_reward: FIL = nan
    baseline_reward: FIL = nan

    @property
    def block_reward(self):
        return self.simple_reward + self.baseline_reward


@dataclass
class SimpleMinting():
    time_offset: Year = 0.0
    total_issuance: FIL = 0.33e9
    decay = log(2) / 6.0

    def issuance(self, years_passed: Year) -> FIL:
        issuance_fraction = (1 - exp(-1 * self.decay * (years_passed + self.time_offset)))
        return self.total_issuance * issuance_fraction

    
@dataclass
class BaselineMinting(SimpleMinting):
    # Parameters
    time_offset: Year = 0.0
    total_issuance: FIL = 0.77e9
    decay: float = log(2) / 6.0
    initial_baseline: FIL = 2888
    annual_baseline_growth: Annotated[float, "%/year"] = 1.0
    # gamma: float = 0.0 # TODO

    @property
    def log_baseline_growth(self) -> PerYear:
        return log(1 + self.annual_baseline_growth)

    def effective_network_time(self,
                               cumm_capped_power: FILYear) -> Year:
        g = self.log_baseline_growth
        inner_term = (g * cumm_capped_power / self.initial_baseline)
        return log(1 + inner_term) / g

    def baseline_function(self,
                          years_passed: Year) -> FIL:
        return (self.initial_baseline
                * (1 + self.annual_baseline_growth)
                ** (years_passed + self.time_offset))

    def issuance(self, effective_years_passed: Year) -> FIL:
        issuance_fraction = (1 - exp(-1 * self.decay * effective_years_passed))
        return self.total_issuance * issuance_fraction

    # def effective_time_from_share(self,
    #                               issuance_so_far: FIL) -> Year:
    #     return ((-1 / self.gamma)
    #             * log(1 - issuance_so_far / self.issuance_baseline))


@dataclass
class AggregateSector():
    power_rb: PiB
    power_qa: QA_PiB
    remaining_days: Days
    storage_pledge: FIL
    consensus_pledge: FIL
    # Key indicates Simulation Day on which Value is going to the Circ. Supply
    reward_schedule: dict[Days, FIL]
    
    @property
    def collateral(self) -> FIL:
        return self.storage_pledge + self.consensus_pledge

    @property
    def locked_rewards(self) -> FIL:
        return sum(self.reward_schedule.values())

    @property
    def locked(self) -> FIL:
        return self.collateral + self.locked_rewards


@dataclass
class TokenDistribution():
    minted: float
    vested: float
    collateral: float
    locked_rewards: float
    burnt: float

    def update_distribution(self, 
                            new_vested: float,
                            minted: float,
                            aggregate_sectors: list[AggregateSector],
                            marginal_burn: float = 0.0):
        self.minted = minted
        self.vested += new_vested
        self.collateral = sum(el.collateral for el in aggregate_sectors)
        self.locked_rewards = sum(el.locked_rewards for el in aggregate_sectors)
        self.burnt += marginal_burn
        return self


    @property
    def locked(self) -> FIL:
        return self.locked_rewards + self.collateral

    @property
    def available(self) -> FIL:
        return self.minted + self.vested - self.burnt

    @property
    def circulating(self) -> FIL:
        return self.available - self.locked


@dataclass(frozen=True)
class BehaviouralParams():
    label: str
    new_sector_rb_onboarding_rate: PiB_per_Day
    new_sector_quality_factor: float
    new_sector_lifetime: Days
    renewal_probability: float
    renewal_lifetime: Days

@dataclass
class AggregateSectorList():
    aggregate_sectors: list[AggregateSector]

    @property
    def power_qa(self) -> QA_PiB:
        return sum(agg_sector.power_qa for agg_sector in self.aggregate_sectors)


@dataclass
class Metrics():
    locked_rewards: FIL
    collateral: FIL
    consensus_pledge: FIL
    storage_pledge: FIL

class ConsensusPledgeDemoState(TypedDict):
    days_passed: Days
    delta_days: Days
    aggregate_sectors: list[AggregateSector]
    token_distribution: TokenDistribution
    power_qa: QA_PiB
    power_rb: PiB
    baseline: PiB
    cumm_capped_power: FILYear
    effective_network_time: Year
    reward: Reward
    storage_pledge_per_new_qa_power: FIL_per_QA_PiB
    consensus_pledge_per_new_qa_power: FIL_per_QA_PiB
    behaviour: BehaviouralParams


class ConsensusPledgeParams(TypedDict):
    label: str
    timestep_in_days: Days
    vesting_schedule: dict[Days, FIL] # Days = Days since Simulation Start
    # Collateral Params
    target_locked_supply: float
    storage_pledge_factor: Days
    # Minting Params
    simple_mechanism: object # TODO: re-evaluate it
    baseline_mechanism: object # TODO: re-evaluate it
    baseline_activated: bool
    # Reward Schedule Params
    linear_duration: Days
    immediate_release_fraction: float
    # Behavioural Params   
    behavioural_params: dict[Days, BehaviouralParams]



class ConsensusPledgeSweepParams(TypedDict):
    label: list[str]
    timestep_in_days: list[Days]
    vesting_schedule: list[dict[Days, FIL]] # Days = Days since Simulation Start
    # Collateral Params
    target_locked_supply: list[float]
    storage_pledge_factor: list[Days]
    # Minting Params
    simple_mechanism: list[object] # TODO: re-evaluate it
    baseline_mechanism: list[object] # TODO: re-evaluate it
    baseline_activated: list[bool]
    # Reward Schedule Params
    linear_duration: list[Days]
    immediate_release_fraction: list[float]
    # Behavioural Params   
    behavioural_params: list[dict[Days, BehaviouralParams]]