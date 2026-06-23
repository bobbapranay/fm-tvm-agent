from agents.tvm_agent import solve_tvm_query

TVM_KEYWORDS = [
    "present value", "pv", "future value", "fv", "interest", "rate",
    "effective", "nominal", "force", "delta", "equation of value",
    "cashflow", "cash flow", "discount", "accumulate", "accumulated",
    "time value", "tvm", "period", "years", "months"
]

def answer_query(user_query: str) -> str:
    query = user_query.lower()

    if any(word in query for word in TVM_KEYWORDS):
        return solve_tvm_query(user_query)

    return (
        "I can currently handle TVM questions only.\n\n"
        "Supported topics: PV, FV, interest rate, number of periods, "
        "nominal/effective rate conversions, force of interest, and equation of value."
    )
