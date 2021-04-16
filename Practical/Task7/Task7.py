# @Author: Nawar saeed
# @Date:   2021-03-23T16:01:55+01:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task2.py
# @Description: This task is about extending the inverted index from the
# prevuos tasks with an algorithm for merge-based queries with k-keywords
# and also assign scores to the inverted lists. Morever, the score system has
# to be modified by more or replaced with something else e.g. BM25.T
# his is the code for task 2 for the
# @course AI for the Web. It is based on the code of
# @Hannah Best's lectures
# @Hannah Bast <bast@cs.uni-freiburg.de>
# @Last modified by:   nawar
# @Last modified time: 2021-03-23T21:39:22+01:00



import re
import sys
import math


class InvertedIndex:
    ''' A class for constructing an inverted index'''


    def __init__(self):
        """ Constructor to create an empty inverted index. """
        self.inverted_lists = {} #Empty inverted index
        self.total_filmes=0     #this is used to calculate the number of movies
        self.records = dict()  # will be used to split the name of the movie and its description
        self.document_length= [] #store the docs length
        self.benchmarks = {}  #dict to store the benchmarks


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


    def parser(self, file_name,sep):
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
                # this is used to split the name of the movie and its description
                self.records[doc_id] = line.replace('\n', '')
                for word in re.split(sep, line):
                    # this is used to split the name of the movie from its description
                    if len(word) > 0:
                        word = word.lower()
                        #If a word is seen for first time, create an empty inverted list for it.
                        if word not in self.inverted_lists:
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
        n = len(self.records)
        #print("lenght", n)
        avdl = sum(self.document_length)/n
        b=0.0
        k=0.75
        self.bm25_score(n,avdl,k,b) #commet this if you want to use tf=1 score

    def merge(self, list1, list2):
        """
        This function is used to merge two given inverted lists in linear time

        """

        merg_list = []

        # iterate over the two list, and check for equality
        # (example slide 18)
        L1 = 0
        L2 = 0
        while L1 < len(list1) and L2 < len(list2):
            #in case doc_id of the first list < doc_id of the second list
            if list1[L1][0] < list2[L2][0]:
                #print("NNNNNNN",list1[L1][0])
                #append doc_id of list1 to the merge list
                merg_list.append(list1[L1])
                L1 += 1
            #in case doc_id of the first list > doc_id of the second list
            elif list1[L1][0] > list2[L2][0]:
                #print("NNNNNNN2222",list1[L1][0])
                #append doc_id of list2 to the merge list
                merg_list.append(list2[L2])
                L2 += 1
            # the case where the two lists intersect
            else:
                #print("NNNNNNN3333",list1[L1][0])
                merg_list.append((list1[L1][0], list1[L1][1] + list2[L2][1]))
                L1 += 1
                L2 += 1
        # Here, remaining lists will be extended
        if L1 < len(list1):
        	merg_list.extend(list1[L1:])
        elif L2 < len(list2):
        	merg_list.extend(list2[L2:])
        return merg_list

    def query(self, keywords):
        '''
        This function is used to fetch the inverted list for each of the keywords
        and compute the union of all lists.

        keywords: An argument for the all the keywords of a query.
        '''
        lists = []
        if not keywords:
            return []
        # Fetch the inverted lists for each of the given keywords.
        for keyword in keywords:
            if keyword in self.inverted_lists:
                lists.append(self.inverted_lists[keyword])
        # if the list is empty
        if len(lists) == 0:
            return []
        #print("LIST:", lists)

        # Compute the union of all inverted lists.
        merged = lists[0]
        for i in range(1, len(lists)):
            merged = self.merge(merged, lists[i])

        # Filter the lists with score = 0.
        for score in merged:
            if score[1] !=0:
                score = merged
        # Sort by scores, in descending order.
        sorted_result = sorted(merged, key=lambda x: x[1], reverse=True)
        return sorted_result

    def get_benchmark(self, file_name):
        """
        A function used to parse the benchmark file and get the
        query and its ground truth

        file_name: name of the benchmark file
        """

        with open(file_name) as file:
            for line in file:
                #we split the line into query and ground truth
                query, ground_truth = line.strip().split("\t")
                #split each ground truth into ids
                self.benchmarks[query] = {int(x) for x in ground_truth.split(" ")}

        return self.benchmarks

    def precision_at_k(self, result_ids, relevant_docs, k ):
        """
        Computes the precision @ k of a given result list and a
        given set of relevant docs.
        """
        results = 0
        if (k == 0):
            return 0
        for i in range(0, min(len(result_ids), k)):
            if result_ids[i] in list(relevant_docs):
                results += 1
        results /= k
        return results

    def average_precision(self, result_ids, relevant_docs):
        """
        Computes the average precision of the given result list and a
        given set of relevant docs.
        """
        avg_prec = 0

        for i in range(0, len(result_ids)):
            if result_ids[i] in relevant_docs:
                avg_prec += self.precision_at_k(result_ids, relevant_docs, i + 1)
        avg_prec /= len(relevant_docs)
        return avg_prec

    def evaluate_benchmark(self, inverted_index, benchmark_query):
        '''
        A function used to evaliates the given benchmark.

        inverted_index : an argument for fetch the inverted list
        benchmark_query: an argument for geting the benchmarks
        '''
        number_of_queries = len(benchmark_query)
        total_avg_p = 0
        #loop through the benchmarks
        for query, relevant_docs in benchmark_query.items():
            doc_ids = [] # store th dockument ids
            r = len(relevant_docs) #length of the relevant documents
            #split the query and convert all letters to samll
            keywords = [x.lower().strip() for x in re.split("[^a-zA-Z]+", query)]
            for doc_id in self.query(keywords):
            	doc_ids.append(doc_id[0]) # append to the doc_ids list
            #compute the average precision
            avg_precision = self.average_precision(doc_ids, relevant_docs)
            total_avg_p += avg_precision
            #compute the mean average precision
            mean_avg_p = total_avg_p / number_of_queries

        return mean_avg_p

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 Task7.py <movies name> < benchmark file>")
        sys.exit(1)
    file_name = sys.argv[1]
    benchmark_file = sys.argv[2]

    inverted_index = InvertedIndex()
    print("Loading...\n")

    sep= "[^A-Za-z]+"

    inverted_l = inverted_index.parser(file_name,sep)

    benchmark = inverted_index.get_benchmark(benchmark_file)

    value= inverted_index.evaluate_benchmark(inverted_index.inverted_lists,benchmark)

    print("Mean Average Precision =%s" % round(value, 3))
