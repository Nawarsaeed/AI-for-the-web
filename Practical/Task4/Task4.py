# @Author: Nawar saeed
# @Date:   2021-03-23T16:01:55+01:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task4.py
# @Description: The task is about extending the inverted index so that
# the inverted lists are not containing several entries of the same document
# id and also about finding out the ten words with the largest number of
# documents.This is the code for task 4 for the
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
import cProfile


class InvertedIndex:
    ''' A class for constructing an inverted index'''


    def __init__(self):
        """ Constructor to create an empty inverted index. """
        self.inverted_lists = {} #Empty inverted index
        self.total_filmes=0     #this is used to calculate the number of movies
        self.records = dict()  # will be used to split the name of the movie and its description
    def parser(self, file_name,sep):
        """ Construct index from given file.

        file_name : name of the txt file
        sep : Specifies the separator to use when splitting the string
        """
        global total_filmes
        doc_id = 0
        with open(file_name) as file:
            #read the file line by line
            for line in file:
                self.total_filmes +=1 #increase total filmes by one
                doc_id += 1
                # this is used to split the name of the movie and its description
                self.records[doc_id] = line.replace('\n', '')
                for word in re.split(sep, line):
                    # this is used to split the name of the movie rom its description
                    if len(word) > 0:
                        word = word.lower()
                        # to make sure that each invertedlist contains one doc id
                        if word not in self.inverted_lists:
                            self.inverted_lists[word] = []

                        ##assign a word a doc id
                        self.inverted_lists[word].append(doc_id)

    def word_frequency(self,invertedlist):
        '''
        This function is used to calculate the frequency of the word.

        invertedlist: argument for the inverted list
        '''
        word_frequency = {} #empty dict used to store the frequency of the words
        for key in self.inverted_lists:
            #append the length of every term inte inverted list into word_frequency
            word_frequency[key] = len(list(dict.fromkeys(invertedlist[key])))
        #sort the list by descending order
        sorted_order = sorted(word_frequency.items(), key=operator.itemgetter(1), reverse=True)

        x=[] # An empty list used to store the keys of sorted_order
        y=[] # An empty list used to store the values of sorted_order
        i =0
        print("The ten words with the largest number of documents:\n")
        for i in range(10):
            # get the ten frequented words
            print(sorted_order[i][0],"-->\t",sorted_order[i][1])
            x.append(sorted_order[i][0])
            y.append(sorted_order[i][1])

    def list_intersect(self, list1, list2):
        """
        A function used to calculate the intersection between two lists

        list1 : argument for the first list
        list2 : argument for the second list
        """
        #create an empty list
        intersect_list = []

        L1 = 0
        L2 = 0
        # iterate over the two list, and check for equality
        while L1 < len(list1) and L2 < len(list2):
            if list1[L1] < list2[L2]:
                L1 += 1
            elif list1[L1] > list2[L2]:
                L2 += 1
            # the case where the two lists intersect
            else:
                intersect_list.append(list1[L1])
                L1 += 1
                L2 += 1
        return intersect_list

    def query(self, keywords):
        """
        For each given keywords, fetch the inverted lists and compute
        their intersection
        """
        #create an empty list
        intersect_list = []

        # Check if the keywords not an empty list
        if len(keywords) == 0:
            return None

        # initialize the intersect_list and check each intersection with
        # each keyword
        if keywords[0] in self.inverted_lists:
            intersect_list = self.inverted_lists[keywords[0]]

        i = 1
        while i < len(keywords):
            #if the words are in the inverted list, subroutine the
            #intersect method and do the intersection
            if keywords[i] in self.inverted_lists:
                intersect_list = self.list_intersect(intersect_list,
                                                self.inverted_lists
                                                [keywords[i]])
            else:
                # return an embpty list
                intersect_list = []

            i += 1

        return intersect_list

    def search_query(self):
        ''' This fuction is used to test the running time to fetch a query'''

        search_query= True

        while search_query:
            # a hard-coded keyword query.
            query =("the movie").lower()

            # Split the query into keywords.
            keywords = [keyword.strip() for keyword in re.split("[^A-Za-z0-9]+", query)]
            if len(keywords) < 3:
                query_list = self.query(keywords)
                query_list = list(set(query_list)) #remove duplicates of the doc ids
                search_query = False
            else:
                print("You have to type one or two keywords!")

        # if ther are any hits, print them
        if query_list:
            for hits in range(len(query_list)):

                print(self.records[query_list[hits]],"\n\n")
        else:
            print("No hits found!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Task4.py <file name>")
        sys.exit(1)
    file_name = sys.argv[1]
    #make an instance of the class
    inverted_index = InvertedIndex()
    sep = "[^A-Za-z0-9]+"

    #To gete where in the code does it spend most of its time
    cProfile.run('inverted_index.parser(file_name,sep)')
    cProfile.run('inverted_index.search_query()')
    #to get the ten frequent words
    inv_list = inverted_index.inverted_lists
    inverted_index.word_frequency(inv_list)
