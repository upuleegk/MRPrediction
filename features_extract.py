#!/usr/bin/python
import networkx as nx
import pygraphviz
import nx_pydot as pydot
import glob
import os
import sys
import numpy as np
import networkx.algorithms.simple_paths as simple_paths

def write_feature_mapping_to_file():
        data_file=open('/home/rahman/Documents/MT/current_feature_set.txt','a+')
        the_data = data_file.read()
        for i in feature_list:
                index = the_data.find(i)
                if index == -1:
					data_file.write(i + ": " + str(feature_list[i]) + '\n')

        data_file.close()
        
def find_node_counts(fileName):

        cfg=pydot.read_dot(fileName)
        #Find the number of weakly connected components in the CFG
        c=nx.number_weakly_connected_components(cfg)

        #create a list node,indegree,outdegree
        data=[]
        n=cfg.nodes()
        edge=cfg.edges()
        for i in edge:
			a=cfg.get_edge_data(*i)
			if(str(a).find('DD')!=-1):
				cfg.remove_edge(*i)
        #get_node_labels(cfg)
        node_labels=get_node_labels(cfg)
        
        
        for x in node_labels:
                y=str(node_labels[x])+'-'+str(cfg.in_degree(x))+'-'+str(cfg.out_degree(x))                       
                data.append(y)
                #print y

        #create a set from the list to get the non repeating features
        feature=set(data)
        #create a dictionary with the feature node, indegree, outdegree and the counmt
        feature_counts={}
        #print data

        for i in feature:
                feature_counts[i]=0
        #print feature_counts

        for i in data:
                feature_counts[i]=feature_counts[i]+1
        #print feature_counts
        return feature_counts
        
def get_node_counts(path):
        
        path="/home/rahman/Documents/MT/dotfiles/"
        node_data={}
        
        for file in os.listdir(path):
                newfile=path+file
                node_data[file]=find_node_counts(newfile)
        #print node_data
        return node_data

def get_path_in_labels(path,node_labels):
        path_labels=''
        for n in path:
                label=node_labels[n]
                path_labels+=str(label)+'-'
        return path_labels


def find_paths_from_start(file_name):
        
        file_name = '/home/rahman/Documents/MT/dotfiles/' + file_name
        cfg=pydot.read_dot(file_name)
        nodes=cfg.nodes()
        edge=cfg.edges()
        for i in edge:
			a=cfg.get_edge_data(*i)
			if(str(a).find('DD')!=-1):
				cfg.remove_edge(*i)
        for n in nodes:
                pred=cfg.predecessors(n)
                if(len(pred)==0):
                        start=n
        
        paths_from_start=nx.shortest_path(cfg,start)    
        node_labels=get_node_labels(cfg)

        all_paths_from_start_names=[]
        for i in paths_from_start:
                all_paths_from_start_names.append(get_path_in_labels(paths_from_start[i],node_labels))
        
        
        start_path_names=set(all_paths_from_start_names)
        start_name_path_counts={}

        for i in start_path_names:
                start_name_path_counts[i]=0

        for i in all_paths_from_start_names:
                start_name_path_counts[i]+=1
  

        return start_name_path_counts

        
def find_paths_to_end(file_name):
       
        file_name = '/home/rahman/Documents/MT/dotfiles/' + file_name
        cfg=pydot.read_dot(file_name)
        nodes=cfg.nodes()
        edge=cfg.edges()
        for i in edge:
			a=cfg.get_edge_data(*i)
			if(str(a).find('DD')!=-1):
				cfg.remove_edge(*i)
        ends=[]
        for n in nodes:
                succ=cfg.successors(n)
                if(len(succ)==0):
                        ends.append(n)
        
        all_paths_to_end=[]
        
        for i in ends:
                for n in nodes:
                        try:
                                path=nx.shortest_path(cfg,source=n,target=i)
                                all_paths_to_end.append(path)
                        except nx.exception.NetworkXNoPath:
                                var = 1
        
        
        node_labels=get_node_labels(cfg)

        all_paths_to_end_names=[]
        for i in all_paths_to_end:
                all_paths_to_end_names.append(get_path_in_labels(i,node_labels))
        
        end_path_names=set(all_paths_to_end_names)
        end_name_path_counts={}

        for i in end_path_names:
                end_name_path_counts[i]=0

        for i in all_paths_to_end_names:
                end_name_path_counts[i]+=1
       

        return end_name_path_counts


def get_start_to_node_path_data(path):

        path = '/home/rahman/Documents/MT/dotfiles/'
        start_to_node_path_name_data={}
        dirs = os.listdir(path)
        for filename in dirs:
                paths=find_paths_from_start(filename)
                start_to_node_path_name_data[filename]=paths 
        #print start_to_node_path_name_data      
        return start_to_node_path_name_data
        
def get_node_to_end_path_data(path):

        path = '/home/rahman/Documents/MT/dotfiles/'
        node_to_end_path_name_data={}
        dirs = os.listdir(path)
        for filename in dirs:
                paths=find_paths_to_end(filename)
                node_to_end_path_name_data[filename]=paths
        
        #print node_to_end_path_name_data       
        return node_to_end_path_name_data      

def get_all_simple_paths(file_name):
        file_name = '/home/rahman/Documents/MT/dotfiles/' + file_name
        G=pydot.read_dot(file_name)
        edge=G.edges()
        for i in edge:
			a=G.get_edge_data(*i)
			if(str(a).find('DD')!=-1):
				G.remove_edge(*i)
        result = []
       
        for paths in (simple_paths.all_simple_paths(G, n, target) for n in G.nodes_iter() for target in G.nodes_iter()):
                result+=paths
        
        node_labels=get_node_labels(G)    
        named_paths=[]
        for i in result:
                named_paths.append(get_path_in_labels(i,node_labels))

        unique_simple_paths=set(named_paths)
        simple_path_counts={}
        
        for i in unique_simple_paths:
                simple_path_counts[i]=0

        for i in named_paths:
                simple_path_counts[i]+=1
                
        #print simple_path_counts
        return simple_path_counts


def calc_simple_paths_for_all_files(dot_file):
        
        path = '/home/rahman/Documents/MT/dotfiles/'
        simple_path_name_data={}
        
        
        simple_paths=get_all_simple_paths(dot_file)
        simple_path_name_data[dot_file]=simple_paths
        
        return simple_path_name_data

def getOp(myName):

        if(myName.find('=')==-1):
                print myName
		return 'ERROR'
        else:
                if(myName.find('+')!=-1):
                        return 'ADD'
                elif(myName.find('-')!=-1):
                        return 'SUB'
                elif(myName.find('&')!=-1):
                        return 'AND'
                elif(myName.find('cmp')!=-1):
                        return 'CMP'
                elif(myName.find('cmpg')!=-1):
                        return 'CMPG'
                elif(myName.find('cmpl')!=-1):
                        return 'CMPL'
                elif(myName.find('/')!=-1):
                        return 'DIV'
                elif(myName.find('==')!=-1):
                        return 'EQL'
                elif(myName.find('>=')!=-1):
                        return 'GEQL'
                elif(myName.find('>')!=-1):
                        return 'GT'
                elif(myName.find('<=')!=-1):
                        return 'LEQL'
                elif(myName.find('<')!=-1):
                        return 'LT'
                elif(myName.find('*')!=-1):
                        return 'MUL'
                elif(myName.find('!=')!=-1):
                        return 'NEQL'
                elif(myName.find('|')!=-1):
                        return 'OR'
                elif(myName.find('%')!=-1):
                        return 'REM'
                elif(myName.find('<<')!=-1):
                        return 'SHL'
                elif(myName.find('>>')!=-1):
                        return 'SHR'
		elif(myName.find('xor')!=-1):
                        return 'XOR'
                else:
                        return 'ASSI'


def get_node_labels(G):
        nodes=G.nodes()
        node_names=nx.get_node_attributes(G,'label')
        #print node_names
        node_labels={}

        for n in nodes:
                myName=node_names[n]
                if(myName.find('if')!=-1):
                        nodeLabel='IF'
                elif(myName.find(':=')!=-1):
                        nodeLabel='IDEN_STMT'
                elif(myName.find('goto')==0 or myName.find('goto')==1 ):
                        nodeLabel='GOTO'
                elif(myName.find('exit')!=-1):
                        nodeLabel='EXIT'
                elif(myName.find('return')!=-1):
                        nodeLabel='RETURN'
                elif(myName.find('(')!=-1 and myName.find(')')!=-1 and (myName.find('double')!=-1 or myName.find('float')!=-1 or myName.find('int')!=-1)):
                        nodeLabel='ASSI'
                elif(myName.find('(')!=-1 and myName.find(')')!=-1):
            
                        nodeLabel='FCALL'
                else:
                        nodeLabel=getOp(myName)
                node_labels[n]=nodeLabel
        return node_labels


path = '/home/rahman/Documents/MT/dotfiles/'
dirs = os.listdir(path) 


feature_list={}
feature_count=0

with open('/home/rahman/Documents/MT/current_feature_set.txt', 'r') as f:
    for line in f:
        index = line.find(':')
        feature = line[0:index]
        count = line[index+2:]
        count = count.strip('\n')
        feature_list[feature] = count


for dot_file in dirs:
    #print dot_file

    node_data=get_node_counts(dot_file)
    node_feature_list=set()
    path_length_feature_list=set()
    start_path_name_feature_list=set()
    end_path_name_feature_list=set()
    simple_path_feature_list=set()

    feature_list={}
    feature_count=0
    prog_names=[]

    for i in node_data:
        for j in node_data[i]:
			node_feature_list.add(j)
           
    for i in node_feature_list:
        feature_list[i]=feature_count
        feature_count+=1
    #print node_data
    

    start_path_name_data=get_start_to_node_path_data(dot_file)
    #print start_path_name_data
    for i in start_path_name_data:
        for j in start_path_name_data[i]:
            start_path_name_feature_list.add(j)

    for i in start_path_name_feature_list:
        feature_list[i]=feature_count
        feature_count+=1

    end_path_name_data=get_node_to_end_path_data(dot_file)
    #print end_path_name_data
    for i in end_path_name_data:
        for j in end_path_name_data[i]:
            end_path_name_feature_list.add(j)


    for i in end_path_name_feature_list:
        feature_list[i]=feature_count
        feature_count+=1


    simple_path_data=calc_simple_paths_for_all_files(dot_file)

    #print simple_path_data
    
    for i in simple_path_data:
        for j in simple_path_data[i]:
            simple_path_feature_list.add(j)

    for i in simple_path_feature_list:
        feature_list[i]=feature_count
        feature_count+=1


   
    file_name = "/home/rahman/Documents/MT/MethodFeatures/" + dot_file 
    data_file = open(file_name, 'w')

   
    my_str=str(dot_file)+',  '
    for f in node_data[dot_file]:
        my_str+= str(feature_list[f])+':'+str(node_data[dot_file][f])+' '

    for spn in start_path_name_data[dot_file]:
        my_str+=str(feature_list[spn])+':'+str(start_path_name_data[dot_file][spn])+' '

    for epn in end_path_name_data[dot_file]:
        my_str+=str(feature_list[epn])+':'+str(end_path_name_data[dot_file][epn])+' '
    
    for sp in simple_path_data[dot_file]:
        my_str+=str(feature_list[sp])+':'+str(simple_path_data[dot_file][sp])+' '
    
    data_file.write(my_str+'\n')        

    data_file.close()

    write_feature_mapping_to_file()

    


print "Done"

