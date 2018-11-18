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
    data = cPickle.load(file)[0]
    file.close()

    training_inputs = [np.reshape(x, (784, 1)) for x in data[0]]
    training_results = [vectorize(y) for y in data[1]]
    training_data = zip(training_inputs, training_results)
    return training_data

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
    	self.biases = [(1.0 if thresholds else 0.0)*np.random.randn(i, 1) for i in self.size_layers[1:]]
    	# define as matrizes de pesos entre cada 
    	print(self.biases)
    	self.weights = [np.random.randn(x,y) for y, x in zip(self.size_layers[:-1], self.size_layers[1:])]
    	print(self.weights)
    	print(zip(self.biases, self.weights))

    def training(self, training_data, learning_rate):
    	"""
			Método para treinamento da rede neural com base nos dados 'training_data' e na
			taxa de aprendizado 'learning_rate'
    	"""
    	while(len(training_data)):
    		output_data = self.calculate_output(training_data[0])
    		error = self.calculate_error(training_data[1], output_data)
    		self.back_propagation(training_data[0], output_data, error)
    		training_data.pop()


    def back_propagation(self, input_data, real_output, error):
    	pass

    def calculate_output(self, input_data):
    	"""
			Calcula a saída da rede neural para uma dada entrada. Além disso,
    	"""
    	for b, w in zip(self.biases, self.weights):
    		# o resultado de 'np.dot(w,input_data) - b)' acaba sendo um 
    		# 'array()' q será calculado pela função 'act_funciton()'
    		input_data = act_function(np.dot(w,input_data) - b, "sigmoid")
    	return input_data

    def calculate_error(self, expected_output, real_output):
    	return expected_output - real_output 

    def act_function(self, value, nm_func = "sigmoid"):
    	"""
    		seleciona qual a saída do neurônio de acordo com sua função de ativação
    	"""
    	if nm_func == "sigmoid":
    		return 1.0/(1.0 + exp(-value))


# 'tr_d' são todas as imagens que serão usadas para treinar a rede
tr_d = load_data('./mnist.pkl.gz', 'rb')

# Criando uma rede cuja a entrada será uma imagem de 28x28 = 784 pixels
# e a saída será um vetor de 10 posições 
network_mlp = MultiLayersPerceptron([784,30,30,10])

# Treinando a rede com o banco de imagens 'tr_d' e a uma taxa de aprendizado de 0.3
network_mlp.training(tr_d, 0.3)