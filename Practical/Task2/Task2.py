# @Author: Nawar saeed
# @Date:   2021-03-23T16:01:55+01:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task2.py
# @Description: The task is about extending the inverted
# index that has been created in the Task1 by a method for
# querying with a set of k-keywords.This is the code for task 2 for the
# @course AI for the Web. It is based on
# @Hannah Best's lectures
# @Hannah Bast <bast@cs.uni-freiburg.de>
# @Last modified by:   nawar
# @Last modified time: 2021-03-23T21:39:22+01:00



import re
import sys


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
                    #print(self.records)

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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Task2.py <file name>")
        sys.exit(1)
    file_name = sys.argv[1]

    inverted_index = InvertedIndex() #making an instance of the class
    print("Loading...\n")

    sep= "[^a-zA-Z0-9]+" # separator to split the file

    inverted_index.parser(file_name,sep) #call the parser function

    #print(inverted_index.hit)

    while True:
        search_query= True
        while search_query:
            # Ask the user for a keyword query.
            query = input("\nType your query: ").lower()

            # Split the query into keywords.
            keywords = [keyword.strip() for keyword in re.split("[^A-Za-z0-9]+", query)]
            if len(keywords) < 3:
                query_list = inverted_index.query(keywords)
                query_list = list(set(query_list)) #remove duplicates of the doc ids
                search_query = False
            else:
                print("You have to type one or two keywords!")


        #print("The two-keyword is found in these documents:\n ", query_list)

        # if ther are any hits, print them
        if query_list:
            for hits in range(len(query_list)):

                print(inverted_index.records[query_list[hits]],"\n\n")
        else:
            print("No hits found!")


    # Three diffrent two-keywords
    # 1- El extraordinario
    # 2- Breastival Vestibule
    # 3- bulma yamcha
