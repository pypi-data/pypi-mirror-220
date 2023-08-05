from .lvs import LV
from .rules import Rule
from simpful import *
import os
import json
import sys

"""
    This is the class where the magic starts.
"""
class FuzzyMagic(): 
    def __init__(self, path_lvs="", path_rules=""): 
        lvs = LV()
        if path_lvs == "": 
            self.lvs = lvs
        else: 
            self.lvs = lvs.read_lvs_from_file(path_lvs, 1)

        rules = Rule()
        if path_rules == "": 
            self.rules = rules
        else: 
            self.rules = rules.add_rules_from_file(path_rules, 1)

    def do_magic(self): 
        """
            Creation of the whole Fuzzy System taking into account
            the lvs and rules parsed in the creation of the object

            Returns: the Fuzzy System
        """
        FS = self.lvs.add_lvs_to_fs()
        FS = self.rules.add_rules_to_fs(FS)

        return FS

def create_fuzzy_rules(filepath="./data/rules.txt"):
    """
        This method has as aim the creation of the Fuzzy Rules in a 
        handmade way. The user can create the rules just taking care of
        the terms and the value they take in the rule.

        It counts with an option to create the rules file that is neccesary 
        to create the Fuzzy System using the "do_magic" method.
    """

    if not os.path.exists("./data"): 
        os.makedirs("./data")
        print("Data folder created")

    rules = []
    
    while True:
        antecedents = {}
        consequents = {}
        
        # Getting antecedents from the user
        print("Enter antecedents:")
        while True:
            term = input("Enter term (or 'done' to finish antecedents): ")
            if term.lower() == "done":
                break
            value = input("Enter value for {}: ".format(term))
            antecedents[term] = value
        
        # Getting consequents from the user
        print("\nEnter consequents:")
        while True:
            term = input("Enter term (or 'done' to finish consequents): ")
            if term.lower() == "done":
                break
            value = input("Enter value for {}: ".format(term))
            consequents[term] = value
        
        # Adding the rule to the list
        rule = {"antecedents": antecedents, "consequents": consequents}
        rules.append(rule)
        
        # Asking if the user wants to add another rule
        choice = input("\nDo you want to add another rule? (y/n): ")
        if choice.lower() != "y":
            break
    
    # Writing the rules in the desired format
    output = ""
    for rule in rules:
        antecedent_str = " AND ".join(["({} IS {})".format(term, value) for term, value in rule["antecedents"].items()])
        consequent_str = " AND ".join(["({} IS {})".format(term, value) for term, value in rule["consequents"].items()])
        output += "IF {} THEN {}\n".format(antecedent_str, consequent_str)

    if filepath != "": 
        with open(filepath, 'w') as f: 
            f.write(output)
            print("Rule file created in {}".format(filepath))
    else: 
        return output
    

def create_linguistic_variables(filepath="./data/lvs.json"): 
    """
        This method has as aim the creation of the Linguistic Variables (LVs) in a 
        handmade way. The user can create the linguistic variable file knowing
        the name of the LV and the terms. Optionally, he/she could add the desired
        membership function and the universe of discourse. If not, it will set by default.
    """

    if not os.path.exists("./data"): 
        os.makedirs('./data')
        print("Data folder created")
    
    lvs = {}
    
    print("Enter the linguistic variables:")
    while True: 
        lv = input("Enter the name: ")
        
        while True: 
            terms = input("Enter the terms separate by commas: ")
            terms = str.split(terms, ',')
            terms = [item.strip() for item in terms]

            if len(terms) < 2: 
                print("You must write at least two terms. Do it again!")
            else: 
                break

        while True: 
            mf_type = input("Enter the type of the membership function. Choose between Trapezoid and Triangular or let it blank: ")
            if not mf_type in ['Trapezoid', 'Triangular', '']: 
                print('The option you choose is not available.')
            else: 
                break
        while True: 
            min_uod = input("Enter the minimum value of the universe of discourse or let it blank: ")
            if min_uod == "": 
                min_uod = 0
            else: 
                try: min_uod = int(min_uod)
                except: 
                    print('You enter something that it is not a number. Minimum set to 0')
                    min_uod = 0

            max_uod = input("Enter the maxium value of the universe of discourse or let it blank: ")
            if max_uod == "": 
                max_uod = 1
            else: 
                try: max_uod = int(max_uod)
                except: 
                    print('You enter something that it is not a number. Maximum set to 1')
                    max_uod = 1

            if min_uod > max_uod: print("The minimum of the universe of discourse can't be greater than the maximum")
            else: break

        lvs[lv] = {"terms":terms, "type":mf_type, "uod":[min_uod, max_uod]}

        # Asking if the user wants to add another lv
        choice = input("\nDo you want to add another linguistic variable? (y/n): ")
        if choice.lower() != "y":
            break
        
    if filepath != "": 
        with open(filepath, 'w') as f: 
            json.dump(lvs, f)
            print("LV file created in {}".format(filepath))
    else: 
        return lvs
    
def where_is_rule_file():
    while True: 
        path_rules = input('Please, tell me where the rule file is: ')
        if not os.path.exists(path_rules): 
            print('There is not a file in that path. Please, try again or CTRL+Z to finish the execution.')
        else: 
            return path_rules

def where_is_lv_file(): 
    while True:
        path_lvs = input('Please, tell me where the lv file is: ')
        if not os.path.exists(path_lvs): 
            print('There is not a file in that path. Please, try again or CTRL+Z to finish the execution.')
        else: 
            return path_lvs
    
def create_fuzzy_system(): 
    """
        This method aims to make it easier for the user to create the fuzzy system through either 
        the creation of the files automatically, or the selection of those files already created 
        for the creation of the fuzzy system.

        The available options are:
            - lv: if the user just wants to create the lv file and already has the rule file.
            - rule: if the user just wants to create the rule file and already has the lv file.
            - both: if the user wants to create both lv and rule files.
            - any: if the user has already created both files.

        Returns: 
            - FS: The Fuzzy System already created with the LVs and the rules.
    """
    print("Welcome to Fuzzy Magic library!")
    path_lvs = "./data/lvs.json"
    path_rules = "./data/rules.txt"
    
    choice = input("\nDo you want to create your linguistic variables file, rules file, both, or any? (lv/rules/both/any): ")
    if choice.lower() == "both": 
        create_linguistic_variables()
        create_fuzzy_rules()
    elif choice.lower() == "lv": 
        create_linguistic_variables()
        path_rules = where_is_rule_file()
    elif choice.lower() == "rules":
        create_fuzzy_rules()
        path_lvs = where_is_lv_file()
    elif choice.lower() == "any": 
        path_lvs = where_is_lv_file()
        path_rules = where_is_rule_file()
    else: 
        print("You don't select any of the options, so there is no trick to do. Have a nice day!")
        sys.exit()
        
    print("The magic starts!")
    FM = FuzzyMagic(path_lvs, path_rules)

    print("The trick is completed. I will return your Fuzzy System now. Enjoy!")
    return FM.do_magic()