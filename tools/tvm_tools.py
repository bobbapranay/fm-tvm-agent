import math

def _validate_rate(i):
    if i <= -1:
        raise ValueError("Interest rate must be greater than -100%.")
    return i

def present_value(fv: float, i: float, n: float) -> float:
    _validate_rate(i)
    return fv / ((1 + i) ** n)

def future_value(pv: float, i: float, n: float) -> float:
    _validate_rate(i)
    return pv * ((1 + i) ** n)

def solve_rate(pv: float, fv: float, n: float) -> float:
    if pv == 0:
        raise ValueError("PV cannot be zero.")
    if n == 0:
        raise ValueError("n cannot be zero.")
    if fv / pv <= 0:
        raise ValueError("FV/PV must be positive to solve rate.")
    return (fv / pv) ** (1 / n) - 1

def solve_n(pv: float, fv: float, i: float) -> float:
    _validate_rate(i)
    if pv == 0:
        raise ValueError("PV cannot be zero.")
    if i == 0:
        raise ValueError("i cannot be zero when solving for n.")
    if fv / pv <= 0:
        raise ValueError("FV/PV must be positive to solve n.")
    return math.log(fv / pv) / math.log(1 + i)

def nominal_to_effective(j: float, m: int) -> float:
    if m <= 0:
        raise ValueError("m must be positive.")
    return (1 + j / m) ** m - 1

def effective_to_nominal(i: float, m: int) -> float:
    _validate_rate(i)
    if m <= 0:
        raise ValueError("m must be positive.")
    return m * ((1 + i) ** (1 / m) - 1)

def force_to_effective(delta: float) -> float:
    return math.exp(delta) - 1

def effective_to_force(i: float) -> float:
    _validate_rate(i)
    return math.log(1 + i)

def equation_of_value(cashflows, i: float, focal_date: float) -> float:
    _validate_rate(i)
    total = 0
    for cf in cashflows:
        amount = cf["amount"]
        time = cf["time"]
        total += amount * ((1 + i) ** (focal_date - time))
    return total
