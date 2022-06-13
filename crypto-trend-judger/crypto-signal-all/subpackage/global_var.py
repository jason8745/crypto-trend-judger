#############
# Author : Yujun Wen
# Last edit: 2022/2/26
# email: yujunwen0517@gmail.com
#############
def _init(): 
    global _global_dict 
    _global_dict = {} 

def set_value(name, value): 
    _global_dict[name] = value 
    
def get_value(name, defValue=None): 
    try: 
        return _global_dict[name] 
    except KeyError: 
        return defValue