import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
bmi = df['weight'] / ((df['height'] / 100) ** 2)
overweight = (bmi > 25).astype(int)
df['overweight'] = overweight

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
cholesterol_is_1 = df['cholesterol'] == 1
df.loc[cholesterol_is_1, 'cholesterol'] = 0
df.loc[~cholesterol_is_1, 'cholesterol'] = 1
gluc_is_1 = df['gluc'] == 1
df.loc[gluc_is_1, 'gluc'] = 0
df.loc[~gluc_is_1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    categorical_cols = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight', 'cardio']
    df_cat = df[categorical_cols]
    df_cat = pd.melt(df_cat, id_vars='cardio', var_name='variable', value_name='value')

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.


    # Draw the catplot with 'sns.catplot()'

    # Get the figure for the output
    fig = sns.catplot(x='variable', hue='value', col='cardio', data=df_cat, kind='count', height=6, aspect=0.7)


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])]
    df_heat = df_heat[(df['height'] >= df['height'].quantile(0.025))]
    df_heat = df_heat[(df['height'] <= df['height'].quantile(0.975))]
    df_heat = df_heat[(df['weight'] >= df['weight'].quantile(0.025))]
    df_heat = df_heat[(df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()
    corr = corr.round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10,10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, cmap="YlGnBu", annot=True, fmt=".1f", mask=mask) 

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig