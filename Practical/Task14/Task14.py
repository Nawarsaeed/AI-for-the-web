# @Author: Nawar saeed <nawar>
# @Date:   2021-04-02T14:26:20+02:00
# @Email:  nawar.saeed@outlook.com
# @Description: This task is about implementing a function that
# computes the prefix edit distance.
# @Filename: Task14.py
# @Last modified by:   nawar
# @Last modified time: 2021-04-12T15:20:27+02:00


import random
from random import choice
from string import ascii_lowercase
import matplotlib.pylab as plt
import numpy as np


def levenshtein(s, t):
    ''' From Wikipedia article; Iterative with two matrix rows.
        Compute the prefix edit distance PED(s, t).
    '''
    if s == t: return 0
    elif len(s) == 0: return len(t)
    elif len(t) == 0: return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    #print(v0)
    return min(v1)#Just return the minimum of the entries in the last row (PED)

if __name__ == '__main__':

    '''
    Create two lists of 5000 random strings of length 10 each and
    compute the prefix edit distance between each pair of string.
    '''
    chars = ascii_lowercase
    lst1 = [''.join(choice(chars) for _ in range(10)) for _ in range(5000)]
    lst2 = [''.join(choice(chars) for _ in range(10)) for _ in range(5000)]
    #print(lst1)
    #print("distance", distance("uni","university"))
    print("distance", levenshtein("FIBU","FREIBURG"))
    plot_list=[]
    for i in range(5000):

        plot_list.append(levenshtein(lst1[i],lst2[i]))
    plt.figure(1)
    plt.xlabel("Words")
    plt.ylabel("PED")
    #plt.plot(range(5000),plot_list)
    plt.plot(range(5000),np.sort(plot_list)[::-1])
    plt.show()
