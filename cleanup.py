import pandas as pd
import re


def cleanup(x):
    cleaned = []
    for i in range(len(x)):
        b = re.sub('\W+'," ", x[i])#remove anything but alphanumeric
        b = re.sub(r"\d+","", b)#remove numbers
        b = b.strip()
        if b == '':
            pass
        else:
            #print(b)
            cleaned.append(b)
    return cleaned
