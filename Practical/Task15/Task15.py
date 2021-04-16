# @Author: Nawar saeed
# @Date:   2021-04-04T11:06:57+02:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task15.py
# @Description: This task is about implementing q-gram index for a document
# collection and also about finding out how many 3-grams are there in the
# collection. It is also about finding out the most frequent 3-grams and
# how may words start with the letter K.This is the code for task 15 for the
# @course AI for the Web. It is based on
# @Hannah Best's lectures
# @Hannah Bast <bast@cs.uni-freiburg.de>
# @Last modified by:   nawar
# @Last modified time: 2021-04-13T20:04:45+02:00



import re
import sys
import operator
import matplotlib.pylab as plt
import numpy as np
class QgramIndex:
    """ A class for q-gram index. """

    def __init__(self, Q):
        """ Constructor to create an empty q-gram index. """
        self.inverted_lists = {}#Empty inverted index
        self.total_filmes=0     #this is used to calculate the number of movies
        self.records = dict()  # will be used to split the name of the movie and its description
        self.Q = Q             #used to specify the number of qgrams
        self.q_grams ={}

    def parser(self, file_name,sep):
        """ Construct index from given file.

        file_name : name of the txt file
        sep : Specifies the separator to use when splitting the string
        """
        qgram_id = 0
        with open(file_name) as file:
            #read the file line by line
            for line in file:
                qgram_id += 1 #increase qgram id by one
                self.total_filmes +=1 #increase total filmes by one
                #split each line by records and its description
                records, rest= line.strip().split("\t",1)
                #split records into words
                records = records.split()
                for record in records:
                    self.records[qgram_id] = line.replace('\n', '')
                    #ignore the first line
                    if record == "name":
                        continue
                    for word in self.qgrams(record):
                        # this is used to split the name of the movie rom its description
                        if len(word) > 0:
                            word = word.lower()
                            #If a word is seen for first time, create an empty inverted list for it.
                            if word not in self.inverted_lists:
                                self.inverted_lists[word] = dict()
                            if qgram_id in self.inverted_lists[word].keys():
                                #increment the tf by 1
                                self.inverted_lists[word][qgram_id] +=1
                            else:
                                #set the tf to 1, if the doc was not already seen
                                self.inverted_lists[word][qgram_id] = 1

                            #self.inverted_lists[word].append(qgram_id)

    def qgrams(self,record):
        '''
        Create q-gram for a given record
        split te record by into a given number of qgram and append
        padding with respect to with observance to the beginning and the end
        of the word. Each single record is considered as qgram, e.g.
        [united kingdom] is divided into the following 3-grams:

        '$$u', '$un', 'uni', 'nit', 'ite', 'ted', 'ed$', 'd$$',
        '$$k', '$ki', ' kin ',' ing ',' ngd','gdo','dom','om$','m$$'
        '''
        record = "$" * (self.Q - 1) + record + "$" * (self.Q - 1)
        return [record[records:records + self.Q] for records in range(0, len(record)- self.Q +1)]

    def top_ten_qgrams(self,inverted_list):
        '''
        A simple function is used to print top-10 most frequent qgrams.

        inverte_list: An argument to be used for the inverted list

        '''
        # loop through all items of the inverted list
        for qgram,inverted_list in QG.inverted_lists.items():
            value =  len(inverted_list) # assign length of the invertedlist to this variable
            key = "%s" % qgram #assign all qgrams to variable key
            self.q_grams[key] =value # fill the q_gram dict with keys and vales
        print("It has been generated ", sum(self.q_grams.values()),"3-grams ")
        print("the top-10 3-grams are:\n")
        iterator=0 # used as iterator in the for loop belwo
        #loop through the sorted qgram dic
        for i,j in sorted(self.q_grams.items(), key=lambda item: item[1],reverse=True):
            if iterator == 10 :
                break
            print("%s\t%s" % (i,j)) # print the ten most frequent qgrams
            iterator +=1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Task15.py <file name>")
        sys.exit(1)
    file_name = sys.argv[1]
    # make an instance of the class
    QG = QgramIndex(3)
    sep= "[^a-zA-Z0-9]+"  # separator
    print("Loading...\n")
    QG.parser(file_name,sep)#subroutine to the parser function

    qgrams = QG.inverted_lists.items()
    print(qgrams)
    QG.top_ten_qgrams(qgrams) # subroutine to top_ten_qgrams function
    #this for loop is used to find out all words who starts with the letter K
    for keys,values in QG.q_grams.items():

        if keys == "$$k":
            print("\n\nThere are", values,"words starting with the letter K ")

    # all stuffs  below are used for plotting purposes
    x=[] #An empty list used to store the keys of the qgram dict
    y=[] #An empty list used to store the values of the qgram dict
    for key,value in QG.q_grams.items():
        x.append(value)
        y.append(key)
    c=len(x) # length of the x list
    #print("CCCCCCCCCCCCC",c)
    plt.loglog(range(c),np.sort(x)[::-1]) # plotting log-log scale
    plt.xlabel("3-grams") #labels for the x_axis
    plt.ylabel("Total 3-grams") #labels for the y_axis
    plt.show()
