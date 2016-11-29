import classifier
import json
import cgi

svm = classifier.svm
tab = classifier.tab

def unknown_method(endpoint):
    return "<h1>Incorrect Usage</h1> \
    <br> {} does not know what to do with this request type".format(endpoint)


def learn_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/learn only accepts POST\
    <br>POST expects a number of image files to be sent to it\
    <br>\
    <br>The return is JSON response of the images that failed, fail messages and the overall sucess\
    <br>Note: If one image fails the overall success is False\
    <br>Example Return:\
    <br>{\
    <br>  'success' : True\
    <br>  'failed_images' : []\
    <br>  'failed_messages' : []\
    <br>} "


def guess_get():
    return "<h1>Incorrect Usage</h1>\
    <br>/guess only accepts POST\
    <br>POST expects a number of image files to be sent to it"


def learn_post(attr_vecs, true_classes):
    return classifier.learn(attr_vecs, true_classes)


def guess_post(attr_vecs):
    return classifier.guess(attr_vecs)

    
def get_all_features():
    print 'Log::Classifier::Message Recieved::/features/'
    features_name_list = tab.find_all_features()
    data = {}

    if len(features_name_list) > 0:
        data['success'] = True
        data['features'] = features_name_list
    else:
        data['success'] = False
        data['features'] = 'No Feature Recorded.'

    return json.dumps(data)

"""
An endpoint to add a new feature to the list

ACCESS: GET

Return: ??success or failure??
"""
def add_new_feature(new_feature):
    print 'Log::Classifier::Message Recieved::/features/<new_feature>'
    msg = tab.add_feature(cgi.escape(new_feature))
    data = {}

    if msg:
        data['success'] = True
        data['message'] = "'" + cgi.escape(new_feature) + "' added."
    else:
        data['success'] = False
        data['message'] = "'" + cgi.escape(new_feature) + "' already exists."

    return json.dumps(data)
