from dateutil.parser import parse


def read_file(path):
    reports = {}
    with open(path, 'r') as infile:
        time = None
        report = None
        key_nonduplicates = 0
        key_duplicates = 0
        key_value_duplicates = 0
        for count, row in enumerate(infile, start=1):
            # if count > 12:
            #     return

            if row in ('', '\n'):
                # it's the empty line between records
                # now we should have time and report, process them
                # print({
                #     'time': time,
                #     'report': report,
                # })
                key = (time, report.split(' ')[0])
                value = {
                    'time': time,
                    'report': report,
                }
                if key in reports:
                    key_duplicates += 1
                    if reports[key] == value:
                        key_value_duplicates += 1
                else:
                    key_nonduplicates += 1
                reports[key] = value
                # reset and start again
                time = None
                report = None
                continue
            elif row[0] == '2':
                time = parse(row.rstrip('\n') + 'UTC')  # force into UTC timezone
            else:
                report = row.rstrip('\n')

            # print(count)
            # print('*' + row.rstrip('\n') + '*')

        from pprint import pprint
        # pprint(reports)
        print(f'{key_duplicates} key duplicates detected')
        print(f'{key_nonduplicates} key nonduplicates detected')
        print(f'{key_value_duplicates} key/value duplicates detected')

        def print_reports(reports):
            count = 0
            for time, station in reports:
                print(time)
                print(station)
                print(reports[(time, station)])
                count += 1
                if count > 1:
                    return

        print_reports(reports)


if __name__ == '__main__':
    read_file('/home/adam/2022/1/28_18.txt')
    # print("?")
