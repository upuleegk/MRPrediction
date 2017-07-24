#!/usr/bin/python
import os


#main starts here
#make an array of feature ids, call is feature_list_array
feature_list_array = []

with open('/home/rahman/Documents/MT/current_feature_set.txt', 'r') as f:
    first_line = f.readline()
    while first_line:
        index = first_line.find(":")
        number = first_line[index+2:]
        number = number[:-1]
        feature_list_array.append(number)
        first_line = f.readline()


#print feature_list_array
path = '/home/rahman/Documents/MT/MethodFeatures/'
outputfile = open("/home/rahman/Documents/MT/data_file.txt", 'w+')

for filename in os.listdir(path):
    print filename
    outputfile.write(filename+ " ")
    
    length = len(filename)
    if length < 32:
        #pad the file with blanks to get the same length file
        length_plus_pad = length
        while(length_plus_pad < 32):
            outputfile.write(" ")
            length_plus_pad = length_plus_pad + 1
        

    my_file = open(path+filename, 'r')       
    the_file = my_file.read()

    for feature in feature_list_array:

        index = the_file.find(str(feature)+":")
        if index != -1:
            
            space_index = the_file.find(" ", index)
            colon_index = the_file.find(":", index)
            count = the_file[colon_index+1:space_index]

            #add the count to the output file
            outputfile.write(count)
            outputfile.write(" ")
        else:
            outputfile.write("0")
            outputfile.write(" ")


    outputfile.write("\n")

outputfile.close()
