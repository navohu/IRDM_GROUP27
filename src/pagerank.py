import networkx as nx
import json

with open("../sitegraph/graphs/sitegraph.json") as data_file:    
    data = json.load(data_file)

graph = data

print json.dumps(graph, indent=2, sort_keys=True)

# graph = {'1': [{'2':'15'}, {'4':'7'}, {'5':'10'}],
#     '2': [{'3':'9'}, {'4':'11'}, {'6':'9'}],
#     '3': [{'5':'12'}, {'6':'7'}],
#     '4': [{'5':'8'}, {'6':'14'}],
#     '5': [{'6':'8'}]}
# new_graph = nx.Graph()
# for source, targets in graph.iteritems():
#     for inner_dict in targets:
#         assert len(inner_dict) == 1
#         new_graph.add_edge(int(source) - 1, int(inner_dict.keys()[0]) - 1,
#                            weight=inner_dict.values()[0])
# adjacency_matrix = nx.adjacency_matrix(new_graph)