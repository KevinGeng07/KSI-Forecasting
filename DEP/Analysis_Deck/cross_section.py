import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

filepath = '../PTC_ts.csv'
savefolder_1 = 'IRA'
savefolder_2 = 'Long Horizon'
cols = ['Hydroelectric conventional', 'Natural gas', 'Nuclear', 'Solar thermal and photovoltaic', 'Wind']

### TODO: OBJECTIVE 1
def create_cross_section(filepath, month_start, year_start, cols, savefolder):
    data_csv = pd.read_csv(filepath)

    # Look-back two months, look ahead 6 months (8 months total interval).
    start_date = datetime.strptime(f'{str(month_start).zfill(0)}/{year_start}', '%m/%Y')
    start_date, end_date = start_date - relativedelta(months=2), start_date + relativedelta(months=6)

    datetimes = pd.to_datetime(data_csv['Datetime'])

    data_csv = data_csv[(datetimes >= start_date) & (datetimes <= end_date)]
    data_csv = data_csv[['Datetime'] + cols]

    colors = ['blue', 'green', 'red', 'orange', 'purple']
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 5))

    plt.subplots_adjust(top=0.775, hspace=0.075)

    for id, col in enumerate(cols):
        axs[0].plot(data_csv['Datetime'], data_csv[col], color=colors[id], label = ' '.join([s[0].upper()+s[1:] for s in col.split()]), linewidth=1.5)
        axs[1].plot(data_csv['Datetime'], data_csv[col], color=colors[id], label = ' '.join([s[0].upper()+s[1:] for s in col.split()]), linewidth=1.5)
    
    axs[0].set_ylim(1e5, 9e6)
    axs[1].set_ylim(0, 2.5e4)

    axs[0].spines.bottom.set_visible(False)
    axs[0].tick_params(top=False, bottom=False, labelbottom=False)
    axs[0].tick_params(labeltop=False)
    axs[1].spines.top.set_visible(False)
    axs[1].xaxis.tick_bottom()

    kwargs = dict(marker=[(-1, -0.5), (1, 0.5)], markersize=12, linestyle='none', color='k', mec='k', mew=1, clip_on=False)
    axs[0].plot([0, 1], [0, 0], transform=axs[0].transAxes, **kwargs)
    axs[1].plot([0, 1], [1, 1], transform=axs[1].transAxes, **kwargs)

    axs[0].set_yticks([1e6+x*2e6 for x in range(5)])
    axs[0].set_yticklabels(['1', '3', '5', '7', '9'])
    axs[1].set_yticks([x*5e3 for x in range(5)])
    axs[1].set_yticklabels(['0', '0.5', '1', '1.5', '2'])

    axs[0].text(5e-3, 1.075, "1e6", transform=axs[0].transAxes, ha="left", va="top", fontsize=9)
    axs[1].text(5e-3, 0.975, "1e4", transform=axs[1].transAxes, ha="left", va="top", fontsize=9)

    fig.supylabel('Power Generation (MWh)', fontsize=13, fontweight='bold', x=0.07, y=0.44)
    fig.supxlabel('Date', fontsize=13, fontweight='bold', x=0.5105, y=0.015)

    handles, labels = axs[0].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    fig.legend(unique.values(), unique.keys(), loc="upper center", ncols=5, bbox_to_anchor=(0.5, 0.9), shadow=True)

    # fig.legend(loc='upper center', ncols=5, bbox_to_anchor=(0.5, 0.9), shadow=True)
    fig.suptitle(f'Cross-Sectional Electricity Generation ({'/'.join(str(start_date).split()[0].split('-')[:2][::-1])}-{'/'.join(str(end_date).split()[0].split('-')[:2][::-1])})', fontsize=14, fontweight='bold', y=0.95)
    axs[1].set_xticks(data_csv['Datetime'].to_list()[::2])
    axs[1].set_xticklabels(['/'.join(s.split('-')[:2][::-1]) for s in data_csv['Datetime'].to_list()][::2])
    plt.savefig(f'{savefolder}/{month_start}_{year_start}_event.jpg')

### IRA signed by Biden.
create_cross_section(filepath, 8, 2022, cols, savefolder_1)

### IRA comes into effect.
create_cross_section(filepath, 1, 2023, cols, savefolder_1)

### OBBBA signed by Trump.
create_cross_section(filepath, 7, 2025, cols, savefolder_1)

### Clean Energy Production Tax Credit passed.
create_cross_section(filepath, 8, 2024, cols, savefolder_1)

### IRA credits expired by Trump.
create_cross_section(filepath, 1, 2025, cols, savefolder_1)

### Donald Trump elected.
create_cross_section(filepath, 11, 2024, cols, savefolder_1)

### $156 million solar grant by Pritzker.
create_cross_section(filepath, 4, 2024, cols, savefolder_1)

### ABP lottery system change.
create_cross_section(filepath, 4, 2019, cols, savefolder_2)


### TODO: OBJECTIVE 2
data_csv = pd.read_csv(filepath)

# Look-back two months, look ahead 6 months (8 months total interval).
start_date = datetime.strptime('2017', '%Y')
start_date, end_date = start_date - relativedelta(months=2), start_date + relativedelta(years=4)

datetimes = pd.to_datetime(data_csv['Datetime'])

data_csv = data_csv[(datetimes >= start_date) & (datetimes <= end_date)]
data_csv = data_csv[['Datetime'] + cols]

colors = ['blue', 'green', 'red', 'orange', 'purple']
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 5))

plt.subplots_adjust(top=0.775, hspace=0.075)

for id, col in enumerate(cols):
    axs[0].plot(data_csv['Datetime'], data_csv[col], color=colors[id], label = ' '.join([s[0].upper()+s[1:] for s in col.split()]), linewidth=1.5)
    axs[1].plot(data_csv['Datetime'], data_csv[col], color=colors[id], label = ' '.join([s[0].upper()+s[1:] for s in col.split()]), linewidth=1.5)

axs[0].set_ylim(1e5, 9e6)
axs[1].set_ylim(0, 2.5e4)

axs[0].spines.bottom.set_visible(False)
axs[0].tick_params(top=False, bottom=False, labelbottom=False)
axs[0].tick_params(labeltop=False)
axs[1].spines.top.set_visible(False)
axs[1].xaxis.tick_bottom()

kwargs = dict(marker=[(-1, -0.5), (1, 0.5)], markersize=12, linestyle='none', color='k', mec='k', mew=1, clip_on=False)
axs[0].plot([0, 1], [0, 0], transform=axs[0].transAxes, **kwargs)
axs[1].plot([0, 1], [1, 1], transform=axs[1].transAxes, **kwargs)

axs[0].set_yticks([1e6+x*2e6 for x in range(5)])
axs[0].set_yticklabels(['1', '3', '5', '7', '9'])
axs[1].set_yticks([x*5e3 for x in range(5)])
axs[1].set_yticklabels(['0', '0.5', '1', '1.5', '2'])

axs[0].text(5e-3, 1.075, "1e6", transform=axs[0].transAxes, ha="left", va="top", fontsize=9)
axs[1].text(5e-3, 0.975, "1e4", transform=axs[1].transAxes, ha="left", va="top", fontsize=9)

fig.supylabel('Power Generation (MWh)', fontsize=13, fontweight='bold', x=0.07, y=0.44)
fig.supxlabel('Date', fontsize=13, fontweight='bold', x=0.5105, y=0.015)

handles, labels = axs[0].get_legend_handles_labels()
unique = dict(zip(labels, handles))
fig.legend(unique.values(), unique.keys(), loc="upper center", ncols=5, bbox_to_anchor=(0.5, 0.9), shadow=True)

fig.suptitle(f'Cross-Sectional Electricity Generation ({'/'.join(str(start_date).split()[0].split('-')[:2][::-1])}-{'/'.join(str(end_date).split()[0].split('-')[:2][::-1])})', fontsize=14, fontweight='bold', y=0.95)
axs[1].set_xticks(data_csv['Datetime'].to_list()[::5])
axs[1].set_xticklabels(['/'.join(s.split('-')[:2][::-1]) for s in data_csv['Datetime'].to_list()][::5])
plt.savefig(f'{savefolder_2}/2017_2021_event.jpg')
