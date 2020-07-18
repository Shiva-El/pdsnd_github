import pandas as pd


def input_msg(msg, valid_list, all_option=None, show_list=True):
    """ prints a msg to user and check if input is in a specific valid list
    :param msg: a msg to user. ex: 'u wanna see 5 more rows?'
    :param valid_list: a list of valid input ex: ['yes','no']
    :param all_option: dose user can accept 'all' ?
    :param show_list: print the valid list to user if it's True.
    :return:
    """
    print(msg)
    if show_list:
        for val in valid_list:
            print(f'-{val.lower().capitalize()}')
    if all_option != None:
        valid_list.append('all')
        print(f'-all({all_option})')
    print()
    valid_list = [val.lower() for val in valid_list]
    user_choice = input().lower().strip()
    while user_choice not in valid_list:
        print('There should be a typo,try again...')
        user_choice = input().lower().strip()
    return user_choice


def user_input():
    """
    :return: city,month and day
    """
    city = input_msg('Which CITY you choose?', ['chicago', 'New york', 'Washington'])
    filter = input_msg('Do you wanna filter on MONTH, DAY, BOTH or NONE?', ['month', 'day', 'both', 'none'],
                       show_list=False)

    if filter == 'month':
        month = input_msg('Which MONTH you choose?', ['january', 'february', 'march', 'april', 'may', 'june'],
                          all_option='for not filtering on specific month')
        day = 'all'
    elif filter == 'day':
        month = 'all'
        day = input_msg('Which DAY you choose?',
                        ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                        all_option='for not filtering on specific day')
    elif filter == 'both':
        month = input_msg('Which MONTH you choose?', ['january', 'february', 'march', 'april', 'may', 'june'],
                          all_option='for not filtering on specific month')
        day = input_msg('Which DAY you choose?',
                        ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
                        all_option='for not filtering on specific day')
    else:
        month = 'all'
        day = 'all'

    print(f"Data iS filtered on: \n City: '{city.upper()}'\n Month:'{month.upper()}'\n Day of week:'{day.upper()}'\n")

    return city, month, day


def load_data(city):
    """ This function load data set from available csv files
    and calculate/add 4 more columns to it ('month', 'day_of_week', 'hour', 'trip') """

    CITY_DATA = {'chicago': 'chicago.csv',
                 'new york': 'new_york_city.csv',
                 'washington': 'washington.csv'}
    data = pd.read_csv('data\\' + CITY_DATA[city])

    data['Start Time'] = pd.to_datetime(data['Start Time'])

    Months = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june'}
    data['month'] = data['Start Time'].dt.month.replace(Months)

    Days = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday'}
    data['day_of_week'] = data['Start Time'].dt.dayofweek.replace(Days)

    data['hour'] = data['Start Time'].dt.hour

    data['trip'] = data['Start Station'] + '  TO  ' + data['End Station']

    return data


def filter_data(data, month, day):
    """
    :param data: raw dataset
    :param month: month
    :param day: day
    :return: a filtered dataset based on a month and a day chosen by user
    """
    df = data

    if month != 'all':
        df = df[data['month'] == month]

    if day != 'all':
        df = df[data['day_of_week'] == day]

    return df


def show_data(df, city):
    """
    :param df: dataset
    :param city: city
    :return: print 5 or more rows of the dataset
    """
    city_columns = {
        'washington': ['Start Time', 'End Time', 'Trip Duration',
                       'Start Station', 'End Station', 'User Type'],
        'new work': ['Start Time', 'End Time', 'Trip Duration',
                     'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'],
        'chicago': ['Start Time', 'End Time', 'Trip Duration',
                    'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year']
    }
    columns = city_columns[city]

    user_input = input_msg('Do you wanna see the first 5 rows of the dataset?', ['yes', 'no'], all_option=None,
                           show_list=False)

    i = 0
    while user_input.lower() == 'yes':
        for i in range(i, i + 5):
            for index, column in enumerate(columns):
                print(column, ':', df.iloc[i, index + 1])
            print('__________')
        user_input = input_msg('Do you wanna see 5 more rows?', ['yes', 'no'], all_option=None, show_list=False)


def stats(df, city, month, day):
    """ This function calculates and print basic statistics of a dataset"""

    df_mode = df[['month', 'day_of_week', 'hour', 'Start Station', 'End Station', 'trip']].mode()

    print('_______________ Calculating Stats for this dataset _______________\n')

    # Calculate Popular times of travel
    print(f'Popular times of travel:')

    if month == 'all':
        common_month = df_mode['month'].iloc[0]
        print(f' Most common month:        {common_month}')

    if day == 'all':
        common_day_of_week = df_mode['day_of_week'].iloc[0]
        print(f'\t\t\tMost common day of week:  {common_day_of_week}')

    common_hour = df_mode['hour'].iloc[0]
    print(f"\t\t\tMost common hour of day:  {common_hour}")

    print()

    # Calculate Popular stations and trip
    start_station_popular = df_mode['Start Station'].iloc[0]
    end_station_popular = df_mode['End Station'].iloc[0]
    trip_popular = df_mode['trip'].iloc[0]

    print(f"Popular stations and trip:\n\
    \t\tMost common start station: {start_station_popular}\n\
    \t\tMost common end station:   {end_station_popular}\n\
    \t\tMost common trip:          {trip_popular}")

    print()

    # Calculates Total $ Average travel time
    total_trip_time = (df['Trip Duration'].sum() / 3600).round(1)
    total_trip_num = df['Trip Duration'].count()
    average_time = (total_trip_time / total_trip_num).round(1)
    print(f"Trip duration(hour):\n\
    \t\tTotal travel time:   {total_trip_time}h\n\
    \t\tAverage travel time: {average_time}h")

    print()

    # Calculate Users subscriptions types breakdown
    print(f'Users subscriptions types:')
    for counter, value in enumerate(df['User Type'].value_counts()):
        print('\t''\t''\t', df['User Type'].value_counts().index[counter], ': ', value)

    print()

    if city == 'new york' or city == 'chicago':
        # Calculates Users gender breakdown
        user_male_count = df['Gender'].value_counts().loc['Male']
        user_female_count = df['Gender'].value_counts().loc['Female']
        print(f"Users gender breakdown:\n\
        \tMale:   {user_male_count}\n\
        \tFemale: {user_female_count}")

        print()

        # Calculates Users Year of Birth info
        earliest_year_birth = int(df['Birth Year'].min())
        recent_year_birth = int(df['Birth Year'].max())
        common_year_birth = int(df['Birth Year'].mode())

        print(f"Users Year of Birth info:\n\
        \tEarliest:    {earliest_year_birth}\n\
        \tMost recent: {recent_year_birth}\n\
        \tMost common: {common_year_birth}")


def main():
    while True:
        city, month, day = user_input()
        data = load_data(city)
        df = filter_data(data, month, day)
        show_data(df, city)
        stats(df, city, month, day)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ['yes', 'no']:
            restart = input("please answer with 'yes' or 'no'")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
