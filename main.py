import datetime
import time
import api_client
import data_processor
import database_manager
import statistics

def main():
    db_manager = database_manager.DatabaseManager()
    symbols = ["BTCUSDT", "ETHUSDT", "ORDIUSDT"]

    current_time = datetime.datetime.now()  # 使用本地时间而不是UTC
    start_time = current_time.replace(minute=0, second=0, microsecond=0)
    start_timestamp = int(start_time.timestamp() * 1000)
    end_timestamp = int(current_time.timestamp() * 1000)

    total_trade_amount = 0  # 初始化所有币对的交易总额

    for symbol in symbols:
        raw_trades = api_client.fetch_trades(symbol, start_time)
        processed_trades = data_processor.process_trade_data(raw_trades)
        db_manager.save_trade_data(processed_trades)

        db_trades = db_manager.get_trades_in_range(symbol, start_timestamp, end_timestamp)
        trade_amount = statistics.calculate_total_trade_amount_from_db(db_trades)
        print(f"测试获取 {symbol} 数据...")
        print(f"{symbol} 的交易总额: {trade_amount}")
        total_trade_amount += trade_amount

    print(f"\n从 {start_time.strftime('%Y-%m-%d %H:%M:%S')} 到 {current_time.strftime('%Y-%m-%d %H:%M:%S')} 的所有币对交易总额: {total_trade_amount}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(30)
        print("等待30s再查")  # 每隔60秒执行一次
