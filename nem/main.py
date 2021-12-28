# import nem12_generator
from nemreader import nem_objects
from nemreader import read_nem_file
from nem12_handler import split_nem12_file
from nem12_handler import connect_transaction, connect_readings
from nem12_handler import PREFIX_FILE
from nem12_handler import get_file_quantity


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
    FILE_QUANTITY = get_file_quantity()

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
