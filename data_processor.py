def process_trade_data(trades):
    processed_trades = []
    for trade in trades["data"]:
        processed_trade = {
            'id': trade['i'],
            'price': float(trade['p']),
            'volume': float(trade['v']),
            'side': trade['S'],
            'symbol': trade['s'],
            'timestamp': trade['T']
        }
        processed_trades.append(processed_trade)
    return processed_trades
