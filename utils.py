# coding: utf-8

def contains_successor(self_id, successor_id):
    if self_id+1 == successor_id:
        return True
    elif self_id==3 and successor_id==0:
        return True
    return False

def contains_predecessor(self_id, predecessor_id):
    if self_id-1 == predecessor_id:
        return True
    elif self_id==0 and predecessor_id==3:
        return True
    return False