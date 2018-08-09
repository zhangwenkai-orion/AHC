import sys
l=[]
for eachline in open(sys.argv[1]):
	line=eachline.rstrip('\n\t\r ')
	sid,num=line.split(' ')
	l.append(sid)
for eachline in open(sys.argv[2]):
	line=eachline.rstrip('\n\r\t ')
	cluster=line.split(' ')
	cluster=[int(i) for i in cluster]
true=[]
for i in cluster:
	true.append(l[i])

f=open(sys.argv[2],'w')
for i in true:
	f.write(str(i)+' ')	



