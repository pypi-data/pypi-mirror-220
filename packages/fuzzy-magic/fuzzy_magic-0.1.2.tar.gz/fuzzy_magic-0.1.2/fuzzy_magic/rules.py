import re
from simpful import *
from .exceptions import InvalidRuleException
import copy

class Rule(): 
    """
        Class that contains any method related with the rules.
    """
    def __init__(self) -> None:
        self.rules = []
    

    def check_rule(self, line):
        """
            Check if the rule is valid in the format "IF (x IS y) THEN (z IS w)"
            Parameters
            ----------
                line: the rule in string format
            Raises
            ------
                InvalidRuleException if the line does not match the pattern
        """    
        # Lets go with the regular expresion here
        # \s+ -> one or more whitespaces
        # (?...) -> possible structure. It could be or not in the pattern
        # .* -> any character (except line break)

        # pattern = r'^IF\s+.*+\s+IS\s(?:\w+\s+AND\s+.*\s+IS*\s+\w+\s)+THEN\s+.*\s+IS(?:\s+AND\s+.*\s+IS)*$' <-- Wrong.
        pattern = r'^IF\s+\(\w+\s+IS\s+\w+\)(?:\s+(?:AND|OR)\s+\(\w+\s+IS\s+\w+\))*\s+THEN\s+\(\w+\s+IS\s+\w+\)(?:\s+(?:AND|OR)\s+\(\w+\s+IS\s+\w+\))*$' #Improving machines, hell yes.
        if not re.match(pattern, line): 
            raise InvalidRuleException(line)
        else: 
            return True
    
    def get_rule_parts(self, line): 
        """
            Separate the antecedents and the consequents

            Parameters
            ----------
                line: the rule in string format
            Raises
            ------
                InvalidRuleException if the line does not match the pattern
        """   
        # Seems that everything could be made with regular expressions (if you know the pattern)
        pattern = r"(\w+)\s+IS\s+(\w+)" # <- This avoid the "AND/OR" and just focus on what is between () (in this case, words and/or numbers)

        if (self.check_rule(line)): 
            antecedents = line[2:line.find("THEN")]
            antecedents = re.findall(pattern, antecedents)

            consequents = line[line.find("THEN"):]
            consequents = re.findall(pattern, consequents)
            
            return antecedents, consequents
        else: raise InvalidRuleException(line)
    
  
    def is_defined(self, FS, name, value): 
        """
        It could happen that you set a rule in your file but the LV name 
        or the value associated to it does not exist or it has been wrong defined.
        This function goes to fix that, checking if the name in the rule and the value in the rule
        are both correct.

        TODO: To be added or be implemented within check_rule()

            Parameters
            ----------
                line: the rule in string format
            Raises
            ------
                InvalidRuleException If the value is not defined in your LV as term.
        """

        if name in FS._lvs.keys(): 
            if FS._lvs.get(name).get_index(value) != -1:
                return True
            else: 
               raise Exception("No '{}' defined in your {} LV. Check your Values!".format(value, name))
        else: 
            raise Exception("No '{}' defined in the fuzzy system. Check your Linguistic Variables!".format(name))
        
    def add_rules_from_file(self, path, r=0):
        """
            Parse a file with rules in the correct format.

            Parameters
            ----------
                path: the path of the file
                r: if 0 (default), it doesn't return anything
                if 1, it returns a copy of the Rule object with the rules inside.

            Raises
            ------
        """   
        with open(path, 'r') as f: 
            for line in f: 
                if self.check_rule(line): 
                    self.rules.append(line)

        if r == 1: 
            return copy.deepcopy(self)
    
    def add_rules_to_fs(self, FS=None): 
        """
            Add the rules to the given Fuzzy System.

            Parameters
            ----------
                FS: the Fuzzy System. If no FS is given, it creates a new one.
        """   
        if FS is None: 
            FS = FuzzySystem()
        
        for line in self.rules: 
            antecedents, consequents = self.get_rule_parts(line) 
            for name, value in antecedents + consequents: 
                self.is_defined(FS, name, value)
            FS.add_rules([line])
        
        return FS