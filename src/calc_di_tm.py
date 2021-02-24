from typing import List, Dict, Union, Optional


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
