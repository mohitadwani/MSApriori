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
            if 'or' in line:
                for i in line.replace(' ', '').replace('\n', '').split(':')[1].split('or'):
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
    count_dict = {}
    tail_count_dict = {}
    min_support = dict(sorted(min_support.items(), key=lambda x:x[1]))
    print("Sorted Itemset is {}".format(min_support))
    # Step 2 is to calculate L using init_pass
    l = init_pass(min_support, transactions_list)
    for one_itemset in list(l.items()):
        count_dict[(one_itemset[0],)] = one_itemset[1]
    f1 = []
    for item, lcount in l.items():
        if lcount/n > min_support[item]:
            f1.append((item,))
    print("F1 = {}".format(f1))
    k = 2
    F.append(f1)
    while True:
        if k == 2:
            c2 = level2_can_gen(l, SDC, min_support, transactions_list)
            C.append(c2)
            print("C2 = {}".format(c2))
        else:
            ck = MSCandidate_can_gen(F[k-2], l, SDC, min_support, transactions_list)
            if len(ck) == 0:
                break
            C.append(ck)
        print("Ck = {}".format(C[k-2]))
        for candidate in C[k-2]:
            count_dict[candidate] = 0
            tail_count_dict[candidate] = 0
        for transaction in transactions_list:
            for candidate in C[k-2]:
                temp_count = 0
                for item in candidate:
                    if item in transaction:
                        temp_count +=1
                if temp_count == len(candidate):
                    count_dict[candidate] += 1
                temp_count = 0
                for item in candidate[1:]:
                    if item in transaction:
                        temp_count +=1
                if temp_count == len(candidate[1:]):
                    tail_count_dict[candidate] += 1
                # if list(candidate) in transaction:
                #     print("suckjsdbnfjksdbjkfbskdnfksdnkf")
                    # count[candidate] += 1
        fk = []
        for candidate in C[k-2]:
            if count_dict[candidate]/n >= min_support[candidate[0]]:
                fk.append(candidate)
        print("Count Dict = {}".format(count_dict))
        print("Fk = {}".format(fk))
        if len(fk) == 0:
            break
        F.append(fk)
        k += 1

    print("**************************MSApriori OVER**********************")
    print("C = {}".format(C))
    print("F = {}".format(F))
    print("Count = {}".format(count_dict))
    if must_have_items:
        F = prune_must_have(F, must_have_items)
    if cannot_be_together:
        F = prune_cannot_be_together(F, cannot_be_together)
    output_pattern(F, count_dict, tail_count_dict)
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
            l[item] = count
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
    # f_something = list(f)
    # f_something.remove((100,120))
    # print("f_something removed with one subset to test = {}".format(f_something))
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
                        print(subset)
                        if subset not in f: # this doesnt work
                            print("Not In F : {}".format(subset))
                            c.remove(temp_f)
                            break
    print("mscan gen ends")
    return c

def prune_must_have(F, must_have_items):
    print(F)
    print("**************")
    print(must_have_items)
    for must_have_item in must_have_items:
        for itemsets in F:
            pass



    return F

def prune_cannot_be_together(F, cannot_be_together):
    print("inside cannot_be_together")
    temp_F = list(F)
    for i, itemsets in enumerate(F):
        if i==0:
            continue
        for j, itemset in enumerate(itemsets):
            for cannot_item in cannot_be_together:
                print(F, cannot_item)
                temp_count = 0
                for one_cannot in cannot_item:
                    if one_cannot in itemset:
                        temp_count += 1
                if temp_count == len(cannot_item):
                    try:
                        temp_F[i].remove(itemset)
                    except:
                        print("Itemset is already removed")

    print(temp_F)
    return temp_F

def output_pattern(F, count_dict, tail_count_dict):
    for i, itemsets in enumerate(F):
        if itemsets:
            print("Frequent {}-itemsets".format(i+1))
            for itemset in itemsets:
                print("\t {} : {{{}}}".format(count_dict[itemset], itemset))
main()
