#!/usr/bin/env python3

import os
import sys
import sqlite3
import readline
from jdatetime import datetime, timedelta
from prettytable import PrettyTable


def change_dir():
    os.chdir('database')


def database_initialize():
    if os.path.exists("database") and os.path.exists("database/reviewty.db"):
        print("- Database is already initialized!")
    else:
        if not os.path.exists("database"):
            os.mkdir('database')
        change_dir()

        con = sqlite3.connect("reviewty.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE reviewty(Book, Units, Lessons, Pages, Dates)")
        con.commit()
        os.chdir("../")
        print("- Database is successfully initialized!\n")


def plan_the_review_dates(studied_lessons):
    change_dir()
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
    print("- Enter the studied lessons seperated with (,)")
    print("- Syntax : [Book] [Units] [Lessons] [Pages], [Book] ....")
    print("- Example : Pyisics 1 1-2 13-22, Calculus 2-3 * *\n")
    studied_lessons = input("- Reviewty: ").split(',')

    plan_the_review_dates(studied_lessons)


def get_todays_plan():
    change_dir()

    con = sqlite3.connect('reviewty.db')
    cur = con.cursor()

    today = datetime.today()
    plans = cur.execute(f"SELECT * FROM reviewty WHERE Dates='{today.strftime('%Y/%m/%d')}'")

    table = PrettyTable(['Book', 'Units', 'Lessons', 'Pages', 'Dates'])

    for lesson in plans.fetchall():
        book, units, lessons, pages, date = lesson
        table.add_row([book, units, lessons, pages, date])

    print(f"\t\t   Today's plan\n{table}")


def get_specific_date_plan():
    change_dir()

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
    print("""
██████╗ ███████╗██╗   ██╗██╗███████╗██╗    ██╗████████╗██╗   ██╗
██╔══██╗██╔════╝██║   ██║██║██╔════╝██║    ██║╚══██╔══╝╚██╗ ██╔╝
██████╔╝█████╗  ██║   ██║██║█████╗  ██║ █╗ ██║   ██║    ╚████╔╝ 
██╔══██╗██╔══╝  ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║   ██║     ╚██╔╝  
██║  ██║███████╗ ╚████╔╝ ██║███████╗╚███╔███╔╝   ██║      ██║   
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝    ╚═╝      ╚═╝""")

    if (not os.path.exists("database") or not os.path.exists("database/reviewty.db")):
        database_initialize()

    print("[0]- add a new lesson\n[1]- get today's plan")
    print("[2]- get a specific date's plan\n[3]- delete a lesson's plan\
        \n[4]- initialize the database\n\
[5]- initialize a new database\n[6]- delete the database\n[7]- exit\n")
    opt = input("~ Reviewty : ")

    if opt == '0':
        get_studied_lessons()
    elif opt == '1':
        get_todays_plan()
    elif opt == '2':
        get_specific_date_plan()
    elif opt == '3':
        pass
    elif opt == '4':
        pass
    elif opt == '5':
        #database_initialize(database_name=dname)
        pass
    elif opt == '6':
        os.remove('database/reviewty.db')
    else:
        sys.exit()


if __name__ == "__main__":
    main()
