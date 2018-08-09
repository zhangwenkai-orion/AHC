from __future__ import division
import sys,os
import numpy as np
def plda(v1, v2):
    if len(v1) != len(v2):
        print sys.stderr, "invalid v1 and v2 !"
        sys.exit(1)
    plda = 0
    f1=open('v1','w')
    f2=open('v2','w')
    for i in range(len(v1)-1):
        f1.write(str(v1[i])+' ')
    f1.write(str(v1[-1]))
    for i in range(len(v2)-1):
        f2.write(str(v2[i])+' ')
    f2.write(str(v2[-1]))
    f1.close()
    f2.close()
    os.system('./plda_scoring plda v1 v2 score')
    score=os.popen('cat score')
    plda=float(score.readline())
    #os.system('rm' + ' ' + arg6)


    return plda
def hcluster(data,l):
    if len(data) <= 0:
        print sys.stderr, "invalid data"
        sys.exit(1)
    sum_ivector=[float(0)]*len(data[0])
    sum_ivector=np.array(sum_ivector)
    print sum_ivector
    for i in l:
       sum_ivector+=np.array(data[i])
    print sum_ivector
    ivector=[sum_ivector[i]/len(data[0]) for i in range(len(sum_ivector))]
    print ivector
    return ivector
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
#cluster


if __name__ == '__main__':

	data = get_matrix(sys.argv[3])
	
	for eachline in open(sys.argv[1]):
                line = eachline.rstrip('\r\t\n ')
                l= line.split(' ')
		l=[int(i) for i in l]
	
	for eachline1 in open(sys.argv[2]):
                line1 = eachline1.rstrip('\r\t\n ')
                l1= line1.split(' ')
                l1=[int(i) for i in l1]
	v1=hcluster(data,l)
	add_utt=[]
	for i in l1:
		score=plda(v1,data[i])
		if score > 8:
			add_utt.append(i)
	l=l+add_utt
	f=open(sys.argv[1],'w')
	for i in range(len(l)-1):
		f.write(str(l[i])+' ')
	f.write(str(l[-1])+'\n')

	
