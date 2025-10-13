#size=25  text=Bahnschrift
import mysql.connector
import random
db=mysql.connector.connect(host="localhost",user="root",password="OPEN SQL",database="ADMS")
cur=db.cursor() 
#----------------------------------------------------user functions----------------------------------------------------

def idcreator():
    cur.execute("select pass_id from passenger")
    x=cur.fetchall()
    r=""
    while(True):
        c=0
        st=random.randint(1,25)
        l=str(st)
        for i in x:
            if(i[0]==l):
                c+=1
        if(c==0):
            r+=l
            break
    return r
   
def passignup(name,mobile,rdate,add):
         pid=idcreator()
         cmd="insert into passenger values(%s,%s,%s,%s,%s)"
         L=[pid,name,add,mobile,rdate]
         cur.execute(cmd,L)
         db.commit()

def passupdt(pid):
    print("what would you like to change?")
    print("1.name")
    print("2.address")
    print("3.reg date")
    print("4.phone no")
    ch=int(input("enter your choice: "))
    if(ch==1):
        cmd="update passenger set name=%s where pass_id=%s"
        name=input("enter new name: ")
        L=[name,pid]
        cur.execute(cmd,L)
        print("updation complete ")
        print()
        ver=input("would you like to change anything else?[yes/no]: ")
        if(ver=="no"):
            db.commit()
            print("you are all signed up!!")
            mainmenu()
        elif(ver=="yes"):
            passupdt(pid)
    elif(ch==2):
        cmd="update passenger set address=%s where pass_id=%s"
        add=input("enter new address: ")
        L=[add,pid]
        cur.execute(cmd,L)
        print("updation complete ")
        print()
        ver=input("would you like to change anything else?[yes/no]: ")
        if(ver=="no"):
            db.commit()
            print("you are all signed up!!")
            mainmenu()
        elif(ver=="yes"):
            passupdt(pid)
    elif(ch==3):
        cmd="update passenger set rdate=%s where pass_id=%s"
        rdate=input("enter new reg.date(yy-mm-dd): ")
        L=[rdate,pid]
        cur.execute(cmd,L)
        print("updation complete ")
        print()
        ver=input("would you like to change anything else?[yes/no]: ")
        if(ver=="no"):
            db.commit()
            print("you are all signed up!!")
            mainmenu()
        elif(ver=="yes"):
            passupdt(pid)
    elif(ch==4):
        cmd="update passenger set mobile=%s where pass_id=%s"
        mobile=input("enter new number: ")
        L=[mobile,pid]
        cur.execute(cmd,L)
        print("updation complete ")
        print()
        ver=input("would you like to change anything else?[yes/no]: ")
        if(ver=="no"):
            db.commit()
            print("you are all signed up!!")
            mainmenu()
        elif(ver=="yes"):
            passupdt(pid)

def seatchooser(n,ch,fname):
    cur.execute("select seats from ticket where Flight=%s",(fname,))
    x=cur.fetchall()
    Le=[]
    for i in x:
        Le.append(i[0].split())
    #print(Le)
    avail=getremainingseats(ch,fname)
    if(ch==1):
        S=["1-FC","2-FC","3-FC","4-FC","5-FC","6-FC","7-FC","8-FC","9-FC","10-FC","11-FC","12-FC"]
        if(avail<n):
            print("seats not available")
            return []
        St=[]
        for i in S:
            flag=0
            if(Le==[]):
                St=S
                break
            else:
                for j in Le:
                    if(i  not in j):
                        flag=1
                    else:
                        flag=0
                        break
                if(flag==1):
                    St.append(i)
        return St[0:n]          
             
    elif(ch==3):
        S=["1-BC","2-BC","3-BC","4-BC","5-BC","6-BC","7-BC","8-BC","9-BC","10-BC","11-BC","12-BC"]
        if(avail<n):
            print("seats not available")
            return []
        St=[]
        for i in S:
            flag=0
            if(Le==[]):
                St=S
                break
            else:
                for j in Le:
                    if(i  not in j):
                        flag=1
                    else:
                        flag=0
                        break
                if(flag==1):
                    St.append(i)
        return St[0:n] 
    
    elif(ch==2):
        S=["1-EC","2-EC","3-EC","4-EC","5-EC","6-EC","7-EC","8-EC","9-EC","10-EC","11-EC","12-EC"]
        if(avail<n):
            print("seats not available")
            return []
        St=[]
        for i in S:
            flag=0
            if(Le==[]):
                St=S
                break
            else:
                for j in Le:
                    if(i  not in j):
                        flag=1
                    else:
                        flag=0
                        break
                if(flag==1):
                    St.append(i)
        return St[0:n]

def getremainingseats(ch,fname):
    cur.execute("select seats from ticket where Flight=%s",(fname,))
    x=cur.fetchall()
    Le=[]
    for i in x:
        Le.append(i[0].split())
    if(ch==1):
        S=["1-FC","2-FC","3-FC","4-FC","5-FC","6-FC","7-FC","8-FC","9-FC","10-FC","11-FC","12-FC"]
        L=[]
        for i in Le:
            for j in i:
                if(j in S):
                    S.remove(j)
        return len(S)
    elif(ch==3):
        S=["1-BC","2-BC","3-BC","4-BC","5-BC","6-BC","7-BC","8-BC","9-BC","10-BC","11-BC","12-BC"]
        L=[]
        for i in Le:
            for j in i:
                if(j in S):
                    S.remove(j)
        return len(S)
    elif(ch==2):
        S=["1-EC","2-EC","3-EC","4-EC","5-EC","6-EC","7-EC","8-EC","9-EC","10-EC","11-EC","12-EC"]
        L=[]
        for i in Le:
            for j in i:
                if(j in S):
                    S.remove(j)
        return len(S)

def passignin(no):
    cur.execute("select * from passenger")
    x=cur.fetchall()
    c=0
    for i in x:
        if(i[3]==no):
            c+=1
            return True 
    if(c==0):
        return False
               
def getname(no):
    cur.execute("select name from passenger where mobile=%s",(no,))
    x=cur.fetchall()
    for i in x:
        return i[0] 

def getid(no):
    cur.execute("select pass_id from passenger where mobile=%s",(no,))
    x=cur.fetchall()
    for i in x:
        return i[0]
    
def hasbooked(no):
    id=getid(no)
    cur.execute("select * from ticket where pass_id=%s",(id,))
    x=cur.fetchall()
    if(x==[]):
        return False
    else:
        return True
          
def getdestinations(source):
    cmd="select Going_to from schedule where Leave_from=%s"
    L=[source]
    cur.execute(cmd,L)
    x=cur.fetchall()
    return x   

def getflights(source,destination):
    cmd="select Flight,Date,status,Leave_from,Going_to from schedule where Leave_from=%s and Going_to=%s"
    L=(str(source),str(destination[0]))
    cur.execute(cmd,L)
    return cur.fetchall()

def getclass():
    cur.execute("select * from classtype order by sno")
    return cur.fetchall()

def getseat_info(ch):
    cur.execute("select * from classtype where item_name=%s",(ch,))
    return cur.fetchone()

def getseats(n,ch,fname):
    return seatchooser(n,ch,fname)

def booktickets(id,name,fl,dep,arr,cls,date,rate1,rate2,srate,total,st):
    try:
        cmd="insert into ticket values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        L=[id,name,fl,dep,arr,cls+" class",date,rate1,rate2,srate,total,st]
        cur.execute(cmd,L)
        db.commit()
        return True
    except:
        return False
    
def getticket(id):
    cur.execute("select * from ticket where pass_id=%s",(id,))
    return cur.fetchall()

def cancelticket(id):
    try:
        cmd="delete from ticket where pass_id=%s"
        L=[id]
        cur.execute(cmd,L)
        db.commit()
        return True
    except:
        return False

def getstatus(id):
    cur.execute("select Flight,Leave_from,Going_to,Date,status from schedule natural join ticket where pass_id=%s",(id,))
    return cur.fetchall()

def getflightname(fl):
    if(fl[0:2] in "AI"):
        return "AIR INDIA AIRWAYS"
    elif(fl[0:2] in "ET"):
        return "ETIHAD AIRWAYS"
    elif(fl[0:2] in "EM"):
        return "EMIRATES AIRWAYS"
    elif(fl[0:2] in "IN"):
        return "INDIGO AIRWAYS"
  
def get_luggage(sno):
    if(sno==0):
        cur.execute("select * from luggage order by sno")
        return cur.fetchall()
    cur.execute("select * from luggage where sno=%s",(sno,))
    return cur.fetchone()
    
# print(getflights("kannur",("dubai",)))
# print(getclass())
# print(getseats(3,1))
# print(getticket(12))   
  


                
                     
###################################################################################

     
 

     
    
    
    

    
    
        
        

   
    
    

    
    
        
        

