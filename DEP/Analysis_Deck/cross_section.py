import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

filepath = '../PTC_ts.csv'
savefolder = 'IRA'
cols = ['Hydroelectric conventional', 'Natural gas', 'Nuclear', 'Solar thermal and photovoltaic', 'Wind']

def create_cross_section(filepath, month_start, year_start, cols, savefolder):
    data_csv = pd.read_csv(filepath)

    # Look-back two months, look ahead 6 months (8 months total interval).
    start_date = datetime.strptime(f'{str(month_start).zfill(0)}/{year_start}', '%m/%Y')
    start_date, end_date = start_date - relativedelta(months=2), start_date + relativedelta(months=6)

    datetimes = pd.to_datetime(data_csv['Datetime'])

    data_csv = data_csv[(datetimes >= start_date) & (datetimes <= end_date)]
    data_csv = data_csv[['Datetime'] + cols]

    colors = ['blue', 'green', 'red', 'orange', 'purple']
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))
    plt.subplots_adjust(top=0.775)
    for id, col in enumerate(cols):
        axs.plot(data_csv['Datetime'], data_csv[col], color=colors[id], label = ' '.join([s[0].upper()+s[1:] for s in col.split()]), linewidth=1.5)
    
    fig.legend(loc='upper center', ncols=5, bbox_to_anchor=(0.5, 0.9), shadow=True)
    axs.set_xlabel('Date', fontsize=13, fontweight='bold')
    axs.set_ylabel('Power Generation (MWh)', fontsize=13, fontweight='bold')
    fig.suptitle(f'Cross-Sectional Electricity Generation ({'/'.join(str(start_date).split()[0].split('-')[:2][::-1])}-{'/'.join(str(end_date).split()[0].split('-')[:2][::-1])})', fontsize=14, fontweight='bold', y=0.95)
    
    axs.set_yticks([x*1.5e6 for x in range(7)])

    axs.set_xticks(data_csv['Datetime'].to_list()[::2])
    axs.set_xticklabels(['/'.join(s.split('-')[:2][::-1]) for s in data_csv['Datetime'].to_list()][::2])
    plt.savefig(f'{savefolder}/{month_start}_{year_start}_event.jpg')

### IRA signed by Biden.
create_cross_section(filepath, 8, 2022, cols, savefolder)

### IRA comes into effect.
create_cross_section(filepath, 1, 2023, cols, savefolder)

### OBBBA signed by Trump.
create_cross_section(filepath, 7, 2025, cols, savefolder)

### Clean Energy Production Tax Credit passed.
create_cross_section(filepath, 8, 2024, cols, savefolder)

### IRA credits expired by Trump.
create_cross_section(filepath, 1, 2025, cols, savefolder)

### Donald Trump elected.
create_cross_section(filepath, 11, 2024, cols, savefolder)

### $156 million solar grant by Pritzker.
create_cross_section(filepath, 4, 2024, cols, savefolder)
