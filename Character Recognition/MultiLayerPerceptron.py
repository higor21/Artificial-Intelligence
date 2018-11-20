# -*- coding: utf-8 -*-
import numpy as np
from math import exp

# importando bibliotecas para pegar os dados de treinamento da rede
import cPickle
import gzip


def vectorize(x):
	"""
		cria matris 10x1 e coloca o valor 1 na posição 'x'
	"""
	e = np.zeros((10, 1))
	e[x] = 1.0
	return e

def load_data(path, cmd):
	"""
		Abre o arquivo no caminho 'path' e retorna os dados das
		imagens que serão utilizados para o treinamento da rede neural
	"""
	file = gzip.open(path, cmd)
	data_input, trash, test_data = cPickle.load(file)	 
	file.close()

	test_inputs = [np.reshape(x, (784, 1)) for x in test_data[0]]
	test_results = [vectorize(y) for y in test_data[1]]
	test_data = zip(test_inputs, test_results)	

	training_inputs = [np.reshape(x, (784, 1)) for x in data_input[0]]
	training_results = [vectorize(y) for y in data_input[1]]
	training_data = zip(training_inputs, training_results)

	return (training_data, test_data)

def arrayToList(vect):
	"""
		Função usada para converter um vetor do tipo 'nparray' para o tipo 'list'
	"""
	if type(vect).__module__ == np.__name__:
		vect = vect.tolist()
	for i in range(len(vect)):
		if type(vect[i]).__module__ == np.__name__:
			vect[i] = vect[i].tolist()
	return vect

def vects_equal(vect1, vect2):
	return vect2[vect1.index(max(vect1))] == [1]

def test_network(datas, network):
	"""
		Função utilizada para testar a rede neural
	"""
	cont, lenght = 0, len(datas)
	while len(datas):
		if vects_equal(network.calculate_output(datas[-1][0])[0].tolist() , datas[-1][1]): cont += 1
		datas.pop()
	return (cont*100.0)/lenght

class MultiLayersPerceptron():
	def __init__(self, layers, thresholds = True):
		"""
			Inicializa a rede neural com várias camadas (layers) de distintos tamanhos. 
			Dentre essas camandas, a primeira e a última representa a entrada e saida da
			Multi-Layers Perceptron (MPL), respectivamente. 
			Além disso, ainda inicia aleatoriamente os pesos entre cada camada e os 'thresholds'(limites == biases)
			de cada neurônio ()
		"""
		self.num_layers = len(layers)
		self.size_layers = layers
		# define os limites de cada neurônio
		self.biases = arrayToList([(1.0 if thresholds else 0.0)*np.random.randn(i, 1) for i in self.size_layers[1:]])
		# define as matrizes de pesos entre cada 
		#print(self.biases)
		self.weights = arrayToList([np.random.randn(x,y) for y, x in zip(self.size_layers[:-1], self.size_layers[1:])])

		self.deltaW = arrayToList([0.0*np.random.randn(x,y) for y, x in zip(self.size_layers[:-1], self.size_layers[1:])])
		self.deltaW_A = arrayToList([0.0*np.random.randn(x,y) for y, x in zip(self.size_layers[:-1], self.size_layers[1:])])

	def training(self, training_data, alfa = 0.5, learning_rate = 0.5):
		"""
			Método para treinamento da rede neural com base nos dados 'training_data' e na
			taxa de aprendizado 'learning_rate'
		"""

		while(len(training_data)):
			output_data, list_outs = self.calculate_output(training_data[-1][0])
			error = self.calculate_error(training_data[-1][1], output_data)
			self.back_propagation(self.num_layers - 2, error, len(training_data), alfa, list_outs, learning_rate)
			training_data.pop()
			break
		print('\nO treinamento da rede acabou!')

	def dAtivFunc(self,fx):
		return fx*(1.0-fx)

	def back_propagation(self, n_layers, error, quatity_ex, alfa, list_outs, learning_rate):
		delta = np.asarray([self.dAtivFunc(fx[0]) for fx in list_outs[n_layers]])
		delta = np.multiply(list_outs[n_layers], error)
		delta = delta.transpose()  #Vetor coluna

		A = np.dot(delta, list_outs[n_layers])
		B = np.dot(alfa, self.deltaW_A[n_layers])
		#matriz numero_neuronios_list_outs x numero_entradas
		self.deltaW[n_layers] = np.add(np.dot((learning_rate/quatity_ex), A ), B)

		self.weights[n_layers] = np.add(self.weights[n_layers], self.deltaW[n_layers])

		erro2 = np.dot(self.weights[n_layers].transpose(), delta.transpose())
		if(n_layers != 0):
			self.back_propagation(n_layers - 1, erro2, quatity_ex, alfa, list_outs, learning_rate)

	def calculate_output(self, input_data):
		"""
			Calcula a saída da rede neural para uma dada entrada. Além disso,
		"""
		list_outs = []
		for b, w in zip(self.biases, self.weights):
			# o resultado de 'np.dot(w,input_data) - b)' acaba sendo um 
			# 'array()' q será calculado pela função 'act_funciton()'
			for i in range(len(w)):
				input_data[i] = self.act_function(np.dot(w[i],input_data) - b[i], "sigmoid")        
			input_data = input_data[:i+1]
			list_outs.append(input_data)

		return (input_data, arrayToList(list_outs))

	def calculate_error(self, expected_output, real_output):
		return expected_output - real_output 

	def act_function(self, value, nm_func = "sigmoid"):
		"""
			seleciona qual a saída do neurônio de acordo com sua função de ativação
		"""
		if nm_func == "sigmoid":
			return 1.0/(1.0 + exp(-value))


# 'tr_d' são todas as imagens que serão usadas para treinar a rede
# 'tt_d' são todas as imagens que serão usadas para verificar a eficiencia da rede
tr_d, tt_d = load_data('./mnist.pkl.gz', 'rb')

# Criando uma rede cuja a entrada será uma imagem de 28x28 = 784 pixels
# e a saída será um vetor de 10 posições 
network_mlp = MultiLayersPerceptron([784,30,30,10])

# Treinando a rede com o banco de imagens 'tr_d' e a uma taxa de aprendizado de 0.3
network_mlp.training(tr_d, 0.3)


# Testando a rede
print('\n\nRede treinada com ' + str(test_network(tt_d, network_mlp))) + '% de presisão!\n'