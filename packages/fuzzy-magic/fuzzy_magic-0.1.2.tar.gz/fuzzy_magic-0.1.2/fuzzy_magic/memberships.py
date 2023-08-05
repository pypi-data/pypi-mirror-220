from .exceptions import *
from simpful import *
import json

"""
    1. Count how many points. 
        - make_triangular works with 3.
        - make_trapezoid needs 5
    2. Send it to the LV.
"""

class MembershipFunction(): 
    
    def make_triangular(points, term):
        """
            Creation of a triangular membership functions using simpful methods
            Parameters
            ----------
                points: array of three points to create the function
                term: name of the term
            Raises
            ------
                InvalidPointsArray
        """   
        try: 
            return TriangleFuzzySet(points[0], points[1], points[2], term)
        except: 
            raise InvalidPointsArray(3)
        
    def make_trapezoid(points, term):
        """
            Creation of a trapezoid membership functions using simpful methods
            Parameters
            ----------
                points: array of five points to create the function
                term: name of the term
            Raises
            ------
                InvalidPointsArray
        """
        try: 
            return TrapezoidFuzzySet(points[0], # a  
                                 points[1], # b
                                 points[2], # c
                                 points[3], # d
                                 term)
        except: 
            raise InvalidPointsArray(5)
