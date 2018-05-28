import os 
import csv 
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, uid):
        self.uid = uid
        self.cesd_score = None
        self.ocean_score = None
        self.friends_ocean_score = None 
        self.gender = None 
        self.satisfaction_with_life = None
        self.age = None
        self.education = None
        self.latitude = None
        self.longitude = None
    
    def add_ocean_score(self, o, c, e, a, n):
        self.ocean_score = {"O":o,"C":c, "E":e, "A":a, "N":n}
    def add_friends_ocean_score(self, o, c, e, a, n):
        self.friends_ocean_score = {"O":o,"C":c, "E":e, "A":a, "N":n}
    # Not sure if I calculated the cesd scores correctly 
    def calculate_cesd_score(self, row):
        score = int(row['q1']) + int(row['q2']) + int(row['q3']) + int(4 - int(row['q4'])) + int(row['q5']) + int(row['q6']) + int(row['q7']) + int(4 - int(row['q8'])) + int(row['q9']) + int(row['q10']) + int(row['q11']) + int(4 - int(row['q12'])) + int(row['q13']) + int(row['q14']) + int(row['q15']) + int(4 - int(row['q16'])) + int(row['q17']) + int(row['q18']) + int(row['q19']) + int(row['q20']) - 16
        return score 
    def add_cesd_score(self, score):
        self.cesd_score = score 
    def add_age(self, age):
        self.age = age 
    def add_gender(self, gender):
        if gender == 0:
            self.gender = "Male"
        else:
            self.gender = "Female"
    def add_satisfaction_with_life(self, score):
        self.satisfaction_with_life = score
    def add_location(self, lat, lon):
        self.latitude = lat
        self.longitude = lon 

    def __str__(self):
        result = "UID: " + str(self.uid) + "\n" + "Depression Score: " + str(self.cesd_score) + "\n" + "Ocean Score: " + str(self.ocean_score) + "\nFriends Ocean Score: " + str(self.friends_ocean_score) + "\nAge: " + str(self.age) + "\nGender: " + str(self.gender) +"\nSatisfaction with Life: " + str(self.satisfaction_with_life) + "\nLatitude: " + str(self.latitude) +"\nLongitude: " + str(self.longitude) + "\n"
        return result

def main():
	G = nx.Graph()
	makeGraph(G)
	# # print(avg_cesd(G.nodes()))
	# centrality_measures(G)
	# clustering_measures(G)
	drawGraph(G)

def makeGraph(G):
	os.getcwd() 
	external_hard_drive_path = "/Volumes/Seagate Backup /Facebook Data"
	if os.path.exists(external_hard_drive_path):
		nodes = {}
		edges = []
		# Creating Nodes
		# Get OCEAN Scores 
		with open(external_hard_drive_path + '/big5.csv', 'r') as big5:
			big5_reader = csv.DictReader(big5)
			for row in big5_reader:
				uid = row['userid']
				if uid in nodes:
					node = nodes[uid]
				else:
					node = Node(uid)
				node.add_ocean_score(row['ope'], row['con'], row['ext'], row['agr'], row['neu'])
				# Modify Object
				nodes[uid] = node
		# Not necessarily sure what this means, but added friends OCEAN score. 
		with open(external_hard_drive_path + '/cross_ratings.csv', 'r') as cross_ratings:
			cross_ratings_reader = csv.DictReader(cross_ratings)
			for row in cross_ratings_reader:
				uid = row['userid']
				if uid in nodes:
					node = nodes[uid]
				else:
					node = Node(uid)
				node.add_friends_ocean_score(row['friend_ope'], row['friend_con'], row['friend_ext'], row['friend_agr'], row['friend_neu'])
				# Modify Object
				nodes[uid] = node
		# Get CESD Scores
		# Interesting Data: Ethnicity, Marital Status, Whether Parents are Together, Question Order 
		# Why are some of the responses negative 
		with open(external_hard_drive_path + '/cesd_item_level.csv', 'r') as cesd: 
			cesd_reader = csv.DictReader(cesd)
			# i = 0
			for row in cesd_reader:
				uid = row['userid']
				if uid in nodes:
					node = nodes[uid]
				else:
					node = Node(uid)
				score = node.calculate_cesd_score(row)
				if(score < 0):
					score = 0 
				node.add_cesd_score(score)
				# Modify Object 
				nodes[uid] = node
		# Get Age and Gender Data 
		# Does 0 correspond to male or female?
		# What does mf stand for? 
		# What does 0 1 2 3 stand for in relationship status?
		# Not included: "interested_in","mf_relationship","mf_dating","mf_random","mf_friendship","mf_whatever","mf_networking","locale","network_size","timezone"
		with open(external_hard_drive_path + '/demog.csv', 'r') as demog: 
			demographic_reader = csv.DictReader(demog)
			for row in demographic_reader:
				uid = row['userid']
				# Get Gender 
				if row['gender'] != '':
					if uid in nodes:
						node = nodes[uid]
					else:
						node = Node(uid)
					node.add_gender(int(row['gender']))
				# Get Age 
				if row['age'] != '':
					if uid in nodes:
						node = nodes[uid]
					else:
						node = Node(uid)
					node.add_age(int(row['age']))
				nodes[uid] = node
		# Get latitude and longitude of Couple Data  
		# There is more data in couples like relationships status, distance, friends, groups, likes, and tags, not sure what to do with it
		with open(external_hard_drive_path + '/couples.csv') as couples:
			couples_reader = csv.DictReader(couples)
			for row in couples_reader:
				uid = row['userid']
				sig_oth_uid = row['significant_other_id']

				lat1 = row['lat1']
				lon1 = row['lon1']
				lat2 = row['lat2']
				lon2 = row['lon2']

				if uid in nodes:
					node = nodes[uid]
				else:
					node = Node(uid)

				if lat1 != "NULL" and lon1 != "NULL":
					node.add_location(lat1, lon1)
					nodes[uid] = node

				if sig_oth_uid in nodes:
					node = nodes[sig_oth_uid]
				else:
					node = Node(sig_oth_uid)

				if lat2 != "NULL" and lon2 != "NULL":
					node.add_location(lat2, lon2)
					nodes[sig_oth_uid] = node 
		# swl- statisfation with life.csv Add each person's satisfaction with life. What is the scale? How was it measured?
		with open(external_hard_drive_path + '/swl.csv', 'r' ) as swl:
			swl_reader = csv.DictReader(swl)
			for row in swl_reader:
				uid = row['userid']
				if uid in nodes:
					node = nodes[uid]
				else:
					node = Node(uid)
				node.add_satisfaction_with_life(float(row['swl']))
				nodes[uid] = node 

		# HARD PART CREATING FRIENDSHIPS (EDGES IN THE GRAPH)
		with open(external_hard_drive_path + '/sample-friends.csv', 'r') as fb_friends:
			friends_reader = csv.DictReader(fb_friends)
			for row in friends_reader:
				friend1_uid = row['\ufeffa']
				friend2_uid = row['b']

				if friend1_uid in nodes:
					node1 = nodes[friend1_uid]
				else:
					node1 = Node(friend1_uid)

				if friend2_uid in nodes:
					node2 = nodes[friend2_uid]
				else:
					node2 = Node(friend2_uid)

				#Creates the edges as we add friends 
				edge = (node1,node2)
				edges.append(edge)

		# Adds the Nodes to the Graph 
		G.add_nodes_from(list(nodes.values()))
		# print(G.nodes())
		# Adds Edges to the Graph
		G.add_edges_from(edges)
		# print(G.edges())
	else:
		print("Please insert External Hard Drive")
def drawGraph(G):
	nx.draw(G)
	plt.show()
def getNameAsKeysOfDictionary(old_dict):
	m_dict = {}
	for element in old_dict:
		m_dict[element.name] = old_dict[element]
	return m_dict
def degree_centrality(G):
	m_dict = getNameAsKeysOfDictionary(nx.degree_centrality(G))
	return m_dict 
def eigenvector_centrality(G):
	m_dict = getNameAsKeysOfDictionary(nx.eigenvector_centrality(G))
	return m_dict 
def closeness_centrality(G):
	m_dict = getNameAsKeysOfDictionary(nx.closeness_centrality(G))
	return m_dict 
def betweenness_centrality(G):
	m_dict = getNameAsKeysOfDictionary(nx.betweenness_centrality(G))
	return m_dict 
def centrality_measures(G):
	d_centrality = degree_centrality(G)
	d_avg  = avg_centrality(d_centrality)
	print("Average Degree Centrality: \n" + str(d_avg)+ "\n")
	print("Degree Centrality: \n" + str(d_centrality)+ "\n")
	print("Difference Between Avg and Value for Nodes: " + str(diff_from_mean(d_centrality,d_avg)))
	
	e_centrality = eigenvector_centrality(G)
	e_avg  = avg_centrality(e_centrality)
	print("Average Eigenvector Centrality: \n" + str(e_avg)+ "\n")
	print("Eigenvector Centrality: \n" + str(e_centrality)+ "\n")
	print("Difference Between Avg and Value for Nodes: " + str(diff_from_mean(e_centrality,e_avg)))

	c_centrality = closeness_centrality(G)
	c_avg  = avg_centrality(c_centrality)
	print("Average Closeness Centrality: \n" + str(c_avg)+ "\n")
	print("Closeness Centrality: \n" + str(c_centrality)+ "\n")
	print("Difference Between Avg and Value for Nodes: " + str(diff_from_mean(c_centrality,c_avg)))

	b_centrality = betweenness_centrality(G)
	b_avg  = avg_centrality(b_centrality)
	print("Average Betweenness Centrality: \n" + str(b_avg)+ "\n")
	print("Betweenness Centrality: \n" + str(b_centrality)+ "\n")
	print("Difference Between Avg and Value for Nodes: " + str(diff_from_mean(b_centrality,b_avg)))

	# print("Betweenness Centrality: \n" + str(betweenness_centrality(G))+ "\n")
def clustering_of_each_node(G):
	m_dict = getNameAsKeysOfDictionary(nx.clustering(G))
	return m_dict
def avg_clustering_of_graph(G):
	return nx.average_clustering(G)
def clustering_measures(G):
	avg = avg_clustering_of_graph(G)
	m_dict = clustering_of_each_node(G)
	print("Clustering : \n" + str(m_dict)+ "\n")
	print("Average Clustering Coefficient for graph G: \n" + str(avg))
	print("Difference between Mean Clustering and Individual Clustering: \n"+ str(diff_from_mean(m_dict,avg)))
def diff_from_mean(m_dict,avg):
	result = {}
	for key in m_dict:
		result[key] = abs(m_dict[key]-avg)
	return result 
def avg_centrality(m_dict):
	return (sum(m_dict[d] for d in m_dict))/(len(m_dict))
def avg_age(m_dict):
	return (sum(d.age for d in m_dict))/(len(m_dict))
def avg_cesd(m_dict):
	return (sum(d.cesd_score for d in m_dict))/(len(m_dict))

# Functions that I will implement. Waiting for input type otherwise will be waste of effort 
if __name__ == '__main__':
	main()