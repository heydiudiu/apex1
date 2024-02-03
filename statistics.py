def calculate_total_trade_amount_from_db(trades):
    total_amount = 0
    for trade in trades:
        total_amount += trade[1] * trade[2]  # price * volume
    return total_amount
