import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('trades.db')
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS trades (
            id TEXT PRIMARY KEY,
            price REAL,
            volume REAL,
            side TEXT,
            symbol TEXT,
            timestamp INTEGER
        )
        """
        self.conn.execute(query)

    def save_trade_data(self, trade_data):
        with self.conn:
            for trade in trade_data:
                timestamp = trade['timestamp']
                query = "INSERT OR IGNORE INTO trades (id, price, volume, side, symbol, timestamp) VALUES (?, ?, ?, ?, ?, ?)"
                result = self.conn.execute(query, (trade['id'], trade['price'], trade['volume'], trade['side'], trade['symbol'], timestamp))
                # print(f"数据插入（{trade['symbol']}）: {'成功' if result.rowcount > 0 else '失败或忽略'}")  # 调试输出
    def get_trades_in_range(self, symbol, start_timestamp, end_timestamp):
        # 转换为UTC时间戳
        # utc_offset = 28800000  # 8小时的毫秒数
        # start_timestamp_utc = start_timestamp + utc_offset
        # end_timestamp_utc = end_timestamp + utc_offset
        start_timestamp_utc = start_timestamp
        end_timestamp_utc = end_timestamp
        print(f"执行查询: SELECT * FROM trades WHERE symbol = ? AND timestamp BETWEEN ? AND ?，参数: {symbol}, {start_timestamp_utc}, {end_timestamp_utc}")
        result = self.conn.execute("SELECT * FROM trades WHERE symbol = ? AND timestamp BETWEEN ? AND ?", (symbol, start_timestamp_utc, end_timestamp_utc)).fetchall()
        print(f"从数据库检索到的交易数量: {len(result)}")
        return result


