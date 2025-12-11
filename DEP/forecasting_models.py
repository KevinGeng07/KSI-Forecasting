import sklearn
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import os

data_file = pd.read_csv('PTC_ts.csv')

if not os.path.exists('ML'): os.mkdir('ML')

def correlation_cluster_test():
    data = data_file[(data_file['C RES PRICE'] != 0) & (data_file['A RES PRICE'] != 0)]

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(14, 7))
    plt.subplots_adjust(top=0.775, hspace=0.075)

    orgs = ['ComEd', 'Ameren']
    for i, org in enumerate(['C RES PRICE', 'A RES PRICE']):

        for color, split in zip(['#E69F00', '#56B4E9', '#009E73'], ['RESIDENTIAL Sales', 'COMMERCIAL Sales', 'INDUSTRIAL Sales']):

            X = data[split].to_list()
            X = (X - np.mean(X)) / np.std(X)

            y = data[org].to_list()

            axs[i].scatter(X, y, c=color, s=65, linewidths=0.5, edgecolor='black',
                            label=split.split(' ')[0].lower().capitalize())
            
            axs[i].set_xticks([-3, -2, -1, 0, 1, 2, 3])
            axs[i].set_yticks([3.5, 5, 6.5, 8, 9.5, 11, 12.5])

            axs[i].tick_params(axis='x', labelsize=14)
            axs[i].tick_params(axis='y', labelsize=14)

        
        axs[i].set_title(orgs[i], fontsize=18, fontweight='bold')


    fig.supxlabel("Standard Deviation Sales ($)", fontsize=16, fontweight='bold', y=0.025)
    fig.supylabel("Static PTC Price (¢/kWh)", fontsize=16, fontweight='bold', x=0.065, y=0.45)
    fig.suptitle("3-Class Demand vs. PTC Prices", fontsize=20, fontweight='bold', y=0.935)

    handles, labels = [], []
    for ax in axs:
        h, l = ax.get_legend_handles_labels()
        handles += h
        labels += l

    # Remove duplicates while keeping order
    unique = dict(zip(labels, handles))
    fig.legend(unique.values(), unique.keys(), loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.9), shadow=True, fontsize=14)

    fig.savefig('ML/correlation_test.jpg')

def feature_importances():
    data = data_file[data_file['Coal'] != 0]

    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(14, 7))
    plt.subplots_adjust(top=0.7, hspace=0.075)

    features = ['Coal', 'Hydroelectric conventional', 'Natural gas', 'Nuclear', 'Other', 'Other biomass', 'Other gases', 
                'Petroleum', 'Solar thermal and photovoltaic', 'Wind', 'Wood and wood derived fuels']


    legend_labels = [f'{i+1}. {name}' for i, name in enumerate(features)]

    # 2. Create the legend handles. We need a dummy handle for the legend to draw a key.
    # We use a scatter plot handle with a simple circle marker.
    # We only need one handle, as the key is the index-to-name mapping.
    # Note: 's=0' makes the scatter points invisible, and 'color' is just for the key's color.
    legend_handle = axs[0].scatter([], [], s=100, marker='s', color='white', label='Feature Key')
    legend_handles = [legend_handle] * len(legend_labels)


    orgs = ['Residential', 'Commercial', 'Industrial']
    for i, (color, split) in enumerate(zip(['#E69F00', '#56B4E9', '#009E73'], ['RESIDENTIAL Sales', 'COMMERCIAL Sales', 'INDUSTRIAL Sales'])):
        X = data[features]
        y = data[split]
        
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        model = Ridge(alpha=1.0)
        model.fit(X, y)

        result = permutation_importance(model, X, y, n_repeats=25, random_state=67, scoring='r2')

        importances_mean = result.importances_mean
        importances_std = result.importances_std

        print(importances_mean)

        z = stats.norm.ppf(0.975)

        ci_lower = importances_mean - z * importances_std / np.sqrt(15)
        ci_upper = importances_mean + z * importances_std / np.sqrt(15)


        indices = np.argsort(importances_mean)[::-1]  # descending
        top_n = 7
        top_indices = indices[:top_n]
        
        top_importances = importances_mean[top_indices]
        top_ci_lower = ci_lower[top_indices]
        top_ci_upper = ci_upper[top_indices]

        # Compute symmetric error bars for matplotlib
        top_err = [top_importances - top_ci_lower, top_ci_upper - top_importances]

        y_pos = np.arange(len(top_indices))

        axs[i].barh(y_pos, top_importances, xerr=top_err, color=color, edgecolor='black')

        axs[i].set_yticks(y_pos)
        axs[i].set_yticklabels([str(i+1) for i in top_indices])

        axs[i].tick_params(axis='x', labelsize=14)
        axs[i].tick_params(axis='y', labelsize=14)

        axs[i].invert_yaxis()

        axs[i].set_title(orgs[i], fontsize=18, fontweight='bold')


    fig.legend(legend_handles, legend_labels, loc='upper center', ncol=4, 
               bbox_to_anchor=(0.5, 0.89), fontsize=12, shadow=True, handlelength=0)

    fig.supxlabel("Permutation Importance Score", fontsize=16, fontweight='bold', y=0.025)
    fig.supylabel("Feature", fontsize=16, fontweight='bold', x=0.08, y=0.4)
    fig.suptitle("3-Class Sales' Permutation Importance", fontsize=20, fontweight='bold', y=0.95)

    fig.savefig('ML/permutation_importance.jpg')
    print(features)


correlation_cluster_test()
feature_importances()
