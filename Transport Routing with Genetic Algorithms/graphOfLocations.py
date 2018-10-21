# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
import re

file = open("final.txt", "r") # abrindo o arquivo 
G = nx.Graph() # criando um grafo vazio

fixed_positions = {}
k = 0

# lendo e armazenando todos os pontos do gráfico 
data = file.readline();

while data[0] != ';':
	xy = data.split(', ')
	xy[1] = xy[1][0:len(xy[1])-1]
	fixed_positions[k] = tuple(map(lambda x: float(x),xy))
	G.add_node(k)
	k += 1
	data = file.readline()

#G = nx.complete_graph(G.nodes(), nx.Graph) # nx.Graph é opcional

new_data = data.split('->') + str(file.readlines()).split('->')
new_data = list(re.findall(r'\d+',str(new_data)))
print(new_data)

plt.ion()
#plt.subplot(200)

new_data

for i in range(0,len(new_data)-1):
	G.add_edge(int(new_data[i]), int(new_data[i+1]))
G.add_edge(int(new_data[0]), int(new_data[len(new_data)-1]))

#G = nx.dodecahedral_graph()
#print fixed_positions

print("Arestas: \n")
print(G.edges())
print(fixed_positions)

fixed_nodes = fixed_positions.keys()
pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)

color = ['g','r','b','b','b','b','b','r','b','b','b','b','b','b','r','b','b','b','b']
node_list = tuple(range(0,18))

#print fixed_positions
nx.draw_networkx(G, pos, node_color = color)
#nx.draw(G,pos) # imprime o grafo 

file.close()
input('exit?')