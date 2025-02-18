import ephem
from datetime import datetime, timedelta
import pytz

# 设置观察地点，使用经纬度和海拔高度
observer = ephem.Observer()
observer.lat = '39.9042'  # 纬度：北京的纬度
observer.lon = '116.4074'  # 经度：北京的经度
observer.elevation = 43    # 海拔高度（可以省略，默认为0）

# 获取当前时间
local_tz = pytz.timezone('Asia/Shanghai')  # 设定你想使用的本地时区（例如：上海时区）
start_date_local = datetime.strptime('2025/01/01', '%Y/%m/%d')

# 将本地时间转换为 UTC 时间
start_date_utc = start_date_local.astimezone(pytz.utc)

# 将时区信息移除，确保 start_date_utc 是一个“naive” datetime
start_date_utc_naive = start_date_utc.replace(tzinfo=None)

# 计算未来两年内的满月
end_date = start_date_utc_naive + timedelta(days=365*2)

# 设置起始日期为下一个新月
full_moon = ephem.next_full_moon(start_date_utc_naive)

# 循环计算未来两年内每个月的满月
while full_moon.datetime() < end_date:
    
    # 将满月时间设置为 UTC
    observer.date = full_moon.datetime()
    
    # 获取月亮的升起时间
    moonrise = observer.previous_rising(ephem.Moon())
    moonrise_time = ephem.localtime(moonrise)

    observer.date=moonrise_time.astimezone(pytz.utc)
    
    # 获取月亮的方位角（升起时）
    moon = ephem.Moon(observer)
    moon_azimuth = moon.az  # 方位角
    moon_azimuth_deg = float(moon_azimuth) * 180 / 3.14159  # 转换为度
    
    # 打印满月信息
    print(f"满月日期: {full_moon.datetime().strftime('%Y-%m-%d')}")
    print(f"月升时间: {moonrise_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"月升时的方位角: {moon_azimuth_deg:.2f}°")
    print("=" * 50)
    
    # 查找下一个新月
    full_moon = ephem.next_full_moon(full_moon)

