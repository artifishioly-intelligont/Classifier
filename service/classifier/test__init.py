import unittest
import __init__ as classifier
import random
import os

class InitUnitTest(unittest.TestCase):

    def setUp(self):
        self.feature_table_csv = "TABLE_ENTRIES.csv"
        if(os.path.isfile(self.feature_table_csv)):
            os.remove(self.feature_table_csv)
            
        self.random_list_1 = []
        self.random_list_2 = []
        self.random_list = []
        max_value = 0
        min_value = 100
        self.svm = classifier.svm
        self.tab = classifier.tab

        # creating 1024 random float number which acts as feature attributes
        for i in range(0, 1024):
            self.random_list_1.append(random.uniform(min_value, max_value))
            self.random_list_2.append(random.uniform(min_value, max_value))
            
        self.random_list.append(self.random_list_1)
        self.random_list.append(self.random_list_2) 
        
    def test_learn(self):

        #given two 1024 float feature attributes as a list and true class which is a string
        self.random_list
        true_classes = ['TREE','TREE']

        #when attributes and true class fed into the learn method
        classifier.learn(self.random_list, true_classes)

    def test_guess(self):

        #given two 1024 feature attributes as a list
        self.random_list

        #when feature attributes are fed into guess method
        results, probabilities = classifier.guess(self.random_list)
        for result in results:
            bool = result in self.tab.feature_dictionary.values()
            
            # then it should return a class from within the class table and should be string
            self.assertEqual(bool, True)
            self.assertEqual(type(result) is str, True)    

if __name__ == '__main__':
    unittest.main()