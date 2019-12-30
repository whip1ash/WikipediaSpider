import json
from py2neo import Node, Relationship, Graph, NodeMatcher
import os

class Neo4j:
	def __init__(self):
		try:
			graph = Graph('127.0.0.1:7687', user='neo4j',password='qwer1234')
		except:
			print("connect neo4j failed!")
			os._exit()
		
		graph.delete_all()
		self.matcher = NodeMatcher(graph)
		self.graph = graph
		
		print("init neo4j success")

def import_json(file_dir):
	data = list()
	
	with open(file_dir) as f:
		for line in f:
			if line[-2] == ',':
				json_data = line[:-2]
			else:
				json_data = line
				
			json_object = json.loads(json_data)
			data.append(json_object)
	return data

def insert_data(data):
	for obj in data:
		print(obj)
		insert_one_data(obj)
		
def insert_one_data(json_object):
	start = look_and_create(json_object["entity"])
	if json_object["sonNode"]:
		for node in json_object["sonNode"]:
			end = look_and_create(node)
			relation = Relationship(start,"connect",end)
			neo4j.graph.create(relation)
	
def look_and_create(name):
	node = neo4j.matcher.match("Test", name=name).first()
	if node is None:
		node = Node('Test', name=name)           
	return node


if __name__ == "__main__":
	neo4j = Neo4j()
	result = import_json("/Users/Whip1ash/Code/KM/Wikipedia_Spider/output.json")
	insert_data(result)
		
		