f = open("0024.note",'r')             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
i=0
q=line.split()
time=float(q[1])
pitch=float(q[3])
tmp=[time,pitch]
list=[]
list=[tmp]

while line:
    #print(line)
    i=i+1	
    line = f.readline()
    if line:
        q=line.split()
        time=float(q[1])
        pitch=float(q[3])
        tmp=[time,pitch]
        list.append(tmp)
print(list)
print(list[0][0])
print(type(list[0][0]))