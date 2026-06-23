# FM TVM Solver

A Streamlit Community Cloud app for Financial Mathematics Time Value of Money questions.

## Features

- Present Value
- Future Value
- Solve interest rate
- Solve number of periods
- Nominal to effective rate conversion
- Effective to nominal rate conversion
- Force of interest
- Equation of value

## Sign Convention

Cash inflows are positive. Cash outflows are negative. All cashflows must be valued at a clearly stated focal date.

## Architecture

- `app.py`: Streamlit chat interface
- `agents/orchestrator.py`: routes user questions
- `agents/tvm_agent.py`: TVM subagent response logic
- `tools/tvm_tools.py`: deterministic backend calculation functions
- `tests/test_tvm.py`: test cases with known FM answers

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run Tests

```bash
pytest
```

## Deployment

Deploy this repo to Streamlit Community Cloud and set `app.py` as the entry point.
