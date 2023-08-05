"""
    This file contains all the exceptions created for managing the different
    problems/issues that could appear during the execution of the different parts
    of this library
"""


class InvalidRuleException(Exception): 
    """
    InvaludRuleException is raised when the rule format does not follow the 
    Simpful library syntax.
    Example of GOOD rule: 
        IF (term1 IS valueTerm1) AND (term2 IS valueTerm2) THEN (term3 IS valueTerm3)
    """
    def __init__(self, line):
        self.message = 'The rule {} is not valid'.format(line)
    def __str__(self) -> str:
        return self.message


class InvalidMembershipException(Exception): 
    """
    InvalidMembershipException is raised when the user enter neither Triangular, 
    Trapezoid, or blank for membership function type.
    """   
    def __init__(self, name):
        self.message = "The function {} is not available. Please, choose between Triangular and Trapezoid, or leave it blank".format(name)

    def __str__(self) -> str:
        return self.message


class InvalidJsonFormat(Exception):
    """
    InvalidJsonFormat could have two reasons: 
        1. The file you are trying to use is not JSON or have a correct JSON format
        2. Since the LVs needs terms and the type of the MFs, if there are any of them, it raises.

    """
    def __init__(self, number):
       self.value = number

    def __str__(self) -> str:
        if self.value == 1:
            self.message = "The file you are trying to load is not in JSON format. Please, check it" 
        if self.value == 2:
            self.message = "The input or output in the file does not contain at least 'terms' and/or 'type' values" 
        # if self.value == 3: 
        #     self.message = "JSON file does not have the right structure to be loaded. Please, check it"

        return self.message


class InvalidPointsArray(Exception):
    """
    InvalidPointsArray appears if you don't use the minimum amount of points for each MFs, 
        i.e. you need 3 points for a Triangular MF and 5 for a Trapezoid MF.
    """
    def __init__(self, number):
        self.message = "Points array should contains at least {} points to create the MF".format(number)

    def __str__(self) -> str:
        return self.message
