# @Author: Nawar saeed <nawar>
# @Date:   2021-04-04T11:06:57+02:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task19.py
# @Description: This task is about implementing k-means for sparse term-document matrices
# @Last modified by:   nawar
# @Last modified time: 2021-04-16T09:47:57+02:00

import re
import sys
import random
from math import log
import math
from time import time
import numpy as np
from scipy.sparse import csr_matrix


class Kmeans:
    """ Class for a implementing a k-means. """

    def __init__(self):
        self.inverted_lists = dict()
        self.record_lengths = dict()
        self.terms = []
        self.total_filmes=0
        self.records = dict()  # will be used to split the name of the movie and its description
        self.document_length= [] #store the docs length
        self.n = 0      # Total number of records (documents) [Lines]
        self.m = 0      # Total number of terms
        self.A = None   # Term-document matrix


    def bm25_score(self, N, AVDL, k=0.75, b=0.0):
        ''' Return the BM25 score'''

        for word, inverted_list in self.inverted_lists.items():
            for i, (doc_id, tf) in enumerate(inverted_list):
                # Obtain the document length (dl) of the document.
                dl = self.document_length[doc_id - 1]  # doc_id is 1-based.
                # Compute alpha = (1 - b + b * DL / AVDL).
                alpha = 1 - b + (b * dl / AVDL)
                # Compute tf2 = tf * (k + 1) / (k * alpha + tf).
                if k > 0:

                    tf = tf * (1 + (1 / k)) / (alpha + (tf / k))
                else:
                    tf = 1
                # Compute df (that is the length of the inverted list).
                df = len(self.inverted_lists[word])
                # Compute the BM25 score = tf' * log2(N/df).
                inverted_list[i] = (doc_id, tf * math.log(N / df, 2))


    def parser(self, file_name):
        """ Construct index from given file.

        file_name : name of the txt file
        sep : Specifies the separator to use when splitting the string
        """
        doc_id = 0
        with open(file_name) as file:
            #read the file line by line
            for line in file:
                self.total_filmes +=1 #increase total filmes by one
                doc_id += 1
                self.records[doc_id] = line.replace('\n', '')
                terms, rest= line.strip().split("\t",1)
                terms = re.split('\W+', terms)
                # this is used to split the name of the movie and its description

                for word in terms:
                    # this is used to split the name of the movie from its description
                    if len(word) > 0:
                        word = word.lower()
                        #If a word is seen for first time, create an empty inverted list for it.
                        if word not in self.inverted_lists:
                            self.terms.append(word)
                            self.inverted_lists[word] = [(doc_id,1)]
                            continue
                        last_posting= self.inverted_lists[word][-1]
                        if last_posting[0]==doc_id:
                            #increment the tf by tf=1
                            self.inverted_lists[word][-1] = (doc_id,last_posting[1]+1)
                        else:
                            #set the tf to 1, if the doc was not already seen
                            self.inverted_lists[word].append((doc_id,1))
                #document length
                self.document_length.append(doc_id)

        #replace the tf scores by BM25 scores
        self.n = len(self.records)
        #print("lenght", n)
        avdl = sum(self.document_length)/self.n
        b=0.0
        k=0.75
        #self.bm25_score(self.n,avdl,k,b) #uncommet to use BM25 scores



    def build_td_matrix(self, m=10000):
        """
        Computes the sparse term-document matrix using the
        inverted index.
        """
        #make a sorted list
        terms = sorted(self.terms,
                       key=lambda t: len(self.inverted_lists[t]),
                       reverse=True)[:m]
        row = [] #list to storing the rows
        col = [] #list to storing the columns
        values = [] #list to storing the values
        for i, t in enumerate(terms):
            #loop through the inverted lists and append row,col and values
            for doc, score in self.inverted_lists[t]:
                row.append(i)
                col.append(doc - 1)
                values.append(score)
        #compute the sparse matrix
        self.A = csr_matrix((values, (row, col)), dtype=float)


    def initialize_centriods(self, k):
        '''
        Compute a (terms x clusters) matrix with the
        initial (random) centroids.
        '''
        # Randomly selects any K documents from the document vectors.
        rows = sorted(random.sample(range(self.n), k))
        cols = [i for i in range(k)]
        values = [1 for _ in range(k)]
        return self.A * csr_matrix((values, (rows, cols)), shape=(self.n, k))




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python3 Task19.py <file_name>')
        sys.exit()

    k = Kmeans()
    file_name = sys.argv[1]
    print("Loading...")
    k.parser(file_name)
    print('Computing term-document matrix A...')
    k.build_td_matrix()
    initial_centriods = k.initialize_centriods(2) # initialize centriods
    print("Term Document Matrix : ")
    print(k.A.todense(),"\n")
    print("Randomly initialized centriods : ")
    print(initial_centriods.todense())
