# @Author: Nawar saeed
# @Date:   2021-03-23T16:01:55+01:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task3.py
# @Description: This task is about computing the frequency for every
# word that occurs in the collection and also about estimating the
# constant factor α from Zipf’s law.This is the code for task 3 for the
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

class InvertedIndex:
    ''' A class for constructing an inverted index'''
    def __init__(self):
        """ Constructor to create an empty inverted index. """
        self.inverted_lists = {} #Empty inverted index
        self.total_filmes=0     #this is used to calculate the number of movies
        self.log_x_axis = []    # list to store log values for x-axis
        self.log_y_axis = []    # list to store log values for y-axis

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
                for word in re.split(separator, line):
                    #If a word is seen for first time, create an empty inverted list for it.
                    if len(word) > 0:
                        #convert to samll letters
                        word = word.lower()
                    #If a word is seen for first time, create an empty inverted list for it.
                        if word not in self.inverted_lists:
                            self.inverted_lists[word] = []
                        #assign a word a doc id
                        self.inverted_lists[word].append(doc_id)


    def zipf(self, des_order):
        '''
        A function for Estimate the constant factor α from Zipf’s law
                    Fn = c+n^-alpha , where c = 1/ln(M)

        des_order: a list that contains frequency of the terms, sorted in descending order
        '''

        Fn = 0
        #loop through the reange of the list
        for i in range(len(des_order)):
            #append 0 values into the log_x_axis list
            if (i == 0):
                self.log_x_axis.append(i)
            else:
                #append the log10 values into the x_axis list
                x = math.log10(i)
                self.log_x_axis.append(x)

            #append the values of des_order list into the y_axis list
            self.log_y_axis.append(math.log10(des_order[i][1]))
            Fn += des_order[i][1]
        # Fn = c+n^-alpha , where c = 1/ln(M)
        c = 1/np.log(len(des_order))
        #Approximate the alpha
        alpha = (math.log10(Fn) - c ) / math.log10(len(des_order))

        print(" The estimeated factor alpha is :",alpha)

    def word_frequency(self, invertedlist):
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
        #subroutine to zipf, in order to calculate the alpha
        self.zipf(sorted_order)
        x=[] # An empty list used to store the keys of sorted_order
        y=[] # An empty list used to store the values of sorted_order
        i =0
        for i in range(10):
            x.append(sorted_order[i][0])
            y.append(sorted_order[i][1])
            print(sorted_order[i][0],"\t",sorted_order[i][1])
        #print(x) # print the ten most frequent
        #ploting stuf
        plt.figure(1)
        plt.subplot(1, 2, 1)
        plt.title("inear scale frequency")
        plt.xlabel("Word")
        plt.ylabel("Frequency of the word")
        plt.xticks(rotation=90)


        plt.plot(x,y)

        plt.subplot(1, 2, 2)
        plt.title("log-log scale frequency")
        plt.plot(self.log_x_axis, self.log_y_axis )
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Task3.py <file name>")
        sys.exit(1)
    file_name = sys.argv[1]
    #make an instance of the calss
    inverted_index = InvertedIndex()
    sep = "[^A-Za-z0-9]+"  # separator to split the file
    inverted_index.parser(file_name,sep)
    inv_list = inverted_index.inverted_lists
    inverted_index.word_frequency(inv_list)
