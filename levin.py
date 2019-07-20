#!/usr/bin/env python
# coding: utf-8

# Computation of the Pascal triangle modulo some integer called 'base'.
# If the integer is 2, this is also called the Sierpinski triangle.
# The triangle is put in a square: what is usually a line is now a diagonal.
# 
# Usual Pascal triangle     
# 
#     1                         
#     1 1                       
#     1 2 1                     
#     1 3 3 1                   
#     1 4 6 4 1 
# 
# Pascal triangle in a square
# 
#     1 1 1 1 1
#     1 2 3 4 5
#     1 3 6 10
#     1 4 10
#     1 5 15
# 
# Two dimensional array s[][] such that
#  - s[i][0] = s[O][i] = 1 for all i >= 0
#  - s[i][j] = s[i-1][j] + s[i][j-1] mod base for all i,j >= 1

import itertools
import math
import numpy
import matplotlib.pyplot as plt
import sys

BASE = 2

class PascalModulo:
    def __init__(self,base):
        self.base = base
        self.diags = [[1]]
        
    #Add a diagonal and fill it
    def _add(self):
        self.diags[0].append(1)
        i = 1
        while i <= len(self.diags) - 1:
            self.diags[i].append( (self.diags[i-1][len(self.diags[i])] + self.diags[i][len(self.diags[i]) - 1]) % self.base )
            i+=1
        self.diags.append([1])
            
    #Get element
    def get(self,i,j):
        if (i < 1 or j < 1):
            return 1
        # Compute diagonal if not computed yet
        while (len(self.diags[0]) <= i+j):
            self._add()
        return self.diags[i][j]
    


class Levin:
    
    def __init__(self,size=1):
        self.size = size
        self.iterator = itertools.product([False, True], repeat=self.size)
        self.block = next(self.iterator)
        self.block_index = 0
        self.sierp = PascalModulo(2)
    
    def get_next_digit(self):
#       print('block: ' + str(self.block) + ' ' + str(self.block_index))
        #check if the whole block was consumed and get a new one
        if len(self.block)  == self.block_index:
            try:
                self.block = next(self.iterator)
            except:
                self.size += 1
                self.iterator = itertools.product([False, True], repeat=self.size)
                self.block = next(self.iterator)
            self.block_index = 0
        res = 0
        for j in range(self.size):
            res += self.sierp.get(self.block_index,self.size-j-1) * self.block[j]
        self.block_index += 1
        return res%2
        

def get_occurrences(amounts,M):
    occs = {}
    total = 0
    for k,v in amounts.items():
        total += 1
        if v not in occs:
            occs[v] = 0
        occs[v] = occs[v] + 1
    occs[0] = int(2**M - total)
    for k,v in occs.items():
        occs[k] = v/2**M
    return (amounts,occs)


def get_amounts_for_first(N,lamb=1):
    levin = Levin()
    M = int(math.ceil(math.log(N,2)))
    amounts = {}
    counter = 0
    word = ''
    while len(word) < M:
        counter += 1
        word = word + str(levin.get_next_digit())
    amounts[word] = 1
    while counter < N*lamb:
        print(counter)
        word = word[1:]
        word = word + str(levin.get_next_digit())
        if  word not in amounts:
            amounts[word] = 1
        else:
            amounts[word] = amounts[word] + 1
        counter += 1
    return get_occurrences(amounts,M)

    

lamb = float(sys.argv[1])
print('lambda: '+ str(lamb))

N = int(2**int(sys.argv[2]))
print("N: " + str(N))
(amounts,occs) = get_amounts_for_first(N,lamb=lamb)

print(occs)
plt.bar(occs.keys(), occs.values(), bottom=len(occs.keys()))
plt.show()
    
    





