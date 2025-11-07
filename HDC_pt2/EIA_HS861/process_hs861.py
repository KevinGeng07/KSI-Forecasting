import pandas as pd
import matplotlib.pyplot as plt

hs_1990 = pd.read_excel('HS861M 1990-2009.xlsx')
hs_2010 = pd.read_excel('HS861M 2010-.xlsx')

sector_types = ['RESIDENTIAL', 'COMMERCIAL', 'INDUSTRIAL', 'TRANSPORTATION', 'TOTAL']
pricing_types = ['Revenue', 'Sales', 'Customers', 'Price']
unit_types = ['Thousand Dollars', 'Megawatthours', 'Count', 'Cents/kWh']
metadata = ['Year', 'Month']

### Filter out non-IL states.
hs_1990 = hs_1990.iloc[2:][hs_1990['Unnamed: 2'] == 'IL']
hs_2010 = hs_2010.iloc[2:][hs_2010['Unnamed: 2'] == 'IL']

### Drop unnecessary columns.
hs_1990.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'OTHER', 'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23'], inplace=True)
hs_2010.drop(columns=['Unnamed: 2', 'Unnamed: 3'], inplace=True)

hs_1990 = pd.concat([pd.DataFrame(hs_2010.to_numpy()), pd.DataFrame(hs_1990.to_numpy())], ignore_index=True).iloc[::-1]
hs_1990.columns = metadata + [s + ' ' + p for s in sector_types for p in pricing_types]

### Convert Year & Month to string format.
hs_1990['Year'] = hs_1990['Year'].astype(str)
hs_1990['Month'] = hs_1990['Month'].astype(str).apply(lambda x: x.zfill(2))

### Inspect null values. -> No nulls, but '.' in-place of null.
print(hs_1990.isna().sum())
hs_1990 = hs_1990.replace('.', 0)

hs_1990.to_csv('EIA_electricpowerindustryreport.csv', index=False)

### Create basic trend plots.
fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(20, 15))
plt.subplots_adjust(left=0.1, right=0.9, top=0.925, bottom=0.05, hspace=0.4)

dates = (hs_1990['Year'] + hs_1990['Month']).astype(int)
colors = ['red', 'orange', 'blue', 'green', 'purple']

lines = []
labels = []

for c in range(4):
    for i, start_index in enumerate([c + 2 + i * 4 for i in range(5)]):
        line, = axs[c].plot(dates, hs_1990[hs_1990.columns[start_index]], 
                            label=sector_types[i], color=colors[i], linewidth=1.5)
        
        if c == 0:
            lines.append(line)
            labels.append(sector_types[i])
    
    if c == 3:
        axs[c].set_xlabel('Date', fontsize=10)
    
    axs[c].set_xticks([199001, 199501, 200001, 200501, 201001, 201501, 202001, 202501])
    axs[c].set_xticklabels(['1990', '1995', '2000', '2005', '2010', '2015', '2020', '2025'])
    axs[c].set_ylabel(f'{pricing_types[c]}\n({unit_types[c]})', fontsize=10)
    axs[c].set_title(pricing_types[c], fontsize=12, fontweight='bold', pad=7.5)
    axs[c].tick_params(axis='x', rotation=45, labelsize=8)
    axs[c].tick_params(axis='y', labelsize=8)
    axs[c].set_xlim([dates.min(), dates.max()])
    axs[c].grid(True, alpha=0.3, linestyle='--')


fig.legend(lines, labels, loc='upper center', ncol=5, bbox_to_anchor=(0.5, 0.975), frameon=True, fancybox=True, shadow=True, fontsize=9)

fig.suptitle('Illinois Electricity Market Analysis (1990-2025)', fontsize=14, fontweight='bold', y=0.99)

plt.savefig('HS861M_Plots.jpg')
