import csv
import json
import nem12_generator
from nemreader import nem_objects
from nemreader import read_nem_file

# Prefix file when split into multiple files
PREFIX_FILE = "NEM12#Split#"
# Quantity of files after splited
FILE_QUANTITY = 0


def max_line_file(file_path: str) -> int:
    """ Get max line of file
    :param file_path: the path of file
    :returns: max line of file
    """
    max_line = 0
    with open(file_path, 'r') as data_file:
        for line in data_file:
            max_line += 1
    return max_line


def split_nem12_file(file_path: str, line_quantity: int):
    """ Split the file into multiple files with given line quantity
    :param file_path: the path of file
    :param line_quantity: the line quantity you want to split for small files
    """
    global FILE_QUANTITY
    max_line = max_line_file(file_path)

    count = 0
    line_container = []
    number_id = 1
    current_line = 0
    with open(file_path, 'r') as data_file:
        for line in data_file:
            current_line += 1
            count += 1
            line_container.append(list(line.rstrip("\n").split(",")))
            if(count > line_quantity and
               list(line.split(","))[0] != "200"
               or current_line == max_line):
                with open(PREFIX_FILE+str(number_id)+".csv", mode='w') as file:
                    nem_writer = csv.writer(
                        file, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
                    for record in line_container:
                        nem_writer.writerow(record)
                count = 0
                number_id += 1
                FILE_QUANTITY = number_id-1
                line_container = []


def connect_readings(d1: dict, d2: dict):
    """ Connect 2 readings dicts together, d2 connect to d1
    :param d1: first dict
    :param d2: second dict
    """
    for nmi in d2:
        if nmi not in d1:
            d1[nmi] = {}
        for suffix in d2[nmi]:
            if suffix not in d1[nmi]:
                d1[nmi][suffix] = []
            for readings in d2[nmi][suffix]:
                d1[nmi].setdefault(suffix, []).append(readings)


def connect_transaction(d1: dict, d2: dict):
    """ Connect 2 transaction dicts together, d2 connect to d1
    :param d1: first dict
    :param d2: second dict
    """
    for nmi in d2:
        if nmi not in d1:
            d1[nmi] = {}
        for suffix in d2[nmi]:
            if suffix not in d1[nmi]:
                d1[nmi][suffix] = []
            for readings in d2[nmi][suffix]:
                d1[nmi].setdefault(suffix, []).append([])


def print_json(response):
    print(json.dumps(response, sort_keys=True, indent=4, default=str))


def main():
    # Generate nem12.csv
    # nem12_generator.write_to_csv("NEM12.csv", 2)

    # use library and analyse
    # m = read_nem_file('NEM12.csv', 1)

    # for nmi in m.readings:
    #     for suffix in m.readings[nmi]:
    #         for reading in m.readings[nmi][suffix]:
    #             print(reading)

    # spilt file and analyse
    split_nem12_file('NEM12.csv', 2)
    for file_id in range(1, FILE_QUANTITY+1):
        if(file_id == 1):
            m = read_nem_file(PREFIX_FILE+str(file_id) + ".csv",
                              quantity=1)
            nem = nem_objects.NEMFile(m.header, m.readings, m.transactions)
        else:
            m = read_nem_file(PREFIX_FILE+str(file_id) + ".csv",
                              quantity=file_id,
                              ignore_missing_header=True)
            connect_readings(nem.readings, m.readings)
            connect_transaction(nem.transactions, m.transactions)

    for nmi in nem.readings:
        for suffix in nem.readings[nmi]:
            for reading in nem.readings[nmi][suffix]:
                print(reading)


if __name__ == "__main__":
    main()
