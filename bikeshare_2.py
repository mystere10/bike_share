import time
import pandas as pd

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

def calculate_time_duration(time, message):
    """
    Calculates days, hours, minutes and seconds.

    Parameters:
        time in seconds (number): number of seconds.
        message (str): string to display during the printing.
    Returns:
        None
    """
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    
    print("{}: {} days {} hours {} minutes {} seconds".format(message, day, hour, minutes, seconds))

def get_time_elapsed(time, start_time):
    """
    Prints the time elapsed since items from the DataFrame each time a user press a key.

    Parameters:
        df (DataFrame): object of all the data.

    Returns:
        None
    """
    
    # Displays time taken to complete the above calculations.
    print("\nThis took %s seconds." % (time - start_time))
    
    # Displays a line of 40 dashes
    print('-'*40)

def display_data(df):
    """
    Prints five items from the DataFrame each time a user press a key.

    Parameters:
        df (DataFrame): object of all the data.

    Returns:
        None
    """
    
    current_page = 0
    total_rows = len(df)
    
    while current_page * 5 < total_rows:
        if current_page * 5 + 5 < total_rows:
            display_df = df.iloc[current_page * 5 : current_page * 5 + 5]
        else:
            display_df = df.iloc[current_page * 5 : total_rows]
        
        print(display_df)
        
        if current_page * 5 + 5 < total_rows:
            user_input = input("Do you want to see the next 5 rows of data: ")
        else:
            user_input = input("All data has been displayed. Type 'no' to stop: ")
        
        if user_input.lower() == 'no':
            break
        
        current_page += 1

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze.
        (str) month - name of the month to filter by, or "all" to apply no month filter.
        (str) day - name of the day of week to filter by, or "all" to apply no day filter.
    """
    print('Hello! Let\'s explore some US bike-share data!')
        
    def get_month_and_day():
        """
        Processes user input for month and day and.

        Parameters:
            None

        Returns:
            (str): month - a specific month to analyze.
            (str): day - a specific day to analyze.
        """
    
        while True:
            try:            
                period = input("Would you like to filter the data by month, day, or not at all?\n").lower()
                if period == 'month':
                    # Get user input for month (all, january, february, ... , june).
                    month = input("Which month you would like to filter by\n")
                    if month.title() in MONTH_DICT.values():
                        return month, None, None
                    
                if period == 'day':
                    # Get user input for day of week (all, monday, tuesday, ... sunday).
                    day = input("Which day you would like to filter by\n")
                    if day.title() in DAYS_DICT.values():
                        return None, day, None
                
                if period == 'not at all':
                    # Get user input for day of week (all, monday, tuesday, ... sunday).
                    all_data = 'all'
                    return None, None, all_data
                    
            except Exception as e:
                print("Invalid data input", e) 
    
    while True:
        try:
            # Get user input for city (chicago, new york city, washington).
            city = input("Would you like to see data for Chicago, New York, or Washington?\n").strip().lower()
            if city in CITY_DATA:
                month, day, all_data = get_month_and_day()
                return city, month, day, all_data
            else:
                print("Invalid choice. Please enter 'chicago', 'new york city' or 'washington'.")
        except Exception as e:
            print("Invalid data input", e) 
    
    return city, month, day, all_data


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze.
        (str) month - name of the month to filter by, or "all" to apply no month filter.
        (str) day - name of the day of week to filter by, or "all" to apply no day filter.
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day.
    """
    
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Check if day exist.
    if day is not None:
        df['Start Day'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Start Time'].dt.strftime('%A')
    # Check if month exist.
    if month is not None:      
        df['Start Month'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Start Time'].dt.strftime('%B')

    # Convert the end Time column to datetime.
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Check if day or moth exist before saving the corresponding data based on the user input.
    if day is not None:
        df['End Day'] = df[df['End Time'].dt.strftime('%A') == day.title()]['End Time'].dt.strftime('%A')

    if month is not None:
        df['End Month'] = df[df['End Time'].dt.strftime('%B') == month.title()]['End Time'].dt.strftime('%B') 
    
    # Extract Start Time from Start Time based on user input.
    if month is not None:
        df['month'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Start Time'].dt.strftime('%B')
    if day is not None:
        df['month'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Start Time'].dt.strftime('%B')
    
    # Extract Start Station based on user input.
    if month is not None:
        df['Start Station'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Start Station']
    if day is not None:
        df['Start Station'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Start Station']
    
    # Extract End Station based on user input.
    if month is not None:
        df['End Station'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['End Station']
    if day is not None:
        df['End Station'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['End Station']

    # Extract Gender based on user input.
    if month is not None:
        df['User Type'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['User Type']
    if day is not None:
        df['User Type'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['User Type']

    # Extract Gender from Start Time to create new columns based on user input.
    if month is not None:
        df['Gender'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Gender']
    if day is not None:
        df['Gender'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Gender']
    
    # Extract day of week from Start Time to create new columns based on user input.
    if month is not None:
        df['Birth Year'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Birth Year']
    if day is not None:
        df['Birth Year'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Birth Year']
        
    # Extract day of week from Start Time to create new columns based on user input.
    if month is not None:
        df['day_of_week'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Start Time'].dt.day_name()
    if day is not None:
        df['day_of_week'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Start Time'].dt.day_name()
    
    # Extract hours from Start Time to create new columns based on user input.
    if month is not None:
        df['hour'] = df[df['Start Time'].dt.strftime('%B') == month.title()]['Start Time'].dt.hour
    if day is not None:
        df['hour'] = df[df['Start Time'].dt.strftime('%A') == day.title()]['Start Time'].dt.hour


    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    if 'month' in df.columns:
        common_month = df['month'].mode()[0]
        print("The most common month is", common_month)

    # Display the most common day of week.
    if 'day_of_week' in df.columns:
        common_week_day = df['day_of_week'].mode()[0]
        print("The most common day of the week is", common_week_day)

    # Display the most common start hour.
    if 'hour' in df.columns:
        common_hour = df['hour'].mode()[0]
        print("The most common hour is", str(common_hour)+'H')

    get_time_elapsed(time.time(), start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    print(df)

    # Display most commonly used start station.
    common_used_start_station = df['Start Station'].mode()[0]
    print("The most common start station", common_used_start_station)

    # Display most commonly used end station.
    common_used_end_station = df['End Station'].mode()[0]
    print("The most common end station", common_used_end_station)

    # Display most frequent combination of start station and end station trip.
    group = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    common_trip = group.loc[group['count'].idxmax()]
    print("The most common trip from start to end", common_trip)

    get_time_elapsed(time.time(), start_time)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['travel_duration'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    total_travel_time = df['travel_duration'].sum()
    
    calculate_time_duration(total_travel_time, 'Total travel time')

    # Display mean travel time.
    mean_travel_time = df['travel_duration'].mean()
    calculate_time_duration(mean_travel_time, 'Mean travel time')

    get_time_elapsed(time.time(), start_time)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_types = df['User Type'].value_counts()
    print("\nUser types", user_types)

    # Display counts of gender.
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print("\nUser gender", user_gender)
    else:
        print("\nThe 'Gender' column does not exist in the DataFrame.")

    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        earliest_birthdate = df['Birth Year'].min()
        recent_birthdate = df['Birth Year'].max()
        common_birthdate = df['Birth Year'].mode()[0]
    
        print("\nEarliest birthdate", earliest_birthdate, '\n')
        print("\nRecent birthdate", recent_birthdate,  '\n')
        print("\nCommon birthdate", common_birthdate,  '\n')
    else:
        print("The 'Birth Year' column does not exist in the DataFrame.")

    get_time_elapsed(time.time(), start_time)



def main():
    """The main function that executes all other functions."""

    while True:
        city, month, day, all_data = get_filters()
        df = load_data(city, month, day)
        
        if all_data is None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        
        display = input("Do you want to see 5 rows of data? Enter 'yes' or 'no': ")
        if display.lower() == 'yes' or all_data is not None:
            display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
