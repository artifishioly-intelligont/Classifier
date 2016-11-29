
class FeatureTable:

    feature_dictionary = None

    def __init__(self, start, increment_number, initital_entries):
        self.start = start
        self.increment_number = increment_number
        self.feature_dictionary = initital_entries


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

        if len(self.feature_dictionary) > 0:
            store_features = self.feature_dictionary.values()

        return store_features

    def add_feature(self, feature_name):
        n = len(self.feature_dictionary)
        msg = True

        msg = feature_name.upper() in self.feature_dictionary.values()

        if n == 0:
            self.feature_dictionary[1 * self.increment_number] = feature_name.upper()
            print 'Added'
            msg = True
        else:
            if not msg:
                self.feature_dictionary[(n + 1) * self.increment_number] = feature_name.upper()
                print 'Added'
                msg = True
            else:
                print 'Already Exist'
                msg = False

        return msg

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