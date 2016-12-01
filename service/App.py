from flask import Flask, request
import AppReactions as react
from copy import deepcopy
import json

app = Flask(__name__)

@app.route('/')
def show_endpoints():
    print "{} /".format(request.method)
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/learn -- learn the class of a collection of vectors<br>' \
           '\t/guess -- Guess the class of a collection of vectors<br>' \
           '\t/features -- Returns all features currently known to the SVM<br>' \
           '\t/features/{new_feature} -- Adds {new feature} to the list of features<br>' 
           


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    print "{} /learn".format(request.method)

    if request.method == 'GET':
        return react.learn_get()
        
    elif request.method == 'POST':
        true_class = request.get_json()['theme']
        vector_dict = request.get_json()['vectors']
        
        attr_vecs = []
        true_classes = []
        for url in vector_dict.keys():
            # looks up the attribute vector matching the url in the dictionary, 
            # converts each attribute to a float, and creates a deepcopy
            attr_vec = deepcopy([float(i) for i in vector_dict[url]])
            attr_vecs.append(attr_vec)
            true_classes.append(true_class)
        
        success = react.learn_post(attr_vecs, true_classes)
        
        data = {}
        
        data['success'] = success
        
        return json.dumps(data)
        
    else:
        return react.unknown_method('/learn')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    print "{} /guess".format(request.method)

    if request.method == 'GET':
        return react.guess_get()
        
    elif request.method == 'POST':
        vector_dict = request.get_json()['vectors']
        
        urls = vector_dict.keys()
        attr_vecs = []
        
        for url in urls:
            # looks up the attribute vector matching the url in the dictionary, 
            # converts each attribute to a float, and creates a deepcopy
            attr_vec = deepcopy([float(i) for i in vector_dict[url]])
            attr_vecs.append(attr_vec)
            
        img_classes, img_probas = react.guess_post(attr_vecs)
        
        data = {}
        
        try:
            if len(urls) != len(img_classes):
                raise MismatchUrlToClassException("Received %d urls but computed %d classes. Check classifier has sufficient data to predict." % (len(urls), len(img_classes)))              
        except MismatchUrlToClassException as e:
            print e
            data["success"] = False
            return json.dumps(data)
        
        for i in range (0, len(urls)):
            data[str(urls[i])] = img_classes[i]
            
        data["success"] = True        
        
        return json.dumps(data)
        
    else:
        return react.unknown_method('/guess')
        
        
"""
An endpoint used to fill the class drop down in the GUI

Access: GET

Return:	- classes - An array of strings (classes)
"""
@app.route('/features')
def get_all_features():
    return react.get_all_features()
    

"""
An endpoint to add a new feature to the list

ACCESS: GET

Return: ??success or failure??
"""
@app.route('/features/<new_feature>')
def add_new_feature(new_feature):
    return react.add_new_feature(new_feature)
        
        
class MismatchUrlToClassException(Exception):
        pass


if __name__ == '__main__':
    print 'Log::App:: Starting server'
    app.run(port=5002)
    print 'Log::App:: Server closing'
