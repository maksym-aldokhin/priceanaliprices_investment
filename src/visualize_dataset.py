import pandas as pd

import matplotlib.pyplot as plt

air_quality = pd.read_excel("H:\\data_for_analiz\\report.xlsx")

air_quality.head()

air_quality.plot()
plt.show()