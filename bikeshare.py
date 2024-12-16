import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Enter city name as : Chicago, New York City, or Washington: ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("Please try entering that again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Select month: All, January, February, March, April, May, or June: ").lower()
        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            print("Please try entering that again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("Select Day: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ").lower()
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("Please try entering that again.")
            continue
        else:
            break

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
         
         # filter by day of week to create the new dataframe
         df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month: ", popular_month)

    # display the most common day of week    
    popular_day = df['day'].mode()[0]
    print("The most common day: ", popular_day)


    # display the most common start hour    
    popular_hour = df['hour'].mode()[0]
    print("The most common hour: ", popular_hour)  


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most popular starting station: ", popular_start) 

    # display most commonly used end station    
    popular_end = df['End Station'].mode()[0]
    print("The most popular end station: ", popular_end)


    # display most frequent combo start station and end station
    df['route'] = df['Start Station'] + df['End Station']
    print("The most popular route is:", df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time in hours:", int(sum((df['Trip Duration']) / 60) / 60))

    # display mean travel time    
    print("Mean travel time in minutes:", int(df['Trip Duration'].mean() % 60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types    
    print("Count user type:\n", df.groupby(['User Type'])['User Type'].count())
  
    
    # Display counts of gender
    try:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print("Count gender:\n", gender_count)
    
    # Display earliest, most recent, and most common year of birth    
        oldest_user = int(df['Birth Year'].min())
        print("Earliest known user year of birth:\n", oldest_user)
    
        youngest_user = int(df['Birth Year'].max())
        print("Most recent known user year of birth:\n", youngest_user)
    
        common_user = int(df['Birth Year'].mode()[0])
        print("Most common known user year of birth:\n", common_user)
    
    except KeyError:
        print("Some information not available for Washington.")
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    """
    Prompts the user if they wants to view 5 lines of raw data (yes/no).
    Displays that data if the answer is yes.
    Asks if the user would like to see the next 5 lines of raw data.  
    """
    
    x = 0
    while True:
        reply = input("View 5 lines of raw data?/n Please enter Yes or No:  ")
        if reply.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
