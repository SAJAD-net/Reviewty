#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
import sqlite3
import readline
from prettytable import PrettyTable


def database_initialize():
    """ first, it checks if the database has already been initialized or not,
    if not, creates a directory named `.database`.
    then creates a database named `reviewty.db` in it."""

    if not os.path.exists(".database/reviewty.db"):
        if not os.path.exists(".database"):
            os.mkdir('.database')

        # changing current directory to the .database.
        os.chdir('.database')

        # initializing the database
        con = sqlite3.connect("reviewty.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE reviewty(Book,\
                    Units, Lessons, Pages, Dates)")
        con.commit()

        os.chdir("../")


def plan_the_review_dates(studied_lessons):
    """ writes the review dates on the database, for the next 1, 3, 7, and 30 days.
    then prints a table containing the review dates. """

    os.chdir('.database')

    con = sqlite3.connect("reviewty.db")
    cur = con.cursor()

    today = datetime.today()

    for lesson in studied_lessons:
        book, units, lessons, pages = lesson.strip().split(' ')

        table = PrettyTable(['Book', 'Units', 'Lessons', 'Pages', 'Dates'])

        for day in 1, 3, 7, 30:
            date = today + timedelta(day)
            date = date.strftime("%Y/%m/%d")

            cur.execute(f"INSERT INTO reviewty VALUES(\
            '{book}', '{units}', '{lessons}', '{pages}', '{date}')")

            table.add_row([book, units, lessons, pages, date])

        print(table)

    con.commit()


def get_studied_lessons():
    """ gets the studied lessons from user.
    then sends them to `plan_the_review_date` funciton to set the review dates.
    """

    print("- Enter the studied lessons seperated with (,)")
    print("- Syntax : [Book] [Units] [Lessons] [Pages], [Book] ....")
    print("- Example : Pyisics 1 1-2 13-22, Calculus 2-3 * *\n")
    studied_lessons = input("- Reviewty: ").split(',')

    plan_the_review_dates(studied_lessons)


def get_todays_plans():
    """ first, it gets today's reviewing plans from the database.
    then shows them to the user in a table shape. """

    os.chdir('.database')

    con = sqlite3.connect('reviewty.db')
    cur = con.cursor()

    today = datetime.today()
    plans = cur.execute(f"SELECT * FROM reviewty\
                        WHERE Dates='{today.strftime('%Y/%m/%d')}'")
    # initializing table columns.
    table = PrettyTable(['Book', 'Units', 'Lessons', 'Pages', 'Dates'])

    for lesson in plans.fetchall():
        book, units, lessons, pages, date = lesson
        table.add_row([book, units, lessons, pages, date])

    print(f"\t\t   Today's plan\n{table}")


def get_specific_date_plan():
    """ gets the plans of a specific day which user enters.
    the date should be in this format : Year/Month/Day ."""

    os.chdir('.database')

    con = sqlite3.connect('reviewty.db')
    cur = con.cursor()

    print("- Enter a date to get it's plan, Syntax : Year/Month/Day")
    sdate = input("- Reviewty: ")

    plans = cur.execute(f"SELECT * FROM reviewty WHERE Dates='{sdate}'")

    table = PrettyTable(['Book', 'Units', 'Lessons', 'Pages', 'Dates'])

    for lesson in plans.fetchall():
        book, units, lessons, pages, date = lesson
        table.add_row([book, units, lessons, pages, date])

    print(f"\t\t   {sdate} plan\n{table}")


def main():
    """ prints the flag and waits for the user to choose one of the options."""

    print("""
██████╗ ███████╗██╗   ██╗██╗███████╗██╗    ██╗████████╗██╗   ██╗
██╔══██╗██╔════╝██║   ██║██║██╔════╝██║    ██║╚══██╔══╝╚██╗ ██╔╝
██████╔╝█████╗  ██║   ██║██║█████╗  ██║ █╗ ██║   ██║    ╚████╔╝
██╔══██╗██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║   ██║     ╚██╔╝
██║  ██║███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝   ██║      ██║
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝    ╚═╝      ╚═╝""")

    database_initialize()

    print("\t[0]- add a new lesson\n\t[1]- get today's plan")
    print("\t[2]- get a specific day's plan\n\t\
[3]- initialize the database\n\t\
[4]- delete the database\n\t[5]- exit\n")

    opt = input("~ Reviewty : ")

    if opt == '0':
        get_studied_lessons()
    elif opt == '1':
        get_todays_plans()
    elif opt == '2':
        get_specific_date_plan()
    elif opt == '3':
        database_initialize()
    elif opt == '4':
        os.remove(".database/reviewty.db")
        print('- database is successfully deleted!')
    else:
        sys.exit()


if __name__ == "__main__":
    main()
