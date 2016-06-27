import random


def remove(in_path, out_path, proportion_to_toss):
    with open(in_path, 'r') as in_file:
        with open(out_path, 'w') as out_file:
            out_file.write(in_file.readline())
            for line in in_file.readlines():
                if random.random() > proportion_to_toss:
                    out_file.write(line)

remove("/Users/alexchescheir/Documents/TIY/solid-adventures-with-bacon/data/MED_SV_PLANT_ACTY_DTL(Claims).csv",
       "/Users/alexchescheir/Documents/TIY/solid-adventures-with-bacon/data/OBF_MED_SV_PLANT_ACTY_DTL(Claims).csv",
       .146)
