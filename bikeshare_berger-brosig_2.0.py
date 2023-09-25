#!/usr/bin/env python 3.10.0
import calendar
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    valid_cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input('What is the name of the city to analyze data? (E.g. Input either Chicago, New York City, Washington): ').lower()
        if city in valid_cities:
            break
        else:
            print('Sorry, the city you entered is not in the list. Please try again.')

    # get user input for month (all, january, february, ... , june)
     months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input('What is the name of the month to filter data? Use "all" for the entire period from January to June: ').lower()
        if month in months:
            break
        else:
            print('Sorry, the month you entered is not in the list. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input('What is the name of the day to filter data? (E.g. Input either "all" to apply no day filter or Monday, Tuesday, ... Sunday: ').lower()
        if day in days:
            break
        else:
            print('Sorry, the day you entered is not valid. Please try again.')

    print('-' * 40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].mode()[0]

    print('The most common month from the given filtered data is:', calendar.month_name[popular_month])

    # display the most common day of week

    popular_day = df['day_of_week'].mode()[0]

    print('The most common day of week from the given filtered data is:', popular_day)

    # display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('The most common start hour from the given filtered data is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]

    print('The most commonly used start station from the given filtered data is: ', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]

    print('The most commonly used end station from the given filtered data is: ', popular_end_station)

    # display most frequent combination of start station and end station trip

    df ['start_end_station'] = df['Start Station'] + ' - ' + df['End Station']

    popular_combination_stations = df['start_end_station'].mode()[0]

    print('The most frequent combination of start station and end station trip is : ', popular_combination_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()

    print('The total travel time from the given filtered data is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('The mean travel time from the given filtered data is:', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    ct_user_types = df['User Type'].value_counts()

    print('The count of user types from the given filtered data is: ', ct_user_types)

    # Display counts of gender
    if 'Gender' in df:
        ct_gender = df['Gender'].value_counts()
        print('\nThe count of user gender from the given filtered data is: ', ct_gender)
    else:
        print('\nGender stats cannot be calculated because Gender does not appear in the dataframe.')




    # Display earliest, most recent, and most common year of birth
    if 'Gender' in df:
        earliest_yob = df['Birth Year'].min()
        recent_yob = df['Birth Year'].max()
        common_yob = df['Birth Year'].mode()[0]

        print('\nEarliest year of birth from the given filtered data is: ', earliest_yob)
        print('Most recent year of birth from the given filtered data is: ', recent_yob)
        print('Most common birth from the given filtered data is: ', common_yob)
    else:
        print('\nBirth stats cannot be calculated because Birth Year does not appear in the dataframe.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_raw_data(df):
    #Displays raw data on user request.

    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)

        df = load_data(city, month, day)

        while len(df.index) == 0:
            print('Sorry,no records matching criteria!\n')
            city, month, day = get_filters()
            print(city, month, day)

            df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
