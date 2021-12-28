import csv

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


def get_file_quantity():
    global FILE_QUANTITY
    return FILE_QUANTITY


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
