from .memberships import MembershipFunction
from simpful import *
from .exceptions import InvalidJsonFormat, InvalidMembershipException
import json
import numpy as np
import copy
"""
Way to go: 
    1. Get the values from inputs and outputs
        1.1. i1, i2, o1 is the name of the label
        1.2. the values are the terms for each label 
            (see simpful example)
        1.3. the universe of discourse is the interval where the value works
            if not given, uod = [0,1]
    2. Send it to a MembershipFunction object to create the fuzzy set
    3. Add linguistic value to the system.
""" 

class LV(): 
    def __init__(self) -> None:
        self.linguistic_variables = {}

    def read_lvs_from_file(self, filepath, r=0):
        """
            Read the linguistic variables defined in filepath

            Parameters
            ----------
                filepath: the path of the file
                r: if 0 (default), it doesn't return anything
                if 1, it returns a copy of the LV object with the LVs inside.
            Raises
            ------
                InvalidJsonFormat
        """   
        with open(filepath) as f: 
            try: 
                mfs = json.load(f)
            except: raise InvalidJsonFormat(1)

            print(mfs.keys())
            
            for lv in mfs.keys():
                #Valid format? 
                try: 
                    terms = mfs[lv]['terms']
                    mf_type = mfs[lv]['type']

                    if 'universe_of_discourse' in mfs[lv].keys():
                        uod = mfs[lv]['universe_of_discourse']
                    else: 
                        uod = [0,1]
                except: 
                    raise InvalidJsonFormat(2)
                
                # Check if type is inside the ones that you can use
                self.is_type(mf_type)

                # Number of sets needed -> len(terms)
                n_sets = len(terms)
                term_mf = []
                if mf_type=='Triangular' or mf_type=='':
                    points = self.generate_triangular_points(n_sets, uod[0], uod[1])
                    for term in terms: 
                        term_mf.append(MembershipFunction.make_triangular(points[terms.index(term)], 
                                                                            term))
                elif mf_type=='Trapezoid': 
                    points = self.generate_trapezoid_points(n_sets, uod[0], uod[1])
                    for term in terms: 
                        term_mf.append(MembershipFunction.make_trapezoid(points[terms.index(term)],
                                                                term))
                self.linguistic_variables[str(lv)] = [term_mf, uod]
            
            if r == 1: 
                return copy.deepcopy(self)

    def add_lvs_to_fs(self, FS=None):
        """
            Add the LVs defined in the object to the given Fuzzy System.
            Parameters
            ----------
                FS: the Fuzzy System. If no FS is given, it creates a new one.
        """   
        if FS is None: 
            FS = FuzzySystem()

        for lv in self.linguistic_variables.keys():
            # LinguisticVariable(MFS, concept, uod)
            FS.add_linguistic_variable(str(lv), LinguisticVariable(self.linguistic_variables[lv][0], str(lv), 
                                                                self.linguistic_variables[lv][-1]))
        return FS
    
    def is_type(self, type): 
        """
            Check if the type described in the file is Triangular, Trapezoid, or ''
            Parameters
            ----------  
                type: the type defined in the json file
            Raises
            ------
                InvalidMembershipException if the type is different.
        """   
        available_formats = ['Triangular', 'Trapezoid', '']
        if not type in available_formats: 
            return InvalidMembershipException()
        return True
    
    def generate_triangular_points(self, num_terms, init, end):
        """
            Generate 3 triangular points for each one of the terms knowing
            the universe of discourse

            Parameters
            ----------
                num_terms: number of terms the LV could take
                init: start of the universe of discourse
                end: end of the universe of discourse

        """   
        # Calculate the step
        step = (end - init) / (num_terms-1)
        # Generate points for each triangle
        points = []
        for i in range(0, num_terms):
            if i == 0:
                a = init
                b = init
                c = init + step
            elif i == num_terms:
                a = b
                b = end
                c = end
            else:
                a = b
                b = a + step
                c = b + step
            points.append((a, b, c))
        
        return points
    
    def generate_trapezoid_points(self, num_terms, init, end):
        """
            Generate 5 trapezoid points for each one of the terms knowing
            the universe of discourse

            Parameters
            ----------
                num_terms: number of terms the LV could take
                init: start of the universe of discourse
                end: end of the universe of discourse

        """   

        # Calculate the step
        step = (end - init) / num_terms
        c_value = step / num_terms
        
        # generar los puntos para cada trapecio
        points = []
        for i in range(0, num_terms):
            if i == 0: 
                a = init
                b = init
                c = b + c_value/2
                d = c + step
            elif i == num_terms-1: 
                a = c
                b = a + step
                c = end
                d = end
            else: 
                a = c
                b = d
                c = b+c_value
                d = c + step

            points.append((a, b, c, d))
        
        return points