# @Author: Nawar saeed
# @Date:   2021-03-23T16:01:55+01:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task3.py
# @Description: This task is about finding the longest inverted list and
# compute the amount of space needed for storing the index uncompressed
# and compressed.This is the code for task 4 for the
# @course AI for the Web. It is based on
# @Hannah Best's lectures
# @Hannah Bast <bast@cs.uni-freiburg.de>
# @Last modified by:   nawar
# @Last modified time: 2021-03-23T21:39:22+01:00

import re
import sys
import matplotlib.pylab as plt
import operator
import math
import numpy as np
import time

class InvertedIndex:
    ''' A class for constructing an inverted index'''


    def __init__(self):
        """ Constructor to create an empty inverted index. """
        self.inverted_lists = {} #Empty inverted index
        self.total_filmes=0     #this is used to calculate the number of movies
        self.records = dict()  # will be used to split the name of the movie and its description


    def parser(self, file_name,separator):
        """
        Construct the inverted index from given file.

        file_name : name of the txt file
        separator : Specifies the separator to use when splitting the string
        """
        doc_id = 0 # used to assign every word a document id
        with open(file_name) as file:

            #read the file line by line
            for line in file:
                self.total_filmes +=1 #increase total filmes by one
                doc_id += 1
                # this is used to split the name of the movie and its description
                self.records[doc_id] = line.replace('\n', '')
                for word in re.split(separator, line):
                    if len(word) > 0:
                        #convert to samll letters
                        word = word.lower()
                    #If a word is seen for first time, create an empty inverted list for it.
                        if word not in self.inverted_lists:
                            self.inverted_lists[word] = []
                        #assign a word a doc id
                        self.inverted_lists[word].append(doc_id)

    def gamma_encoding(self,number):
        ''' A function used for gap encoding based on Elias-gamma approach'''
        logn = int(math.log(number,2))
        #print("looooooooooog",logn)
        gap_code="0"*logn + bin(number)[2:]
        return gap_code

    def word_frequency(self,invertedlist):
        '''
        This function is used to calculate the frequency of the word.

        invertedlist: argument for the inverted list
        '''
        word_frequency = {} #empty dict used to store the frequency of the words
        for key in self.inverted_lists:
            #append the length of every term inte inverted list into word_frequency
            word_frequency[key] = len(invertedlist[key])
        #sort the list by descending order
        sorted_order = sorted(word_frequency.items(), key=operator.itemgetter(1), reverse=True)

        x=[] # An empty list used to store the keys of sorted_order
        y=[] # An empty list used to store the values of sorted_order
        i =0
        print("Befor compression:\n")
        for i in range(1):
            ## get he longest invertedlist
            print("the longest invertedlist:","(",sorted_order[i][0],"-->\t",sorted_order[i][1],")", "needs",sorted_order[i][1]*4,"[byts]\n\n")
            x.append(sorted_order[i][0])
            y.append(sorted_order[i][1])
        # find the longest inverted list
        longest_inverted_list =sorted_order[0][0]
        longest_inverted_list=list(dict.fromkeys(self.inverted_lists[sorted_order[0][0]]))

        #needed to sort the list
        x= longest_inverted_list[0]
        # calculate the difference between the indexes of the list
        longest_inverted_list=np.diff(longest_inverted_list)
        longest_inverted_list = np.insert(longest_inverted_list,0,x)

        gamma_len=[] #Empty list to store te compressed value
        for i in longest_inverted_list:
            #append the compressed into the list
            gamma_len.append(len(self.gamma_encoding(i)))

        print("After compression:\n")
        print("needs ",sum(gamma_len), "[bits]", "or ",sum(gamma_len)/8, " in [bytes]")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Task13.py <file name>")
        sys.exit(1)
    file_name = sys.argv[1]
    #make an instance of the class
    inverted_index = InvertedIndex()
    sep = "[^A-Za-z0-9]+"
    inv_list = inverted_index.inverted_lists
    inverted_index.parser(file_name,sep)
    inverted_index.word_frequency(inv_list)
