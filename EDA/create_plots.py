import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime

xslx = pd.ExcelFile('EDA/GH_IL_2024 Interim Community Solar Forecasts_06072024_NLE.xlsx')
# print(xslx.sheet_names)
temp_xslx = pd.read_excel(xslx, sheet_name='Rate Table')


def plot_rates(s_i, e_i, file_name):

    rates_df = pd.read_excel(xslx, sheet_name='Rate Table')
    cols = rates_df.columns

    # Filter rates_df into supply rates and transmission rates.
    supply_dates = rates_df[cols.tolist()[5:]][rates_df.index == s_i-1].iloc[0].tolist()
    supply_dates = [x.strftime("%Y-%m-01 01:00:00") for x in supply_dates]
    # print(supply_dates)
    # exit()
    # supply_dates = ['-'.join(str(x).split(' ')[0].split('-')[:2]) for x in supply_dates]
    

    supply_rates = rates_df[(rates_df.index >= s_i) & (rates_df.index <= e_i)]
    supply_rates = supply_rates[cols.tolist()[5:]]

    supply_meta = rates_df[cols.tolist()[1:5]][(rates_df.index >= s_i) & (rates_df.index <=e_i)]
    supply_meta = [' '.join(supply_meta.iloc[i].tolist()) for i in range(len(supply_meta.index))]

    rates_df = supply_rates.T
    rates_df.columns = supply_meta
    rates_df['DATE'] = supply_dates
    rates_df.to_csv(f'HDC/{file_name}.csv', index=False)
    # supply_rates.columns = supply_meta
    # print(len(supply_meta))
    # print(rates_df)
    # exit()

    # For design.
    colors = list(mpl.colormaps['Set2'].colors)

    s_f, supply_fig = plt.subplots(figsize=(12, 8))

    for id in range(len(supply_meta)):
        supply_fig.plot(list(range(len(supply_dates))), supply_rates.iloc[id].to_list(), color=colors[id], 
                        label=supply_meta[id], linewidth=2)
        
    supply_fig.set_ylabel('Price ($)')
    supply_fig.set_xlabel('Months Since 2023')
    
    b = supply_fig.get_position()
    supply_fig.set_position([b.x0, b.y0, b.width, b.height * 0.8])
    supply_fig.legend(loc='upper left', bbox_to_anchor=(0, 1.4))


    ss_f, supply_small_fig = plt.subplots(figsize=(12, 8))

    for id in range(len(supply_meta)):
        supply_small_fig.plot(supply_dates[107:119], supply_rates.iloc[id].to_list()[110:122], color=colors[id], 
                        label=supply_meta[id], linewidth=2)
        
    supply_small_fig.set_ylabel('Price ($)')
    supply_small_fig.set_xlabel('Date (YYYY-MM)')
    supply_small_fig.set_xticks(['2032-01', '2032-04', '2032-07', '2032-10', '2032-12'])
    supply_small_fig.set_xticks(['2032-01-01 01:00:00', '2032-04-01 01:00:00', '2032-07-01 01:00:00', '2032-10-01 01:00:00', '2032-12-01 01:00:00'])
    supply_small_fig.set_xticklabels(['2031-01', '2032-04', '2032-07', '2032-10', '2032-12'])
    
    b = supply_small_fig.get_position()
    supply_small_fig.set_position([b.x0, b.y0, b.width, b.height * 0.8])
    supply_small_fig.legend(loc='upper left', bbox_to_anchor=(0, 1.4))


    s_f.savefig(f'{file_name}.jpg')
    ss_f.savefig(f'{file_name}_small.jpg')


def plot_lmps(s_i, e_i, file_name):
    lmps_df = pd.read_excel(xslx, sheet_name='Monthly LMPs')
    cols = lmps_df.columns.tolist()

    rate_cols = ['All Hours', 'On Peak', 'Off Peak']

    lmp_dates = lmps_df[cols[2]][lmps_df.index >= 5]
    lmp_dates = [x.strftime("%Y-%m-01 01:00:00") for x in lmp_dates]

    lmp_rates = lmps_df[cols[s_i:e_i]][lmps_df.index >= 5]
    lmp_rates.columns = rate_cols

    # Create CSV for analysis.
    lmp_df = lmp_rates
    lmp_df['DATE'] = lmp_dates
    lmp_df.to_csv(f'HDC/{file_name}_data.csv', index=False)


    lmp_f, lmp_fig = plt.subplots(figsize=(12, 8))
    colors = list(mpl.colormaps['Set1'].colors)

    for i in range(len(rate_cols)):
        lmp_fig.plot(list(range(len(lmp_dates))), lmp_rates[lmp_rates.columns[i]], 
                     color=colors[i], label=rate_cols[i], linewidth=2 if i==0 else 1, alpha=0.7 if i>0 else 1)
    
    lmp_fig.set_xlabel('Months since June 2024')
    lmp_fig.set_ylabel('Price ($/MWh)')
    lmp_fig.legend(loc='upper left', prop={'size':15})
    lmp_f.tight_layout()
    lmp_f.savefig(f'EDA/{file_name}.jpg')

    slmp_f, lmp_small_fig = plt.subplots(figsize=(12, 8))
    for i in range(len(rate_cols)):
        lmp_small_fig.plot(lmp_dates[91:103], lmp_rates[lmp_rates.columns[i]].tolist()[91:103],
                     color=colors[i], label=rate_cols[i], linewidth=2 if i==0 else 1, alpha=0.7 if i>0 else 1)
        
    lmp_small_fig.set_xlabel('Date (YYYY-MM)')
    lmp_small_fig.set_ylabel('Price ($/MWh)')
    lmp_small_fig.legend(loc='upper left', prop={'size':15})
    lmp_small_fig.set_xticks(['2032-01-01 01:00:00', '2032-04-01 01:00:00', '2032-07-01 01:00:00', '2032-10-01 01:00:00', '2032-12-01 01:00:00'])
    lmp_small_fig.set_xticklabels(['2031-01', '2032-04', '2032-07', '2032-10', '2032-12'])
    slmp_f.tight_layout()
    slmp_f.savefig(f'EDA/{file_name}_small.jpg')


# plot_lmps(3, 6, 'PJM_LMP')
# plot_lmps(8, 11, 'MISO_LMP')
plot_rates(6, 13, 'supply_rates')
plot_rates(17, 22, 'transmission_rates')
