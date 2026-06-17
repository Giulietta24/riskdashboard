def style_risk_table(frame):
    styled = frame.style.format({
        "qty": "{:,.0f}",
        "avg_price": "{:.3f}",
        "last": "{:.3f}",
        "market_value": "{:,.0f}",
        "delta": "{:.3f}",
        "gamma": "{:.3f}",
        "theta": "{:.3f}",
        "vega": "{:.3f}",
        "unrealized_pnl": "{:,.0f}",
        "theta_per_vega": "{:.3f}",
        "theta_per_gamma": "{:.3f}",
    })

    def color_series(s):
        col = s.name
        if col in ["theta", "delta", "gamma", "vega", "action"]:
            return [cell_color(v, col) for v in s]
        return [""] * len(s)

    return styled.apply(color_series)
