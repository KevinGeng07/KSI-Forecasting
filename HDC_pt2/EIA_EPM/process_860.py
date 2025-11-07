import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sheet_names = ['2001_2002_FINAL', '2003_2004_FINAL', '2005-2007_FINAL', '2008-2009_FINAL', '2010-2011_FINAL', '2012_Final', '2013_Final', '2014_Final', '2015_Final', '2016_Final', '2017_Final', '2018_Final', '2019_Final', '2020_Final', '2021_Final', '2022_Final', '2023_Final', '2024_Final', '2025_Preliminary']

def process_sheet(in_sheet):
    in_sheet = pd.read_excel('generation_monthly.xlsx', sheet_name=in_sheet)
    if 'YEAR' not in in_sheet.columns:
        in_sheet.columns = in_sheet.iloc[3]
        in_sheet = in_sheet.iloc[4:]
    
    in_sheet.columns = list(map(lambda x: x.replace('\n', ' '), in_sheet.columns))

    ### Filter out non-IL states & keep only total electric generation stats.
    in_sheet = in_sheet[(in_sheet['STATE'] == 'IL') & (in_sheet['TYPE OF PRODUCER'] == 'Total Electric Power Industry')]

    ### Pivot energy source as new columns.
    in_sheet = in_sheet.pivot(index=['YEAR', 'MONTH'], columns='ENERGY SOURCE', values='GENERATION (Megawatthours)')

    ### Join year & month columns to the left of dataframe.
    ### TODO: IMPLEMENT .reset_index()
    in_sheet = in_sheet.reset_index()
    print(in_sheet.columns)

    return in_sheet

### Create combined dataframe for generation data.
combined_generation = None
for sheet in sheet_names:
    print(sheet)
    out_sheet = process_sheet(sheet)

    if combined_generation is None:
        combined_generation = out_sheet
    else: 
        combined_generation = pd.concat([combined_generation, out_sheet], axis=0)

### Inspect NaNs -> fill missing values with 0.
print(combined_generation.isna().sum())
combined_generation = combined_generation.fillna(0)

### Convert Year & Month to string format.
combined_generation['YEAR'] = combined_generation['YEAR'].astype(str)
combined_generation['MONTH'] = combined_generation['MONTH'].astype(str).apply(lambda x: x.zfill(2))

### Rearrange columns + update names for readability.
sorted_cols = ['YEAR', 'MONTH'] + sorted([c for c in combined_generation.columns if c not in ['YEAR', 'MONTH', 'Total']]) + ['Total']
combined_generation = combined_generation[sorted_cols]
combined_generation.columns = list(map(lambda x: x[0].upper() + x[1:].lower(), combined_generation.columns))

combined_generation.to_csv('EIA_netgeneration.csv', index=False)

### Create basic trend plots.
fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(20, 5))

dates = (combined_generation['Year'] + combined_generation['Month']).astype(int)
# colors = iter(plt.cm.viridis(np.linspace(0, 1, 12)))
colors = iter(plt.get_cmap('tab20').colors)

for c in range(12):
    axs.plot(dates, combined_generation[combined_generation.columns[2 + c]], label=combined_generation.columns[2+c], color=next(colors), linewidth=1.5)


axs.set_xticks([200101, 200601, 201101, 201601, 202101, 202508])
axs.set_xticklabels(['2001', '2006', '2011', '2016', '2021', '08/2025'])
axs.set_ylabel('Generation (Megawatthours)')
axs.set_title('Electrical Generation by Source', fontsize=12, fontweight='bold', pad=7.5)
axs.tick_params(axis='x', rotation=45, labelsize=8)
axs.tick_params(axis='y', labelsize=8)
axs.set_xlim([dates.min(), dates.max()])
axs.grid(True, alpha=0.3, linestyle='--')


# fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.975), frameon=True, fancybox=True, shadow=True, fontsize=9)

fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.125), frameon=True, fancybox=True, shadow=True, fontsize=9, ncols=6)
plt.subplots_adjust(bottom=0.2)

fig.suptitle('Illinois Electricity Generation Analysis (2001-2025)', fontsize=14, fontweight='bold', y=0.99)
plt.savefig('EPM_Plots.jpg')
