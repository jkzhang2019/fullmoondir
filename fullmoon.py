import ephem
from datetime import datetime, timedelta
import pytz

# 设置观察地点，使用经纬度和海拔高度
observer = ephem.Observer()
observer.lat = '39.9042'  # 纬度：北京的纬度
observer.lon = '116.4074'  # 经度：北京的经度
observer.elevation = 43    # 海拔高度（可以省略，默认为0）

# 设置起始时间
start_date_local = datetime.strptime('2025/01/01', '%Y/%m/%d')

# 将本地时间转换为 UTC 时间
start_date_utc = start_date_local.astimezone(pytz.utc)

# 将时区信息移除，确保 start_date_utc 是一个“naive” datetime
start_date_utc_naive = start_date_utc.replace(tzinfo=None)

# 计算未来两年内的满月
end_date = start_date_utc_naive + timedelta(days=365*2)

# 设置起始日期为下一个新月
full_moon = ephem.next_full_moon(start_date_utc_naive)



def get_moonrise_info(observer,moonrise):

    moonrise_time = ephem.localtime(moonrise)

    observer.date = moonrise

    moon = ephem.Moon(observer)
    moon_azimuth = moon.az  # 方位角
    moon_azimuth_deg = float(moon_azimuth) * 180 / 3.14159  # 转换为度

    return moonrise_time,moon_azimuth_deg




# 循环计算未来两年内每个月的满月
while full_moon.datetime() < end_date:
    
    # 将满月时间设置为观察时间(UTC)
    observer.date = full_moon.datetime()
    
    # 获取月亮的升起时间,满月前和满月后各一次。
    prev_moonrise = observer.previous_rising(ephem.Moon())
    next_moonrise = observer.next_rising(ephem.Moon())

    
    # 打印满月信息
    print(f"满月时间: {ephem.localtime(full_moon).strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    prev_rise_time,prev_rise_deg = get_moonrise_info(observer,prev_moonrise)
    
    next_rise_time,next_rise_deg = get_moonrise_info(observer,next_moonrise)

    print(f"月升时间: {prev_rise_time.strftime('%m-%d %H:%M:%S')}  \t{next_rise_time.strftime('%m-%d %H:%M:%S')}")
    print(f"月升方位: {prev_rise_deg:.2f}° \t\t{next_rise_deg:.2f}°")
    
    print("=" * 50)
    # 查找下一个满月
    full_moon = ephem.next_full_moon(full_moon)

