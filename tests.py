import stock_data.processing.stock_prediction as sp
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta


data = sp.load_predictions('TSLA')
for i in range(0, len(data)):
    data[i] = data[i][0][0]

time = []
for i in range(0, len(data)):
    time.append(date.today() + timedelta(days=i))


xpoints = np.array(time)
ypoints = np.array(data)
plt.plot(xpoints, ypoints, label='STOCK_NAME')
plt.xticks(rotation=20)
plt.title('Predicted Stock Price')
plt.xlabel('Time')
plt.ylabel('Price in EU')
plt.legend()
plt.autoscale(enable=True, axis='both', tight=None)
plt.savefig('stock_data/predictions/stock_plot.png')
