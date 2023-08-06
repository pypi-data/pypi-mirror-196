import sys
import argparse
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy
from random import shuffle, seed
import seaborn as sns


def get_key_driver_metric(G, seed_drivers):
	if not isinstance(seed_drivers,list):
		seed_drivers = list(seed_drivers)

	seed_dict = {key:value for value, key in enumerate(list(seed_drivers))}
	for s in seed_dict.keys():
		print(s,seed_dict[s])
	seed_drivers = np.array(seed_drivers)

	all_nodes = G.nodes
	for node in all_nodes:
		print('\t',node)

	## get the shortest path mat
	#sp_mat = nx.shortest_path(G) + 1

	## make the shortest_distance matrix
	all_shortest_paths = np.zeros((seed_drivers.shape[0],len(all_nodes)))
	for i in range(0,seed_drivers.shape[0]):
		seed = seed_drivers[i]
		dist_dict = nx.single_source_shortest_path_length(G, seed)
		for node in all_nodes:
			if node != seed:
				if node in dist_dict:
					all_shortest_paths[i,node] = dist_dict[node]
				else:
					all_shortest_paths[i,node] = np.inf
			else:
				all_shortest_paths[i,node] = 1#np.inf
	all_shortest_paths += 1

	print(all_shortest_paths[:,seed_drivers])
	inverse_sp_mat = 1/all_shortest_paths

	print(inverse_sp_mat[:,seed_drivers])

	key_driver_metric = 1+np.sum(inverse_sp_mat,axis = 0)
	print(key_driver_metric[seed_drivers])
	return(key_driver_metric)

def get_random_networks(G):
	num_nodes = G.number_of_nodes()
	num_edges = G.number_of_edges()
	rand_G = nx.gnm_random_graph(num_nodes, num_edges)
	for node in rand_G.nodes:
		print(node)
	return(rand_G)
	# temp_adj = list(nx.generate_adjlist(G))
	# #print(temp_adj)
	# adj_list_1 = []
	# adj_list_2 = []
	# for i in range(0,len(temp_adj)):
	# 	adj = list(map(int,temp_adj[i].split(' ')))
	# 	for node in adj[1:]:
	# 		if i != node:
	# 			adj_list_1.append(adj[0])
	# 			adj_list_2.append(node)
	# #for i in range(0,len(adj_list_1)):
	# #	print(adj_list_1[i],adj_list_2[i])
	# ## make a new graph & populate it with the edge lists
	# shuffle(adj_list_2)
	# rand_G=nx.Graph()
	# for i in range(0,len(adj_list_1)):
	# 	G.add_edge(adj_list_1[i],adj_list_2[i])
	# return(G)

def get_random_key_driver_metrics(G, seed_drivers, iters=20):
	all_random_key_drivers = []
	for i in range(iters):
		all_random_key_drivers.append(get_key_driver_metric(get_random_networks(G),seed_drivers))
	all_random_key_drivers = np.array(all_random_key_drivers)
	non_seed_indices = np.ones((len(G.nodes)),dtype=bool)
	non_seed_indices[seed_drivers] = False
	#all_random_key_drivers[:,non_seed_indices]
	return(all_random_key_drivers[:,non_seed_indices])

def get_sd_cutoff(in_vect, sd = 2):
	mean = np.mean(in_vect)
	return(mean + sd * np.std(in_vect))

def get_key_drivers(G, seed_drivers):
	key_driver_metric = get_key_driver_metric(G, seed_drivers)

	all_random_driver_metrics = get_random_key_driver_metrics(G,seed_drivers,iters=100)
	all_random_driver_metrics = all_random_driver_metrics.flatten()
	
	sns.distplot(all_random_driver_metrics)
	plt.show()

	print(key_driver_metric)
	key_driver_cutoff = get_sd_cutoff(all_random_driver_metrics)
	print(key_driver_cutoff)

	key_drivers = key_driver_metric > key_driver_cutoff
	key_driver_dict = {'key_drivers':np.where(key_drivers)[0],
	                   'key_driver_metric':key_driver_metric}
	return(key_driver_dict)

def parse_args(args):
	##########################################################################
	parser = argparse.ArgumentParser()
	parser.add_argument(
		    '-plot',
		    dest='plot',
		    help='if you want to make some plots',
		    action='store_true')

	args = parser.parse_args()
	return(args)

if __name__ == '__main__':
	## do dodecahedral
	seed(1234567789)

	G = nx.dodecahedral_graph()
	seed_drivers = [9,10,11,12,13]


	# pos=nx.spring_layout(G)

	# print(key_driver_metric)
	# shells = [[2, 3, 4, 5, 6], [8, 1, 0, 19, 18, 17, 16, 15, 14, 7], [9, 10, 11, 12, 13]]
	# key_driver_metric_dict = {key:value for key, value in enumerate(key_driver_metric)}
	# nx.draw_shell(G, nlist=shells, node_size = key_driver_metric*100, with_labels = True)
	# plt.show()
	# plt.clf()

	G = nx.karate_club_graph()
	seed_drivers = [6,7,8]

	key_driver_dict = get_key_drivers(G, seed_drivers)
	key_driver_metric = key_driver_dict['key_driver_metric']
	key_driver_indices = key_driver_dict['key_drivers']
	

	pos=nx.spring_layout(G)

	nx.draw(G, node_size = key_driver_metric**8, with_labels = True)
	plt.show()
	plt.clf()

	args = parse_args(sys.argv)

	
