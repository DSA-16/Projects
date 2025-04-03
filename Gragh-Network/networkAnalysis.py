#!/usr/bin/env python3

import json
import networkx as nx
import random

# ========================
#  Main
# ========================

def main():
	random.seed()

	# Amazon

	amazonNetwork = parseAmazonData('com-amazon.ungraph.txt')
	amazonNetworkSize = amazonNetwork.number_of_nodes()

	printNetworkMetrics('amazon', amazonNetwork)

	amazonNetwork.clear()

	# Twitch

	twitchNetwork = parseTwitchData('large_twitch_edges.csv')
	twitchNetworkSize = twitchNetwork.number_of_nodes()

	printNetworkMetrics('twitch', twitchNetwork)

	twitchNetwork.clear()

	# Amazon, Watts-Strogatz

	wsAmazonNetwork = buildWattsStrogatz(amazonNetworkSize, 2, 0.0)

	printNetworkMetrics('ws-amazon', wsAmazonNetwork)

	wsAmazonNetwork.clear()

	# Twitch, Watts-Strogatz

	wsTwitchNetwork = buildWattsStrogatz(twitchNetworkSize, 2, 0.0)

	printNetworkMetrics('ws-twitch', wsTwitchNetwork)

	wsTwitchNetwork.clear()

	# Amazon, Barabasi-Albert

	baAmazonNetwork = buildBarabasiAlbert(amazonNetworkSize, 2, 0.0)

	printNetworkMetrics('ba-amazon', baAmazonNetwork)

	baAmazonNetwork.clear()

	# Twitch, Barabasi-Albert

	baTwitchNetwork = buildBarabasiAlbert(twitchNetworkSize, 2, 0.0)

	printNetworkMetrics('ba-twitch', baTwitchNetwork)

	baTwitchNetwork.clear()

# ========================
#  Simulations
# ========================

def buildWattsStrogatz(size, degree, rewiringParameter):
	result = nx.Graph()

	adjacencyList = [None for _ in range(size)]

	for i in range(size):
		adjacencyList[i] = [((i + j) % size) for j in range(1, int(degree / 2) + 1)]

	for i in range(size):
		for j in range(int(degree / 2)):
			if random.random() <= rewiringParameter:
				while True:
					node = random.randrange(size)

					if node != i and node not in adjacencyList[i] and i not in adjacencyList[node]:
						adjacencyList[i][j] = node
						break

	for i, neighbors in enumerate(adjacencyList):
		result.add_edges_from([(i, j) for j in neighbors])

	return result

def buildBarabasiAlbert(size, initialSize, newEdges):
	result = nx.Graph()
	degrees = [0 for _ in range(size)]

	for i in range(initialSize):
		for j in range(i + 1, initialSize):
			result.add_edge(i, j)

		degrees[i] = initialSize - 1

	for i in range(initialSize, size):
		selectedNodes = random.choices(population = range(i), weights = degrees[:i], k = newEdges)

		for selectedNode in selectedNodes:
			result.add_edge(i, selectedNode)
			degrees[selectedNode] += 1

		degrees[i] = newEdges

	return result

# ========================
#  Metrics
# ========================

def printNetworkMetrics(name, network):
	print('Calculating network metrics for ' + name + '...')

	size = network.number_of_nodes()

	print(' -> average path length')

	averagePathLength = nx.average_shortest_path_length(network)

	print(' -> clustering coefficient')

	clusteringCoefficient = nx.average_clustering(network)

	print(json.dumps({
		'name': name,
		'size': size,
		'averageDegree': 2.0 * network.size() / size,
		'averagePathLength': averagePathLength,
		'clusteringCoefficient': clusteringCoefficient
	}, indent = '\t'))

# ========================
#  Parsing
# ========================

def parseAmazonData(filename):
	print('Parsing Amazon data...')

	with open(filename, 'rb') as file:
		network = nx.read_edgelist(file, comments = '#', delimiter = '\t', nodetype = int)
		return getLargestComponent(network)

def parseTwitchData(filename):
	print('Parsing Twitch data...')

	with open(filename, 'rb') as file:
		file.readline()
		network = nx.read_edgelist(file, comments = None, delimiter = ',', nodetype = int)
		return getLargestComponent(network)

def getLargestComponent(network):
	largestComponent = max(nx.connected_components(network), key = len)
	return network.subgraph(largestComponent).copy()

main()
