import numpy as np
import csv
from sklearn import svm
from copy import deepcopy


class SVM:

	lin_clf = None
	csv_file = None
	
	X = []
	Y = []
	
	fitted = False

	def __init__(self, seed_csv="VECTOR_DATA.csv"):
	
		self.lin_clf = svm.SVC(kernel='linear',probability=True)
		self.csv_file = seed_csv
		
		try:
			with open(seed_csv) as myfile:
				csvread = csv.reader(myfile)
				for row in csvread:
					x = []
					for val in row[1:]:
						x.append(float(val))
					self.X.append(x)
					self.Y.append(float(row[0]))
				
				try:
					self.safe_fit()
				except self.InsufficientDataForFitException as e:
					print e
				
		except IOError:
			open(seed_csv, 'a')
			print "File '" + seed_csv + "' doesn't exist. Creating it."
			
		if len(self.X) != len(self.Y):
			raise self.MismatchedTrainingDataException('Vector set and Class set are different lengths')	
	
	"""
	:function
			learn
	:param	
			input_vectors: an array of attribute vectors
			true_values: an array of corresponding classes
	:return 
			None
	:description
			Fits the SVM based on the data provided, and all 
			previous data used.
	"""
	def learn(self, input_vectors, true_values):	
	
		if(len(input_vectors) != len(true_values)):
			raise self.MismatchedTrainingDataException("Number of attribute vectors doesn't match number of true values")
		
		for i in range(len(input_vectors)):
			self.X.append(input_vectors[i])
			self.Y.append(true_values[i])
		
		try:
			self.safe_fit()
		except self.InsufficientDataForFitException as e:
				print e
	
	"""
	:function
			predict
	:param	
			input_vectors: an array of attribute vectors
	:return
			predictions: an array of predicted classes for each vector
			probabilities: a 2d array containing the probabilities of each
					vector belonging to each class
	:description
			Predicts the classes of all vectors provided, and returns 
			the probabilities to show how confident the SVM is
	"""
	def predict(self,input_vectors):
	
		predictions = []
		probabilities = []
	
		for i in range(len(input_vectors)):
			try:
				pred, prob = self.safe_predict(input_vectors[i])
				if(pred.any() and prob.any()):
					predictions.append(pred)
					probabilities.append(prob)
			except self.UnableToPredictException as e:
				print e
			
		return predictions, probabilities
		
		
	"""
	:function
			safe_fit
	:param	
			None
	:return
			None
	:description
			A safe version of the SVC fit function. Ensures that there are
			at least 2 different classes in the training data before fitting.
	"""
	def safe_fit(self):
		if len(set(self.Y)) >= 2:
			self.lin_clf.fit(self.X, self.Y)
			self.fitted = True
		else:
			raise self.InsufficientDataForFitException("Unable to fit: Currently only trained for %d class(es) - fit function requires at least 2" % (len(set(self.Y))))
	
	
	"""
	:function
			safe_predict
	:param	
			input_vector: a single attribute vector to be predicted
	:return
			Returns a tuple containing the predicted class of the vector
			and an array of the probabilities of it belonging to all other classes
	:description
			A safe version of the SVC predict function. Ensures the SVM has
			been fit before attempting to predict.
	"""
	def safe_predict(self, input_vector):
		if self.fitted:
			return self.lin_clf.predict(np.array([input_vector])), self.lin_clf.predict_proba(np.array([input_vector]))
		else:
			raise self.UnableToPredictException("Unable to predict: SVM has not been fitted")
			return None, None
		
	"""
	:function
			save
	:param	
			None
	:return
			None
	:description
			Saves the data currently used to train the SVM to a csv file,
			in the form [class_id, attr1, attr2, attr3,...,attr1024]
	"""	
	def save(self):
		data = deepcopy(self.X)
		# Add the true_value as the first item of every entry
		for i in range(len(data)):
			data[i] = [self.Y[i]] + list(data[i])
		# Save it locally
		with open(self.csv_file, 'wb') as f:
			wtr = csv.writer(f, delimiter= ',')
			wtr.writerows(data)

		
	def __del__(self):
	
		self.save()
		
	class MismatchedTrainingDataException(Exception):
		pass

	class InsufficientDataForFitException(Exception):
		pass	
		
	class UnableToPredictException(Exception):
		pass	
		
"""
# An example / test of how to use these functions. Requires a table of attribute vectors and their classes
if __name__ == "__main__":
	s = SVM()
	#test_array_1 is whatever 400 is...
	test_array_1 = [0.33326, 0.00000, 0.75381, 0.89670, 0.02223, 0.00000, 0.10488, 0.00488, 0.00000, 0.00000, 0.00000, 0.94988, 0.00000, 0.00000, 0.27462, 0.25323, 0.00000, 0.00000, 0.62393, 0.24872, 0.00000, 1.19744, 0.00000, 0.00000, 0.00000, 0.00000, 0.79234, 0.00000, 0.00000, 1.09947, 0.00000, 0.00000, 1.33734, 0.00000, 0.69351, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.05095, 0.00000, 0.00000, 0.30186, 0.00000, 0.13331, 0.11087, 0.83408, 0.00000, 0.00000, 0.00000, 0.27116, 0.88524, 0.00000, 0.87102, 0.00000, 0.00000, 0.02488, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.81304, 0.00000, 1.06466, 1.07204, 0.00000, 0.00000, 0.00000, 0.00000, 0.30243, 0.76263, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.13485, 0.00000, 0.63721, 0.66755, 0.00000, 0.00000, 0.00000, 0.29270, 0.00000, 0.57555, 0.96087, 0.00000, 0.00000, 0.37980, 0.61860, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.33558, 0.00000, 0.00000, 0.00000, 1.83317, 0.52524, 0.00000, 0.00000, 0.02904, 0.00000, 0.86578, 0.00000, 1.34316, 0.11639, 0.00000, 0.00000, 0.00000, 1.84545, 0.00000, 0.25532, 0.00000, 0.02608, 0.00000, 0.00000, 0.69548, 0.71984, 0.69700, 0.34689, 0.61029, 0.94369, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.03809, 1.19569, 0.00000, 0.00000, 1.28407, 0.00000, 0.00000, 0.00000, 0.00000, 0.64483, 1.01437, 0.00000, 0.00000, 0.12578, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.33201, 0.00000, 0.00000, 0.00000, 0.41464, 0.35880, 0.02451, 0.00000, 1.21737, 0.00000, 0.00000, 0.00000, 0.00000, 0.08635, 0.00000, 0.00000, 1.28713, 0.01230, 0.83346, 0.00000, 0.00000, 0.13934, 0.00000, 0.00000, 0.31494, 0.00000, 1.39669, 0.00000, 1.03947, 0.64399, 0.00000, 0.00000, 0.00000, 1.00272, 0.00000, 1.33304, 0.00000, 0.00000, 1.18542, 0.00000, 0.29004, 0.00000, 0.00000, 0.01586, 0.09614, 0.00000, 0.00000, 0.18806, 0.00000, 0.10605, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.41785, 0.00000, 0.00000, 0.01590, 0.06401, 0.00000, 0.00000, 0.00000, 0.91324, 0.00000, 1.56986, 0.00000, 0.00000, 0.00000, 0.00000, 0.71779, 0.57728, 0.00000, 0.43498, 0.75372, 0.09479, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.99652, 0.00000, 0.69125, 0.00000, 0.00000, 0.25701, 0.00000, 0.00000, 0.00000, 0.03598, 0.00000, 0.00000, 0.00652, 0.73438, 0.00000, 0.00000, 1.04913, 0.00000, 0.54049, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.22221, 0.88981, 0.00000, 0.00000, 0.00000, 0.63726, 0.00000, 0.62216, 1.09613, 0.00000, 0.00000, 0.45891, 0.24805, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.94641, 0.00000, 0.00000, 0.63170, 0.23496, 0.00000, 0.00000, 0.00000, 0.00000, 0.90622, 0.00000, 0.00000, 0.46444, 0.01901, 0.00000, 0.00000, 0.00000, 0.00000, 0.08419, 0.23158, 0.00000, 0.24176, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.17683, 0.55776, 0.12953, 0.00000, 0.00000, 0.37734, 0.00000, 0.00000, 0.69574, 0.00000, 0.67404, 0.00000, 0.00000, 0.00000, 0.29372, 0.00000, 0.00000, 0.70405, 0.00000, 0.00000, 0.00000, 0.71464, 0.00000, 0.83030, 0.00000, 0.00000, 0.00000, 0.00000, 0.87097, 0.00607, 0.00000, 0.00000, 0.00000, 0.00000, 0.92438, 0.53444, 0.00000, 0.00000, 0.00000, 0.57285, 0.00000, 0.00000, 0.00000, 0.65175, 1.30970, 0.39596, 0.00000, 0.68540, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.39530, 0.00000, 0.00000, 0.00000, 0.00000, 1.54842, 1.42240, 0.00000, 0.22893, 0.93387, 0.00000, 0.00000, 0.59209, 0.00000, 0.00000, 0.00000, 0.51952, 0.00000, 0.00000, 1.16472, 0.00000, 0.00000, 0.00000, 0.57985, 0.00000, 0.94704, 0.36309, 0.78555, 0.00000, 0.44993, 0.00000, 0.00000, 0.00214, 0.00000, 0.77474, 0.00000, 0.49985, 0.00000, 0.17409, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.42356, 0.22835, 0.43602, 0.35751, 0.00000, 0.00000, 0.00000, 0.30446, 0.18871, 0.00000, 0.00000, 0.56213, 0.00000, 0.54119, 0.64610, 0.00000, 1.00797, 0.00000, 0.00000, 0.00000, 0.00000, 1.26712, 0.32461, 0.00000, 0.00000, 0.00000, 0.25491, 0.00000, 0.00000, 0.00000, 0.00480, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.74669, 0.84178, 0.00000, 0.00000, 0.43303, 0.00000, 0.00000, 0.00000, 1.33137, 0.67979, 0.23323, 0.00000, 1.63376, 0.00000, 0.38887, 0.00000, 0.00000, 1.10377, 0.00000, 0.00000, 0.00000, 0.70958, 0.00000, 0.20156, 0.00000, 0.00000, 1.97232, 0.00000, 0.00000, 0.25781, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.79607, 0.00000, 0.92952, 0.00000, 0.20567, 0.00000, 0.00000, 0.00000, 0.49112, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.79786, 0.00000, 0.90893, 0.00000, 0.00000, 0.66412, 0.00000, 0.00000, 0.00000, 1.06814, 0.00000, 0.29951, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.31704, 1.17290, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.13335, 0.00000, 0.00000, 0.07770, 0.00000, 0.51672, 0.74074, 0.00000, 0.00000, 0.89798, 0.23254, 0.82505, 0.00000, 0.00000, 0.44567, 0.00000, 0.00000, 0.42454, 0.61125, 0.83790, 0.00000, 0.00000, 0.90113, 0.00000, 1.09449, 0.19664, 0.00000, 0.32484, 0.00000, 0.55264, 0.00000, 0.74892, 0.00000, 0.00000, 0.46041, 0.00000, 0.28054, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.00460, 0.00000, 2.06463, 0.66151, 0.00000, 0.00000, 0.00000, 0.62124, 0.85195, 1.20239, 0.07451, 0.00000, 0.55597, 0.00000, 0.00000, 0.73451, 0.17281, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.04920, 0.00000, 0.00000, 0.00000, 0.72105, 0.00000, 0.00000, 1.07274, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.45835, 0.86905, 0.00000, 1.19789, 0.00000, 0.48600, 0.00000, 0.00000, 0.00000, 0.00000, 0.68319, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.24375, 0.00000, 0.00000, 1.21635, 0.00000, 0.15667, 0.89989, 0.00000, 0.38339, 1.04251, 0.28592, 0.00000, 0.00000, 1.04031, 1.19296, 0.62981, 0.29263, 0.00000, 0.13843, 0.00000, 0.00000, 0.01493, 0.00000, 0.93621, 0.00000, 0.00000, 0.39039, 0.53628, 0.00000, 0.00000, 0.00000, 0.72982, 0.47678, 2.01175, 0.00000, 0.33116, 0.28584, 0.13515, 0.00000, 0.00000, 1.18437, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.17167, 0.00000, 0.00000, 0.00000, 0.71042, 0.98899, 0.00000, 0.85815, 0.00000, 0.00000, 0.90721, 0.00000, 0.00000, 0.00000, 0.10411, 0.33700, 0.00000, 0.00000, 0.86243, 0.00000, 0.51819, 0.00000, 0.00000, 0.42018, 0.14901, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.88983, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.01452, 0.36591, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.41448, 0.00000, 1.61496, 0.00000, 0.35559, 0.99291, 0.00000, 0.00000, 0.00000, 0.00544, 0.06733, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.10870, 1.41049, 0.00000, 0.75465, 0.00000, 0.36594, 0.09592, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.63856, 0.00000, 0.69956, 0.04071, 0.00000, 1.64973, 0.72604, 0.07219, 0.00000, 0.47419, 0.04340, 1.11205, 0.00000, 0.00000, 0.56005, 0.00000, 0.00000, 0.00000, 0.00000, 0.05538, 0.00000, 1.20361, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.67016, 0.32938, 0.00000, 0.00000, 0.00000, 0.51174, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.37276, 0.89077, 0.00000, 0.00000, 0.44372, 0.00000, 0.00000, 0.00000, 0.43139, 0.00000, 0.41744, 0.00000, 1.28495, 0.77272, 0.00000, 0.74516, 0.00000, 0.00000, 0.26542, 0.43637, 0.00000, 0.00000, 0.07239, 0.00000, 0.14099, 0.00000, 0.00000, 0.00000, 0.00000, 0.06574, 0.00000, 0.00000, 0.00000, 0.11374, 0.00000, 0.00000, 1.45524, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.50942, 0.10072, 0.60963, 0.27902, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.40381, 0.00000, 0.89711, 1.39208, 0.84449, 0.00000, 0.75746, 0.00000, 0.00000, 0.00000, 0.37493, 0.00000, 0.00000, 0.00000, 0.00000, 0.71090, 0.00000, 0.00000, 0.01530, 0.00000, 0.00000, 0.29815, 0.00000, 0.02845, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.05742, 0.09676, 0.07748, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.73891, 1.93554, 0.22141, 0.03303, 0.74237, 1.48096, 1.04175, 0.11679, 0.00000, 0.00000, 0.23399, 0.00000, 1.35937, 0.00000, 0.59279, 0.00000, 0.00000, 0.00000, 0.72307, 0.93800, 0.00000, 0.00000, 0.41947, 0.00000, 0.08374, 0.05387, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.91725, 0.59553, 0.00000, 0.66699, 0.00000, 0.50420, 0.00000, 0.00000, 0.80289, 0.70942, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.06241, 0.00000, 0.00000, 0.00000, 0.00000, 0.52157, 0.00000, 0.26129, 2.84335, 0.00000, 0.00000, 0.00000, 0.20395, 0.33490, 0.75374, 0.00000, 0.99310, 0.93934, 0.00000, 0.00000, 0.00000, 1.87862, 0.00000, 0.91199, 0.00000, 0.00000, 0.80176, 1.14207, 0.50336, 0.07652, 0.05374, 0.16737, 0.00000, 0.00000, 0.00000, 0.65767, 0.00000, 0.00000, 0.00000, 0.00000, 0.62004, 2.31215, 0.00000, 0.24659, 0.42006, 0.96491, 0.71585, 0.00000, 0.75319, 0.00000, 0.55629, 1.20366, 0.00000, 0.00000, 0.94735, 2.03909, 0.14746, 0.00000, 0.00000, 0.00000, 0.00000, 1.52151, 0.00000, 0.09780, 0.00000, 0.00000, 0.00000, 0.45130, 0.00000, 0.00000, 0.59088, 0.00000, 0.00000, 0.04043, 1.91514, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.71805, 0.99144, 0.00000, 0.41939, 1.21752, 0.77823, 0.00000, 0.57640, 1.73883, 0.00000, 1.17343, 0.00000]
	print s.predict([test_array_1])
	
	
	#test_array_2 is a building (100)
	test_array_2 = [0.00000, 0.00000, 1.60835, 1.10371, 0.84623, 0.00000, 0.00000, 1.24427, 0.00000, 0.00000, 2.11816, 0.00000, 0.00000, 0.58096, 0.46415, 0.12998, 0.00000, 0.22069, 2.10195, 1.05729, 0.00000, 0.00000, 1.19500, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.42405, 0.00000, 0.00000, 0.00000, 2.22057, 0.00000, 1.58705, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 3.48604, 0.00000, 0.00000, 0.00000, 1.80627, 0.00000, 2.88351, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 4.85293, 0.00000, 0.65454, 0.00000, 1.09351, 0.00000, 0.00000, 0.00000, 0.00000, 2.26001, 0.00000, 0.00000, 0.54577, 0.00000, 2.71236, 0.00000, 0.00000, 0.00000, 1.33979, 2.51255, 0.18886, 0.00000, 0.24386, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 2.18889, 0.66810, 0.00000, 0.00000, 0.00000, 4.10682, 0.35955, 0.00000, 0.05971, 0.00000, 0.19949, 0.69164, 0.13437, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.95849, 0.15296, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 4.47027, 2.15941, 0.71468, 0.00000, 0.00000, 0.00000, 1.91359, 0.00000, 3.65096, 0.05096, 0.00000, 0.00000, 0.00000, 5.55085, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.23570, 0.33639, 0.76696, 0.00000, 0.00000, 3.53920, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.75508, 0.00000, 0.00000, 0.21994, 2.88344, 2.79306, 1.10997, 0.00000, 1.22958, 0.15891, 0.00000, 0.00000, 0.00000, 0.86592, 0.54415, 0.00000, 0.00000, 0.72476, 0.00000, 0.00000, 1.65393, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.67334, 0.00000, 0.00000, 0.00000, 3.86608, 1.23796, 0.00000, 2.29010, 1.01097, 0.00000, 0.00000, 0.00000, 2.92722, 0.00000, 2.31840, 0.00000, 0.00000, 3.19271, 0.00000, 0.00000, 2.13961, 0.00000, 4.27634, 0.00000, 3.42981, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.58524, 6.56188, 0.00000, 0.00000, 4.92786, 0.00000, 0.00340, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 2.31455, 0.42689, 0.10483, 0.00000, 0.00000, 0.00000, 0.01127, 2.91334, 3.37055, 0.00000, 0.00000, 0.00000, 0.37340, 1.58775, 0.00000, 0.00000, 1.98841, 0.00000, 4.87231, 0.00000, 0.00000, 0.00000, 0.86897, 4.34866, 0.00000, 0.00000, 0.00000, 0.70476, 0.00000, 0.00000, 0.00000, 0.00000, 2.03115, 0.00000, 0.00000, 0.37148, 0.21525, 0.00000, 0.00000, 0.55852, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.86104, 0.72614, 0.00000, 0.00000, 0.00000, 3.41683, 0.00000, 0.00000, 2.22587, 0.00000, 0.00000, 0.05292, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.37487, 0.46607, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.56367, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.54889, 0.00000, 0.00000, 2.07759, 0.00000, 0.80927, 3.05446, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.46321, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.35264, 0.00000, 0.00000, 0.00000, 1.02323, 0.00000, 3.10320, 0.00000, 0.00000, 0.00000, 0.00000, 2.24888, 0.00000, 0.00000, 0.83398, 0.00000, 0.00000, 1.50630, 0.00000, 0.00000, 1.51804, 0.63947, 2.71583, 1.07015, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.12575, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 2.61837, 0.56082, 0.42906, 0.00000, 0.96234, 0.18045, 0.00000, 0.00000, 0.00000, 0.40001, 0.00000, 0.00000, 0.00000, 0.59290, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.13024, 6.48536, 5.21934, 0.00000, 0.85864, 0.72981, 0.00000, 0.00000, 0.90945, 0.00000, 0.00000, 1.00271, 1.46227, 0.00000, 0.00000, 3.05847, 0.00000, 0.00000, 0.00000, 0.74770, 0.00000, 0.00000, 2.01122, 0.00000, 0.00000, 0.05127, 0.00000, 0.00000, 1.55694, 0.00000, 0.00000, 1.49636, 0.00000, 0.00000, 1.08484, 1.07026, 0.00000, 0.00000, 0.79359, 0.00000, 0.00000, 0.00000, 0.12083, 0.00000, 0.24859, 0.00000, 0.00000, 0.00000, 0.00000, 2.77140, 0.00000, 0.00000, 0.00000, 2.77467, 0.00000, 0.00000, 3.36497, 1.20917, 1.49109, 0.65546, 0.00000, 0.00000, 0.00000, 5.53000, 0.00000, 0.00000, 0.67827, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 2.96290, 0.00000, 3.80427, 4.48791, 0.00000, 0.00000, 0.00000, 0.13349, 0.09168, 0.00000, 3.80902, 3.18059, 0.00000, 1.01890, 4.27628, 0.00000, 1.05295, 1.38448, 1.19006, 4.75543, 1.44791, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.19287, 4.61823, 0.00000, 0.00000, 0.70436, 0.27775, 1.72898, 0.00000, 0.86945, 0.00000, 0.00000, 0.00000, 2.97624, 0.15372, 0.96534, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.34450, 0.00000, 2.23094, 0.02463, 1.67346, 3.42601, 0.00000, 2.57260, 0.00000, 0.00000, 0.00000, 0.00000, 0.80479, 0.96433, 2.93213, 0.00000, 0.00000, 0.13393, 0.00000, 1.62752, 0.00000, 2.29110, 2.17039, 2.64885, 4.17406, 0.86303, 0.00000, 0.67668, 1.80349, 0.00000, 0.00000, 0.00000, 0.00000, 1.45309, 0.00000, 1.36054, 0.82336, 0.00000, 0.00000, 4.43950, 0.14440, 2.52793, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.61853, 0.70665, 0.00000, 0.00000, 0.00000, 0.37963, 0.00000, 0.30011, 0.00000, 0.00000, 0.00000, 0.00000, 3.50544, 0.00000, 0.00000, 1.47560, 0.00000, 0.00000, 1.68783, 0.00000, 0.00000, 0.00000, 2.27583, 0.31392, 0.00000, 4.73259, 0.00000, 0.00000, 0.00000, 0.00000, 2.13931, 0.00000, 1.84785, 0.00000, 0.00000, 3.57508, 0.00000, 0.00000, 3.49125, 1.59280, 0.00000, 0.00000, 3.10587, 0.00000, 0.00000, 0.50689, 1.62287, 0.00000, 0.00000, 0.00000, 1.55909, 0.00000, 0.00000, 2.68913, 0.00000, 0.00000, 0.00000, 0.00000, 0.89451, 2.76201, 0.00000, 0.12603, 2.77580, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.27170, 0.00000, 0.49144, 0.00000, 0.00000, 0.58439, 0.00000, 0.94904, 1.70053, 0.00000, 2.22506, 2.92062, 0.00000, 0.41440, 4.43353, 1.94822, 0.00000, 0.00000, 0.36160, 5.57516, 1.00537, 0.01551, 0.00000, 3.30006, 0.00000, 0.00000, 0.00000, 1.49392, 2.13815, 0.42471, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 3.37099, 0.00000, 1.33513, 5.46222, 0.00000, 1.81649, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.72690, 1.75915, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.53981, 0.08639, 2.51770, 0.80742, 1.15722, 0.00000, 0.00000, 3.88279, 0.00000, 0.00000, 0.30579, 0.16440, 1.73771, 1.24916, 0.00000, 1.60385, 0.00000, 2.33981, 0.00000, 0.00000, 1.62621, 1.52811, 1.77915, 0.00000, 0.00000, 0.00000, 0.00000, 1.21534, 0.00000, 0.00000, 2.06258, 0.00000, 4.06373, 0.00000, 0.00000, 0.00000, 0.00000, 1.03192, 1.18526, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 2.31320, 0.00000, 0.48581, 0.00000, 0.00000, 2.07850, 0.00000, 0.00000, 0.00000, 0.65118, 0.00000, 0.00000, 1.80311, 0.00000, 0.00000, 0.00000, 2.50783, 3.71816, 1.55863, 2.53429, 0.00000, 1.12286, 0.48619, 0.00000, 0.00000, 0.00000, 1.61403, 0.00000, 1.25095, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.80333, 0.00000, 4.98465, 0.22878, 0.00000, 0.00000, 2.22769, 0.00000, 3.67457, 1.51179, 0.55162, 0.00000, 0.00000, 0.00000, 2.76293, 0.00000, 0.00000, 0.00000, 2.77963, 0.00000, 0.00000, 0.00000, 1.13502, 1.54799, 0.00000, 1.78149, 0.55157, 0.00000, 0.00000, 0.00000, 0.02937, 1.42146, 1.54441, 0.00000, 0.74861, 0.00000, 1.66661, 0.00000, 0.00000, 1.88589, 0.02144, 0.00000, 0.00000, 0.00000, 2.74300, 0.00000, 0.05629, 0.00000, 3.93919, 1.18867, 1.77478, 0.93364, 1.12465, 0.00000, 0.00000, 4.92363, 0.32171, 2.17134, 2.20317, 0.40703, 1.33957, 0.00000, 0.00000, 0.00000, 0.16236, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.41639, 0.00000, 0.00000, 0.00000, 2.05372, 0.00000, 0.00000, 1.66296, 0.00000, 0.00000, 1.55005, 0.00000, 0.00000, 0.75007, 0.00000, 0.00000, 1.54887, 0.00000, 0.00000, 0.00000, 1.52533, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.08118, 0.00000, 0.00000, 1.03492, 0.00000, 0.01916, 2.92553, 0.00000, 0.00000, 0.96676, 0.00000, 1.17563, 0.05894, 0.00000, 0.03748, 0.00000, 1.13227, 0.00000, 0.94611, 0.00000, 0.22089, 0.00000, 0.42654, 0.00000, 0.00000, 2.11224, 0.00000, 0.21730, 0.03506, 3.67343, 0.00000, 0.00000, 3.28398, 3.12240, 0.94853, 0.00000, 0.00000, 0.00000, 1.44026, 0.00000, 4.30135, 0.00000, 2.42209, 0.00000, 0.00000, 0.57995, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.06806, 0.00000, 0.00000, 0.19780, 0.00000, 2.20870, 0.00000, 0.00000, 1.96625, 0.00000, 0.11591, 0.22731, 0.22888, 1.01237, 0.00000, 0.88336, 3.67525, 1.48861, 0.00000, 0.00000, 0.58924, 0.00000, 0.00000, 0.00000, 0.18124, 0.00000, 2.41723, 1.75204, 0.00000, 1.49197, 1.27260, 0.00000, 5.34589, 1.48569, 0.00000, 0.00000, 0.00000, 1.28358, 0.00000, 0.00000, 2.28182, 3.69177, 0.00000, 0.00000, 0.00000, 4.43135, 0.00000, 2.21293, 0.00000, 0.00000, 4.66100, 0.00000, 1.06023, 0.19471, 0.00000, 0.03635, 0.00000, 0.00000, 0.00000, 1.90316, 0.00000, 0.00000, 0.00000, 0.00000, 0.58134, 6.04520, 0.00000, 0.00000, 0.00000, 0.00000, 1.62318, 0.00000, 0.00000, 0.00000, 1.33250, 2.87006, 0.00000, 0.18631, 0.00000, 7.42709, 1.71375, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 1.19389, 0.00000, 2.14686, 0.00000, 0.16949, 0.00000, 0.00000, 4.53787, 1.57014, 0.00000, 0.00000, 6.93958, 0.00000, 0.00000, 0.00000, 0.00000, 0.57712, 1.54319, 0.00000, 1.45202, 0.00000, 0.04695, 0.10399, 2.08010, 1.97667, 0.00000, 0.32269, 5.35255, 0.00000, 0.00000, 0.00000]
	print s.predict([test_array_2])
	
	s.learn([test_array_1],[400])
	s.learn([test_array_2],[100])
	
	s.save()
"""