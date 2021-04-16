# @Author: Nawar saeed <nawar>
# @Date:   2021-04-02T08:44:30+02:00
# @Email:  nawar.saeed@outlook.com
# @Description: This task is about creating two lists of length n and
# filling one with numbers from 0 to n-1 and the other in the same way
# and shuffle it from the first list. The purpose is to sum up all the
# indexes to the lists and observe the difference between the methods.
# @Filename: Task5.py
# @Last modified by:   nawar
# @Last modified time: 2021-04-12T13:13:26+02:00



import random
import time

N=10 # A global variable to Specifiy the length of an array

def list1():
    '''
    This function is used to create an array of doc_length
    n an fill it with number from 0 to n-1 in sorted way
    e.g [0,1,2,3,....,n-1]

    '''

    l1=[] #An empty list
    for i in range(N):
        #append the numbers into l1
        l1.append(i)

    return l1

def list2():
    '''
    This function is used to create an array of doc_length
    n an fill it by shuffle the first list into it
    e.g [2,100,1,3879,....,n-1]

    '''
    #shuffle the first list ande append numbers from random indexes
    l2 = list1()
    random.shuffle(l2)

    return l2


def add_lists_elemets(list):
    ''' A simple function used to summing the array indexes'''

    result =0 # set result to 0
    #loop through the list
    for i in list:
        #sum upp the indexes
        result= result + i

    return result

if __name__ == "__main__":

    #list1()
    start_time= time.monotonic()
    print("Sum of list1:\t",add_lists_elemets(list1()))
    print("milliseconds:",((time.monotonic()- start_time) * 1000),"\n\n")
    start_time2= time.monotonic()
    print("Sum of list2:\t",add_lists_elemets(list2()))
    print("milliseconds:",((time.monotonic()- start_time2) * 1000))
