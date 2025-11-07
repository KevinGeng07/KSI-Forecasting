### Combining all past data files for historical data analysis.
import pandas as pd
from datetime import datetime
import numpy as np
from tabulate import tabulate 


### EIA-861M Monthly Electric Power Industry Report
eia_861_csv = pd.read_csv('../HDC_pt2/EIA_861/EIA_electricpowerindustryreport.csv')

### EIA Electric Power Monthly
eia_epm_csv = pd.read_csv('../HDC_pt2/EIA_EPM/EIA_netgeneration.csv')

### ICC Historical Prices-to-Compare
icc_ptc_csv = pd.read_csv('../HDC/historical_PTC.csv')

print(len(eia_861_csv), len(eia_epm_csv), len(icc_ptc_csv))

### Convert all datasets to have the time format as a datetime.datetime object in "YYYY-MM" format.
eia_861_datetime = [datetime.strptime(x+y, '%Y%m') for x, y in zip(eia_861_csv['Year'].astype(str).tolist(), eia_861_csv['Month'].astype(str).tolist())]
eia_861_csv.insert(0, 'Datetime', eia_861_datetime)
eia_861_csv.drop(['Year', 'Month'], axis=1, inplace=True)

eia_epm_datetime = [datetime.strptime(x+y, '%Y%m') for x, y in zip(eia_epm_csv['Year'].astype(str).tolist(), eia_epm_csv['Month'].astype(str).tolist())]
eia_epm_csv.insert(0, 'Datetime', eia_epm_datetime)
eia_epm_csv.drop(['Year', 'Month'], axis=1, inplace=True)

icc_ptc_datetime = [datetime.strptime(x.split()[0], '%Y-%m-%d') for x in icc_ptc_csv['DATE'].tolist()]
icc_ptc_csv.insert(0, 'Datetime', icc_ptc_datetime)
icc_ptc_csv.drop(['DATE'], axis=1, inplace=True)

### Join dataframes together.
combined_csv = pd.concat([eia_861_csv.set_index('Datetime'), eia_epm_csv.set_index('Datetime'), icc_ptc_csv.set_index('Datetime')], axis=1, join='outer')
combined_csv = combined_csv.reset_index()

### Remove redundant columns (SEE MORE).
## Some columns, like the 'Total' columns, contain redundant information, as they are the summation of other features. 
## For most linear models for analysis, redundant information obfuscates proper analytical insights.
## Sources: Dormann et al. 2013 (https://nsojournals.onlinelibrary.wiley.com/doi/full/10.1111/j.1600-0587.2012.07348.x), Tu et al. 2004 (https://onlinelibrary.wiley.com/doi/full/10.1111/j.1600-0722.2004.00160.x), 
combined_csv.drop(['TOTAL Revenue', 'TOTAL Sales', 'TOTAL Customers', 'TOTAL Price', 'Total'], axis=1, inplace=True)


### Compute raw data statistics.
writefile = 'PTC_ts_stats.txt'
open(writefile, 'w').close()
labels = ['Feature', '25th', 'Median', '75th', 'Mean', 'Std. Dev']

with open(writefile, 'a') as f:
    f.write('Raw Data Statistics\n')

    f_stats = []
    for c in combined_csv.columns:
        if c == 'Datetime': continue

        c_list = combined_csv[c].to_numpy()
        f_stats.append([c, np.nanpercentile(c_list, 25), np.nanmedian(c_list), np.nanpercentile(c_list, 75), np.nanmean(c_list), np.nanstd(c_list)])
    
    f.write(tabulate([labels] + f_stats))
    f.write('\n\n')
    f.close()

### Inspect NaNs -> impute NaNs with 0s.
print(combined_csv.isna().sum())

combined_csv = combined_csv.fillna(0)

### Compute imputed data statistics.
with open(writefile, 'a') as f:
    f.write('Imputed Data Statistics\n')

    f_stats = []
    for c in combined_csv.columns:
        if c == 'Datetime': continue

        c_list = combined_csv[c].to_numpy()
        f_stats.append([c, np.nanpercentile(c_list, 25), np.nanmedian(c_list), np.nanpercentile(c_list, 75), np.nanmean(c_list), np.nanstd(c_list)])
    
    f.write(tabulate([labels] + f_stats))
    f.write('\n\n')
    f.close()

combined_csv.to_csv('PTC_ts.csv', index=False)
