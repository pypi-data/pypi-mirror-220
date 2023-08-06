"""
参数含义定义：
    地理坐标参数为lat(南北向, 北为正), lon(东西向, 东为正)。
    大地坐标参数为X(东西向, 东为正), Y(南北向, 北为正)。
    矩阵行列参数为row(南北向, 南为正), col(东西向, 东为正)
    x(东西向), y(南北向); (GDAL同样)
仿射变换六参数:
    0：图像左上角的X坐标(东西向)或lon坐标(东西向)；
    1：图像东西方向分辨率；
    2：旋转角度，如果图像北方朝上，该值为0；
    3：图像左上角的Y坐标(南北向)或lat坐标(南北向)；
    4：旋转角度，如果图像北方朝上，该值为0；
    5：图像南北方向分辨率；
"""

def XYcoord2Plines(coordinate, affine_trans):
    """投影坐标下XY坐标转像素行列位置

    Args:
        coordinate: (X, Y)   经纬度或大地坐标->(东西向, 南北向)
        affine_trans (list): 仿射变换六参数
    
    Returns:
        tuple: 数据矩阵的行号,列号
        
    Note: 由于左上角点中心位置为 (0.5,0.5)，故直接int就可以取值
    """
    X, Y = coordinate
    x0, dx, rx, y0, ry, dy = affine_trans
    a = X - x0
    b = Y - y0
    c = (dx * dy - ry * rx)
    # 注意, 左上角点中心位置为 (0.5,0.5)
    col = (a * dy - b * rx) / c
    row = (b * dx - a * ry) / c
    return row, col


def Plines2XYcoord(rasterXYPixel, affine_trans):
    """像素行列位置转投影坐标下XY坐标

    Args:
        rasterXYPixel (tuple): 数据矩阵的行列号->(南北向, 东西向)
        affine_trans (list): 仿射变换六参数
    
    Returns:
        tuple: (X, Y)   东西向, 南北向
    """
    col = rasterXYPixel[1] # 东西向
    row = rasterXYPixel[0] # 南北向
    # 获得东西向结果
    lon = X = affine_trans[0] + affine_trans[1] * col + affine_trans[2] * row
    # 获得南北向结果
    lat = Y = affine_trans[3] + affine_trans[4] * col + affine_trans[5] * row
    return [X, Y]

def destination(point, bearing, distance:float):
    """
        lat, lon
    """
    try:
        import geopy.distance
    except:
        raise Exception("导入geopy失败，请先安装")
    return geopy.distance.distance(kilometers=distance).destination(point, bearing=bearing)
    

def toOrientationEN(sr, point):
    """
        北为1， 东为3
    """
    orient = [sr.GetAxisOrientation(None, i) for i in range(2)]
    if orient == [3, 1]:
        return point[:2]
    if orient == [1, 3]:
        return reversed(point[:2])
    raise ValueError("ERROR: toOrientationEN: 特殊的投影坐标系，请检查!")

def bounding(datarange, brange):
    row_min_1, row_max_1, col_min_1, col_max_1 = [int(i) for i in datarange]
    row_min_2, row_max_2, col_min_2, col_max_2 = [int(i) for i in brange]

    row_min_3 = row_min_1 if row_min_1 >= row_min_2 else row_min_2
    row_max_3 = row_max_1 if row_max_1 < row_max_2 else row_max_2 - 1
    col_min_3 = col_min_1 if col_min_1 >= col_min_2 else col_min_2
    col_max_3 = col_max_1 if col_max_1 < col_max_2 else col_max_2 - 1
    width_from_data = col_max_3 - col_min_3 + 1
    height_from_data = row_max_3 - row_min_3 + 1

    row_min_array = row_min_3 - row_min_1
    row_max_array = row_max_3 - row_min_1
    col_min_array = col_min_3 - col_min_1
    col_max_array = col_max_3 - col_min_1
        

    bounding_range = (row_min_3, row_max_3, col_min_3, col_max_3)
    data_get_setting = (col_min_3, row_min_3, width_from_data, height_from_data)
    array_get_setting = (row_min_array, row_max_array+1, col_min_array, col_max_array+1)
    return bounding_range, data_get_setting, array_get_setting
