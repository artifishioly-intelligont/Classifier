import SVM, table as Table

svm = SVM.SVM()
tab = Table.FeatureTable()

def guess(attr_vecs):
    """
    Guesses which class the sub-images belong to.

    e.g. Given an image it could return 'tree'

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :return: The name of the class the classifier believes the sub-image belongs to
    """
    
    prediction_ids, probabilities = svm.predict(attr_vecs)
    prediction_names = []
    
    for i in range(0, len(prediction_ids)):
        prediction_names.append(tab.find_name(prediction_ids[i]))
    
    return prediction_names, probabilities


def learn(attr_vecs, true_class_names):
    """
    Trains the SVM on an array of attribute vectors and their corresponding class names

    :param attr_vec: The long list of numerical representations of the attributes extracted (by olivia module) of a sub-image
    :param true_class: The class that the sub-image belongs to
    :return: {1,2,3} depending on state
    """
    true_class_ids = []
    
    for i in range(0, len(true_class_names)):
        id = tab.find_id(true_class_names[i])
        if id:
            true_class_ids.append(id)
        else:
            print "Classifier::log::Error: Unrecognised class name: " + true_class_names[i] + ". Aborting."
            return False
    
    return svm.learn(attr_vecs, true_class_ids)
    
    
def clear_memory():
    ready = svm.clear_memory()
    # If the SVM is not ready, it has cleared all its knowledge, so do the same in table
    tab.clear_entries()
        
    return ready
    
def reset_memory():
    ready, message = svm.reset_memory()
    if ready:
        tab.reset_entries()
    else:
        tab.clear_entries()
        
    return ready, message