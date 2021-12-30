import nem12_generator
from nemreader import nem_objects
from nemreader import read_nem_file
from nem12_handler import split_nem12_file
from nem12_handler import connect_transaction, connect_readings
from nem12_handler import PREFIX_FILE
from nem12_handler import get_file_quantity
import json


def main():
    # Generate nem12.csv
    nem12_generator.write_to_csv("NEM12.csv", 10)

    # use library and analyse
    # m = read_nem_file('NEM12.csv', 1)

    # for nmi in m.readings:
    #     for suffix in m.readings[nmi]:
    #         for reading in m.readings[nmi][suffix]:
    #             print(reading)

    # spilt file and analyse

    split_nem12_file('NEM12.csv', 5)
    FILE_QUANTITY = get_file_quantity()
    data_container = {}
    for file_id in range(1, FILE_QUANTITY+1):
        if(file_id == 1):
            m = read_nem_file(PREFIX_FILE+str(file_id) + ".csv",
                              quantity=file_id)
            contain_header = []
            for field in m.header:
                contain_header.append(str(field))
            data_container['header'] = contain_header
            data_container['readings'] = {}
            data_container['transactions'] = {}
            nem = nem_objects.NEMFile(m.header, m.readings, m.transactions)
            connect_readings(data_container['readings'], m.readings)
            connect_transaction(data_container['transactions'], m.transactions)

        else:
            m = read_nem_file(PREFIX_FILE+str(file_id) + ".csv",
                              quantity=file_id,
                              ignore_missing_header=True)
            connect_readings(nem.readings, m.readings)

    # import json
    # print(json.dumps(test, indent=4, default=str))
    f = open("demofile2.txt", "w")
    f.write(json.dumps(data_container, default=str, indent=4))
    f.close()

    # open and read the file after the appending:
    f = open("demofile2.txt", "r")
    # a = f.read()
    # print(eval(a))


if __name__ == "__main__":
    main()
