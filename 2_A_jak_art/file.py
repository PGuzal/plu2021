def greetings(get_data):
    def get_greeting(*args):
        data = ""
        split_string = get_data(*args).split()
        if len(split_string)>0:
            name = split_string[0]
            if len(split_string)==3:
                second_name = split_string[1]  
                surname = split_string[2]
                data+="Hello "+name[0].upper()+name[1:].lower()+" "+second_name[0].upper()+second_name[1:].lower()+" "+surname[0].upper()+surname[1:].lower()
            else: 
                surname = split_string[1]
                data+="Hello "+name[0].upper()+name[1:].lower()+" "+surname[0].upper()+surname[1:].lower()
        return data
    return get_greeting

@greetings
def name_surname(name):
    return name


# assert name_surname("jan nowak") == "Hello Jan Nowak"

def is_palindrome(palindrome):
    def check_palindrome(*args):
        palindrome_to_check = palindrome(*args)
        translate_dict = {".":"",",":""," ":"","?":"","!":""}
        palindrome_to_check_clean = palindrome_to_check.translate(palindrome_to_check.maketrans(translate_dict))
        if palindrome_to_check_clean.lower() == palindrome_to_check_clean[::-1].lower():
            palindrome_to_check+=" - is palindrome"
        else:
            palindrome_to_check+=" - is not palindrome"
        return palindrome_to_check
    return check_palindrome

@is_palindrome
def sentence(palindrome):
    return palindrome

#assert sentence("Eva, can I see bees in a cave?") == "Eva, can I see bees in a cave? - is palindrome"

#import pytest
def format_output(*args):
    list_of_key = []
    list_of_key.extend(args)
    def dec_make_dict(dict_received):
        def make_dict(*args):
            dict_new = {}
            data_dict = dict_received(*args)
            for key in list_of_key:
                try:
                    all_key = key.split("__")
                    temp = ""
                    for i in all_key:
                        temp+=data_dict[i]+" "
                    dict_new[key] = temp.strip()
                except:
                    raise ValueError
            return dict_new
        return make_dict
    return dec_make_dict


@format_output("first_name__last_name", "city","lato")
def first_func(dict_received):
    return dict_received

@format_output("first_names", "age")
def second_func(dict_received):
    return dict_received
first_func({
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw",
        "lato":"nie"
    }) 

# with pytest.raises(ValueError):
#      second_func({
#         "first_name": "Jan",
#         "last_name": "Kowalski",
#         "city": "Warsaw",
#         "lato":"nie"
#     })


class A:
    pass

from functools import wraps
def add_class_method(class_name):
    def add_method(method):
        @classmethod
        @wraps(method)
        def wrapper(*args,**kwargs):
            return method(*args,**kwargs)
        setattr(class_name, method.__name__, wrapper)
        return method
    return add_method

def add_instance_method(class_name):
    def instance_method(method):
        @wraps(method)
        def wrapper(*args,**kwargs):
            return method(*args,**kwargs)
        setattr(class_name, method.__name__, staticmethod(wrapper))
        return method
    return instance_method
@add_class_method(A)
def foo():
    return "Hello again!"
@add_instance_method(A)
def boo():
    return "Hello again!"
A.boo()
A().foo()


