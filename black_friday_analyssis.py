# -*- coding: utf-8 -*-
"""Black_Friday_Analyssis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1C4YCQo655-gN-MIuKYLUV7gD_8UeI3Bz
"""

import numpy as np # linear algebra
import pandas as pd # data processing
import seaborn as sns
import matplotlib.pyplot as plt
!pip install miceforest
!pip install plotly
!pip install fancyimpute
from fancyimpute import IterativeImputer  # MICE imputer

bfs=pd.read_csv(r'/content/train.csv')

bfs.head()

"""Reading info from data"""

bfs.info()

bfs.columns

bfs.duplicated().value_counts()

"""Here we have total 550068 number of rows data including NaN value with no duplicated data"""

bfs.rename(columns=str.lower,inplace=True) #Convertig all the columns name in the lowercase for easy use.

bfs.columns

def unique(bfs):
    # Initialize an empty list to store rows
    data = []

    # Loop through the columns in the dataframe
    for col in bfs.columns:
        # Get the number of unique values in the column
        num_unique = bfs[col].nunique()

        # Add the unique values as a list to the 'Unique_values' column if num_unique <= 10
        if num_unique <= 10:
            unique_vals = list(bfs[col].unique())
        else:
            unique_vals = "More than 10 unique values"

        # Get the data type of the column
        data_type = bfs[col].dtype

        # Count the number of missing values in the column
        num_missing = bfs[col].isnull().sum()
        percent_of_missing = round((num_missing / bfs.shape[0]) * 100, 2)

        # Append a dictionary with the column details to the list
        data.append({
            'Column_name': col,
            'Data_type': data_type,
            'Number_of_unique': num_unique,
            'Unique_values': unique_vals,
            'Number_of_missing': num_missing,
            'percent_of_missing': percent_of_missing
        })

    # Create a dataframe from the list of dictionaries
    bfs_unique = pd.DataFrame(data)

    return bfs_unique

unique(bfs)

"""Handling the Missing values"""

mean_value = bfs["product_category_2"].mean()
mean_imputation=bfs["product_category_2"].fillna(mean_value)

median_value = bfs["product_category_2"].median()
median_imputation = bfs["product_category_2"].fillna(median_value)

"""Mean Imputation:

Filled missing values with the average (mean) of the column.

Result: The imputed distribution didn't align well with the original distribution.

"""

plt.figure(figsize=(12,8))

mean_imputation.plot(kind="kde" , color="blue")
median_imputation.plot(kind="kde" , color ="red")
bfs["product_category_2"].plot(kind="kde" , color ="yellow")
plt.legend()
plt.show()

"""Median Imputation:
used the middle value (median) of the column to fill in missing values.
Result: Similarly, this approach also failed to match the original distribution.
"""

from sklearn.preprocessing import LabelEncoder
Black_df_clean_mice = bfs.drop(["product_id" ,"user_id" ,"gender" ,"age" ,"city_category" ,"stay_in_current_city_years"] ,axis=1)
label_encoder_gender = LabelEncoder()
Black_df_clean_mice['Gender'] = label_encoder_gender.fit_transform(bfs['gender'])

label_encoder_age = LabelEncoder()
Black_df_clean_mice['Age'] = label_encoder_age.fit_transform(bfs['age'])
label_encoder_city = LabelEncoder()
Black_df_clean_mice['City_Category'] = label_encoder_city.fit_transform(bfs['city_category'])
label_encoder_city = LabelEncoder()
Black_df_clean_mice['Stay_In_Current_City_Years'] = label_encoder_city.fit_transform(bfs['stay_in_current_city_years'])

pip install dask[dataframe]

from miceforest import ImputationKernel

mice_kernel = ImputationKernel(data = Black_df_clean_mice,random_state = 2023)

mice_kernel.mice(2)
mice_imputation = mice_kernel.complete_data()
mice_imputation.head()

plt.figure(figsize=(12,8))

mean_imputation.plot(kind="kde" , color="blue")
median_imputation.plot(kind="kde" , color ="red")
Black_df_clean_mice["product_category_2"].plot(kind="kde" , color ="yellow") # mice (yellow)
bfs["product_category_2"].plot(kind="kde" , color="green") #original (green)
plt.legend()
plt.show()

"""MICE (Multiple Imputation by Chained Equations):

MICE is an advanced technique that uses all available data to predict missing values iteratively.
Since MICE requires numeric data, I performed quick encoding of categorical columns to numeric format.
Result: The imputed values using MICE matched the original data distribution almost perfectly! It was clear that MICE produced a far better result than simple mean or median imputation.

**Univariate Analysis**
"""

sns.set(style="whitegrid")

# Set the figure size (15x10 inches)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Customize and create countplots

# Age Distribution
sns.countplot(x='age', data=bfs,palette='pastel', ax=axes[0, 0],
              order=["0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"])
axes[0, 0].set_title('age distribution')
axes[0, 0].set_xlabel('age Group')
axes[0, 0].set_ylabel('count')

# Gender Distribution
sns.countplot(x='gender', data=bfs, palette='Set2', ax=axes[0, 1])
axes[0, 1].set_title('gender distribution')
axes[0, 1].set_xlabel('gender')
axes[0, 1].set_ylabel('count')

# Occupation Distribution
sns.countplot(x='occupation', data=bfs, palette='colorblind', ax=axes[0, 2])
axes[0, 2].set_title('occupation distribution')
axes[0, 2].set_xlabel('occupation')
axes[0, 2].set_ylabel('count')

# City Category Distribution
sns.countplot(x='city_category', data=bfs, palette='muted', ax=axes[1, 0])
axes[1, 0].set_title('city category distribution')
axes[1, 0].set_xlabel('city category')
axes[1, 0].set_ylabel('count')

# Stay in Current City Distribution
sns.countplot(x='stay_in_current_city_years', data=bfs, palette='pastel', ax=axes[1, 1])
axes[1, 1].set_title('stay in durrent dity distribution')
axes[1, 1].set_xlabel('years of stay')
axes[1, 1].set_ylabel('Count')

# Marital Status Distribution
sns.countplot(x='marital_status', data=bfs, palette='husl', ax=axes[1, 2])
axes[1, 2].set_title('marital status Distribution')
axes[1, 2].set_xlabel('marital status')
axes[1, 2].set_ylabel('count')

# Adjust layout to avoid overlapping and improve spacing
plt.tight_layout()

# Show the plot
plt.show()

# Distribution and Outliers of 'purchase'
plt.figure(figsize=(15,5))
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=1,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.subplot(1,2,1)
sns.kdeplot(x='purchase',data=bfs)
plt.subplot(1,2,2)
sns.boxplot(y='purchase',data=bfs)

plt.show()

#distribution of customer frequency by gender
bfs.groupby('gender').agg({'gender':'count'}).gender.plot(kind='pie',autopct='%1.1f%%',figsize=(5,5),shadow=True)
plt.show()

# distribution of purchases made by male and female customers separately using kernel density plots.
plt.figure(figsize=(10,4))
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=1.2,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
ma=bfs[bfs['gender']=='M'].value_counts('purchase').reset_index()
fe=bfs[bfs['gender']=='F'].value_counts('purchase').to_frame()
plt.subplot(1,2,1)
sns.kdeplot(x='purchase',data=ma).set_title('Male')
plt.subplot(1,2,2)
sns.kdeplot(x='purchase',data=fe).set_title('Female')
plt.show()

# total purchases made by each gender
p=bfs.groupby('gender').agg({'purchase':sum}).reset_index()
sns.barplot(x='gender',y='purchase',data=p,palette=['red','green'])
p

# top 50 most frequently purchased products
p_id=bfs.value_counts('product_id').sort_values(ascending=False).head(50)
plt.figure(figsize=(5,10))
sns.barplot(y=p_id.index,x=p_id,palette='viridis')
plt.show()

# the distribution of purchases made by unmarried and married customers
UM_P=bfs[bfs['marital_status']==0].value_counts('purchase').to_frame()
M_P=bfs[bfs['marital_status']==1].value_counts('purchase').to_frame()
plt.figure(figsize=(10,4))
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=1.2,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.subplot(1,2,1)
sns.kdeplot(x='purchase',data=UM_P).set_title('UnMarried')
plt.subplot(1,2,2)
sns.kdeplot(x='purchase',data=M_P).set_title('Married')
plt.show()

# distribution of marital status
bfs.groupby('marital_status').agg({'marital_status':'count'}).marital_status.plot(kind='pie',autopct='%1.1f%%',figsize=(5,5),shadow=True)
plt.show()

#purchase data based on gender and marital status
M_UM_P=bfs.groupby(['gender','marital_status']).agg({'purchase':sum}).reset_index()
UM=bfs[bfs['marital_status']==0].value_counts('product_id').nlargest(10)
M=bfs[bfs['marital_status']==1].value_counts('product_id').nlargest(10)
plt.subplots_adjust(left=1,
                    bottom=1,
                    right=3,
                    top=3,
                    wspace=0.4,
                    hspace=0.4)
plt.subplot(2,2,1)
sns.barplot(x='marital_status',y='purchase',hue='gender',data=M_UM_P)
plt.subplot(2,2,3)
UM.plot(x=UM.index,y=UM,kind='bar',title='UnMarried_Customer')
plt.subplot(2,2,4)
M.plot(x=M.index,y=M,kind='bar',title='Married_Customer')
M_UM_P

"""### Insights Gained

The analysis of the Black Friday shopping dataset provides valuable insights into consumer behavior and highlights key demographic trends. These findings can guide retailers in crafting effective marketing strategies.

---

#### **Findings**  

1. **Gender Distribution**  
   - **Male shoppers outnumber female shoppers**, indicating a potential gender imbalance in Black Friday participation.  

2. **Age Group**  
   - The **26–35 age group** is the most active demographic, suggesting this group drives the bulk of Black Friday shopping activity.  

3. **City Category**  
   - **City Category B** recorded the highest number of shoppers, emphasizing its prominence in Black Friday sales.  

4. **Stay Duration**  
   - Shoppers with a **1-year stay duration** in their current city were the most engaged, highlighting a trend among newer residents.  

5. **Marital Status**  
   - **Singles (Marital Status 0)** were the largest group of shoppers, making them a significant demographic during Black Friday.  

---

#### *Recommendations*  

1. **Targeted Gender-Based Campaigns**  
   - Design promotions and product bundles catering specifically to male and female shoppers.  
   - Use gender-specific advertising to enhance engagement and inclusivity.  

2. **Customized Age-Group Offers**  
   - Focus marketing efforts on the **26–35 age group**, the largest demographic.  
   - Create promotions tailored to their preferences and purchasing power.  

3. **City-Centric Marketing**  
   - Prioritize campaigns for **City Category B**, which has the highest shopper engagement.  
   - Offer exclusive, location-specific promotions to further incentivize purchases.  

4. **Appealing to New Residents**  
   - Develop strategies targeting individuals with a **1-year stay duration**, offering special deals for newcomers.  
   - Introduce **welcome packages** or **introductory discounts** to attract these customers.  

5. **Singles-Focused Promotions**  
   - Create campaigns tailored to the interests of singles (Marital Status 0).  
   - Highlight products and offers that resonate with single shoppers’ needs and lifestyles.  

6. **Omnichannel Engagement**  
   - Use an **omnichannel approach** to engage customers across platforms (e.g., social media, email, in-store).  
   - Provide consistent, personalized experiences across all touchpoints.  

7. **Personalized Recommendations**  
   - Leverage data analytics to recommend products based on **age, gender, and location**.  
   - Implement personalized promotions to improve conversion rates and customer satisfaction.  

8. **Customer Retention Strategies**  
   - Introduce **loyalty programs** and post-Black Friday deals to encourage repeat business.  
   - Focus on key demographic segments to build long-term relationships.

***Bivariate Analysis***
"""

# Creating and new df based  user_id and Total Purchase
user_purchase_sum = bfs.groupby('user_id')['purchase'].sum().reset_index()
user_purchase_sum.columns = ['user_id', 'total_purchase']

# Sort by 'Total_Purchase' in descending order and select the top 20 users
top_20_users = user_purchase_sum.sort_values(by='total_purchase', ascending=False).head(20)
top_20_users.head()

# Get the top 1000 users by purchase
top_1000_users = user_purchase_sum.nlargest(1000, 'total_purchase')

# Sum the total purchases for the top 1000 users
top_1000_sum = top_1000_users['total_purchase'].sum()

# Sum the total purchases for the remaining users
remaining_sum = user_purchase_sum['total_purchase'].sum() - top_1000_sum

# Create data for the pie chart
contributions = [top_1000_sum, remaining_sum]
labels = ['Top 1000 Users', 'Remaining Users']

# Plot a pie chart for top 1000 users vs remaining users' contribution
plt.figure(figsize=(8, 8))
plt.pie(contributions, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel2.colors)
plt.title('Top 1000 Users Contribution vs Remaining Users')
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
plt.show()

# Step 1: Group by User_ID and sum the purchases
user_purchase_sum = bfs.groupby('user_id')['purchase'].sum().reset_index()

# Step 2: Add the gender information to the aggregated user data
user_purchase_sum = user_purchase_sum.merge(bfs[['user_id', 'gender']].drop_duplicates(), on='user_id', how='left')

# Step 3: Get the top 1000 users by total purchase
top_1000_users = user_purchase_sum.nlargest(1000, 'purchase')

# Step 4: Count how many are male and how many are female in the top 1000 users
gender_count = top_1000_users['gender'].value_counts()

M, F = gender_count

# Create a list of 'M' and 'F' based on their counts
gender_data = ['M'] * M + ['F'] * F  # Creating a list of 'M' and 'F'

# Convert the list to a pandas Series
gender_series = pd.Series(gender_data)

# Create a countplot
plt.figure(figsize=(8, 6))
sns.countplot(x=gender_series, color='skyblue')

# Set plot labels and title
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Gender Distribution of Top 1000 Users')

# Show the plot
plt.show()

def plot_bivariate_analysis(feature):
    unique_values = bfs[feature].unique()
    num_values = len(unique_values)

    # Set up subplots
    fig, axes = plt.subplots(num_values, 3, figsize=(15, 4 * num_values)) #Fixed: Removed extra indentation
    fig.suptitle(f'Bivariate Analysis of Purchase with {feature} in Black Friday Dataset')
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    sns.set_style('darkgrid')

    for idx, value in enumerate(unique_values):
        # Histogram
        sns.histplot(bfs.loc[bfs[feature] == value]['purchase'], kde=False, ax=axes[idx, 0], label=value, bins=30 , palette='viridis' ) #Fixed: Changed 'Purchase' to 'purchase' to match the column name
        axes[idx, 0].set_title(f'Histogram - {value}')
        axes[idx, 0].set_xlabel('Purchase')
        axes[idx, 0].set_ylabel('Frequency')

        # KDE Plot
        sns.kdeplot(data=bfs.loc[bfs[feature] == value]['purchase'], ax=axes[idx, 1], label=value) #Fixed: Changed 'Purchase' to 'purchase' to match the column name
        axes[idx, 1].set_title(f'Kernel Density Estimation (KDE) - {value}')
        axes[idx, 1].set_xlabel('Purchase')
        axes[idx, 1].set_ylabel('Density')

        # Box Plot
        sns.boxplot(x=bfs[feature], y=bfs['purchase'], ax=axes[idx, 2], color='skyblue') #Fixed: Changed 'df' to 'bfs' to match the DataFrame variable and 'Purchase' to 'purchase'
        axes[idx, 2].set_title(f'Box Plot of Purchase by {feature} - {value}')
        axes[idx, 2].set_xlabel(f'{feature}')
        axes[idx, 2].set_ylabel('Purchase')

    plt.show()

plot_bivariate_analysis('gender')
plot_bivariate_analysis('city_category')
plot_bivariate_analysis('marital_status')

def plot_purchase_histogram_separately(feature, bfs):
    # Ensure the feature exists in the DataFrame
    if feature not in bfs.columns:
        raise ValueError(f"{feature} not found in DataFrame columns")

    # Sort the DataFrame by 'Purchase' within each category
    sorted_df = bfs.groupby(feature)['purchase'].sum().reset_index()
    sorted_df = sorted_df.sort_values('purchase', ascending=False)

    # Create a separate histogram for each feature with reduced size
    plt.figure(figsize=(8, 5))  # Reduced figure size

    # Plot the histogram for the 'Purchase' values grouped by the feature's categories
    sns.histplot(sorted_df, x=feature, weights='purchase', kde=False, discrete=False, bins=len(sorted_df), palette='viridis')

    # Set title and labels
    plt.title(f'Purchase Distribution by {feature}')
    plt.xlabel(feature)
    plt.ylabel('purchase')

    # Show the plot
    plt.show()

# Example Usage:
plot_purchase_histogram_separately('age', bfs)
plot_purchase_histogram_separately('occupation', bfs)
plot_purchase_histogram_separately('stay_in_current_city_years', bfs)

"""# ***Insights ***

The analysis highlights that a significant concentration of purchasing power lies within a small portion of the user base, with the top 1000 users contributing 50.3% of total sales out of 5891 unique user IDs. This distribution aligns with the Pareto Principle, where a smaller group drives a disproportionately large share of revenue.


* Top 1000 Users: Contribute 50.3% of total purchases.
Remaining 4891 Users: Account for 49.7% of purchases.
* Gender Distribution: Among the top 1000 users, 797 are male and 203 are female, reflecting a strong contribution from male users while also highlighting a notable market share for female users.

* Targeted Marketing: Prioritize engagement with the top 1000 users to capitalize on their significant contribution to total sales.
* Gender-Specific Strategies: Although male users dominate purchasing activity, the contribution from female users presents an opportunity to enhance engagement and boost their share of sales.
* By focusing on the top-performing users and implementing tailored strategies for both genders, businesses can further optimize sales and foster stronger customer retention.


"""

# Convert categorical columns to numerical codes
bfs_copy = bfs.copy()

columns_to_convert = ['product_id', 'gender', 'age', 'city_category', 'stay_in_current_city_years']
for col in columns_to_convert:
    bfs_copy[col] = bfs_copy[col].astype('category').cat.codes

# Calculate correlation matrix
correlation_matrix = bfs_copy.corr(method='pearson')

# Plot heatmap
plt.figure(figsize=(13, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, center=0)
plt.title('Correlation Heatmap for Categorical Features')
plt.show()

"""### Correlation Analysis of Features with Purchase  

The correlation matrix provides the following insights regarding the relationship between various features and purchase behavior:  

---

#### **Features with Low Correlation to Purchase**  
1. **Marital_Status**:  
   - Correlation: **-0.00046**  
   - Insight: Marital status has no significant impact on purchasing behavior.  

2. **Stay_In_Current_City_Years**:  
   - Correlation: **0.0054**  
   - Insight: The duration of stay in the current city shows minimal influence on purchase decisions.  

3. **Gender**:  
   - Correlation: **0.0603**  
   - Insight: Gender has a very weak positive correlation, indicating little effect on purchasing behavior.  

---

#### **Features with Weak Positive Correlation**  
1. **Age**:  
   - Correlation: **0.0158**  
   - Insight: Age has a slight positive correlation, suggesting a minimal impact on purchasing patterns.  

2. **City_Category**:  
   - Correlation: **0.0619**  
   - Insight: City category has a weak positive correlation, indicating limited influence on purchases.  

---

#### **Product Categories**  
1. **Product_Category_1**:  
   - Correlation: **-0.3437**  
   - Insight: A moderate negative correlation suggests an inverse relationship with purchase behavior and warrants further investigation.  
   
2. **Product_Category_2** and **Product_Category_3**:  
   - Correlation: Weak negative correlations.  
   - Insight: These categories show limited impact on purchasing behavior.  

---

#### **Key Insights**  
- **Low-Impact Features**: Marital_Status, Stay_In_Current_City_Years, and Gender show negligible correlation with Purchase and may not significantly contribute to predictive modeling.  
- **Product_Category_1**: The most notable feature with a moderate negative correlation, deserving further exploration to understand its effect.  

---

#### **Recommendations**  
1. **Feature Selection**:  
   - Remove low-impact features like Marital_Status, Stay_In_Current_City_Years, and Gender to reduce dimensionality and improve model efficiency.  

2. **Focus on Product Categories**:  
   - Conduct deeper analysis of Product_Category_1 and other product categories to better understand their influence on purchasing behavior.  
   - Refine feature selection for predictive modeling based on these insights.  

---

This analysis suggests prioritizing actionable features and optimizing the model by eliminating irrelevant variables, ultimately improving predictive accuracy and efficiency.
"""