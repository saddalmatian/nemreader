# NEMreader with lambda function
----------------------------------------------------------------------------
This is my small nemreader project use to analyze a NEM file by NEMreader.


Inside nem/generate_nem_file.py, you can change the second parameter inside nem12_generator.write_to_csv("NEM12.csv", 10000)\
into any number. If it is 10000, this function will generate a fake data with 10000*4 + 2 line, total 40002 line for you.\
That generator will generate a file named NEM12.csv

Inside lambda folder, there are 3 file that you will need to upload on to aws lambda console.

____________________________________________________________________________

I have only finished all the stuff with NEM12, NEM13 is not yet implemented\
Please wait for me for the next version.
