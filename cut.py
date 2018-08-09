from __future__ import division
import sys, os
import commands
from scipy.spatial.distance import pdist, squareform


class Hierarchical:
    def __init__(self, ivector, left = None, right = None, flag = None, plda = 0.0):
        self.ivector = ivector
        self.left = left
        self.right = right
        self.flag = flag
        self.plda = plda


def get_arr(f):
        arr=[]
        for eachline in open(f):
                line=eachline.rstrip('\r\n\t ')
                arr.append(float(line))
        return  arr

def traverse(node):
    if node.left == None and node.right == None:
        return [node.flag]
    else:
        return traverse(node.left) + traverse(node.right)

def traverse_plda(v1,k,pred):

    arr=get_arr(sys.argv[4])
    plda_matrix=squareform(arr,force='tomatrix',checks=True)
    
    flag_list= [int(i) for i in pred]
    l=[]
    for i in flag_list:
        if plda_matrix[i][v1] > k:
            print v1,i,plda_matrix[i][v1]
            l.append(plda_matrix[i][v1])
        else:
            print v1,i,plda_matrix[i][v1] 
    return len(l)/len(flag_list) 
def average_plda(f,data):
	arr=[]
        for eachline in open(f):
                line=eachline.rstrip('\r\n\t ')
		arr=line.split(' ')
		arr=[int(i) for i in arr]
	print "arr"
        print arr
        sumIvector=[0]*len(data[1])
        print sumIvector
	for i in arr:
		sumIvector = [(data[i][j] + sumIvector[j]) for j in range(len(data[i]))]
	print sumIvector
        newIvector=[i/len(arr) for i in sumIvector]
	return newIvector
	

def hcluster(data,pred,k,percent):
	if len(data) <= 0:
		print sys.stderr, "invalid data"
		sys.exit(1)

	clusters=[Hierarchical(data[i], flag = i) for i in pred]
	
	res=[traverse(clusters[i]) for i in range(len(clusters))]
        record=[]
	for i in res:
		for j in i:
			if traverse_plda(j,k,pred) >= percent:
				print traverse_plda(j,k,pred)
				record.append(j)
			elif traverse_plda(j,k,pred) < percent:
				print traverse_plda(j,k,pred)
				 
                		
			
	
	return record


def get_cluster(f):
        for eachline in open(f):
                line=eachline.rstrip('\r\n\t ')
		arr=line.split(' ')
	return arr

def get_matrix(f):
        ivector_matrix=[]
        for eachline in open(f):
                line = eachline.rstrip('\r\t\n ')
                ivector_matrix.append(line.split(' '))
                #print ivector_matrix
        list_to_float = []
        for each in ivector_matrix:
                each_line=list(map(lambda x: float(x), each))
                list_to_float.append(each_line)
        #print list_to_float
        return list_to_float

if __name__ == '__main__':

    data=get_matrix(sys.argv[1])
  
    pred = get_cluster(sys.argv[2])
    k=8
    pred=[int(i) for i in pred]
 
    percent=0.7
    res=hcluster(data,pred,k,percent)
    print res
    if len(res)>4:
    	cut_result=open(sys.argv[3],'w')
    	for i in res:
        	cut_result.write(str(i)+' ')
    	cut_result.close()
