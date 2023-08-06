import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    """
    Load the dataset

    Returns:
    - df (DataFrame): the dataset
    """
    df = pd.read_csv("/Users/tiziano/Documents/Datasets/Spryfox/dataset.csv")
    return df

def plot_prices(df):
    """
    Plot histograms of the prices in the dataset.
    
    Args:
    - df (DataFrame): the dataset
    """
    # create subplots
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))

    # plot histograms with different bin sizes
    axs[0, 0].hist(df['price'], bins=50)
    axs[0, 0].set_title('Bin Size = 50')
    axs[0, 1].hist(df['price'], bins=100)
    axs[0, 1].set_title('Bin Size = 100')

    # plot histograms with different x-axis limits
    axs[1, 0].hist(df['price'], range=(0, 1000))
    axs[1, 0].set_title('X-axis Limit = (0, 1000)')
    axs[1, 1].hist(df['price'], range=(0, 500))
    axs[1, 1].set_title('X-axis Limit = (0, 500)')

    # plot histograms with a logarithmic y-axis scale and different bin size
    axs[0, 2].hist(df['price'], bins=50)
    axs[0, 2].set_yscale('log')
    axs[0, 2].set_title('Logarithmic Y-axis (Bin Size = 50)')
    axs[1, 2].hist(df['price'], bins=100)
    axs[1, 2].set_yscale('log')
    axs[1, 2].set_title('Logarithmic Y-axis (Bin Size = 100)')

    # set common x-axis label and y-axis label
    fig.text(0.5, 0.04, 'Price', ha='center')
    fig.text(0.04, 0.5, 'Count', va='center', rotation='vertical')

    # adjust subplot spacing
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # figure title
    plt.suptitle("Histograms of prices")

    # show plot
    plt.show()    

def filter_categories(df):
    """
    Generate new field with the root category code and filter out rows with NaN values in the price column

    Args:
        df (pandas.DataFrame): DataFrame containing the category_code and price columns

    Returns:
        pandas.DataFrame: DataFrame with new columns
    """
    # copy df in order to then extract the 'root' category code
    df_filtered = df.copy().dropna(subset=['category_code'])

    # extract root string
    df_filtered['root_cat_code'] = df_filtered['category_code'].str.split('.').str[0]

    # drop rows with NaN values in the 'price' column
    df_cat_filtered = df_filtered.dropna(subset=['price'])

    return df_cat_filtered

def plot_categories(df, N = 10):
    """
    Plot the top N categories and the "other" category

    Args:
        df (pandas.DataFrame): DataFrame containing the root_cat_code column
        N (int, optional): number of top categories to plot

    Returns:
        None
    """
    # Get the frequency counts for each category
    # Note to self: the resulting Series given by value_counts() is in descending order, so that the first element is the most frequently-occurring row
    counts = df['root_cat_code'].value_counts()

    # Extract the top N categories and group the rest into "other"
    top_n = counts.iloc[:N]
    other = counts.iloc[N:].sum()

    # Create a new DataFrame for the plot data
    plot_data = pd.concat([top_n, pd.Series({'Other': other})])

    # Plot the data as a bar chart
    plt.bar(plot_data.index, plot_data.values)

    # Set the plot title and axis labels
    plt.title(f'Top {N} Categories')
    plt.xlabel('Category')
    plt.ylabel('Frequency')

    # set the rotation of x-axis labels
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()


def generate_fields(df):
    """
    Generate new fields from the event_time column

    Args:
        df (pandas.DataFrame): DataFrame containing the event_time column

    Returns:
        pandas.DataFrame: DataFrame with new columns
    """
    # Convert event_time column to datetime
    df['event_time'] = pd.to_datetime(df['event_time'])

    # Extract hour of the day
    df['time_hours'] = df['event_time'].dt.hour

    # Extract weekday (0 = Monday, 6 = Sunday)
    df['weekday'] = df['event_time'].dt.weekday

    return df

def plot_most_sold_brands(df):
    """
    Find the most sold brand

    Args:
        df (pandas.DataFrame): DataFrame containing the brand column

    Returns:
        None
    """
    # Group the data by brand and sum the sales
    sales_by_brand = df.groupby('brand')['price'].sum()

    # Get the top 5 brands by sales volume
    top_5_brands = sales_by_brand.sort_values(ascending=False)[:5]

    # Plot a bar chart comparing the sales volume of the top 5 brands
    plt.bar(top_5_brands.index, top_5_brands.values)
    plt.xlabel('Brand')
    plt.ylabel('Sales Volume')
    plt.title('Top 5 Brands by Sales Volume')
    plt.show()

def get_category_with_highest_avg_price(df):
    """
    Find the category with the highest average price

    Args:
        df (pandas.DataFrame): DataFrame containing the category_code and price columns

    Returns:
        str: category code
    """

    grouped = df.groupby('category_code')['price'].mean().sort_values(ascending=False)
    category_highest_avg_price = grouped.index[0]
    return category_highest_avg_price

def brand_category_sales_under20(df):
    """
    Find the brand and category with the highest sales volume under 20

    Args:
        df (pandas.DataFrame): DataFrame containing the brand, category_code and price columns

    Returns:
        tuple: (brand, category)
    """

    # filter under 20
    sales_under_20 = df[df['price'] < 20]

    # Group the filtered DataFrame by brand and category, and sum prices
    grouped_prices = sales_under_20.groupby(['brand', 'category_code'])['price'].sum()

    # Find the index of the maximum value in the grouped_sales Series
    max_index = grouped_prices.idxmax()

    # Extract the brand and category from the index
    max_brand, max_category = max_index 

    return max_brand, max_category

def plot_sales_by_weekday(df):    
    """
    Plots the distribution of the sales volume over the weekdays.

    Args:
    - df (DataFrame): pandas DataFrame
    """
    
    # Dictionary with days of the week
    days = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    
    # Group the data by weekday and calculate the total sales volume
    weekday_sales = df.groupby(df['weekday'])['price'].sum()
    
    # Plot the data using a bar chart
    plt.bar(weekday_sales.index.map(days), weekday_sales.values)
    plt.title('Sales Volume by Weekday')
    plt.xlabel('Weekday')
    plt.ylabel('Sales Volume')
    plt.show()

def calculate_sales_cost(X, Y, df):
    """
    Calculates the total cost of sales volume of category X in year Y.
    
    Args:
    - X (string): category code
    - Y (int): year
    
    Returns:
    - total (int): Total cumulative sales
    """
    
    # Filter the data by category and year
    filtered_data = df[(df['category_code'] == X) & (df['event_time'].dt.year == Y)]
    
    # Returns the total cost
    return filtered_data['price'].sum()

def brand_price_probability(X, Y, df):
    """
    Calculates the probability that an item of brand X costs more than Y.
    
    Args:
    - X (string): brand
    - Y (float): price
    
    Returns:
    probability (float): probability that items of brand X costs more than Y
    """
    
    brand = X
    price = Y
    
    # include only rows with the given brand
    brand_data = df[df['brand'] == brand]
    
    # count the total number of purchases for the brand
    total_purchases = len(brand_data)
    
    # count the number of purchases with a price greater than the given value
    expensive_purchases = len(brand_data[brand_data['price'] > price])
    
    # calculate the probability as the ratio of expensive purchases to total purchases
    probability = expensive_purchases / total_purchases
    
    return probability