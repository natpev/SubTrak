#!/bin/python3

###################################
#  Created by:   Nathan Pevlor    #
#  Version:      0.5.1            #
#  Started:      8\20\2021        #
#  Updated:      9\3\2021         #
###################################

############################################################################
#  This Program was created to keep track of and print out a report        #
#  for any subscriptions or payments that are entered into it. This is     #
#  very usefull for doing a monthly budget so that all the little charges  #
#  that seem to pop up don't end up being a suprise.                       #
############################################################################

import json
import datetime
import calendar
import os
from time import sleep

##any global parameters go here
##the data file to use throughout the program
datafile = ("subs_test.json")


##function to load json data
def initialize():
    global Sub_Data
    global interval
    global categories
    global Sub_List
    ##pull in the json config data to use for the program
    with open (datafile, "r") as read_file:
        Sub_Data = json.load(read_file)
    ##set necisarry variables
    interval = Sub_Data["Configurations"]["Intervals"]
    #print(interval)
    categories = Sub_Data["Configurations"]["Categories"]
    #print(categories)
    Sub_List = Sub_Data['Subscriptions']


##write the data to a read_file
def save_it():
    with open(datafile, "w") as write_file:
        json.dump(Sub_Data, write_file, indent=4)

##function to print out a table of all Subscriptions
def print_subs():
    print("Nothing to see here yet")

##the function for addinga new subscription
def add_record():
    initialize()

    try:
        ##retrieving the necissary variables from the user
        print("+-------------------------+\n| press CTL + C to cancel |\n+-------------------------+")
        ##get the name
        sub_name = input("\nWhat is the name of the subscription:\n")
        ##get the category
        while True:
            valid = categories
            sub_category = input("\nWhat category does this subscription fall under:\n" + str(valid) + "\n").upper()

            if sub_category in valid:
                break
            else:
                print("\nPlease enter a valid catagory")
                sleep(.5)
                pass
        ##get the cost
        while True:
            sub_cost = input("\nHow much does this subscription cost:\n$")
            try:
                sub_cost = round(float(sub_cost), 2)
                print(sub_cost)
                break
            except:
                print("Please enter a dollar ammount")
                sleep(.5)
                pass
        ##get the interval
        while True:
            valid = interval
            sub_interval = input("\nOn what interval does this subscription occur:\n" + str(valid) + "\n").lower()

            if sub_interval in valid:
                break
            else:
                print("\nPlease enter a valid interval")
                sleep(.5)
                pass
        ##get the period
        while True:
            sub_period = input("\nWhat frequency does this Subscription occur\n(Every ___ " + sub_interval + "):\n")
            try:
                int(sub_period)
                break
            except:
                print("enter a whole number")
                sleep(.5)
        ##get the date
        while True:
            sub_active_date = input("\nOn what date did this subscription go active (YYYY-MM-DD)\n")
            try:
                datetime.datetime.strptime(sub_active_date, '%Y-%m-%d')
                break
            except ValueError:
                print("incorrect format. Please use the format YYYY-MM-DD")
                sleep(.5)

        ##write all the variables to the imported json data
        Sub_Data["Subscriptions"][sub_name] = {'cost': sub_cost, 'category': sub_category, 'interval': sub_interval, 'period': int(sub_period), 'first_active_date': sub_active_date, 'active': True}

        save_it()
        print("+--------------------------------+\n| Subscription added sucessfully |\n+--------------------------------+")

    ###if ctl + C is entered
    except KeyboardInterrupt:
        print("+------------------------------+\n| Subscription Entry Canceled. |\n+------------------------------+")
        sleep(1)
        pass


###this is the function to add a new category to the Configurations
def add_category():
    initialize()
    try:
        print("+-------------------------+\n| press CTL + C to cancel |\n+-------------------------+")
        new_category = input("Enter the new category name:\n").upper()
        Sub_Data['Configurations']['Categories'].append(new_category)
        save_it()
        length = len(new_category)
        print("+---------" + '-' * length + "-------------+")
        print("| sucessfully added (" + new_category + ") |")
        print("+---------" + '-' * length + "-------------+")
    except KeyboardInterrupt:
        print("+------------------------+\n| Add Category Canceled. |\n+------------------------+")
        sleep(1)
        pass

##this deletes a category
def del_category():
    initialize()
    while True:
        category_to_remove = input("which category would you like to remove?\n" + str(categories) + "\n").upper()
        if category_to_remove in categories:
            break
        else:
            print("\nThis is not a valid category.\n")
            sleep(.5)
    ##compile a list of the categories in use
    for i in Sub_List:
        InUse_list = []
        InUse_list.append(Sub_Data['Subscriptions'][i]['category'])
    ##check if the category is used
    if  category_to_remove not in InUse_list:
        Sub_Data['Configurations']['Categories'].remove(category_to_remove)
        length = len(category_to_remove)
        print("+---------" + '-' * length + "---------------+")
        print("| sucessfully removed (" + category_to_remove + ") |")
        print("+---------" + '-' * length + "---------------+")
    else:
        length = len(category_to_remove)
        print("+---------" + '-' * length + "-----------------------+")
        print("| ERROR category (" + category_to_remove + ") still in use |")
        print("+---------" + '-' * length + "-----------------------+")
        sleep(.5)
    save_it()

##the function to add X number of months to a date
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12        ##this is floor division it cuts off after the decimal
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

###the function to add X number of years
def add_years(sourcedate, years):
    month = sourcedate.month
    year = sourcedate.year + years
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


##function to print a report for a month
def print_report(month, year):
    month = input("What Month to pull data for (MM):")
    year = input("What year to pull data for (YYYY):")
    print_month_start = datetime.datetime.strptime((year + "-" + month + "-01"), '%Y-%m-%d').date()
    print_month_end = add_months(print_month_start, 1)

    print(print_month_start)
    print(print_month_end)
    initialize()

    full_total = 0

    for CAT in categories:
        sub_total = 0
        print(
        "+" + ("-" * 34) + "+\n"
        "| " + CAT + (" " * (32 - len(CAT))) + " |\n"
        "+--------------------+-------------+----------+--------+------------------------------+\n"
        "| Name               |  Date Due   | cost     | active | description                  |\n"
        "+--------------------+-------------+----------+--------+------------------------------+"
        )
        for SUB in Sub_List:
            if (Sub_Data['Subscriptions'][SUB]['category']) == CAT:
                sub_date = datetime.datetime.strptime((Sub_Data['Subscriptions'][SUB]['first_active_date']), '%Y-%m-%d').date()
                while sub_date < print_month_end:
                    if sub_date < print_month_start:
                        if Sub_Data['Subscriptions'][SUB]['interval'] == ("months"):
                            sub_date = add_months(sub_date, (Sub_Data['Subscriptions'][SUB]['period']))
                        if Sub_Data['Subscriptions'][SUB]['interval'] == ("years"):
                            sub_date = add_years(subdate, (Sub_Data['Subscriptions'][SUB]['period']))

                    elif print_month_start <= sub_date <= print_month_end:
                        ##format the name for printout
                        name = SUB
                        if len(name) < 20:
                            name = (name + (" " * (18 - len(name))))
                        else:
                            name = (name[:16] + '..')

                        ##format the date for printout
                        date = str(sub_date)
                        if len(date) < 11:
                            date = (date + (" " * (11 - len(date))))

                        ##format the cost for printout
                        cost = (Sub_Data['Subscriptions'][SUB]['cost'])
                        sub_total += cost
                        full_total += cost
                        if len(str(cost)) < 7:
                            cost = (str(cost) + (" " * (7 - len(str(cost)))))

                        active = (Sub_Data['Subscriptions'][SUB]['active'])

                        print("| {0} | {1} | ${2} | {3}  |".format(name, date, cost, active))
                        sub_date = add_months(sub_date, 1)

        print(
        "+--------------------+-------------+----------+--------+------------------------------+\n"
        "                     |   Subtotal: | ${0} |\n"
        "                     +-------------+----------+\n".format((str(sub_total)+ " "*(7-len(str(sub_total))))))
    print("\n"
    "                     +-------------+----------+\n"
    "                     |    TOTAL    | ${0} |\n"
    "                     +-------------+----------+".format((str(full_total)+ " "*(7-len(str(full_total))))))



########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################
########################################################################################################################################################


Month = ("11")
Year = ("2021")

print("\nWelcome to SubTrak\n")
if os.path.exists(datafile) == False:
    default = {
        "Configurations": {
            "Categories": [
            ],
            "Intervals": [
                "months",
                "years"
            ]
        },
        "Subscriptions": {
        }
    }
    with open(datafile, "w") as write_file:
        json.dump(default, write_file, indent=4)

while True:
    try:
        choice = input(
        "\nSelect an option and press enter\n"
        "0 -- Print report\n"
        "1 -- Add Subscription\n"
        "2 -- \n"
        "3 -- Add category\n"
        "4 -- Delete category\n"
        )
        if choice == "0":
            print_report(Month, Year)
        elif choice == "1":
            add_record()
        elif choice == "2":
            pass
        elif choice == "3":
            add_category()
        elif choice == "4":
            del_category()
        else:
            print("Invalid choice")
    except KeyboardInterrupt:
        print(
        "\n\n\n+-----------------+\n"
        "| Exiting SubTrak |\n"
        "+-----------------+\n")
        sleep(1)
        break
