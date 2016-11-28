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
           '\t/learn/ -- learn the class of a collection of vectors<br>' \
           '\t/guess/ -- Guess the class of a collection of vectors<br>'


@app.route('/learn', methods=['GET', 'POST'])
def learn():
    print "{} /learn".format(request.method)

    if request.method == 'GET':
        return react.learn_get()
        
    elif request.method == 'POST':
        true_class = float(request.get_json()['feature'])
        vector_dict = request.get_json()['vectors']
        
        print len(vector_dict)
        
        attr_vecs = []
        true_classes = []
        for url in vector_dict.keys():
            attr_vec = deepcopy([float(i) for i in vector_dict[url]])
            attr_vecs.append(attr_vec)
            true_classes.append(true_class)
        
        react.learn_post(attr_vecs, true_classes)
        
        data = {}
        
        data['success'] = True
        
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
            data[str(urls[i])] = img_classes[i].item()
            
        data["success"] = True        
        
        return json.dumps(data)
        
    else:
        return react.unknown_method('/guess')
        
        
class MismatchUrlToClassException(Exception):
        pass


if __name__ == '__main__':
    print 'Log::App:: Starting server'
    app.run(port=5002)
    print 'Log::App:: Server closing'
