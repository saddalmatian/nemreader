import random
import csv
import datetime


def nmi_generate()->str:
    """ Generate nmi with 10 random digits """
    nmi = ""
    for i in range(0,10):
        nmi+=str(random.randint(0,9))
    return nmi


def msn_generate()->str:
    """ Generate meter serial number with 5 random digits """
    msn = ""
    for i in range(0,5):
        msn+=str(random.randint(0,9))
    return msn


def nem12_200_generate(nmi: str, msn: str, number_type: int) -> list:
    """ Generate first nem12 indicator 200
    :param nmi: nmi from nmi_generate()
    :param msn: meter serial number from msn_generate()
    :param number_type: number of type behind N. ex: 1, 2
    :returns: return first 200 indicator
    """
    nem12_200=[200,nmi,'E1E2','E1','E1','N'+str(number_type),msn,'KWH',30]
    return nem12_200


def nem12_300_date_generate(add_day: int) -> str:
    """ Generate datetime for indicator 300
    :param add_day: add more day into current day
    :returns: return a type string of date (%Y%m%d), ex: 20211227
    """ 
    a = datetime.datetime.now()
    b = a + datetime.timedelta(days=add_day)
    return b.strftime("%Y%m%d")


def nem12_300_last_update_generate() -> str:
    """ Generate Last update date and time for indicator 300, add 2 days is default
    :returns: return a type string of date (%Y%m%d%H%M%S), ex: 20211227112531
    """ 
    add_day = 2
    a = datetime.datetime.now()
    b = a + datetime.timedelta(days=add_day)
    return b.strftime("%Y%m%d%H%M%S")


def nem12_300_generate(add_day: int) -> list:
    """ Generate nem12 indicator 300
    :param add_day: add more day into current day
    :returns: return 300 indicator
    """
    date_300 = nem12_300_date_generate(add_day)
    nem12_300=[300,date_300]
    for i in range(2,50):
        interval_value_raw = random.uniform(0,2000)
        interval_value = "%.3f" % interval_value_raw
        nem12_300.append(interval_value)
    nem12_300.append("A")
    nem12_300.append("")
    nem12_300.append("")
    last_update = nem12_300_last_update_generate()
    nem12_300.append(last_update)
    return nem12_300


def write_to_csv(file_path:str, loop_time: int):
    """ Write nem12 generator into csv 
    :param file-path: path to save file
    :param loop_time: generate loop, each loop generates 4 row
    """
    with open(file_path, mode='w') as file:
        nem_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        nem12_100 = [100,'NEM12',200505181432,'CNRGYMDP','NEMMCO']
        nem12_900 = [900]
        nem_writer.writerow(nem12_100)
        for i in range(0,loop_time):
            nmi = nmi_generate()
            msn = msn_generate()
            nem12_200_1 = nem12_200_generate(nmi,msn,1)
            nem12_200_2 = nem12_200_generate(nmi,msn,2)
            nem_writer.writerow(nem12_200_1)
            nem12_300 = nem12_300_generate(i)
            nem_writer.writerow(nem12_300)
            nem_writer.writerow(nem12_200_2)
            nem12_300 = nem12_300_generate(i)
            nem_writer.writerow(nem12_300)
        nem_writer.writerow(nem12_900)


