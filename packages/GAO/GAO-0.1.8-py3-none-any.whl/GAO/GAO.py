#Gis Application Objects

from math import sin, asin, cos, acos, radians, fabs, sqrt, pi, atan, tan

def point_in_polygon(p, poly):
    """
    判断点p是否在多边形poly中。

    参数：
    p: 要判断的点的坐标，格式为 (x, y)。
    poly: 多边形的顶点坐标列表，每个顶点的格式为 (x, y)。顶点按顺时针或逆时针顺序排列。

    返回值：
    如果点在多边形内部，返回 True；否则返回 False。
    """

    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if p[1] > min(p1y, p2y):
            if p[1] <= max(p1y, p2y):
                if p[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (p[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or p[0] <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside




axis = 6378245.0
offset = 0.00669342162296594323
x_pi = pi * 3000.0 / 180.0
earthR = 6371000


def gcj2BD09(gcjLat=0, gcjLon=0):
    '''Transform GCJ(国测局，高德地图坐标） coordinate to BD09 (百度地图坐标）
       :return [lat, lon]
    '''
    x = gcjLon
    y = gcjLat

    z = sqrt(x * x + y * y) + 0.00002 * sin(y * x_pi)
    theta = atan(y / x) + 0.000003 * cos(x * x_pi)

    latlon = [z * sin(theta) + 0.006, z * cos(theta) + 0.0065]
    return latlon


def bd092GCJ(bdLat=0, bdLon=0):
    '''Transform BD09 (百度地图坐标） coordinate to GCJ(国测局，高德地图坐标）
       :return [lat, lon]
    '''
    x = bdLon - 0.0065
    y = bdLat - 0.006

    z = sqrt(x * x + y * y) - 0.00002 * sin(y * x_pi)
    theta = atan(y / x) - 0.000003 * cos(x * x_pi)

    latlon = [z * sin(theta), z * cos(theta)]

    return latlon


def bd092WGS(bdLat=0, bdLon=0):
    '''Transform BD09 (百度地图坐标） coordinate to WGS-84
       :return [lat, lon]
    '''
    latlon = bd092GCJ(bdLat, bdLon)

    return gcj2WGS(latlon[0], latlon[1])


def wgs2BD09(wgsLat=0, wgsLon=0):
    '''Transform WGS-84 coordinate to BD09 (百度地图坐标）
       :return [lat, lon]
    '''
    latlon = wgs2GCJ(wgsLat, wgsLon)

    return gcj2BD09(latlon[0], latlon[1])


def wgs2GCJ(wgsLat=0, wgsLon=0):
    '''Transform WGS-84 coordinate to GCJ(国测局，高德地图坐标）
       :return [lat, lon]
    '''
    if outOfChina(wgsLat, wgsLon):
        latlon = [wgsLat, wgsLon]
    else:
        latlon = delta(wgsLat, wgsLon)
        latlon[0] = wgsLat + latlon[0]
        latlon[1] = wgsLon + latlon[1]

    return latlon


def gcj2WGS(gcjLat=0, gcjLon=0):
    '''Transform GCJ(国测局，高德地图坐标） coordinate to WGS-84
       :return [lat, lon]
    '''
    if outOfChina(gcjLat, gcjLon):
        latlon = [gcjLat, gcjLon]
    else:
        latlon = delta(gcjLat, gcjLon)
        latlon[0] = gcjLat - latlon[0]
        latlon[1] = gcjLon - latlon[1]

    return latlon


def gcj2WGSExactly(gcjLat=0, gcjLon=0):
    initDelta = 0.01
    thrdHold = 0.000000001
    dLat = initDelta
    dLon = initDelta
    mLat = gcjLat - dLat
    mLon = gcjLon - dLon
    pLat = gcjLat + dLat
    pLon = gcjLon + dLon

    i = 1
    while True:
        wgsLat = (mLat + pLat) / 2
        wgsLon = (mLon + pLon) / 2
        tmp = wgs2GCJ(wgsLat, wgsLon)
        dLat = tmp[0] - gcjLat
        dLon = tmp[1] - gcjLon

        if abs(dLat) < thrdHold and abs(dLon) < thrdHold:
            break

        if dLat > 0:
            pLat = wgsLat
        else:
            mLat = wgsLat

        if dLon > 0:
            pLon = wgsLon
        else:
            mLon = wgsLon

        i = i + 1

        if i > 10000:
            break

    return [wgsLat, wgsLon]


def distance(latA=0, lonA=0, latB=0, lonB=0):
    x = cos(latA * pi / 180.0) * cos(latB * pi / 180.0) * cos((lonA - lonB) * pi / 180.0)
    y = sin(latA * pi / 180.0) * sin(latB * pi / 180.0)
    s = x + y

    if s > 1:
        s = 1
    elif s < -1:
        s = -1

    alpha = acos(s)

    return alpha * earthR


def delta(wgLat=0, wgLon=0):
    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dlon = transformLon(wgLon - 105.0, wgLat - 35.0)

    radLat = wgLat / 180 * pi
    magic = sin(radLat)
    magic = 1 - offset * magic * magic
    sqrtMagic = sqrt(magic)

    dLat = (dLat * 180.0) / ((axis * (1 - offset)) / (magic * sqrtMagic) * pi)
    dLon = (dlon * 180.0) / (axis / sqrtMagic * cos(radLat) * pi)

    latLon = [dLat, dLon]

    return latLon


def outOfChina(lat=0, lon=0):
    if lon < 72.004 or lon > 137.8347:
        return True
    elif lat < 0.8293 or lat > 55.8271:
        return True
    else:
        return False


def transformLat(x=0, y=0):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret = ret + (20.0 * sin(6 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret = ret + (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret = ret + (160.0 * sin(y / 12.0 * pi) + 320.0 * sin(y / 30.0 * pi)) * 2.0 / 3.0

    return ret


def transformLon(x=0, y=0):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret = ret + (20.0 * sin(6 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret = ret + (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret = ret + (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0

    return ret


# 定义GPS距离解算函数
def get_distance_hav_km(lat0, lng0, lat1, lng1):
    # 用haversine公式计算球面两点间的距离。
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * earthR / 1000 * asin(sqrt(h))

    return distance  # 单位为km


def hav(theta):
    s = sin(theta / 2)
    return s * s



if __name__ == "__main__":
    # print(get_distance_hav_km(31.250258 , 121.378077 , 31.250757999999998 , 121.378077)*1000)
    lat, lon = 31.343275, 120.966299
    print(lat, lon)
    print(gcj2WGS(lat, lon))
    print(gcj2WGSExactly(lat, lon))

if __name__ == '__main__':
    p = (1, 1)  # 要判断的点的坐标
    poly = [(0, 0), (0, 2), (2, 2), (2, 0)]  # 多边形的顶点坐标

    if point_in_polygon(p, poly):
        print("点在多边形内")
    else:
        print("点不在多边形内")
