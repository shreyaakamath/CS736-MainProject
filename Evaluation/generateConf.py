import os 

if __name__ == "__main__":
    
    s=0
    T=24
    units=3600
    A=10
    B=10
    m=180
    mu=2
    prob=0.2
    thresh=5
    basefile="baseForGen.conf"
    
    with open(basefile) as f:
        content = f.readlines()
    
    #Vary T value 
    list=[3,6,12,24,48,96]
    for i in list:
        for s in range(0,4):
            outfile="confFiles/"+str(i)+"-A-"+str(A)+"-B-"+str(B)+"-S-"+str(s)+".conf"
            firstLine=str(s)+","+str(i)+","+str(units)+","+str(A)+","+str(B)+","+str(m)+","+str(mu)+","+str(prob)+","+str(thresh)+"\n"
            with open(outfile,"w+") as f1:
                f1.write(firstLine)
                for line in content:
                    f1.write(line)
    
    #vary A value
    list=[0,10,20,30,40,50,60,70,80,90,100]
    for i in list:
        for s in range(0,4):
            outfile="confFiles/"+str(T)+"-A-"+str(i)+"-B-"+str(B)+"-S-"+str(s)+".conf"
            firstLine=str(s)+","+str(T)+","+str(units)+","+str(i)+","+str(B)+","+str(m)+","+str(mu)+","+str(prob)+","+str(thresh)+"\n"
            with open(outfile,"w+") as f1:
                f1.write(firstLine)
                for line in content:
                    f1.write(line)
                    
    #vary B value
    list=[0,10,20,30,40,50,60,70,80,90,100]
    for i in list:
        for s in range(0,4):
            outfile="confFiles/"+str(T)+"-A-"+str(A)+"-B-"+str(i)+"-S-"+str(s)+".conf"
            firstLine=str(s)+","+str(T)+","+str(units)+","+str(A)+","+str(i)+","+str(m)+","+str(mu)+","+str(prob)+","+str(thresh)+"\n"
            with open(outfile,"w+") as f1:
                f1.write(firstLine)
                for line in content:
                    f1.write(line)
    
