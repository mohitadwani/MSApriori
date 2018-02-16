# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 18:35:24 2018

@author: mohit
"""
from itertools import combinations

class k_itemset:
    items = []
    count = 0
    tail_count = 0

def main():
    transactions_list = read_input_file()
    min_support, SDC, must_have_items, cannot_be_together = read_param_file()
    print("Transaction List {}\n".format(transactions_list))
    print("Must Have Items: {}\n".format(must_have_items))
    print("SDC = {}\n".format(SDC))
    print("Min Support : {}\n".format(min_support))
    print("Cannot be Together: {}\n".format(cannot_be_together))
    ms_apriori(transactions_list, min_support, SDC, must_have_items, cannot_be_together)


def read_input_file():
    transactions_list = []
    file = open("input-data.txt", "r")
    for line in file:
        set_string = line.strip().replace('{', '').replace('}', '')
        set_string = set_string.split(',')
        transactions_list.append(list(map(int, set_string)))
    return transactions_list
    #print(transactions_list)

def read_param_file():
    must_have_items = []
    SDC = 0.0
    min_support = {}
    cannot_be_together = []

    file = open("parameter-file.txt", "r")
    for line in file:
        if 'must' in line:
    #        temp.append(line.replace(' ', '').replace('\n', '').split(':')[1])
            if 'or' in line:
                for i in line.replace(' ', '').replace('\n', '').split(':')[1].split('or'):
        #            print (i)
                    must_have_items.append(int(i))
            else:
                must_have_items.append(int(line.replace(' ', '').replace('\n', '').split(':')[1]))
        if 'SDC' in line:
            SDC = float(line.replace(' ', '').split('=')[1])
            #        print(type(SDC))
        if 'MIS' in line:
            hold = line.strip().replace(' ', '').replace('(', '').replace(')', '').replace('MIS', '').split('=')
            min_support[int(hold[0])] = float(hold[1])
        if 'cannot' in line:
            hold = line.replace(' ', '').rstrip().replace('cannot_be_together:', '').replace(' ', '').replace('\n','')
            hold = hold+','
            hold = hold.replace('{', '').split('},')[:-1]
            for i in hold:
                cannot_be_together.append(list(map(int, i.split(','))))
    # print("Must Have Items: {}".format(must_have_items))
    # print("SDC = {}".format(SDC))
    # print("Min Support : {}".format(min_support))
    # print("Cannot be Together: {}".format(cannot_be_together))
    return min_support, SDC, must_have_items, cannot_be_together

def ms_apriori(transactions_list, min_support, SDC, must_have_items, cannot_be_together):
    # step 1 is to sort the itemset based on their MIS
    n = len(transactions_list)
    F = []
    C = []
    count = {}
    tail_count = {}
    min_support = dict(sorted(min_support.items(), key=lambda x:x[1]))
    print("Sorted Itemset is ")
    print(min_support)
    # Step 2 is to calculate L using init_pass
    l = init_pass(min_support, transactions_list)
    f1 = dict()
    for item, act_sup in l.items():
        if act_sup > min_support[item]:
            f1[item] = act_sup
    print(f1)
    k = 2
    while True:
        if k == 2:
            c2 = level2_can_gen(l, SDC, min_support, transactions_list)
            C.append(c2)
            print(c2)
        else:
            ck = MSCandidate_can_gen(F[k-3], l, SDC, min_support, transactions_list)
            C.append(ck)
        # print(C[k-2])
        for candidate in C[k-2]:
            count[candidate] = 0
            tail_count[candidate] = 0
        for transaction in transactions_list:
            for candidate in C[k-2]:
                temp_count = 0
                for item in candidate:
                    if item in transaction:
                        temp_count +=1
                if temp_count == len(candidate):
                    count[candidate] += 1
                temp_count = 0
                for item in candidate[1:]:
                    if item in transaction:
                        temp_count +=1
                if temp_count == len(candidate[1:]):
                    tail_count[candidate] += 1
                # if list(candidate) in transaction:
                #     print("suckjsdbnfjksdbjkfbskdnfksdnkf")
                    # count[candidate] += 1
        fk = []
        for candidate in C[k-2]:
            if count[candidate]/n >= min_support[candidate[0]]:
                fk.append(candidate)
        print(count)
        print(fk)
        F.append(fk)
        if k == 3: # replace this with F k -1 = empty
            break
        k += 1

def init_pass(min_support, transactions_list):
    # to add first item in L, that item will be the first item which satisfies it's min_support
    l = dict()
    n = len(transactions_list)
    for item, mis in min_support.items():
        count = 0
        if len(l) == 0:
            current_mis = mis
        # count the number of occurances of each item
        for transaction in transactions_list:
            #print(str(transaction))
            if item in transaction:
                count +=1
        act_sup = count/n
        if act_sup >= current_mis:
            l[item] = act_sup
            if len(l) == 1:
                current_mis = mis
    return l

def level2_can_gen(l, SDC, min_support, transactions_list):
    L = list(l.items())
    c2 = []
    for i, l in enumerate(L):
        if l[1] >= min_support[l[0]]:
            for j, h in enumerate(L[i+1:]):
                # print(l , h)
                if h[1] >= min_support[l[0]] and abs(l[1] - h[1]) <= SDC:
                    c2.append((l[0], h[0]))
    return c2

    # for i in range(len(l)):
    #     # pass
    #     print(list(l.items())[i])
    #     if l.items()[i] >= min_support[l[i]]:
    #         print("sdfsdf")

def MSCandidate_can_gen(f, l, SDC, min_support, transactions_list):
    print("inside mscan gen")
    c = []
    f1 = list(f)
    f1.remove((140,120))
    print(f1)
    for i, f1 in enumerate(f):
        temp_f = []
        # print(i, f1)
        for f2 in f[i+1:]:
            if f1[:-1] == f2[:-1] and min_support[f1[-1]] <= min_support[f2[-1]] and abs(l[f1[-1]] - l[f2[-1]]) <= SDC:
                temp_f = f1
                temp_f = temp_f + (f2[-1],)
                c.append(temp_f)
                for subset in list(combinations(temp_f, len(temp_f)-1)):
                    if temp_f[0] in subset or (min_support[temp_f[1]] == min_support[temp_f[0]]):
                        if subset in f: # this doesnt work
                            print("sdkjvfbjdskfnfgkdsfngndkjfng")
                            print(subset)




    print("mscan gen ends")
    return c



main()
