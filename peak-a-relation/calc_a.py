'''
    calculate the average value for a 
    from the processed data.
    final result is printed as 'aver'.
'''

import numpy as np
import pandas as pd

df = pd.read_excel('min-a-relation.xlsx')
a = np.array(df['curve'])
aver = np.average(a)
S2 = np.sum((a - aver) ** 2) / len(a)
print(aver, S2)
