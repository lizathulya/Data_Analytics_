# -*- coding: utf-8 -*-
"""CDC_DEATH_ANALYSIS.

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pW2Llpt5f-oYZlz8Gy5UPvD2id6905rw
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import re

df = pd.read_csv(r'/content/2015_death_data.csv')
df.head()

df.info()

# Check for missing values
print(df.isnull().sum())

# Clean missing values
print(len(df))
df = df[df.detail_age != 999]
# Create a copy of df and assign it to mort
#mort = df.copy()
# Now you can use mort in the following lines
#mort = mort[mort.detail_age_type == 1] # Remove ages below 1
df['detail_age'].loc[df['detail_age_type'] != 1] = 0
df = df[df.day_of_week_of_death != 9]
df = df[df.marital_status != 'U']
df = df[df.place_of_death_and_decedents_status != 9]
#mort = mort[mort.age_recode_27 != 12]
#mort = mort[mort['education_2003_revision']!= 9]
#mort = mort[mort['education_2003_revision'].notna()]
#mort = mort[mort['age_recode_27'] !=27]

print(df)

my_cols=['month_of_death', 'day_of_week_of_death', 'sex']
my_dataset = df[my_cols]

plt.figure(figsize=(14,7))
sns.countplot(x=my_dataset['month_of_death'], hue=my_dataset['day_of_week_of_death'])

my_dataset['day_of_week_of_death'].mean()

column = '39_cause_recode'


disease_dpa =[]
total_dpa = []
age_ratio=[]
max_age = np.max(df['detail_age'].unique())
for i in range(max_age):
    total_deaths = df[column][df['detail_age']==i].count()
    disease_deaths = df[column][df['detail_age']==i][df[column]==27].count()
    if total_deaths == 0:
        total_dpa.append(0)
        disease_dpa.append(0)
        age_ratio.append(0)
    else:
        total_dpa.append(total_deaths)
        disease_dpa.append(disease_deaths)
        age_ratio.append(disease_deaths/total_deaths)



start = 0
end = 105
fig,(ax, ax2) = plt.subplots(1, 2, figsize = (16,9))
total_dpa = total_dpa[start:end]
disease_dpa = disease_dpa[start:end]
age_ratio = age_ratio[start:end]

ax.scatter(np.linspace(start+1,end, num=len(age_ratio)), disease_dpa, marker= '.', label = 'Ischemic Heart Disease')
#ax2=ax.twinx()
ax.scatter(np.linspace(start+1, end, num=len(age_ratio)), total_dpa, c = 'red', marker = '.',label = 'Total Deaths' )

ax.set_xlabel('Age of decedent')
ax.set_ylabel('Deaths')
ax.legend()

ax2.scatter(np.linspace(start+1, end, num=len(age_ratio)), age_ratio, c = 'purple', marker = '.',label = 'Ischemic Heart Disease Ratio' )
ax2.set_xlabel('Age of decedent')
ax2.set_ylabel('Ratio')
ax2.legend()

# Select only numerical features for correlation analysis
numerical_df = df.select_dtypes(include=np.number)

# Calculate and plot the correlation heatmap
sns.heatmap(numerical_df.corr())
print(numerical_df.corr())