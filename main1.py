import os
import datetime
import time
import logging
import datetime
from datetime import timezone, timedelta
from telegram.ext import Application, CallbackContext
from telegram.ext import CommandHandler
from dotenv import load_dotenv
import api_client
import data_processor
import database_manager
import statistics

# 加载环境变量
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 启用日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def calculate_total_usdt_trades(start_timestamp, end_timestamp):
    db_manager = database_manager.DatabaseManager()
    symbols = ["BTCUSDT", "ETHUSDT", "STXUSDT", "BIGTIMEUSDT", "MEMEUSDT", "PYTHUSDT", "FETUSDT", "ORDIUSDT"]
    total_trade_amount = 0
    for symbol in symbols:
        db_trades = db_manager.get_trades_in_range(symbol, start_timestamp, end_timestamp)
        trade_amount = statistics.calculate_total_trade_amount_from_db(db_trades)
        total_trade_amount += trade_amount
    return total_trade_amount

async def send_message(context: CallbackContext, message):
    try:
        await context.bot.send_message(chat_id=CHAT_ID, text=message)
        logger.info(f"消息发送成功: {message}")
    except Exception as e:
        logger.error(f"发送消息时出错: {e}")

async def fetch_and_save_trades(context: CallbackContext):
    db_manager = database_manager.DatabaseManager()
    symbols = ["BTCUSDT", "ETHUSDT", "STXUSDT", "BIGTIMEUSDT", "MEMEUSDT", "PYTHUSDT", "FETUSDT", "ORDIUSDT"]
    current_time = datetime.datetime.now()
    for symbol in symbols:
        raw_trades = api_client.fetch_trades(symbol, current_time)
        if raw_trades:
            processed_trades = data_processor.process_trade_data(raw_trades)
            db_manager.save_trade_data(processed_trades)

async def send_hourly_trade_summary(context: CallbackContext):
    logger.info("开始执行每小时交易总额汇总")
    try:
        # 获取当前的UTC时间
        now_utc = datetime.datetime.now(timezone.utc)
        # 计算上一个小时的开始和结束时间（UTC时间）
        end_timestamp_utc = int(now_utc.replace(minute=0, second=0, microsecond=0).timestamp() * 1000)
        start_timestamp_utc = end_timestamp_utc - 3600000  # 减去1小时的毫秒数

        total_trade_amount = await calculate_total_usdt_trades(start_timestamp_utc, end_timestamp_utc)
        message = f"上一个小时的USDT币对交易总额: {total_trade_amount}"
        await send_message(context, message)
        logger.info("每小时交易总额汇总消息发送成功")
    except Exception as e:
        logger.error(f"发送每小时交易总额汇总消息时出错: {e}")



# ... 其他函数 ...
async def send_daily_trade_summary(context: CallbackContext):
    current_time = datetime.datetime.now()
    start_timestamp = int(current_time.replace(hour=0, minute=0, second=0, microsecond=0, day=current_time.day - 1).timestamp() * 1000)
    end_timestamp = int(current_time.replace(hour=23, minute=59, second=59, microsecond=999999, day=current_time.day - 1).timestamp() * 1000)
    total_trade_amount = await calculate_total_usdt_trades(start_timestamp, end_timestamp)
    message = f"昨天所有USDT币对交易总额: {total_trade_amount}"
    await send_message(context, message)

async def send_season_trade_summary(context: CallbackContext):
    season_start = datetime.datetime(year=2024, month=1, day=22)
    while season_start + datetime.timedelta(weeks=2) <= datetime.datetime.now():
        season_start += datetime.timedelta(weeks=2)
    start_timestamp = int(season_start.timestamp() * 1000)
    end_timestamp = int(datetime.datetime.now().timestamp() * 1000)
    total_trade_amount = await calculate_total_usdt_trades(start_timestamp, end_timestamp)
    days_in_season = (datetime.datetime.now() - season_start).days + 1
    message = f"本赛季所有USDT币对交易总额: {total_trade_amount} (第{days_in_season}天)"
    await send_message(context, message)

async def send_test_trade_summary(context: CallbackContext):
    end_timestamp = int(datetime.datetime.now().timestamp() * 1000)
    start_timestamp = int(datetime.datetime.now().replace(minute=0, second=0, microsecond=0).timestamp() * 1000)
    total_trade_amount = await calculate_total_usdt_trades(start_timestamp, end_timestamp)
    message = f"测试：这个小时所有USDT币对交易总额: {total_trade_amount}"
    await send_message(context, message)

# main 函数和之前的保持一致
# 计算下一个整点时间
async def calculate_total_usdt_trades_since_beginning():
    db_manager = database_manager.DatabaseManager()
    symbols = ["BTCUSDT", "ETHUSDT", "STXUSDT", "BIGTIMEUSDT", "MEMEUSDT", "PYTHUSDT", "FETUSDT", "ORDIUSDT"]
    total_trade_amount = 0
    end_timestamp = int(datetime.datetime.now().timestamp() * 1000)
    
    for symbol in symbols:
        # 假设数据库中的第一笔交易时间戳为 0
        db_trades = db_manager.get_trades_in_range(symbol, 0, end_timestamp)
        trade_amount = statistics.calculate_total_trade_amount_from_db(db_trades)
        total_trade_amount += trade_amount

    return total_trade_amount
async def send_total_trade_summary_since_beginning(context: CallbackContext):
    try:
        logger.info("正在尝试发送从数据库开始的USDT交易总额")
        total_trade_amount = await calculate_total_usdt_trades_since_beginning()
        message = f"从数据库开始到现在的USDT币对交易总额: {total_trade_amount}"
        await send_message(context, message)
        logger.info("消息发送成功")
    except Exception as e:
        logger.error(f"发送消息时出错: {e}")
        raise
def next_full_hour():
    now = datetime.datetime.now()
    next_hour = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    logger.info(f"下一个整点时间: {next_hour}")
    return next_hour

def next_full_hour_utc_plus_8():
    now_utc = datetime.datetime.now(timezone.utc)
    next_hour_utc = (now_utc + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    # 将UTC时间转换为UTC+8
    next_hour_utc_plus_8 = next_hour_utc.astimezone(timezone(timedelta(hours=8)))
    logger.info(f"下一个整点时间 (UTC+8): {next_hour_utc_plus_8}")
    # 返回UTC时间
    return next_hour_utc
async def test_hourly_summary(update, context):
    await send_hourly_trade_summary(context)
async def test_timezones(update, context):
    # 获取当前的UTC时间
    now_utc = datetime.datetime.now(timezone.utc)
    # 转换为本地时间（假设是UTC+8）
    now_local = now_utc.astimezone(timezone(timedelta(hours=8)))
    
    message = f"当前UTC时间: {now_utc}\n当前本地时间 (UTC+8): {now_local}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    logger.info("测试时间信息已发送")
async def test_daily_summary(update, context):
    await send_daily_trade_summary(context)

async def test_season_summary(update, context):
    await send_season_trade_summary(context)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    job_queue = application.job_queue

    # 定期获取并保存交易数据
    job_queue.run_repeating(fetch_and_save_trades, interval=20, first=0)  # 每5分钟执行一次

    # 测试推送 - 每分钟发送一条消息
    #job_queue.run_repeating(send_test_trade_summary, interval=22, first=0)
    # 每天指定时间推送从数据库开始的USDT交易总额
    #scheduled_time = datetime.time(hour=4, minute=6, second=30)  # 调整为您需要的时间
    #logger.info(f"计划每天在 {scheduled_time} 推送从数据库开始的USDT交易总额")
   # job_queue.run_daily(send_total_trade_summary_since_beginning, time=scheduled_time, name="total_trade_summary_since_beginning")

    #logger.info("定时任务已设置")

    # 每小时整点推送消息
    #next_hour = next_full_hour()
    #logger.info(f"设置每小时整点推送任务，下一个执行时间: {next_hour}")
    #job_queue.run_repeating(send_hourly_trade_summary, interval=3600, first=next_hour)

    # 每天凌晨推送前一天的总交易额
    job_queue.run_daily(send_daily_trade_summary, time=datetime.time(hour=0, minute=0, second=0), name="daily_trade_summary")

    # 每天凌晨推送本季度的总交易额
    job_queue.run_daily(send_season_trade_summary, time=datetime.time(hour=0, minute=0, second=0), name="season_trade_summary")

    # 添加测试每小时总结的命令处理器
    test_hourly_summary_handler = CommandHandler('test_hourly_summary', test_hourly_summary)
    application.add_handler(test_hourly_summary_handler)

    # 添加测试时间的命令处理器
    test_timezones_handler = CommandHandler('test_timezones', test_timezones)
    application.add_handler(test_timezones_handler)

    # 设置每小时整点推送任务
    next_hour_utc = next_full_hour_utc_plus_8()
    logger.info(f"设置每小时整点推送任务，下一个执行时间 (UTC): {next_hour_utc}")
    job_queue.run_repeating(send_hourly_trade_summary, interval=3600, first=next_hour_utc)


    # 添加测试每日汇总的命令处理器
    test_daily_summary_handler = CommandHandler('test_daily_summary', test_daily_summary)
    application.add_handler(test_daily_summary_handler)

    # 添加测试季度汇总的命令处理器
    test_season_summary_handler = CommandHandler('test_season_summary', test_season_summary)
    application.add_handler(test_season_summary_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
