from datetime import datetime, timezone, timedelta

def convert_timestamp_to_utc8(timestamp_millis):
    timestamp = timestamp_millis / 1000
    utc_dt = datetime.utcfromtimestamp(timestamp)
    utc_plus_8 = utc_dt + timedelta(hours=8)
    print(f"原始时间戳: {timestamp_millis}, 转换后的时间: {utc_plus_8}")  # 用于调试
    return utc_plus_8

