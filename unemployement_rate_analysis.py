# ## Loading Data and Importing Libraries

# importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns


# reading file
unemployment_df = pd.read_csv("file_directory_here/Unemployment_data.csv")
unemployment_df.info()
unemployment_df.head()


# ## Data Cleaning and Data Preparation


# remove spaces in column names
unemployment_df.columns = unemployment_df.columns.str.strip()

unemployment_df.head()



# handling missing values

# check missing values
print("Missing values in unemployment_df: \n")
print(unemployment_df.isnull().sum())



# remove rows with missing data
unemployment_df = unemployment_df.dropna()



# check missing values
print("Missing values in unemployment_df: ")
print(unemployment_df.isnull().sum())



# change datatype of date to datetime

unemployment_df["Date"] = pd.to_datetime(unemployment_df["Date"], errors = "coerce", dayfirst=True)
print(unemployment_df["Date"].dtype)



# Handling inconsistent values

unemployment_df['Frequency'] = unemployment_df['Frequency'].str.strip()
unemployment_df["Frequency"] = unemployment_df["Frequency"].replace({"M" : "Monthly" , "Monthly" : "Monthly"})

print(unemployment_df.head())



# checking for duplicate rows

duplicate_rows = unemployment_df.duplicated().sum()
print(f'Number of duplicate rows: {duplicate_rows}')


# # Exploratory Data Analysis


unemployment_df.describe()


# ## Average Unemployment Rate by Region


# Group by Region and calculate mean unemployment rate
by_region = unemployment_df.groupby("Region")["Estimated Unemployment Rate (%)"].mean().reset_index()
top_10_region = by_region.sort_values(by = "Estimated Unemployment Rate (%)" , ascending = False).head(10) 


# Graph
plt.figure(figsize = (8,3))
sns.barplot(x= "Region",y="Estimated Unemployment Rate (%)", 
          hue = "Region", data = top_10_region, palette="Reds_r")

plt.xticks(rotation=60, fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("Region")
plt.ylabel("Avg Unemployment Rate (%)")
plt.title("Unemployment Rate by Region", fontsize = 15, fontweight = "bold")
plt.show()


# ## Average Unemployment Rate by Month


# Extracting month and year from "date" column
unemployment_df["Month"] = unemployment_df["Date"].dt.month_name()
unemployment_df["Year"] = unemployment_df["Date"].dt.year.astype(int)

unemployment_df["Year"] = unemployment_df["Year"].sort_values(ascending = True)



# Group by Region and calculate mean unemployment rate

by_month = unemployment_df.groupby(["Year", "Month"],observed=False)["Estimated Unemployment Rate (%)"].mean().reset_index()

# define month order
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# set month_name in correct order
unemployment_df["Month"] = pd.Categorical(unemployment_df["Month"], categories = month_order, ordered = True)

# sorting by year and month
by_month = by_month.sort_values("Year", ascending = True)

# Graph
plt.figure(figsize = (9,4))
sns.barplot(x= "Month",y="Estimated Unemployment Rate (%)", 
          hue = "Year", data = by_month, palette="Set2",dodge = False)

plt.xticks(rotation=60, fontsize = 10)
plt.yticks(fontsize = 10)
plt.xlabel("Month")
plt.ylabel("Avg Unemployment Rate (%)")
plt.title("Unemployment Rate by Month", fontsize = 15, fontweight = "bold")
plt.show()


# ## Average Unemployment Rate by Area (Rural vs Urban)


# Group by Area and calculate mean unemployment rate
by_area = unemployment_df.groupby("Area")["Estimated Unemployment Rate (%)"].mean().reset_index()

# visualization
labels = by_area["Area"]
sizes = by_area["Estimated Unemployment Rate (%)"]
plt.figure(figsize = (6, 4))
plt.pie(sizes, labels = labels, autopct = "%1.1f%%",startangle = 90, colors = sns.color_palette("Paired", len(sizes)))
plt.title("Unemployment Rate by Area", fontweight = "bold")
plt.show


# ## Estimated Labour Participation vs Unemployment Rate


# Sort data by date 
unemployment_df = unemployment_df.sort_values(by="Date")

# Plot line chart
plt.figure(figsize=(8, 4))
sns.lineplot(x="Date", y="Estimated Labour Participation Rate (%)",
             data=unemployment_df,
             label="Labour Participation Rate",
             marker="o",
             errorbar=None)
sns.lineplot(x="Date", y="Estimated Unemployment Rate (%)",
             data=unemployment_df,
             label="Unemployment Rate",
             marker="o",
             errorbar=None)

# Formatting
plt.xlabel("Date")
plt.ylabel("Percentage (%)")
plt.title("Labour Participation Rate vs Unemployment Rate Over Time", fontweight="bold")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()  # Show legend
plt.grid(True, linewidth=0.5, alpha=0.5)
plt.show()



# Calculate averages
avg_labour_participation = unemployment_df["Estimated Labour Participation Rate (%)"].mean()
avg_unemployment = unemployment_df["Estimated Unemployment Rate (%)"].mean()
avg_employment = avg_labour_participation - avg_unemployment 

# Create DataFrame for plotting
avg_data = {
    "Category": ["Labour Participation Rate", "Employment Rate", "Unemployment Rate"],
    "Average (%)": [avg_labour_participation, avg_employment, avg_unemployment]
}

avg_df = pd.DataFrame(avg_data)

# Plot bar chart
plt.figure(figsize=(6, 4))
sns.barplot(x="Category", y="Average (%)", hue="Category", data=avg_df, palette="Set2")

plt.xlabel("")
plt.ylabel("Average Percentage (%)")
plt.title("Average Labour Participation, Employment, and unemployment Rates", fontweight="bold")
plt.xticks(rotation=20)  
plt.show()

