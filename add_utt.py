import sys
for eachline in open(sys.argv[1]):
	line=eachline.rstrip('\n\t\r ')
	full=line.split(' ')
	
for eachline1 in open(sys.argv[2]):
        line1=eachline1.rstrip('\n\t\r ')
        big=line1.split(' ')
small=[]
for i in full:
	if i  not in big:
		small.append(i)
f=open(sys.argv[3],'w')
for i in range(len(small)-1):
	f.write(str(small[i])+' ')
f.write(str(small[-1])+'\n')
