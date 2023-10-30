#!/usr/bin/env python3

import os
import sys
import sqlite3
import readline
from jdatetime import datetime, timedelta
from prettytable import PrettyTable


change_dir = lambda : os.chdir('database')


def database_initialize():
    if os.path.exists("database") and os.path.exists("database/rplanner.db"):
            print("- database is already initialized!")
    else:
        if not os.path.exists("database"):
            os.mkdir('database')
        change_dir()

        con = sqlite3.connect("rplanner.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE rplanner(Book, Units, Lessons, Pages, Dates)")
        con.commit()
        os.chdir("../")
        print("- database is successfully initialized!")


def plan_the_review_dates(studied_lessons):
    change_dir()
    con = sqlite3.connect("rplanner.db")
    cur = con.cursor()

    today = datetime.today()

    for lesson in studied_lessons:
        book, units, lessons, pages = lesson.split(' ')

        table = PrettyTable(['Book', 'Units', 'Lessons', 'Pages', 'Dates'])



        for day in 1, 3, 7, 30:
            date = today + timedelta(day)
            date = date.strftime("%Y/%m/%d")

            cur.execute(f"INSERT INTO rplanner VALUES(\
            '{book}', '{units}', '{lessons}', '{pages}', '{date}')")

            table.add_row([book, units, lessons, pages, date])

        print(table)

    con.commit()


def get_studied_lessons():
    studied_lessons = input("- Enter the studied lessons seperated with (, ):").split(', ')

    plan_the_review_dates(studied_lessons)


def get_todays_plans():
    change_dir()

    con = sqlite3.connect('rplanner.db')
    cur = con.cursor()

    today = datetime.today() + timedelta(days=1)
    plans = cur.execute(f"SELECT * FROM rplanner WHERE Dates='{today.strftime('%Y/%m/%d')}'")

    table = PrettyTable(['Book', 'Units', 'Lessons', 'Pages', 'Dates'])

    for lesson in plans.fetchall():
        book, units, lessons, pages, date = lesson
        table.add_row([book, units, lessons, pages, date])

    print(f"\t\t   Today's plan\n{table}")


def main():
    if (not os.path.exists("database") or not os.path.exists("database/rplanner.db")):
        database_initialize()

    print("[0]- add a new lesson\n[1]- get today's plan")
    print("[2]- delete a lesson's plan\n[3]- initialize the database\n\
[4]- initialize a new database\n[5]- delete the database\n[6]- exit\n")
    opt = int(input("~ PyPlanner : "))

    if opt == 0:
        get_studied_lessons()
    elif opt == 1:
        get_todays_plans()
    elif opt == 2:
        pass
    elif opt == 3:
        database_initialize()
    #elif opt == 4:
        #database_initialize(database_name=dname)
    elif opt == 5:
        os.remove('database/rplanner.db')
    else:
        sys.exit()


if __name__ == "__main__":
    main()