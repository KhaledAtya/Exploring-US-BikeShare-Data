# Udacity/ITIDA DATA ANALYSIS PROFESSIONAL NANODEGREE
# EXPLORING US BIKESHARE PROJECT
# 18-10-2021, VERSION 1.0
import pandas as pd
from tabulate import tabulate
from colorama import Fore

months = ['jan', 'feb', 'mar', 'apr', 'may', 'june']
days = {'sat': 'Saturday', 'sun': 'Sunday', 'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday',
        'fri': 'Friday'}
CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
user_request_dict = {'1': 'raw data', '2': 'statistics'}
# To test user input for Yes/No questions
yes_no_dict = {'yes': 0, 'no': 1}
# Empty variables to be occupied later
month = []
day = []
city = ''
city_load = pd.DataFrame({})


def filter_months():
    """
    Prompts the user to type the month/s to filter by and checks they are entered correctly.
    """
    global month
    while True:
        try:
            print('\nType a month from the following list separated by a comma if more than one month is desired.')
            print('[Jan, Feb, Mar, Apr, May, June]')
            month = input('Filter by month/s: ').lower()
            month = [x.strip() for x in (month.split(','))]
            month = [(months.index(x) + 1) for x in month]
            break
        except ValueError:
            print(Fore.RED + "\n!Invalid Input. Make sure you entered the month/s' name/s correctly." + Fore.RESET)
            input("Press enter to retype the month/s' name/s.")


def filter_days():
    """
    Prompts the user to type the day/s to filter by and checks they are entered correctly.
    """
    global day
    while True:
        try:
            print('\nType the day name separated by comma if more than one day is desired.')
            print('[Sat, Sun, Mon, Tue, Wed, Thu, Fri]')
            day = input('Filter by day/s: ').lower()
            day = [x.strip() for x in (day.split(','))]
            print(day)
            day = [x.replace(x, days[x]) for x in day]
            break
        except ValueError:
            print(Fore.RED + "\n!Invalid Input. Make sure you entered the day/s' name/s correctly." + Fore.RESET)
            input("Press enter to retype the day/s' name/s.")


def load_data_file():
    """
     Prompts the user to type a city, loads raw data ,and creates a DataFrame.
     """
    global city_load
    global city
    while True:
        try:
            print('\nType the name of the city you want to see data for?')
            print('[Chicago, New York, Washington]')
            city = input('Selected City: ').lower().strip()
            file_name = CITY_DATA[city]
            city_load = pd.read_csv(file_name)
            break
        except KeyError:
            print(Fore.RED + '\n!Invalid Input. Make sure you entered the city name correctly.' + Fore.RESET)
            input('Press enter to retype the city name.')


def filter_show_statistics(to_filter_month, to_filter_day):
    """
    Filters data by the specified month/s and/or day/s if applicable and shows BikeShare statistics.

    Args:
        (str) do_filter_month - List of the month/s to filter by.
        (str) do_filter_day - List of the day/s of week to filter by.
    """
    global city_load
    # Filters the Data by month/s and/or day/s.
    city_load['Start Time'] = pd.to_datetime(city_load['Start Time'])
    city_load['Month'] = city_load['Start Time'].dt.month
    city_load['Day of Week'] = city_load['Start Time'].dt.day_name()
    city_load['Hour'] = city_load['Start Time'].dt.hour

    if to_filter_month == 'yes':
        city_load = city_load[city_load['Month'].isin(month)]
    if to_filter_day == 'yes':
        city_load = city_load[city_load['Day of Week'].isin(day)]

    # Displays BikeShare Statistics for the selected city.
    print('____________________')
    print('Popular Travel Times')
    print('____________________')
    popular_month = city_load['Month'].mode()[0]
    print('Most Popular Month: {}'.format(months[popular_month - 1].title()))
    popular_day = city_load['Day of Week'].mode()[0]
    print('Most Popular Day: {}'.format(popular_day))
    popular_hour = city_load['Hour'].mode()[0]
    print('Most Popular Hour: {}'.format(popular_hour))
    print('________________')
    print('Popular Stations')
    print('________________')
    popular_start_station = city_load['Start Station'].mode()[0]
    print('Most Popular Start Station: {}'.format(popular_start_station))
    popular_end_station = city_load['End Station'].mode()[0]
    print('Most Popular End Station: {}'.format(popular_end_station))
    popular_trip = (city_load['Start Station'] + ' ---> ' + city_load['End Station']).mode(0)[0]
    print('Most Popular Trip: {}'.format(popular_trip))
    print('_________')
    print('User Info')
    print('_________')
    user_types = city_load['User Type'].value_counts()[0:2]
    print('<>Counts of User Types<>\n{}'.format(user_types.to_string()))
    if city != 'washington':
        popular_gender = city_load['Gender'].value_counts()[0:2]
        print('<>Counts of Gender<>\n{}'.format(popular_gender.to_string()))
        earliest_birth = int(city_load['Birth Year'].min())
        print('<>Earliest Birth Year: {}'.format(earliest_birth))
        latest_birth = int(city_load['Birth Year'].max())
        print('<>Latest Birth Year: {}'.format(latest_birth))
        popular_birth = int(city_load['Birth Year'].mode()[0])
        print('<>Popular Birth Year: {}'.format(popular_birth))
    else:
        print('<>No Gender or Birth Year data for {} city.'.format(city.title()))


def main():
    # Prompts the user to type the desired service; show raw data or statistics.
    global city_load
    while True:
        try:
            user_request = input('\nDo you want to see raw data for {} or display statistics?\n'
                                 'Type the corresponding number from the list below.\n'
                                 '[1] Raw Data\n[2] Statistics.\n'.format(city.title()))
            print('You want to see {} for {}.\n'.format(user_request_dict[user_request], city.title()))
            break
        except KeyError:
            print(Fore.RED + '\n!Invalid Input. Make sure you typed 1 or 2.' + Fore.RESET)
            input('Press enter to retype your selection.')

    # Displays raw data or statistics based on user's requested service.
    if user_request == '1':
        additional_rows = 'yes'
        x = city_load.shape[0]
        a = 5
        while additional_rows == 'yes':
            if a <= x:
                print(tabulate(city_load.iloc[a - 5: a], headers=city_load.columns, tablefmt='psql'))
                a += 5
            else:
                print(Fore.RED + 'Warning: End of file reached.' + Fore.RESET)

            while True:
                try:
                    additional_rows = input('\nDo you want to see additional rows? [Yes, No] ').lower()
                    yes_no_dict[additional_rows]
                    break
                except KeyError:
                    print(Fore.RED + '\n!Invalid Input. Make sure you typed "Yes" or "No" correctly.' + Fore.RESET)
                    input('Press enter to retype you answer.')
    else:
        # Asks the user if to filter by month and checks the input answer for errors.
        while True:
            try:
                do_filter_month = input('Do you want to filter by month? [Yes, No] ').lower()
                yes_no_dict[do_filter_month]
                break
            except KeyError:
                print(Fore.RED + '\n!Invalid Input. Make sure you typed "Yes" or "No" correctly.' + Fore.RESET)
                input('Press enter to retype your answer.\n')
        # Asks the user if to filter by day and checks the input answer for errors.
        while True:
            try:
                do_filter_day = input('Do you want to filter by day? [Yes, No] ').lower()
                yes_no_dict[do_filter_day]
                break
            except KeyError:
                print(Fore.RED + '\n!Invalid Input. Make sure you typed "Yes" or "No" correctly.' + Fore.RESET)
                input('Press enter to retype your answer.\n')

        if do_filter_month == 'yes':
            filter_months()
        if do_filter_day == 'yes':
            filter_days()

        filter_show_statistics(do_filter_month, do_filter_day)


# Program Execution
while True:
    # Welcome Message
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Welcome to US BikeShare Analysis Tool.')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Run the main program
    load_data_file()
    main()
    print('___________________________________')
    # Asks the user if to restart the program and checks the input answer for errors.
    while True:
        try:
            restart_program = input('Do you want to restart the program? [Yes, No] ').lower()
            yes_no_dict[restart_program]
            break
        except KeyError:
            print(Fore.RED + '\n!Invalid Input. Make sure you typed "Yes" or "No" correctly.' + Fore.RESET)
            input('Press enter to retype your answer.\n')

    if restart_program == 'yes':
        print('***********************************')
        print('***********************************')
        continue
    else:
        print('\n~~~~~~~~~~~')
        print('Good Bye...')
        print('~~~~~~~~~~~')
        break
