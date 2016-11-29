import unittest
import table

class TableUnitTest(unittest.TestCase):

    def setUp(self):
        self.tab = table.FeatureTable(0, 100, {100: 'Pond', 200: 'Tree', 300: 'Park', 400: 'Pathway'})

    def test_find_name(self):

        #given a feature table, a feature value and a feature key
        dict = self.tab.feature_dictionary
        new_feature_value = 'CAR'
        new_feature_key = (len(dict) + 1) * self.tab.increment_number

        #when new feature value is added to the feature class table with its own new key.
        self.tab.feature_dictionary[new_feature_key] = new_feature_value

        # and same feature key fed into find_name method to gets class name as string
        result = self.tab.find_name(new_feature_key)

        #then result value should equal the new feature value which hold its original value
        self.assertEqual(result, new_feature_value)

        #deleting the value from the dictionary
        del self.tab.feature_dictionary[new_feature_key]

    def test_find_id(self):

        # given a feature table, a feature value and a feature key
        dict = self.tab.feature_dictionary
        new_feature_value = 'CAR'
        new_feature_key = (len(dict) + 1) * self.tab.increment_number

        #when new feature value is added to the feature class table with its own new key
        self.tab.feature_dictionary[new_feature_key] = new_feature_value

        #and new feature value fed into find_id method
        result_key = self.tab.find_id(new_feature_value)

        #then the result key should equal new feature key
        self.assertEqual(result_key, new_feature_key)

        # deleting the value from the dictionary
        del self.tab.feature_dictionary[new_feature_key]

    def test_add_feature(self):

        # given a feature table, a feature value and feature key
        dict = self.tab.feature_dictionary
        new_feature_value = 'CAR'
        new_feature_key = len(dict) * self.tab.increment_number

        # when new feature value is added to the feature class table
        result_bool = self.tab.add_feature(new_feature_value)

        #then the boolean result should be true
        self.assertEqual(result_bool, True)

        #then the value should contain in the feature table
        self.assertEqual(new_feature_value in self.tab.feature_dictionary.values(), True)

        #and when same value is added the boolean result should be false
        self.assertEqual(self.tab.add_feature(new_feature_value), False)

        # deleting the value from the dictionary
        del self.tab.feature_dictionary[new_feature_key]

    def test_get_all_feature(self):

        # given a feature table, a feature value and feature key
        dict = self.tab.feature_dictionary
        new_feature_value = 'car'
        new_feature_key = (len(dict) + 1) * self.tab.increment_number

        #when new feature class is added to the feature class table
        initial_table_length = len(self.tab.find_all_features())
        self.tab.feature_dictionary[new_feature_key] = new_feature_value
        new_table_length = len(self.tab.find_all_features())

        #then the length of the feature class table should increment by 1
        self.assertEqual(new_table_length, (initial_table_length + 1))

        # deleting the value from the dictionary
        del self.tab.feature_dictionary[new_feature_key]

if __name__ == "__main__":
    unittest.main()