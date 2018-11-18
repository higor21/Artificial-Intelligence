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

class Neuron():
    """
        Neurônio a ser instanciado 
    """
    def __init__(self, n_inputs = 0, threshold = 0, out = 0):
        self.n_inputs = n_inputs
        self.threshold = threshold
        self.weights = np.random.randn(1,n_inputs)
        self.output = out

    def __str__(self):
        return '[' + str(self.n_inputs) + ' , ' + str(self.threshold) + ' , ' + str(self.output) + ']'

    def calculate_out(self, input_dt, func = "sigmoid"):
        if(len(input_dt) == len(self.weights)):
            self.output = self.act_function(np.dot(self.weights, input_dt) - self.threshold, func)
        return self.output
        
    def act_function(self, value, nm_func):
        """
            seleciona qual a saída do neurônio de acordo com sua função de ativação
        """
        if nm_func == "sigmoid":
            return 1.0/(1.0 + exp(-value))
        

class MultiLayersPerceptron():
    def __init__(self, layers, thresholds = True):
        """
            Inicializa a rede neural com várias camadas (layers) de distintos tamanhos. 
            Dentre essas camandas, a primeira e a última representa a entrada e saida da
            Multi-Layers Perceptron (MPL), respectivamente. 
            Além disso, ainda inicia aleatoriamente os pesos entre cada camada e os 'thresholds'(limites == biases)
            de cada neurônio ()
        """    
        self.size_layers = layers
        self.neurons = []

        # define os limites de cada neurônio
        i = 0
        while i < len(layers):
            self.neurons.append([])
            for k in range(layers[i]):
                neu = Neuron(layers[i-1], np.random.uniform(0.0, 1.0)) if (i != 0) else Neuron(0,0)
                self.neurons[i].append(neu)
            i += 1

    def training(self, training_data, learning_rate):
        """
            Método para treinamento da rede neural com base nos dados 'training_data' e na
            taxa de aprendizado 'learning_rate'
        """
        while(len(training_data)):
            output_data = self.calculate_output(training_data[-1][0])
            print(output_data)
            break
            error = self.calculate_error(training_data[-1][1], output_data)
            self.back_propagation(training_data[-1][0], output_data, error, learning_rate)
            training_data.pop()
            break


    def back_propagation(self, input_data, real_output, error, learning_rate):
        delta = real_output*(1 - real_output)*error
        for b, w in zip(self.biases, self.weights):
            print(str(b) + ' <-> ' + str(w))
            return

    def calculate_output(self, input_data):
        """
            Calcula a saída da rede neural para uma dada entrada. Além disso,
        """

        self.neurons[0] = [Neuron(out = x) for x in input_data]
        listOuts = self.listOutputs(self.neurons[0])
        
        for x in self.neurons[1:]:
            for i in x:
                i.calculate_out(listOuts, "sigmoid")
            listOuts = self.listOutputs(x)

        return listOuts

    def listOutputs(self, neus):
        print(type(neus[0].output))
        out = []

        for x in neus:
            out.append(list(x.output) if type(neus[0].output) != 'int' else x.output)
        return out

    def calculate_error(self, expected_output, real_output):
        return expected_output - real_output 



# 'tr_d' são todas as imagens que serão usadas para treinar a rede
tr_d = load_data('./mnist.pkl.gz', 'rb')

# Criando uma rede cuja a entrada será uma imagem de 28x28 = 784 pixels
# e a saída será um vetor de 10 posições 
network_mlp = MultiLayersPerceptron([784,30,30,10])
#network_mlp = MultiLayersPerceptron([2,3,3,2])

# Treinando a rede com o banco de imagens 'tr_d' e a uma taxa de aprendizado de 0.3
network_mlp.training(tr_d, 0.3)