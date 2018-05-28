import networkx as nx
import matplotlib.pyplot as plt
import random as rdm
class Node:
	def __init__(self, name, cesd_score, ocean_score, age, education, location):
		self.name = name.strip()
		self.cesd_score = cesd_score
		self.ocean_score = ocean_score
		self.age = age
		self.education = education.strip()
		self.location = location.strip()
	def __str__(self):
		result = "Name: " + str(self.name) + "\n" + "Depression Score: " + str(self.cesd_score) + "\n" + "Ocean Score: " + str(self.ocean_score) + "\nAge: " + str(self.age) + "\nEducation: " + str(self.education) + "\nLocation: " + str(self.location) +"\n"
		return result
def main():
	G = nx.Graph()
	makeGraph(G)
	# print(avg_cesd(G.nodes()))
	centrality_measures(G)
	clustering_measures(G)
	drawGraph(G)
def makeGraph(G):
	nodes = []
	names = """
	Cinthia Knittel
	Jacquline Pitchford
	Thea Speaks
	Alonzo Exline
	Alex Oldenburg
	Joaquina Mickens
	Rosalee Waits
	June Hersom
	Celesta Feldstein
	Sandy Cobbs
	Corrina Deitz
	Brenton Miers
	Candelaria Corrigan
	Noah Brodt
	Agatha Hoefer
	Wynell Blaha
	Jacquie Jorgensen
	Vannessa Vazguez
	Tracee Grubaugh
	Leisa Dynes
	Christina Mcnees
	Tod Bouffard
	America Delany
	Raye Bizzell
	Karey Prall
	Adan Schwartzman
	Karima Serafini
	Rosia Trower
	Clarinda Celestine
	Makeda Armagost
	Flossie Sica
	Verla Pedone
	Catharine Vicari
	Isadora Huneycutt
	Sonja Vesey
	Caleb Hulme
	Aura Briscoe
	Loretta Kappler
	Eusebio Rymer
	Vonnie Eskew
	Lashawn Sarro
	Lakenya Melby
	Gertha Pangburn
	Kiersten Brandel
	Breanna Lawry
	Mason Westerfield
	Carey Ewell
	Angella Spicer
	Kaleigh Basler
	Jetta Pai
	""".strip().split("\n")

	colleges = """
	Villanova University
	Franklin and Marshall College
	Lafayette College
	University of California, Santa Barbara
	University of Florida
	Columbia University
	Whitman College
	Amherst College
	DePauw University
	University of Washington
	Pepperdine University
	College of William and Mary
	Smith College
	College of the Holy Cross
	Pomona College
	United States Military Academy
	George Washington University
	Johns Hopkins University
	Wesleyan University
	Washington and Lee University
	Lehigh University
	Oberlin College
	University of Chicago
	Williams College
	California Institute of Technology
	Duke University
	University of Southern California
	Harvard University
	Tufts University
	Virginia Military Institute
	Dartmouth College
	Hamilton College
	Mount Holyoke College
	University of Georgia
	Rice University
	Reed College
	Stanford University
	University of California, Los Angeles
	Brown University
	Wellesley College
	Colorado College
	University of Richmond
	Boston College
	Bowdoin College
	Trinity College
	Santa Clara University
	Wake Forest University
	Cornell University
	Union College
	Vanderbilt University
	""".strip().split("\n")
	states = """
	List of 50 U.S. State Capitals
	Alabama - Montgomery
	Alaska - Juneau
	Arizona - Phoenix
	Arkansas - Little Rock
	California - Sacramento
	Colorado - Denver
	Connecticut - Hartford
	Delaware - Dover
	Florida - Tallahassee
	Georgia - Atlanta
	Hawaii - Honolulu
	Idaho - Boise
	Illinois - Springfield
	Indiana - Indianapolis
	Iowa - Des Moines
	Kansas - Topeka
	Kentucky - Frankfort
	Louisiana - Baton Rouge
	Maine - Augusta
	Maryland - Annapolis
	Massachusetts - Boston
	Michigan - Lansing
	Minnesota - St. Paul
	Mississippi - Jackson
	Missouri - Jefferson City
	Montana - Helena
	Nebraska - Lincoln
	Nevada - Carson City
	New Hampshire - Concord
	New Jersey - Trenton
	New Mexico - Santa Fe
	New York - Albany
	North Carolina - Raleigh
	North Dakota - Bismarck
	Ohio - Columbus
	Oklahoma - Oklahoma City
	Oregon - Salem
	Pennsylvania - Harrisburg
	Rhode Island - Providence
	South Carolina - Columbia
	South Dakota - Pierre
	Tennessee - Nashville
	Texas - Austin
	Utah - Salt Lake City
	Vermont - Montpelier
	Virginia - Richmond
	Washington - Olympia
	West Virginia - Charleston
	Wisconsin - Madison
	Wyoming - Cheyenne
	""".strip().split("\n")
	# Creating Nodes
	for x in range(0,50):
		node = Node(names[x],rdm.randint(0,60),({"O":rdm.uniform(0.0,1.0),"C":rdm.uniform(0.0,1.0), "E":rdm.uniform(0.0,1.0), "A":rdm.uniform(0.0,1.0), "N":rdm.uniform(0.0,1.0)}),rdm.randint(0,100),colleges[x],states[x])	
		G.add_node(node)
	# Adding Edges

	for node in G.nodes():
		for node1 in G.nodes():
			if rdm.randint(0,5) == 3: 
				if node!= node1: 
					edge = (node,node1)
					G.add_edge(*edge)
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
