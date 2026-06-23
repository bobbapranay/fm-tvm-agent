import re
from tools.tvm_tools import (
    present_value,
    future_value,
    solve_rate,
    solve_n,
    nominal_to_effective,
    effective_to_nominal,
    force_to_effective,
    effective_to_force,
    equation_of_value,
)

def _numbers(text):
    cleaned = text.replace(",", "")
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", cleaned)]

def _rate_from_percent(value):
    return value / 100 if value > 1 else value

def _money(x):
    return f"₹{x:,.2f}"

def solve_tvm_query(query: str) -> str:
    q = query.lower()
    nums = _numbers(query)

    try:
        if "nominal" in q and "effective" in q and len(nums) >= 2:
            rate = _rate_from_percent(nums[0])
            m = int(nums[1])
            eff = nominal_to_effective(rate, m)
            return (
                "**Given:**\n"
                f"- Nominal rate = {rate:.6f}\n"
                f"- Compounding frequency = {m}\n\n"
                "**Formula:**\n"
                "Effective rate = (1 + j/m)^m - 1\n\n"
                "**Substitution:**\n"
                f"(1 + {rate:.6f}/{m})^{m} - 1\n\n"
                "**Final Answer:**\n"
                f"Effective annual rate = **{eff * 100:.4f}%**"
            )

        if "effective" in q and "nominal" in q and "convert" in q and len(nums) >= 2:
            eff = _rate_from_percent(nums[0])
            m = int(nums[1])
            nom = effective_to_nominal(eff, m)
            return (
                "**Given:**\n"
                f"- Effective rate = {eff:.6f}\n"
                f"- Compounding frequency = {m}\n\n"
                "**Formula:**\n"
                "Nominal rate = m[(1 + i)^(1/m) - 1]\n\n"
                "**Substitution:**\n"
                f"{m}[(1 + {eff:.6f})^(1/{m}) - 1]\n\n"
                "**Final Answer:**\n"
                f"Nominal annual rate = **{nom * 100:.4f}%**"
            )

        if "force" in q and "effective" in q and len(nums) >= 1:
            delta = _rate_from_percent(nums[0])
            eff = force_to_effective(delta)
            return (
                "**Given:**\n"
                f"- Force of interest δ = {delta:.6f}\n\n"
                "**Formula:**\n"
                "i = e^δ - 1\n\n"
                "**Substitution:**\n"
                f"e^{delta:.6f} - 1\n\n"
                "**Final Answer:**\n"
                f"Effective rate = **{eff * 100:.4f}%**"
            )

        if "force" in q and len(nums) >= 1:
            eff = _rate_from_percent(nums[0])
            delta = effective_to_force(eff)
            return (
                "**Given:**\n"
                f"- Effective rate i = {eff:.6f}\n\n"
                "**Formula:**\n"
                "δ = ln(1 + i)\n\n"
                "**Substitution:**\n"
                f"ln(1 + {eff:.6f})\n\n"
                "**Final Answer:**\n"
                f"Force of interest = **{delta:.6f}**"
            )

        if ("equation of value" in q or "cashflow" in q or "cash flow" in q) and len(nums) >= 3:
            rate = _rate_from_percent(nums[-2])
            focal_date = nums[-1]
            values = nums[:-2]
            cashflows = [{"amount": values[i], "time": values[i + 1]} for i in range(0, len(values) - 1, 2)]
            total = equation_of_value(cashflows, rate, focal_date)
            cf_text = ", ".join([f"{c['amount']} at t={c['time']}" for c in cashflows])
            return (
                "**Given:**\n"
                f"- Cashflows = {cf_text}\n"
                f"- Interest rate = {rate:.6f}\n"
                f"- Focal date = {focal_date}\n\n"
                "**Formula:**\n"
                "Value at focal date = Σ C(1+i)^(focal_date - t)\n\n"
                "**Substitution:**\n"
                f"Each cashflow is moved to t = {focal_date}\n\n"
                "**Final Answer:**\n"
                f"Value at focal date = **{_money(total)}**"
            )

        if ("present value" in q or "pv" in q) and len(nums) >= 3:
            fv, n, rate = nums[0], nums[1], _rate_from_percent(nums[2])
            pv = present_value(fv, rate, n)
            return (
                "**Given:**\n"
                f"- FV = {_money(fv)}\n"
                f"- i = {rate:.6f}\n"
                f"- n = {n}\n\n"
                "**Formula:**\n"
                "PV = FV / (1 + i)^n\n\n"
                "**Substitution:**\n"
                f"PV = {fv} / (1 + {rate:.6f})^{n}\n\n"
                "**Final Answer:**\n"
                f"PV = **{_money(pv)}**"
            )

        if ("future value" in q or "fv" in q) and len(nums) >= 3:
            pv, rate, n = nums[0], _rate_from_percent(nums[1]), nums[2]
            fv = future_value(pv, rate, n)
            return (
                "**Given:**\n"
                f"- PV = {_money(pv)}\n"
                f"- i = {rate:.6f}\n"
                f"- n = {n}\n\n"
                "**Formula:**\n"
                "FV = PV(1 + i)^n\n\n"
                "**Substitution:**\n"
                f"FV = {pv}(1 + {rate:.6f})^{n}\n\n"
                "**Final Answer:**\n"
                f"FV = **{_money(fv)}**"
            )

        if ("rate" in q or "interest" in q or " i " in f" {q} ") and len(nums) >= 3:
            pv, fv, n = nums[0], nums[1], nums[2]
            i = solve_rate(pv, fv, n)
            return (
                "**Given:**\n"
                f"- PV = {_money(pv)}\n"
                f"- FV = {_money(fv)}\n"
                f"- n = {n}\n\n"
                "**Formula:**\n"
                "i = (FV / PV)^(1/n) - 1\n\n"
                "**Substitution:**\n"
                f"i = ({fv} / {pv})^(1/{n}) - 1\n\n"
                "**Final Answer:**\n"
                f"i = **{i * 100:.4f}%**"
            )

        if ("period" in q or "how long" in q or " n " in f" {q} ") and len(nums) >= 3:
            pv, fv, rate = nums[0], nums[1], _rate_from_percent(nums[2])
            n = solve_n(pv, fv, rate)
            return (
                "**Given:**\n"
                f"- PV = {_money(pv)}\n"
                f"- FV = {_money(fv)}\n"
                f"- i = {rate:.6f}\n\n"
                "**Formula:**\n"
                "n = ln(FV / PV) / ln(1 + i)\n\n"
                "**Substitution:**\n"
                f"n = ln({fv} / {pv}) / ln(1 + {rate:.6f})\n\n"
                "**Final Answer:**\n"
                f"n = **{n:.4f} periods**"
            )

        return (
            "I can solve this TVM question, but I need clear values.\n\n"
            "Example: `Find the present value of ₹10,000 due in 3 years at 8% effective annual interest.`"
        )

    except Exception as e:
        return (
            "**Error:** I could not safely compute this.\n\n"
            f"Reason: `{str(e)}`\n\n"
            "Please check the inputs and try again."
        )
