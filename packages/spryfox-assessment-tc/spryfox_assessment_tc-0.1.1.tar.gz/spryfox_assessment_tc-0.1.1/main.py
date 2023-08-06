from tasks import dummy as dm
from tasks import data_analysis as da
df = None

def menu():
    print("Menu:")
    print("1. Task 1")
    print("2. Task 2")
    print("3. Task 3")
    print("4. Exit")
    choice = input("Enter your choice: ")

    # Sanitize input
    while choice not in ['1', '2', '3', '4']:
        choice = input("Invalid choice. Please enter 1, 2, 3 or 4: ")

    return int(choice)

if __name__ == '__main__':
    while True:
        choice = menu()

        if choice == 1:
            print('######################### Task 1 #########################')

            dummy = dm.Dummy(0.5)

            # prints 0.5
            print(f'Bias: {dummy.bias}') 

            # prints 0.3333333333333333 (the default value)
            print(f'Baseline: {dummy.baseline}') 

            dummy.baseline = 0.25
            # prints 0.25 (the new value)
            print(f'New baseline: {dummy.baseline}')

            # 1.231*0.25 + 0.5 = 0.80775, prints 0.808
            print(f'Calculation: {dummy.calculate(1.231)}')

            # prints current formatted datetime
            print(f'Datetime: {dummy.get_current_datetime()}')
        elif choice == 2:
            print('######################### Task 2 #########################')
            if df is None:
                print('Loading data...')
                df = da.load_data()

            # plot prices
            da.plot_prices(df)

            # plot of categories (not required by the assignment)
            df_filtered = da.filter_categories(df)
            da.plot_categories(df_filtered)

            # generate fields time_hours, weekday
            df = da.generate_fields(df)

            # plot brand with most sales
            da.plot_most_sold_brands(df)

            # find category with highest average price
            category_highest_avg_price = da.get_category_with_highest_avg_price(df)
            print('Category with highest average price:', category_highest_avg_price)

            # Which brand and category has the most sales of a price of under 20 currency units?
            max_brand, max_category = da.brand_category_sales_under20(df)
            print(f"The brand with the most sales under 20 is {max_brand}.")
            print(f"The category with the most sales under 20 is {max_category}.")

            # Write a function that plots the distribution of the sales volume over the weekdays.
            da.plot_sales_by_weekday(df)
        elif choice == 3:
            print('######################### Task 3 #########################')

            if df is None:
                print('Loading data...')
                df = da.load_data()

            sales_cost = da.calculate_sales_cost("electronics.audio.headphone", 2020, df)
            print(f'The sales cost for electronics.audio.headphone in 2020 is {sales_cost}.')

            prob1 = da.brand_price_probability("apple", 100, df)
            prob2 = da.brand_price_probability("apple", 1000, df)
            print(f'The probability of selling an apple product for 100 is {prob1}.')
            print(f'The probability of selling an apple product for 1000 is {prob2}.')
        elif choice == 4:
            break

