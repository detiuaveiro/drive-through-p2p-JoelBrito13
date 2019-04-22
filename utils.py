# coding: utf-8

def contains_successor(self_id, successor_id):
    if self_id+1 == successor_id:
        return True
    return False

def check_lst_true(lst):
    if lst == []:
        return True
    elif lst[0] == False:
        return False
    return check_lst_true(lst[1:])