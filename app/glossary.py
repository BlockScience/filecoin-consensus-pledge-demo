import streamlit as st


def glossary():
    st.write(
        """
## Glossary

### Network Power

#### Raw Bytes Network Power (RB PiB)

Total network storage capacity. This is the sum total of the active onboarded storage by all miners and sectors.

#### Quality Adjusted Network Power (QAP PiB)

Total network storage capacity adjusted for Quality. In Filecoin Plus, useful storage is incentivized through additional quality multipliers. Storage Deals through notarized Clients, called Verified Deals (VD), receive a 10x multiplier for QAP and earn Storage Providers higher Block Rewards. QAP is used to calculate the probability of being assigned as a block producer and is as such a key metric for consensus power. 

#### Quality Factor (QF)

The average multiplier for a given amount of PiB. This simulation lets users adjust the average QF for newly onboarded sectors, allowing for experimentation with different demand assumptions and the effects of potentially accepted Filecoin Improvement Proposals (FIPs) introducing additional multipliers (such as a Sector Duration Multiplier for long-term storage, see FIP-0056 (SDM)).

### Initial Pledge / Miner Collaterals
When a Storage Provider onboards new storage, they must provide two collaterals serving different functions. Together, these two collaterals form the Initial Pledge that every Storage Provider must provide for onboarding new storage. 

#### Storage Pledge
The Storage Pledge collateral serves to ensure Clients against Storage Provider faults and penalties. The Storage Pledge is computed as an estimate of 20days of Block Rewards earned by the onboarded sector. 

#### Consensus Pledge 
The Consensus Pledge collateral provides additional security against consensus attacks on the network.
The size of the required Consensus Pledge depends on the Target Locked Supply - a governance tunable parameter targetting a certain fraction of the Circulating Supply to be locked up - and the relative size of newly onboarded QAP to Baseline Power or NetworkQAP, whichever is higher.  
More information on the Consensus Pledge and its dynamics can be found in the description and the references. 
It is computed as:

SectorConsensusPledge(t) = TLS * CirculatingSupply(t) * SectorQAP / {max(BaselinePower(t), NetworkQAPEstimate(t)}

### Token Distribution
The distribution of FIL over the ecosystem is constantly evolving and has effects on mechanisms such as the Consensus Pledge. 

#### Available Tokens
All FIL that are currently in "existence", calculated as:

Available FIL = FIL that have been minted + FIL that have been vested - FIL that have been burnt

#### Locked Tokens
Some FIL are not actively in circulation and cannot be used until unlocked.

Locked FIL = Locked Block Rewards + Miner Collaterals 

##### Locked Block Rewards
When a Storage Provider earns Block Rewards, 75% are locked and released linearly over 180 days. The remaining 25% are paid immediately. 

##### Miner Collaterals
When a Storage Provider onboards new storage, they must provide the Storage Pledge and the Consensus Pledge collaterals to ensure safety for Clients and the network. 

#### Circulating Tokens
All the FIL that is in circulation and can be immediately transferred by stakeholders (and attackers, as further seen through the Circulating Surplus metric). This is the supply that users have available for deal-making and actions on the secondary market. 

Circulating FIL = Available FIL - Locked FIL

### Sector Metrics
For simplification, this simulation uses metrics to describe aggregated sector characteristics.

#### Sector Lifetime
The average lifetime of a sector. Within Filecoin, sectors can currently have a lifetime from 6 months up to 42 months. 

#### Monthly Renewal Probability
Sectors in Filecoin can be renewed by their providers at any time. This simulation checks daily on the amount of existing sector PiB that is renewed, depending on the Monthly Renewal Probability set by the user for the respective phase. 

### Security Metrics
The Consensus Pledge serves to protect the network from attackers gaining a 33% share of QAP by significantly increasing the need for FIL to onboard additional storage.

#### Critical Cost
The Critical Cost metric allows users to test how much FIL an attacker would have to acquire to have the means of onboarding enough storage for a share of 33% of Network QAP. 
The Critical Cost is calculated as:

CC = OnboardingPledge per QAP * Network QAP * 1/3 

#### Circulating Surplus
The Circulating Surplus metric divides the Circulating FIL by the Critical Cost and gives users more intuition about the FIL available to attackers and the amount they need. A Critical Surplus of 10 shows that there are 10 FIL in circulation for every 1 FIL that an attacker needs to acquire. A lower Circulating Surplus means that an attacker would need to acquire a larger share of the circulating FIL for their attack. 

### Block Reward

In a given period, the Block Reward is the sum total amount of Filecoin minted through Simple Minting and Baseline Minting mechanisms.

#### Simple Minting

A mechanism for issuing Filecoin as storage mining rewards through a function that decays exponentially with time.

#### Baseline Minting

Similiar to Simple Minting, but uses the concept of an "Effective Network Time," rather than the "time since launch," for issuing rewards. This allows Baseline Minting to dynamically adjust minting depending on the network storage meeting a baseline target.

## References

[1]: Baseline Minting Incentives (Danilo Lessa Bernardineli, Gabriel Lefundes, Burrrata, Jeff Emmett, Jessica Zartler and ZX Zhang). https://medium.com/block-science/baseline-minting-incentives-743b229b9b80

[2]: Reviewing the FIP-0056 and CDM Debate on Filecoin (BlockScience, Danilo Lessa Bernardineli). https://medium.com/block-science/reviewing-the-fip-0056-and-cdm-debate-on-filecoin-6a6af0ed4b78
    """
    )
