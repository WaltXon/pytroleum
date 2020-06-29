import math


def arps_hyperbolic_rate(qi, di, b, t):
    return qi / ((1.0 + b * di * t) ** (1.0 / b))


def arps_hyperbolic_cumulative(qi, q, di, b, t):
    return ((qi ** b) / (di * (1.0 - b))) ** (qi ** (1.0 - b) - q ** (1.0 - b))


def arps_exponential_rate(qi, di, b):
    return qi * math.e(-di)


def arps_exponential_cumulative(qi, q, di, b, t):
    return qi / di * (1 - math.e ** (-di * t))


def rate_at_time_t(
    nominal_monthly_decline,
    initial_rate,
    prior_interval_rate,
    b_factor,
    b_factor_adj,
    Dmin_monthly,
    standard_time,
):
    if (
        nominal_monthly_decline * (prior_interval_rate / initial_rate) ** b_factor
        >= Dmin_monthly
    ):
        return initial_rate * (
            (1.0 + b_factor_adj * nominal_monthly_decline * standard_time)
            ** (-1.0 / b_factor_adj)
        )
    else:
        return prior_interval_rate * math.e ** (-Dmin_monthly)


def cumulative_at_time_t(
    nominal_monthly_decline,
    initial_rate,
    prior_interval_rate,
    b_factor,
    b_factor_adj,
    Dmin_monthly,
    standard_time,
    prior_standard_time,
    prior_cum_production,
):
    if (
        nominal_monthly_decline * (prior_interval_rate / initial_rate) ** b_factor
        >= Dmin_monthly
    ):
        return (initial_rate / (nominal_monthly_decline * (b_factor_adj - 1.0))) * (
            (
                (1 + b_factor_adj * nominal_monthly_decline * standard_time)
                ** (1 - (1 / b_factor_adj))
            )
            - 1.0
        )
    else:
        return (prior_interval_rate / Dmin_monthly) * (
            1 - (math.e ** (-Dmin_monthly * (standard_time - prior_standard_time)))
        ) + prior_cum_production


def nominal_decline_annual(
    nominal_annual_decline, prior_interval_rate, initial_rate, b_factor, Dmin_annual
):
    if (
        nominal_annual_decline * (prior_interval_rate / initial_rate) ** b_factor
        >= Dmin_annual
    ):
        return nominal_annual_decline * (prior_interval_rate / initial_rate) ** b_factor
    else:
        return nominal_annual_decline


def effective_decline_annual(nominal_annual_decline):
    return 1 - math.e ** (-nominal_annual_decline)
