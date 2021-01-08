import argparse

from scraper.controller.councilmember import CouncilMember
from scraper.model.councilmember import CouncilMember as CouncilMemberModel


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sdn",
        "--show_dept_names",
        help="show dept names",
        dest="show_depts",
        action="store_true",
    )
    parser.add_argument(
        "-dn", "--dept", help="dept name", type=str, default="All Departments"
    )
    parser.add_argument("-w", "--wait_time", help="wait time", type=int, default=1)
    return parser.parse_args()


def show_depts():
    cc = CouncilMember()
    cc.go_to_councilmember_page()
    dept_strs = cc.get_depts()
    cc.close()

    print("Depts:")
    print("------")
    for dept_str in dept_strs:
        print(dept_str)


def scrape(args):
    cc = CouncilMember()

    cc.go_to_councilmember_page()

    councilmember_dict = cc.query("All Departments")

    councilmember_list = [
        councilmember_dict[x] for x in sorted(councilmember_dict.keys())
    ]

    # turn to json
    cm_json = CouncilMemberModel.to_map_list_json(councilmember_list)

    print(cm_json)

    cc.close()


def main():
    args = get_args()

    if args.show_depts:
        show_depts()
    else:
        scrape(args)


if __name__ == "__main__":
    main()
