import re

def phone_number(number):
    patern = r"^\+9891[0-9]{8}$"
    
    if re.match(patern, number):
        print("Valid Phone number")
    else:
        print("Invalid Phone number")

def rg_code_meli(codeMeli):
    patern = r"^[0-9]{10}$"

    if re.match(patern, codeMeli):
        print("Valid CodeMeli number")
    else:
        print("Invalid CodeMeli number")
        
        
def feth_name(name):
    patern = r"^[آ-یA-Za-z\s]+$"
    
    if re.match(patern, name):
        print("Valid Name")
    else:
        print("Invalid Name")
        
        

        
