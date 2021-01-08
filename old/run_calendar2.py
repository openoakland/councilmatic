import argparse

from scraper.controller.calendar import Calendar
from scraper.model.calendar import Calendar as CalendarModel


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sd",
        "--show_dates",
        help="show date values",
        dest="show_dates",
        action="store_true",
    )
    parser.add_argument(
        "-sdn",
        "--show_dept_names",
        help="show dept names",
        dest="show_depts",
        action="store_true",
    )
    parser.add_argument("-s", "--search", help="search words", type=str, default="")
    parser.add_argument("-d", "--date", help="date", type=str, default="All Years")
    parser.add_argument(
        "-dn", "--dept", help="dept name", type=str, default="All Departments"
    )
    parser.add_argument(
        "-n", "--notes", help="notes flag (i.e. 0, 1)", type=int, default=0
    )
    parser.add_argument(
        "-c", "--cc", help="closed caption flag (i.e. 0, 1)", type=int, default=0
    )
    parser.add_argument("-w", "--wait_time", help="wait time", type=int, default=5)
    return parser.parse_args()


def show_dates():
    cal = Calendar()
    cal.go_to_cal_page()
    date_strs = cal.get_dates()
    cal.close()

    print("Dates:")
    print("------")
    for date_str in date_strs:
        print(date_str)


def show_depts():
    cal = Calendar()
    cal.go_to_cal_page()
    dept_strs = cal.get_depts()
    cal.close()

    print("Depts:")
    print("------")
    for dept_str in dept_strs:
        print(dept_str)


def scrape(args):
    cal = Calendar()
    cal.go_to_cal_page()

    cal_rows = cal.query(
        search_str=args.search,
        date_sel=args.date,
        dept=args.dept,
        notes=args.notes,
        closed_caption=args.cc,
        sleep_time=args.wait_time,
        wait_time=args.wait_time,
    )
    cal.close()

    print(CalendarModel.to_csv(cal_rows))


def main():
    args = get_args()

    if args.show_dates:
        show_dates()
    elif args.show_depts:
        show_depts()
    else:
        scrape(args)


if __name__ == "__main__":
    main()
