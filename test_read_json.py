import json


def load_json(file_name):
    with open(file_name, 'r') as myfile:
        json_data=myfile.read()

    return json.loads(json_data)

def main():
    cal_data = load_json('last_month.json')

    # cal_data is a list
    print("cal_data is %s" % str(type(cal_data)))

    # iterate through cal_data
    for i, cal_row in enumerate(cal_data):
        # cal_row is a dictionary
        print("###%d - cal_row is %s" % (i, str(type(cal_row))))
        print("###available keys: ", cal_row.keys())

        # iterate through cal_row dictionary
        for cal_row_key in cal_row.keys():
            if cal_row_key != 'meeting_details':
                print("###%s : %s" % (cal_row_key, cal_row[cal_row_key]))
            else:
                # meeting details is a dictionary
                meeting_details = cal_row[cal_row_key]
                print("###meeting details is %s" % str(type(meeting_details)))
                print("######available keys: ", meeting_details.keys())

                # iterate through meeting details dictionary
                for meeting_details_key in meeting_details.keys():
                    if meeting_details_key != 'meeting_items':
                        print("######%s : %s" % (meeting_details_key, meeting_details[meeting_details_key]))
                    else:
                        # meeting_items is a list
                        meeting_items = meeting_details[meeting_details_key]
                        print("###meeting items is %s" % str(type(meeting_items)))
                        for j, meeting_item in enumerate(meeting_items):
                            # meeting item is a dictionary
                            print("######%d - meeting_item is %s" % (j, str(type(meeting_item))))
                            print(meeting_item)

        if i < 2:
            break

if __name__ == "__main__":
    main()