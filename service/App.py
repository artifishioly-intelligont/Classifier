from flask import Flask, request
import AppReactions as react
import SVM as SVM
from copy import deepcopy

app = Flask(__name__)

@app.route('/')
def show_endpoints():
    print "{} /".format(request.method)
    return 'Endpoints: <br>' \
           '\t/ -- List All Endpoints<br>' \
           '\t/learn/ -- learn the class of a collection of vectors<br>' \
           '\t/guess/ -- Guess the class of a collection of vectors<br>'


@app.route('/learn')
def learn():
    print "{} /learn".format(request.method)

    if request.method == 'GET':
        return react.learn_get()
        
    elif request.method == 'POST':
        true_class = request.form['feature']
        vector_dict = request.get_json['vectors']
        
        attr_vecs = []
        true_classes = []
        for url in vector_dict.keys():
            attr_vec = deepcopy(vector_dict[url])
            attr_vecs.append(attr_vec)
            true_classes.append(true_class)
        
        return react.learn_post(attr_vecs, true_classes)
        
    else:
        return react.unknown_method('/learn')


@app.route('/guess')
def guess():
    print "{} /guess".format(request.method)

    if request.method == 'GET':
        return react.guess_get()
    elif request.method == 'POST':
        return react.guess_post()
    else:
        return react.unknown_method('/guess')


if __name__ == '__main__':
    print 'Log::App:: Starting server'
    app.run()
    print 'Log::App:: Server closing'
