import streamlit as st

# TODO: Re-factor this document to reflect that'we re doing an Consesus Pledge Model

def description():
    st.write(
        """
## Description
        
### Simulation

This app allows you to interactively understand the Consensus Pledge mechanism. You can set the parameters directly in the sidebar, download the currently set parameters to edit them offline and then upload a set of parameters. You can also download the results of the experiment at the very bottom, right after the Glossary. 

### Scenarios

The Consensus Pledge has various interplays between effects and depends on a multitude of factors. As such, its effects are not always very intuitive. The educational calculator can help you to visualize these effects and to consider how various metrics might evolve.
The app displays two scenarios: One for a Filecoin system that requires a Consensus Pledge, and one where there is no more Consensus Pledge required. 

The sidebar on the left lets you set a total time for your simulation and then adjust the scenario for up to five distinct phases. There are five adjustments that can be made for each phase:

I) First, you can adjust the duration of each phase. This lets you test the evolution under various scenarios, for example a long period of consistent growth, with a brief short drop after. 

Then, you can adjust some assumptions about new sectors that are onboarding:

II) The Raw-Byte Power (in PiB) onboarded per day. Varying this lets you test different growth scenarios on a Raw-Byte Basis.

III) The Quality Factor (QF) of this newly onboarded RB Power. The Quality Factor will determine the additional QAP added by the sector, as well as the network QAP over time. The Quality Factor is multiplied with the daily onboarded RBP for each day in the respective phase. In Filecoin+, useful storage - reached through deals with notarized clients - is incentivized through a 10x QAP multiplier. 

Varying the QF lets you experiment with different demand assumptions as well as the effects of potentially accepted Filecoin Improvement Proposals (FIPs) introducing additional multipliers (such as a Sector Duration Multiplier for long-term storage, see [3]).

IV) The Sector Lifetime, measured in days. You can go from the minimum 6 month Sector Lifetime up to a 40 months of Sector Lifetime, incremented in days. 

V) The monthly probability that a sector will be renewed. Each day of the simulation, sectors might be renewed by their providers. Under the hood, this simulation calculates the share of RBP that gets renewed each timestep with a daily probability. Users can set a monthly probability, where a 15% renewal probability on sectors with 180d lifetime would be somewhat analogous to 90% of the related RBP being renewed over their lifetime.  

### References

[1]: Filecoin Consensus Pledge GitHub Repository: https://github.com/BlockScience/filecoin-consensus-pledge-demo

[2]: Filecoin Consensus Pledge (Danilo Lessa Bernardineli, ...): Forthcoming 

[3]: Reviewing the FIP-0056 and CDM Debate on Filecoin
 (BlockScience: Danilo Lessa Bernardineli): https://medium.com/block-science/reviewing-the-fip-0056-and-cdm-debate-on-filecoin-6a6af0ed4b78

### Contributors

This calculator has been developed as part of the ongoing collaboration between BlockScience and Filecoin. We acknowledge the work of the following contributors for making it come to life:

- Will Wolf (BlockScience, ML Engineer)
- Danilo Lessa Bernardineli (BlockScience, Subject Matter Expert)
- Burrrata (BlockScience, Community Lead)
- Jamsheed Shorish (BlockScience, Scientist)
- Jakob Hackel (BlockScience)
- ZX Zhang (Protocol Labs, Research Lead at CryptoEconLab)

### BlockScience
Who Is BlockScience?

BlockScience® is a complex systems engineering, R&D, and analytics firm. Our goal is to combine academic-grade research with advanced mathematical and computational engineering to design safe and resilient socio-technical systems. With deep expertise in Blockchain, Token Engineering, AI, Data Science, and Operations Research, we provide engineering, design, and analytics services to a wide range of clients including for-profit, non-profit, academic, and government organizations.

Our R&D occurs in iterative cycles between open-source research and software development, and application of the research and tools to client-based projects. Our client work includes pre-launch design and evaluation of economic and governance mechanisms based on research, simulation, and analysis. We also provide post-launch monitoring and maintenance via reporting, analytics, and decision support software. With our unique blend of engineering, data science, and social science expertise, the BlockScience team aims to diagnose and solve today’s most challenging frontier socio-technical problems.

We’ve been involved with the Filecoin ecosystem for (as of this writing) over 3 years, and we’ve supported several workstreams both with Protocol Labs and Filecoin Foundation that helped to design, prototype, and monitor the Filecoin Economy as well as more recently to research and analyze governance.

Some of our prior public artifacts include (among others): 

Supporting Filecoin’s economy design before launch: https://www.youtube.com/watch?v=kBzwgfnk91c

Monitoring through the first wave of sector expiration...: https://github.com/filecoin-project/FIPs/issues/56#issuecomment-804841505 

...and the first baseline crossing: https://filecoin.io/blog/posts/filecoin-network-crosses-baseline-sustainability-target-for-first-time/

Describing Filecoin’s Cryptoeconomic Mechanisms in terms of KPIs and Counterfactuals: https://hackmd.io/@bsci-filecoin/measuring-filecoin-cryptoecon

Surfacing High Impact Research Topics for Filecoin Cryptoeconomics: https://hackmd.io/@bsci-filecoin/high-impact-research-2022q4

Support on Design & Optimization for the Retrieval Assurance Protocol: https://hackmd.io/@irenegia/retriev

Building an Educational Calculator for exploring Baseline Minting: https://medium.com/block-science/a-cadcad-interactive-calculator-to-explore-minting-scenarios-in-filecoin-284009a2e941

More about the collaboration can be found in the BlockScience + Filecoin Collaboration Book: https://hackmd.io/@bsci-filecoin/cockpit
    """
    )
