import sys, os
import commands
#import numpy as np
from scipy.spatial.distance import pdist, squareform

class Hierarchical:
    def __init__(self, ivector, left = None, right = None, flag = None, plda = 0.0,num=1):
        self.ivector = ivector
        self.left = left
        self.right = right
        self.flag = flag
        self.plda = plda
        self.num = num
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

def traverse_plda(node1,node2,plda_matrix):
    min_plda=1000
    #plda_matrix=get_arr('dist')
    
    #plda_matrix=squareform(plda_matrix,force='tomatrix',checks=True)
    #plda_matrix=[[0,9.7,13.34],
	#	[9.7,0,10.23],
	#	[13.34,10.23,0]]
    flag_list_1= traverse(node1)
    flag_list_2= traverse(node2)
    print flag_list_1,flag_list_2
    l=[]
    for i in flag_list_1:
        for j in flag_list_2:
            #print plda_matrix[j][i]
            if plda_matrix[j][i]<min_plda:
                min_plda=plda_matrix[j][i]
                print "*******"
                print min_plda,j,i
            l.append(plda_matrix[j][i])
    
    return min(l)



def plda(v1, v2):#plda_score flag?
    if len(v1) != len(v2):
        print sys.stderr, "invalid v1 and v2 !"
        sys.exit(1)
    plda = 0
    f1=open(sys.argv[4],'w')
    f2=open(sys.argv[5],'w')
    for i in range(len(v1)-1):
        f1.write(str(v1[i])+' ')
    f1.write(str(v1[-1]))
    for i in range(len(v2)-1):
        f2.write(str(v2[i])+' ')
    f2.write(str(v2[-1]))
    f1.close()
    f2.close()
    arg4=sys.argv[4]
    arg5=sys.argv[5]
    arg6=sys.argv[6]
    os.system('./plda_scoring plda' +' '+arg4+' '+ arg5+' '+ arg6)    
    score=os.popen('cat'+' '+ arg6)
    plda=float(score.readline())
    os.system('rm' + ' ' + arg6)
    
    
    return plda


def hcluster(data):
    if len(data) <= 0:
        print sys.stderr, "invalid data"
        sys.exit(1)


    clusters = [Hierarchical(data[i], flag = i) for i in range(len(data))]
    #print data[1].ivector
    plda_dict = {}
    max_id1 = None
    max_id2 = None
    currentCluster = -100
    count=0
    maxDist = 19
    #while(len(clusters) > n ):
    while (maxDist > 12):    
        maxDist = -10000000
        for i in range(len(clusters) - 1 - count):
            
       
            for j in range(i + 1, len(clusters) - count):
                   
                if plda_dict.get((clusters[i].flag, clusters[j].flag)) == None:
                    plda_dict[(clusters[i].flag, clusters[j].flag)] = plda(clusters[i].ivector, clusters[j].ivector)


                if plda_dict[(clusters[i].flag, clusters[j].flag)] >= maxDist:
                    max_id1 = i
                    max_id2 = j
                    maxDist = plda_dict[(clusters[i].flag, clusters[j].flag)]
      
        if max_id1 != None and max_id2 != None and maxDist > 12:
            count+=1
            print max_id1,max_id2,maxDist
            newnum=clusters[max_id1].num+clusters[max_id2].num
            newIvector = [(clusters[max_id1].ivector[i] * clusters[max_id1].num+ clusters[max_id2].ivector[i] * clusters[max_id2].num)/newnum for i in range(len(clusters[max_id2].ivector))]
            newFlag = currentCluster
            print newFlag
            currentCluster -= 1
            newCluster = Hierarchical(newIvector, clusters[max_id1], clusters[max_id2], newFlag, maxDist,newnum)
            del clusters[max_id2]
            del clusters[max_id1]
            clusters.append(newCluster)
    
    print clusters
    return clusters


def hcluster_global(clusters,plda_matrix):
    if len(clusters) <= 0:
        print sys.stderr, "invalid data"
        sys.exit(1)
    
    #print data[1].ivector
    min_dict = {}
    max_id1 = None
    max_id2 = None
    currentCluster = -100
    count=0
    maxDist = 11
    #while(len(clusters) > n ):
    while (maxDist > 8):
        maxDist=8
        #oldclusters=clusters
        
        for i in range(len(clusters) - 1 - count):
            for j in range(i + 1, len(clusters) - count ):
                if min_dict.get((clusters[i].flag, clusters[j].flag)) == None:
                    min_dict[(clusters[i].flag, clusters[j].flag)] = traverse_plda(clusters[i], clusters[j],plda_matrix)

        
                if min_dict[(clusters[i].flag, clusters[j].flag)] >= maxDist:
                  
                    max_id1 = i
                    max_id2 = j
                    maxDist = min_dict[(clusters[i].flag, clusters[j].flag)]
        print max_id1,max_id2
        if max_id1 != None and max_id2 != None and maxDist > 8:
            		
            count+=1
            newnum=clusters[max_id1].num+clusters[max_id2].num
            newIvector = [(clusters[max_id1].ivector[i] * clusters[max_id1].num+ clusters[max_id2].ivector[i] * clusters[max_id2].num)/newnum for i in range(len(clusters[max_id2].ivector))]
          
            newFlag = currentCluster
            print newFlag
            currentCluster -= 1
            newCluster = Hierarchical(newIvector, clusters[max_id1], clusters[max_id2], newFlag, maxDist,newnum)
            del clusters[max_id2]
            del clusters[max_id1]
            clusters.append(newCluster)
        
    #if oldclusters==clusters:
         #   break
    
    return clusters

def hcluster_final(clusters):
    
    plda_dict = {}
    max_id1 = None
    max_id2 = None
    currentCluster = -100
    count=0
    maxDist = 19
    #while(len(clusters) > n ):
    while (maxDist > 12):
        maxDist = -10000000
        for i in range(len(clusters) - 1 - count):


            for j in range(i + 1, len(clusters) - count):

                if plda_dict.get((clusters[i].flag, clusters[j].flag)) == None:
                    plda_dict[(clusters[i].flag, clusters[j].flag)] = plda(clusters[i].ivector, clusters[j].ivector)


                if plda_dict[(clusters[i].flag, clusters[j].flag)] >= maxDist:
                    max_id1 = i
                    max_id2 = j
                    maxDist = plda_dict[(clusters[i].flag, clusters[j].flag)]

        if max_id1 != None and max_id2 != None and maxDist > 12:
            count+=1
            print max_id1,max_id2,maxDist
            newnum=clusters[max_id1].num+clusters[max_id2].num
            newIvector = [(clusters[max_id1].ivector[i] * clusters[max_id1].num+ clusters[max_id2].ivector[i] * clusters[max_id2].num)/newnum for i in range(len(clusters[max_id2].ivector))]
            newFlag = currentCluster
            print newFlag
            currentCluster -= 1
            newCluster = Hierarchical(newIvector, clusters[max_id1], clusters[max_id2], newFlag, maxDist,newnum)
            del clusters[max_id2]
            del clusters[max_id1]
            clusters.append(newCluster)


    return clusters

def morethan12(clusters):
	for i in range(len(clusters)-1):
		for j in range(i+1,len(clusters)):
			score=plda(clusters[i].ivector,clusters[j].ivector)
			print score
			if score < 12:				
				return False
	return True

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
    #data = [[123,321,434,4325,345345],[23124,141241,434234,9837489,34743],\
    #[128937,127,12381,424,8945],[322,4348,5040,8189,2348],\
    #[51249,42190,2713,2319,4328],[13957,1871829,8712847,34589,30945],\
    #[1234,45094,23409,13495,348052],[49853,3847,4728,4059,5389]]
    #finalCluster = hcluster(data, 7)
    #print finalCluster


    plda_matrix=get_arr(sys.argv[3])

    plda_matrix=squareform(plda_matrix,force='tomatrix',checks=True)
    #print plda_matrix
    data = get_matrix(sys.argv[1])
    #print data[1]
    clusters=hcluster(data)
    #old_len=0
    #while(len(clusters)!=old_len):
    for i in range(10):
    	clusters = hcluster_global(clusters,plda_matrix)
    old_len=0
    while(len(clusters)!=old_len):
        old_len=len(clusters)
        clusters = hcluster_final(clusters)
        
    finalCluster = [traverse(clusters[i]) for i in range(len(clusters))]
    print finalCluster
    f=open(sys.argv[2],'w')
    for i in range(len(clusters)):
        f.write(str(traverse(clusters[i]))+'\n')
    f.close()




