from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any, Iterator

import numpy as np


# listの値の型変換
def list_val_type_conv(data: List[str]) -> List[Any]:
    numbers = {str(i) for i in range(10)}
    result = []
    for value in data:
        if (type(value) is float) or (type(value) is int):
            result.append(value)
            continue
        str_set = set()
        for string in value:
            str_set.add(str(string))
        try:
            result.append(float(value))
        except ValueError:
            if value in ['True', 'False', 'true', 'false']:
                result.append(bool(value))
            elif str_set - numbers:
                try:
                    if '-' in value:
                        ts = datetime.strptime(value + '+0900', '%Y-%m-%d %H:%M:%S.%f%z').isoformat()
                        result.append(ts)
                    elif '/' in value:
                        ts = datetime.strptime(value + '+0900', '%Y/%m/%d %H:%M:%S.%f%z').isoformat()
                        result.append(ts)
                except ValueError:
                    result.append(value)
            elif value == '':
                result.append(np.nan)
            else:
                pass
    return result
