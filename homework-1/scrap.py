import pandas as pd
import numpy as np
import seaborn as sns

sns.set_style('darkgrid')




raw = [1,1,3,3,2,2]

bin = [float(i)/sum(raw) for i in raw]

sns.histplot(x=bin)
