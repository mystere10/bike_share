import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DICT = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

DAYS_DICT = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday',
}

def display_data(df):
        current_page = 0
        total_rows = len(df)
        
        while current_page * 5 < total_rows:
            if current_page * 5 + 5 < total_rows:
                display_df = df.iloc[current_page * 5 : current_page * 5 + 5]
            else:
                display_df = df.iloc[current_page * 5 : total_rows]
            
            print(display_df)
            
            if current_page * 5 + 5 < total_rows:
                user_input = input("Press Enter to display the next 5 rows or type 'exit' to stop: ")
            else:
                user_input = input("All data has been displayed. Type 'exit' to stop: ")
            
            if user_input.lower() == 'exit':
                break
            
            current_page += 1

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    counts = 0

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    def handle_month_and_day():
        while True:
            try:            
                period = input("Would you like to filter the data by month, day, or not at all?\n").lower()
                if period == 'month':
                    month = input("Which month you would like to filter by\n")
                    if month.title() in MONTH_DICT.values():
                        return month, None
                if period == 'day':
                    day = input("Which day you would like to filter by\n")
                    if day.title() in DAYS_DICT.values():
                        return day, None
            except Exception as e:
                print("Invalid data input", e) 
    
    while True:
        try:    
            city = input("Would you like to see data for Chicago, New York, or Washington?\n").strip().lower()
            if city in CITY_DATA:
                month, day = handle_month_and_day()
                return city, month, day
            else:
                print("Invalid choice. Please enter 'chicago', 'new york city' or 'washington'.")
        except Exception as e:
            print("Invalid data input", e) 
    
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # convert the end Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    
    # extract day of week from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    df['hour'] = df['Start Time'].dt.hour
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is", common_month)

    # display the most common day of week
    common_week_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is", common_week_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is", str(common_hour)+'H')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_used_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_used_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    
    group = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    common_week_day = group.loc[group['count'].idxmax()]
    print("The most common week day", common_week_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    total_travel_time = df['travel_duration'].sum()
    print(total_travel_time)

    # display mean travel time
    mean_travel_time = df['travel_duration'].mean()
    print("Mean travel time", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types", user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print("User gender", user_gender)
    else:
        print("The 'Gender' column does not exist in the DataFrame.")
 


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birthdate = df['Birth Year'].min()
        recent_birthdate = df['Birth Year'].max()
        common_birthdate = df['Birth Year'].mode()[0]
    
        print("Earliest birthdate", earliest_birthdate, '\n')
        print("Recent birthdate", recent_birthdate,  '\n')
        print("Common birthdate", common_birthdate,  '\n')
    else:
        print("The 'Birth Year' column does not exist in the DataFrame.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display = input("Do you want to display all the data? Enter 'yes' or 'no': ")
        if display.lower() == 'yes':
            display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
