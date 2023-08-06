from house_gen import House
from plot_house_graph import plot
import networkx as nx
import pickle
import logging

NUM_HOUSES = 5

if __name__ == '__main__':
	num_times = 0
	while num_times < NUM_HOUSES:
		try:
			h=House()
			vals = h.gen()
			if vals is not None:
				scene_graph_list = nx.to_dict_of_lists(vals[3])
				meta_data = vals[2]
				img = vals[1]
				storage_dict = {"world": img, "data": meta_data, "scene_graph": scene_graph_list}
				pickle.dump(storage_dict, open(f'/home/isaac/grid_graphs/environments/house_env/houses/house{num_times}.pickle', 'wb'))
				num_times += 1
				# logging.info("Wrote world files successfully")
			else:
				logging.warning("Regenerating...")
		except TimeoutError as e:
			pass

	# storage_dict = pickle.load(open('/home/isaac/grid_graphs/environments/house_env/houses/house0.pickle', 'rb'))
	# scene_graph = nx.Graph(storage_dict["scene_graph"])
	# plot(storage_dict["data"], scene_graph)