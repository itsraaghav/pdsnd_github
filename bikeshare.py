import time
import pandas as pd
import numpy as np

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). 
    city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
    while city not in ('chicago','new york', 'washington'):
        print("Please enter a valid city name!")
        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()

    
    # if user selects none the filters will default to all
    month = 'All'
    day_of_week = 'All'
        
    # TO DO: get user input for filter options
    filter_month_option = input("Would you like to filter the data by month, day, both or none? ").lower()
    while filter_month_option not in ('month','day','both','none'):
        print("Please provide a valid input!")
        filter_month_option = input("Would you like to filter the data by month, day, both or none? ").lower()

    if filter_month_option == "month":
        month = input("Please enter a month name: ").title()
        while month not in ('January','February', 'March','April','May','June','All'):
            month = input("Please enter a valid month name! ").title()
    elif filter_month_option == "day":
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day_of_week = input("Please enter a day of week: ").title()
        while day_of_week not in ('Sunday','Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','All'):
            day_of_week = input("Please enter a valid day of week! ").title()
    elif filter_month_option == "both":
        # TO DO: get user input for month and day
        month = input("Please enter a month name: ").title()
        while month not in ('January','February', 'March','April','May','June','All'):
            month = input("Please enter a valid month name! ").title()

        day_of_week = input("Please enter a day of week: ").title()
        while day_of_week not in ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','All'):
            day_of_week = input("Please enter a valid day of week! ").title()
    
    print('-'*40)
    return city, month, day_of_week


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
    CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
    
    file_path = CITY_DATA[city]

    try:
        df = pd.read_csv(file_path)
        #Convert nulls in column Gender and User Type to "Data Not Available" only if this column 
        #is available in the file
        if "Gender" in df:
            df["Gender"].fillna(value="Data Not Available",inplace=True)
        if "User Type" in df:    
            df["User Type"].fillna(value="Data Not Available",inplace=True)
        
        #convert the column to datetime from string
        df['start_time'] = pd.to_datetime(df['Start Time'])
        
        #use the series dt to access the month and week names from the datetime column and create 3 
        #new columns in the dataframe
        df['month_name'] = df['start_time'].dt.strftime('%B')
        df['day_of_week'] = df['start_time'].dt.strftime('%A')
        df['start_hour'] = df['start_time'].dt.strftime('%H')
        
        #create a new column with start and end destinations to find the stat on the whole trip
        df['start_end_station'] = df['Start Station'] + ' - ' + df['End Station']

        
        if month != 'All':
            df = df[(df['month_name'] == month)]

        if day != 'All':
            df = df[(df['day_of_week'] == day)]

    except Exception as e:
        #print a error message and create a empty dataframe
        print("Error locating the file!", e)
        df= pd.DataFrame()

    return df


def time_stats(df,city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for chosen filters city: {}, month: {}, day: {}\n'.format(city, month, day))
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month is: " + str(df['month_name'].mode()[0]))

    # TO DO: display the most common day of week
    print("Most common day of week is: " + str(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print("Most common start hour is: " + str(df['start_hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip for chosen filters city: {}, month: {}, day: {}\n'.format(city, month, day))
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most commonly used start station is: " + str(df['Start Station'].mode()[0]))
        
    # TO DO: display most commonly used end station
    print("Most commonly used end station is: "+ str(df['End Station'].mode()[0])) 

    # TO DO: display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip is: "+ str(df['start_end_station'].mode()[0])) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration for chosen filters city: {}, month: {}, day: {}\n'.format(city, month, day))
    start_time = time.time()

    # TO DO: display total travel time
    print("Total Trip duration in seconds is: " + str(df['Trip Duration'].sum()))
      
    # TO DO: display mean travel time
    print("Mean travel time is: "+ str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats for chosen filters city: {}, month: {}, day: {}\n'.format(city, month, day))
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Count by User Type : "+ df.groupby(['User Type'])['User Type'].count().to_string())
    print("\n")

    # TO DO: Display counts of gender
    if "Gender" in df:
        print("Count by Gender : "+ df.groupby(['Gender'])['Gender'].count().to_string())
    else:
        print("Count by Gender cannot be calculated as the column data is unavailable.")
    print("\n")

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("Earliest year of birth: "+ str(int(df['Birth Year'].min())))
        print("Recent year of birth: "+ str(int(df['Birth Year'].max())))
        print("Most common year of birth: "+ str(int(df['Birth Year'].mode()[0])))
    else:
        print("Earliest, Most Recent and Most Common year of birth cannot be calculated as data is unavailable for Birth Year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df,city, month, day):
    """Displays the data 5 rows at a time for the filters used."""

    print('\nDisplaying the data for chosen filters city: {}, month: {}, day: {}\n'.format(city, month, day))
    
    display_option = input("Do you want to view the data? [yes/no] ").lower()
    while display_option not in ("yes","no"):
        print("Please enter a valid option! ")
        input("Do you want to view the data? [yes/no] ").lower()
    
    i=0
    #loop till user says no or index goes beyond the dataframe rows
    while display_option in ("yes") and (i+5) < df.shape[0]:
        print((df[i:i+5]).to_json(orient='records'))
        display_option = input("Do you want to view the data? [yes/no] ").lower()
        i+=5
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)
        if df.empty:
            print("There is some problem with the inputs provided!")
        else:
            print("Printing statistics for chosen filters city: {}, month: {}, day: {}".format(city, month, day))
            print('-'*40)
            time_stats(df,city, month, day)
            time.sleep(5)
            station_stats(df,city, month, day)
            time.sleep(5)
            trip_duration_stats(df,city, month, day)
            time.sleep(5)
            user_stats(df,city, month, day)
            time.sleep(5)
            display_data(df,city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
