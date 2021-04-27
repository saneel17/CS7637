from itertools import combinations
from collections import defaultdict
import time


class MonsterDiagnosisAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, diseases, patient):
        # Add your code here!
        #
        # The first parameter to this method is a list of diseases, represented as a
        # list of 2-tuples. The first item in each 2-tuple is the name of a disease. The
        # second item in each 2-tuple is a dictionary of symptoms of that disease, where
        # the keys are letters representing vitamin names ("A" through "Z") and the values
        # are "+" (for elevated), "-" (for reduced), or "0" (for normal).
        #
        # The second parameter to this method is a particular patient's symptoms, again
        # represented as a dictionary where the keys are letters and the values are
        # "+", "-", or "0".
        #
        # This method should return a list of names of diseases that together explain the
        # observed symptoms. If multiple lists of diseases can explain the symptoms, you
        # should return the smallest list. If multiple smallest lists are possible, you
        # may return any sufficiently explanatory list.
        c_diseases = []
        length = len(diseases) + 1
        if length > 7:
            length = 7
        for x in range(1, length):
            for p in combinations(diseases, x):
                c_diseases.append(p)

        new_dict1 = {}
        for i in c_diseases:
            subdict = {x: diseases[x]
                       for x in i if x in diseases}
            list_of_dics = [value for value in subdict.values()]
            result = {key: tuple(d.get(key) for d in list_of_dics)
                      for key in set().union(*list_of_dics)}
            print(result)
            new_dict2 = {}
            for j in result:
                value = result.get(j)
                count = self.count(value)
                new_dict2[j] = count
            new_dict1[i] = new_dict2

        for key, value in new_dict1.items():
            if patient == value:
                return list(key)

    def count(self, tuple):
        positive = tuple.count('+')
        negative = tuple.count('-')

        if positive > negative:
            return "+"
        elif negative > positive:
            return "-"
        else:
            return "0"

            '''
        z = new_dict1.get(('Alphaitis', 'Betatosis'))
        shared_items = {k: z[k]
                        for k in z if k in patient and z[k] == patient[k]}
        
        print(z)
        print(patient)
        print(shared_items)
        print(len(shared_items))
        '''
