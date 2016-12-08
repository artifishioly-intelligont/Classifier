from copy import deepcopy
import csv
import os
from itertools import izip


class FeatureTable:

    feature_dictionary = None

    def __init__(self, start=0, increment_number=100, initial_entries={100 : 'building', 200 : 'house', 300 : 'road', 400 : 'tree'}):
        self.csv_file = "TABLE_ENTRIES.csv"
        self.start = start
        self.increment_number = increment_number    
        self.feature_dictionary = {}
        self.default_entries = initial_entries
        
        # Opens the csv file if it exists, and extracts its contents into feature_dictionary
        if(os.path.isfile(self.csv_file)):
            try:
                with open(self.csv_file) as myfile:
                    csvread = csv.reader(myfile)
                    for row in csvread:
                        self.feature_dictionary[int(row[0])] = row[1]
                # If any of the entries in initial_entries are somehow missing, add them now
                for id,name in initial_entries.items():
                    if str(id) not in self.feature_dictionary.keys():
                        self.feature_dictionary[id] = name
                    
            except IOError:
                print "Could not open " + self.csv_file
                self.feature_dictionary = initial_entries
        # If it doesn't exist, just use the initial_entries
        else:
            self.feature_dictionary = initial_entries


    def find_id(self, feature_name):
        cls = None
        for k, v in self.feature_dictionary.items():
            if feature_name.upper() == v.upper():
                cls = float(k)
                break

        return cls

    def find_name(self, dbl_id):

        id = min(self.feature_dictionary, key=lambda x: abs(x - dbl_id))

        if self.feature_dictionary.has_key(id):
            cls = self.feature_dictionary.get(id)
        else:
            cls = None

        return cls

    def find_all_features(self):
        store_features = []
        count = 0

        for id in sorted(self.feature_dictionary.keys()):
            store_features.append(self.feature_dictionary[id])

        return store_features

    def add_feature(self, feature_name):
        n = len(self.feature_dictionary)
        msg = True

        msg = feature_name.lower() in [feature.lower() for feature in self.feature_dictionary.values()]

        if n == 0:
            self.feature_dictionary[1 * self.increment_number] = feature_name.lower()
            print 'Added'
            msg = True
        else:
            if not msg:
                self.feature_dictionary[(n + 1) * self.increment_number] = feature_name.lower()
                print 'Added'
                msg = True
            else:
                print 'Already Exists'
                msg = False

        return msg
    
    
    def save(self):        
        ids = deepcopy(sorted(self.feature_dictionary.keys()))
        names = []

        for id in ids:
            names.append(deepcopy(self.feature_dictionary[id]))
        
        # Save it locally
        with open(self.csv_file, 'wb') as f:
            wtr = csv.writer(f, delimiter= ',')
            wtr.writerows(izip(ids, names))
            
    def clear_entries(self):
        self.feature_dictionary = {}
    
    def reset_entries(self):
        self.feature_dictionary = self.default_entries
        
    def __del__(self):
        self.save()

if __name__ == "__main__":

    t = FeatureTable(1, 100)

    t.add_feature('pond')
    t.add_feature('pen')
    t.add_feature('chalk')

    print t.find_all_features()

    print t.find_id('pen')
    print t.find_name(100)
    print t.find_name(200)
    print t.find_name(600)

    print t.find_name(230)