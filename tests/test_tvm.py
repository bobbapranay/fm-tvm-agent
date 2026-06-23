import math
from tools.tvm_tools import (
    present_value,
    future_value,
    solve_rate,
    solve_n,
    nominal_to_effective,
    force_to_effective,
    equation_of_value,
)

def test_present_value():
    assert round(present_value(10000, 0.08, 3), 2) == 7938.32

def test_future_value():
    assert round(future_value(5000, 0.06, 4), 2) == 6312.38

def test_solve_rate():
    assert round(solve_rate(1000, 1210, 2), 4) == 0.1000

def test_solve_n():
    assert round(solve_n(1000, 1210, 0.10), 2) == 2.00

def test_nominal_to_effective():
    assert round(nominal_to_effective(0.12, 12), 4) == 0.1268

def test_force_to_effective():
    assert round(force_to_effective(0.05), 4) == 0.0513

def test_equation_of_value():
    cashflows = [
        {"amount": -1000, "time": 0},
        {"amount": 600, "time": 1},
        {"amount": 600, "time": 2},
    ]
    assert round(equation_of_value(cashflows, 0.10, 0), 2) == -4.13
