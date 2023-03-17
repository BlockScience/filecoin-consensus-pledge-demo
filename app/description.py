import streamlit as st

# TODO: Re-factor this document to reflect that'we re doing an Consesus Pledge Model

def description():
    st.write(
        """
## Description
        
### Simulations

This app allows you to interactively understand the Consensus Pledge mechanism by showcasing the evolution of various network metrics and comparing them to a world where Filecoin does not require a Consensus Pledge collateral.

You have full control over various parameters to test how the network evolves under different conditions. Additionally, you can set them differently for two phases and test the effects of a changing environment.  

### Scenarios

#### User

The Consensus Pledge has various interplays between effects and depends on a multitude of factors. As such, its effects are not always very intuitive. The educational calculator can help you to visualize these effects and to consider how various metrics might evolve.
The app displays two scenarios: One for a Filecoin system that requires a Consensus Pledge, and one where there is no Consensus Pledge required. 
The sidebar on the left lets you set a total time for your simulation and then adjust the scenario for two distinct phases. There are five adjustments that can be tested for each phase:
I) First, you can adjust the duration of each phase. This lets you test the evolution under various scenarios, for example a long period of consistent growth, with a brief short drop after. 
Then, you can adjust some assumptions about new sectors that are onboarding:
II) The Raw-Byte Power (in PiB) onboarded per day. Varying this lets you test different growth scenarios on a Raw-Byte Basis.
III) The Quality Factor of this newly onboarded RB Power. The Quality Factor will determine the additional QAP added by the sector, as well as the network QAP over time. 
IV) The Sector Lifetime, measured in days. You can go from the minimum 6 month Sector Lifetime up to a full year of Sector Lifetime, incremented in days. 
V) The daily probability that a sector will be renewed. Each day of the simulation, sectors are reaching the end of their lifetime. This parameter lets you vary the likelihood of them being renewed. 

### References

[1]: Filecoin Consensus Pledge GitHub Repository: https://github.com/BlockScience/filecoin-consensus-pledge-demo

[2]: Filecoin Consensus Pledge (Danilo Lessa Bernardineli, ...): 

[3]: Filecoin Network Crosses Baseline Sustainability Target for First Time
 (Danilo Lessa Bernardineli, Gabriel Lefundes, Jamsheed Shorish, ZX Zhang, Michael Zargham): https://filecoin.io/blog/posts/filecoin-network-crosses-baseline-sustainability-target-for-first-time/

[4]: Filecoin Consensus Performance Analysis (Marcel Wursten): https://crypto.unibe.ch/archive/theses/2022.msc.marcel.wuersten.pdf

### Contributors

This calculator has been developed as part of the ongoing collaboration between BlockScience and Filecoin. We acknowledge the work of the following contributors for making it come to life:

- Will Wolf (BlockScience, ML Engineer)
- Danilo Lessa Bernardineli (BlockScience, Subject Matter Expert)
- Burrrata (BlockScience, Community Lead)
- Jamsheed Shorish (BlockScience, Scientist)
- ZX Zhang (Protocol Labs, Research Lead at CryptoEconLab)
    """
    )
