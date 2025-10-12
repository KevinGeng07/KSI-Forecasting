import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from natsort import natsorted
from datetime import datetime, timedelta

### Downloaded segments:
# 10/10/23-12/31/23
# 1/1/24-3/31/24
# 4/1/24-6/30/24
# 7/1/24-9/30/24
# 10/1/24-12/31/24
# 1/1/25-3/31/25
# 4/1/25-6/30/25
# 7/1/25-10/9/25

csvpath = 'HDC/Raw RTP'

combined_csv = pd.DataFrame()
for file in natsorted(os.listdir(csvpath)):
    print(file)
    csv = pd.read_csv(os.path.join(csvpath, file))
    combined_csv = pd.concat([combined_csv, csv], axis=0, ignore_index=False)

# Verify all dates are present in the data.
start, end = datetime(2023, 10, 10), datetime(2025, 10, 9)
dates = [(start + timedelta(days=i)).strftime("%m/%d/%Y") for i in range((end - start).days + 1)]

assert set(combined_csv['DATE'].to_list()) == set(dates)

# Aggregate date and hour columns together.
combined_csv['DATETIME'] = pd.to_datetime(combined_csv['DATE']) + pd.to_timedelta(combined_csv['HOUR'], unit='h')
combined_csv = combined_csv[['DATETIME', 'PRICE']]

# print(combined_csv)
combined_csv.to_csv('HDC/AmerenRTP.csv', index=False)


colors = list(mpl.colormaps['Set1'].colors)

# print(list(combined_csv['PRICE'].rolling(window=5)))
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(range(len(combined_csv['DATETIME'])), combined_csv['PRICE'], label='Raw Price', color=colors[1], alpha=0.3)
ax.plot(range(len(combined_csv['DATETIME'])), combined_csv['PRICE'].ewm(span=24, adjust=False).mean(), label='Daily Price', color=colors[0], linewidth=1.25)
ax.plot(range(len(combined_csv['DATETIME'])), combined_csv['PRICE'].ewm(span=168, adjust=False).mean(), label='Weekly Price', color=colors[2], linewidth=1.5)
ax.plot(range(len(combined_csv['DATETIME'])), combined_csv['PRICE'].ewm(span=672, adjust=False).mean(), label='Monthly Price', color=colors[3], linewidth=2)


ax.set_yscale('log')
ax.set_xlabel('Days Since 10/09/23')
ax.set_ylabel('Price (¢)')
ax.set_xticks([24 * x for x in [0, 150, 300, 450, 600, 750]])
ax.set_xticklabels([0, 150, 300, 450, 600, 750])
ax.set_yticks([0.01, 0.05, 0.25, 0.45])
ax.set_yticklabels([1, 5, 25, 40])
fig.tight_layout()
ax.legend(loc='upper left')

fig.savefig('HDC/viz/Ameren_RTP.jpg')
