# Filecoin Consensus Pledge Interactive Calculator

## Executive Summary

This github repository hosts both the cadCAD model for monitoring consensus pledge as well as the streamlit dashboard which displays it. Economic incentives can be explored through scenario analysis which cadCAD supports using monte carlo simulations

## How to run it

- Option 1 (CLI): Just pass `python -m consensus_pledge_model`
This will generate an pickled file at `data/simulations/` using the default single run
system parameters & initial state.
    - To perform a multiple run, pass `python -m consensus_pledge_model -e`
- Option 2 (cadCAD-tools easy run method): Import the objects at `consensus_pledge_model/__init__.py`
and use them as arguments to the `cadCAD_tools.execution.easy_run` method. Refer to `consensus_pledge_model/__main__.py` to an example.
- Option 3 (Streamlit, local)
    - `streamlit run app/main.py`
- Option 4 (Streamlit, cloud)
    1. Fork the repo
    2. Go to https://share.streamlit.io/ and log in
    3. Create an app for the repo pointing to `app/main.py`
    4. **Make sure to use Python 3.9 on the Advanced Settings!**
    5. Wait a bit and done!

## File structure

```
.
├── LICENSE
├── README.md
├── SPEC.md
├── app: The `streamlit` app
│   ├── assets
│   │   ├── icon.png
│   │   └── logo.png
│   ├── chart.py
│   ├── const.yaml
│   ├── description.py
│   ├── glossary.py
│   ├── main.py
│   ├── model.py
│   └── utils.py
├── consensus_pledge_model: the `cadCAD` model as encapsulated by a Python Module
│   ├── __init__.py
│   ├── __main__.py
│   ├── experiment.py: Code for running experiments
│   ├── logic.py: All logic for substeps
│   ├── params.py: System parameters
│   ├── structure.py: The PSUB structure
│   └── types.py: Types used in model
├── notebooks: Notebooks for aiding in development
│   ├── Testing.ipynb
│   ├── nb_test_consensus_pledge_demo.py
│   └── simulation_eda.ipynb
├── profiling
│   ├── output.png
│   ├── output.pstats
│   └── profile_default_run.sh
├── requirements-dev.txt: Dev requirements
├── requirements.txt: Production requirements
└── tests: Test scenarios
    ├── __init__.py
    └── test_scenario.py
```

## What is cadCAD
## Installing cadCAD for running this repo

### 1. Pre-installation Virtual Environments with [`venv`](https://docs.python.org/3/library/venv.html) (Optional):
It's a good package managing practice to create an easy to use virtual environment to install cadCAD. You can use the built in `venv` package.

***Create** a virtual environment:*
```bash
$ python3 -m venv ~/cadcad
```

***Activate** an existing virtual environment:*
```bash
$ source ~/cadcad/bin/activate
(cadcad) $
```

***Deactivate** virtual environment:*
```bash
(cadcad) $ deactivate
$
```

### 2. Installation: 
Requires [>= Python 3.6](https://www.python.org/downloads/) 

**Install Using [pip](https://pypi.org/project/cadCAD/)** 
```bash
$ pip3 install cadcad==0.4.28
```

**Install all packages with requirement.txt**
```bash
$ pip3 install -r requirements.txt
```