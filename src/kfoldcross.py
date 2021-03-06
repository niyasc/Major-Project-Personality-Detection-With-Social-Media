import random
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer
import pylab
import sys

sys.path.append('./lib')

from ReadCSV import ReadCSV

class InvalidNumberofTrainingTuples(Exception):
	def __init__(self,message):
		self.message=message
		
		

def make_list(inputs):
	'''
		Make a list corresponding to ids of inputs and return the result
	'''
	ids=[]
	for id in inputs.keys():
		ids.append(id)
	return ids

def find_accuracy(k, ids, hidden_layers, inputs, outputs):
	'''
		INPUT
		n	:	Number of training tuples
		ids	:	List of ids of training tuples
		hidden_layers	:	Number of hidden layers that should be used in network
		OUTPUT
		accuracy	:	Accuracy using n tuples for training and remainings for testing
	'''
	ERRORS = [] #store error in each iteration
	#Number of  items in each fold
	n = len(ids) / k
	
	for i in range(0, k) :
		print 'Iteration Number', i
		train_set = ids[0 : i*n] + ids[ (i+1) * n:]
		test_set = ids[i*n:(i+1)*n]
		print 'train set', train_set
		print 'test set', test_set
		#Now construct the neural network
		net = buildNetwork(178, hidden_layers, 5, bias = True, hiddenclass = TanhLayer)
		ds=SupervisedDataSet(178,5)
		for id in train_set:
			ds.addSample(inputs[id],outputs[id])

		trainer = BackpropTrainer(net, ds)
		'''for t in range(0, 1000):
			trainer.train()'''
		trainer.trainUntilConvergence(maxEpochs=1000)
		#print 'Training Completed'

		errors=[]
		for id in test_set:
			predicted=net.activate(inputs[id]);
			actual= outputs[id];
			e=[]
			for i in range(5):
				d=abs(predicted[i]-actual[i])
				e.append(d)
			errors.append(((sum(e)/len(e))/5)*100)
		ERRORS.append((sum(errors)/len(errors)))
	return (100 - sum(ERRORS)/len(ERRORS)) # Return 100 - average error
	
def main():
	inputs = ReadCSV('./data/input.csv')
	outputs = ReadCSV('./data/output.csv')
	ids = make_list(outputs)
	x = []
	y = {}
	
	for i in range(2, 11, 2) :
		x.append(i)
	
	for hidden_layers in range(1, 6) : #change loop for plot also if you change here
		print 'Number of hidden layers', hidden_layers
		y[hidden_layers]=[]
		for i in x :
			print 'Number of folds', i
			y[hidden_layers].append(find_accuracy(i,ids,hidden_layers, inputs, outputs))
	#print x
	#print y
	#Now plot the graph
	for i in range(1, 6) :
		t=pylab.plot(x,y[i],label="Number of hidden layers "+str(i),linewidth=4,linestyle='-')
	t=pylab.xlabel("Number of folds")
	t=pylab.ylabel("Accuracy %")	
	t=pylab.title("K-Fold cross validation (Number of folds vs Accuracy)")
	t=pylab.legend(loc='lower right')
	t=pylab.grid()
	pylab.show()


if __name__ == "__main__" :
	main()
