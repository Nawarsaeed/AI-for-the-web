# @Author: Nawar saeed
# @Date:   2021-03-23T16:01:55+01:00
# @Email:  nawar.saeed@outlook.com
# @Filename: Task1.py
# @Description: about Implementing a simple parser
# that can be used to build an inverted index for 7
# a document collection.This is the code for task 1 for the
# @course AI for the Web. It is based on
# @Hannah Best's lectures
# @Hannah Bast <bast@cs.uni-freiburg.de>
# @Last modified by:   nawar
# @Last modified time: 2021-03-23T21:39:22+01:00



import re
import sys

class InvertedIndex:
    """ A class for constructing the inverted index. """

    def __init__(self):
        """ Constructor to create an empty inverted index. """
        self.inverted_lists = {}
        self.total_filmes=0 #this is used to calculate the number of movies

    def parser(self, file_name,separator):
        """
        Construct the inverted index from given file.

        file_name : name of the txt file
        separator : Specifies the separator to use when splitting the string
        """
        global total_filmes
        doc_id = 0 # used to assign every word a document id
        with open(file_name) as file:
            #read the file line by line
            for line in file:
                self.total_filmes +=1 #increase total filmes by one
                doc_id += 1
                # this is used to split the name of the movie rom its description
                for word in re.split(separator, line):
                    if len(word) > 0:
                        #convert to small letters
                        word = word.lower()
                        #If a word is seen for first time, create an
                        #empty inverted list for it.
                        if word not in self.inverted_lists:
                            self.inverted_lists[word] = []
                        #assign a word a doc id
                        self.inverted_lists[word].append(doc_id)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Task1.py <file name>")
        sys.exit(1)
    file_name = sys.argv[1]
    #make an instance of the class
    inverted_index = InvertedIndex()
    print("Make a choice!\n1-Total filmes in the file\n2-Total tokens in the file\n3-Total different tokens in the file")
    inp= int(input(""))
    if inp==1:
        sep="\t+" #Specifies the separator to use when splitting the string
        inverted_index.parser(file_name,sep)
        #for word, inverted_list in inverted_index.inverted_lists.items():
            #print("%s\t%d" % (word, len(inverted_list)))
        print("Total films in the file: ",inverted_index.total_filmes)

    if inp==2:
        sep = "[^A-Za-z0-9]+" #Specifies the separator to use when splitting the string
        total_tok = 0 #used to count the number
        inverted_index.parser(file_name,sep)
        for word, inverted_list in inverted_index.inverted_lists.items():
            #print("%s\t%d" % (word, len(inverted_list)))
            total_tok +=len(inverted_list)
        print("Total tokens in the file: ",total_tok)
    if inp==3:
        sep = "[^A-Za-z0-9]+" #Specifies the separator to use when splitting the string
        inverted_index.parser(file_name,sep)
        #for word, inverted_list in inverted_index.inverted_lists.items():
            #print("%s\t%d" % (word, len(inverted_list)))
        print("Total different tokens in the file: ",len(inverted_index.inverted_lists.values()))
    else:
        sys.exit()
