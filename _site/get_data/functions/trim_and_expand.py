import datetime as dt
def trim_claims(in_path, out_path):
    with open(in_path, 'r') as in_file:
        with open(out_path, 'w') as out_file:
            out_file.write(in_file.readline())
            print(in_file.readline())
            for line in in_file:
                split_line = line.split(",")
                time = dt.datetime.strptime(split_line[11], '%Y-%m-%d %H:%M:%S.%f')
                if time >= dt.datetime(2016, 4, 1):
                    out_file.write(line)


# trim_claims("/Users/alexchescheir/Documents/TIY/solid-adventures-with-bacon/data/old/SV_PLANT_ACTY_DTL_LARGE(Claims).csv",
            # "/Users/alexchescheir/Documents/TIY/solid-adventures-with-bacon/data/MED_SV_PLANT_ACTY_DTL(Claims).csv")

def expand_attendance(in_path, out_path):
    header = []
    lines = []
    employees = {}
    with open(in_path, 'r') as in_file:
        header = in_file.readline()
        for line in in_file:
            lines.append(in_file.readline())
        for line in lines:
            split_line = line.split(",")
            last = len(split_line)
            if (','.join(split_line[:last - 4])) in employees:
                employees[','.join(split_line[:last - 4])].append(','.join(split_line[last - 4:]))
            else:
                employees[','.join(split_line[:last - 4])] = [','.join(split_line[last - 4:])]
    print(len(employees))
    with open(out_path, 'w') as out_file:
        out_file.write(header)
        for i in range(-61, 0, 1):
            if (i+4) % 7 <= 1:
                continue
            shift = dt.timedelta(days=i)
            for j in [dt.date(2016, 6, 1)]:
                to_add = []
                for key in employees:
                    # print( j.strftime('%Y-%m-%d'), [x.split(',')[1][:10] for x in employees[key]])
                    if j.strftime('%Y-%m-%d') in [x.split(',')[1][:10] for x in employees[key]]:
                        idx = [x.split(',')[1][:10] for x in employees[key]].index(j.strftime('%Y-%m-%d'))
                        if employees[key][idx].split(',')[3] == "NULL\n":
                            # print('NULL--2')
                            # to_add.append(key + (",NULL,NULL,NULL,NULL\n"))
                            pass
                        else:
                            # print(idx, employees[key][idx])
                            in_time = dt.datetime.strptime(employees[key][idx].split(',')[1], '%Y-%m-%d %H:%M:%S.%f')
                            in_time += shift
                            in_time = in_time.strftime('%Y-%m-%d %H:%M:%S.%f')
                            out_time = dt.datetime.strptime(employees[key][idx].split(',')[3][:-1], '%Y-%m-%d %H:%M:%S.%f')
                            out_time += shift
                            out_time = out_time.strftime('%Y-%m-%d %H:%M:%S.%f')+'\n'
                            to_add.append(','.join([key, employees[key][idx].split(',')[0], in_time, employees[key][idx].split(',')[2], out_time]))
                    else:
                        # print('NULL')
                        # to_add.append(key + (",NULL,NULL,NULL,NULL\n"))
                        pass
                for each_line in to_add:
                    out_file.write(each_line)
        for line in lines:
            out_file.write(line)

expand_attendance('/Users/alexchescheir/Documents/TIY/solid-adventures-with-bacon/data/emp+item+punch.csv',
                  '/Users/alexchescheir/Documents/TIY/solid-adventures-with-bacon/data/exp_punch.csv')
