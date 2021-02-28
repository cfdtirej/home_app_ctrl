from typing import Union


def calc_di(te: Union[int, float], hu: Union[int, float]) -> float:
    """不快指数DIの計算
    Args:
        te: 温度 Temperature
        hu: 湿度 Humidity
    Returns:
        di: 不快指数 DI
    """
    di = (0.81*te) + (0.01*hu * (0.99*te - 14.3)) + 46.3
    return di


def calc_tm(te: Union[int, float], hu: Union[int, float], wind: Union[int, float] = 0) -> float:
    """ミスナール体感温度Tmの計算
    
    Args:
        te: 温度 Temperature
        hu: 湿度 Humidity
        wind: 風速 Wind Speed
    Returns:
        tm: ミスナール体感温度 Tm
    """
    a = 1.76 + 1.4*wind**0.75
    tm = 37 - ((37 - te) / (0.68 - 0.0014*hu + (1 / a))) - (0.29*te * (1 - hu/100))
    return tm


def di_lebel(di: Union[int, float]) -> int:
    """不快指数DIの評価
    Args:
        di: 不快指数
    Returns:
        指数の評価(0が何も感じない・快適・熱くない、0より低いと寒い、0より大きいと暑い)
    """
    if di < 55:
        return 3
    elif (55 <= di) and (di < 60):
        return 2
    elif (60 <= di) and (di < 65):
        return 0
    elif (65 <= di) and (di < 70):
        return 0
    elif (70 <= di) and (di < 75):
        return 0
    elif (75 <= di) and (di < 80):
        return -1
    elif (80 <= di) and (di < 85):
        return -2
    elif di >= 85:
        return -3
