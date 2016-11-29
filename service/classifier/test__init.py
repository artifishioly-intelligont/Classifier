import unittest
import __init__ as classifier
import random

class InitUnitTest(unittest.TestCase):

    def setUp(self):
        self.random_list = []
        max_value = 0
        min_value = 100
        self.perceptron = classifier.perceptron
        self.tab = classifier.tab

        # creating 1024 random float number which acts as feature attributes
        for i in range(0, 1024):
            self.random_list.append(random.uniform(min_value, max_value))

    def test_guess(self):

        #given 1024 feature attributes as a list
        self.random_list

        #when feature attributes are fed into guess method
        before_weight = self.perceptron.weights[:]
        result = classifier.guess(self.random_list)
        bool = result in self.tab.feature_dictionary.values()

        # then it should return a class from within the class table and should be string
        # also the perceptron weight should not change
        self.assertEqual(bool, True)
        self.assertEqual(type(result) is str, True)
        self.assertEqual(self.perceptron.weights, before_weight)

    def test_learn(self):

        #given 1024 float feature attributes as a list and true class which is a string
        self.random_list
        true_class = 'POND'

        #when attributes and true class fed into the learn method
        before_weight = self.perceptron.weights[:]
        classifier.learn(self.random_list, true_class)

        #then the weights of the perceptron should change as it learns
        self.assertNotEqual(self.perceptron.weights, before_weight)

if __name__ == '__main__':
    unittest.main()