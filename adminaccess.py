#-----------------------------------------------------admin functions----------------------------------------------------------
import mysql.connector
db=mysql.connector.connect(host="localhost",user="root",password="OPEN SQL",database="ADMS")
cur=db.cursor() 
def adminmenu():
    print()
    print("ADMIN MENU")
    print("------------->")
    print()
    print("1.add to schedule")
    print("2.update schedule")
    print("3.add to classtype")
    print("4.update class ")
    print("5.remove passenger data")
    print("6.add new luggage data")
    print("7.update existing luggage rate")
    print("8.view/remove ticket records")
    print("9.return to main menu")
    print()
    ch=int(input("enter your choice: "))
    if(ch==1):
        adminaddsche()
    elif(ch==2):
        adminupdt()
    elif(ch==3):
        adminaddclrate()
    elif(ch==4):
        adminupdtcltype()
    elif(ch==5):
        adminpassremove()
    elif(ch==6):
        adminluggage()
    elif(ch==7):
        adminupdtluggage()
    elif(ch==8):
        adminticketupdt()
    elif(ch==9):
        print()
        print('returning to main menu')
        mainmenu()()
    else:
        print("invalid choice")
        adminmenu()  
def adminticket(id,fl,dep,arr,dte,cls,rate,name,nrate,z,l,st):
    #cur.execute("create table ticket(pass_id char(3) primary key,pass_name varchar(35),Flight char(6),departure varchar(25),arrival varchar(25),class varchar(20),date_of_dept date,extra_luggage varchar(5),luggage_rate int,seat_rate int,total_rate int,seats varchar(40))")
    cmd="insert into ticket values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    L=[id,name,fl,dep,arr,cls,dte,l,z,rate,nrate,st]
    cur.execute(cmd,L)
    db.commit()
    print("your ticket has been booked successfully!!")
    menu2(id)
    
def adminaddsche():
    #cur.execute("create table schedule(Flight  varchar(8) ,Leave_from varchar(20),Going_to varchar(20),Date date,status varchar(20))")
    cmd="insert into schedule values(%s,%s,%s,%s,%s)"
    while(True):
         Flight=input("enter flight id: ")
         Leave_from=input("enter departure destination: ")
         Going_to=input("enter arrival destination: ")
         Date=input("enter the date(yy-mm-dd): ")
         status=input("enter flight status: ")
         L=[Flight,Leave_from,Going_to,Date,status]
         cur.execute(cmd,L)
         print("successfully added")
         print()
         print("press 1 to add more")
         print("press 2 to stop and save")
         ch=int(input("enter your choice: "))
         print()
         if(ch==2):
             print("records added succesfully")
             break
    db.commit()
    cur.close()
    adminmenu()
    
def adminupdt():
    cur.execute("Select Flight,Date,Status from schedule order by Date desc")
    x=cur.fetchall()
    print("Flight id","\t\t","Date","\t\t","Status")
    for i in x:
        print(i[0],"\t\t",i[1],"\t\t",i[2])
    f_id=input("enter flight id to be modified: ")
    ch=input("enter update parameter (departure,arrival,date,status,all): ")
    if(ch=="departure"):
        cmd="update schedule set Leave_from=%s where Flight=%s"
        dept=input("enter new departure destination: ")
        L=[dept,f_id]
        cur.execute(cmd,L)
        print("successfully updated departure location for Flight ",f_id)
    elif(ch=="arrival"):
        cmd="update schedule set Going_to=%s where Flight=%s"
        arr=input("enter new arrival destination: ")
        L=[arr,f_id]
        cur.execute(cmd,L)
        print("successfully updated arrival destination for Flight ",f_id)
    elif(ch=="date"):
        cmd="update schedule set date=%s where Flight=%s"
        date=input("enter new date(yy-mm-dd): ")
        L=[date,f_id]
        cur.execute(cmd,L)
        print("successfully updated date for Flight ",f_id)
    elif(ch=="status"):
        cmd="update schedule set status=%s where Flight=%s"
        stat=input("enter new status: ")
        L=[stat,f_id]
        cur.execute(cmd,L)
        print("status successfully updated for Flight ",f_id)
    elif(ch=="all"):
        nfid=input("enter new flight id: ")
        dept=input("enter new departure destination: ")
        arr=input("enter new arrival destination: ")
        date=input("enter new date(yy-mm-dd): ")
        stat=input("enter new status: ")
        L=[nfid,dept,arr,date,stat,f_id]
        cmd="update schedule set Flight=%s,Leave_from=%s,Going_to=%s,Date=%s,status=%s where Flight=%s"
        cur.execute(cmd,L)
        print("Flight details updated successfully for ",f_id)
    else:
        print("invalid entry")
    db.commit()
    adminmenu()
    
def adminaddclrate():
    #cur.execute("create table classtype(sno int(5),item_name varchar(25),rate int(11),status varchar(15))")
    cmd="insert into classtype values(%s,%s,%s,%s)"
    while(True):
         sno=input("serial number: ")
         cls=input("enter class: ")
         rate=input("enter rate: ")
         status=input("enter class status: ")
         L=[sno,cls,rate,status]
         cur.execute(cmd,L)
         print("successfully added")
         ch=input("add more?(yes/no)")
         if(ch=="no"):
                print("records added succesfully")
                break
    db.commit()
    adminmenu()
def mainmenu():
    print()
    print("ADMIN MENU")
    print("----------->")
    print()
    pas=int(input("enter admin password: "))
    if(pas==12345):
            print()
            print("welcome to admin menu...")
            print()
            adminmenu()
    else:
            print()
            print("***invalid password***")
            mainmenu()

def adminupdtcltype():
    cur.execute("select * from classtype")
    x=cur.fetchall()
    print("\t","class name","\t\t","rate(in Rs)","\t\t","status")
    for i in x:
        print("\t",i[1],"\t\t",i[2],"\t\t\t",i[3])
    print("press 1 to update class rate")
    print("press 2 to update class status")
    ch=int(input("enter your choice: "))
    print()
    if(ch==1):
        cls=input("enter class to be modified: ")
        print("enter new rate for",cls,":-")
        rate=int(input())
        cmd="update classtype set rate=%s where item_name=%s"
        L=[rate,cls]
        cur.execute(cmd,L)
        print("succesfully updated rate for",cls)
    elif(ch==2):
        cls=input("enter class to be modified: ")
        print("enter new status for",cls,":-")
        status=input()
        cmd="update classtype set status=%s where item_name=%s"
        L=[status,cls]
        cur.execute(cmd,L)
        print("status succesfully updated  for",cls)
    else:
        print("invalid entry")
    db.commit()
    adminmenu()

def adminpassremove():
    cur.execute("select pass_id,name from passenger order by pass_id")
    x=cur.fetchall()
    print("pass id","\t\t","name")
    for i in x:
        print(i[0],"\t\t",i[1])
    idp=input("enter passenger id to be removed: ")
    cmd="delete from passenger where pass_id=%s"
    cmd2="delete from ticket where pass_id=%s"
    L=[idp]
    c=0
    for i in x:
        if(i[0]==idp):
            print("passenger removed")
            cur.execute(cmd,L)
            cur.execute(cmd2,L)
            c+=1
    if(c==0):
        print("invalid id entered")
        adminmenu()
    db.commit()
    adminmenu()

def adminluggage():
    #cur.execute("create table luggage(sno int(5),weight varchar(20),rate  int(11))")
    cmd="insert into luggage values(%s,%s,%s)"
    while(True):
        sno=int(input("enter sno: "))
        weight=input("enter weight: ")
        rate=int(input("enter the rate: "))
        L=[sno,weight,rate]
        cur.execute(cmd,L)
        ch=input("add more?[yes/no]: ")
        if(ch=="no"):
            db.commit()
            print("records added successfully")
            print("returning to admin menu....")
            adminmenu()
            
def adminupdtluggage():
    print()
    print("LUGGAGE RATE UPDATER")
    cur.execute("select * from luggage order by sno")
    x=cur.fetchall()
    print("\t\t","sno","\t\t","weight","\t\t","rate(in Rs)")
    for i in x:
        print("\t\t",i[0],"\t\t",i[1],"\t\t",i[2])
    print()
    while(True):
        ch=int(input("enter sno of the weight whose rate is to be updated: "))
        for i in x:
            if(i[0]==ch):
                c=i[1]
        print("enter new rate for",c,"kg:- ")
        rn=int(input())
        cmd="update luggage set rate=%s where sno=%s"
        L=[rn,ch]
        cur.execute(cmd,L)
        db.commit()
        print("luggage rate successfully updated")
        while(True):
            print()
            print("press 1 to continue updation")
            print("press 2 to return to admin menu")
            ver=int(input("enter your choice: "))
            print()
            if(ver==2):
                print("returning to admin menu...")
                adminmenu()
                break
            elif(ver!=1 and ver!=2):
                print("invalid entry")
            elif(ver==1):
                adminupdtluggage()
                break

  
def adminticketupdt():
    print()
    print("TICKET RECORDS")
    print()
    cur.execute("select * from ticket order by date_of_dept")
    dat=cur.fetchall()
    if(dat==[]):
        print()
        print("no record exist")
        print("returning to admin menu....")
        adminmenu()
    print("id","\t","name","\t\t","flight","\t","depart","\t","arrival","\t","class","\t\t","date of depart","\t","ticket cost(in Rs)")
    for i in dat:
        print(i[0],"\t",i[1],"\t\t",i[2],"\t",i[3],"\t",i[4],"\t",i[5],"\t",i[6],"\t",i[10])
    while(True):
                print()
                print("press 1 to return to admin menu: ")
                print("press 2 to remove ticket record")
                ch=int(input("enter your choice: "))
                print()
                if(ch==1):
                    adminmenu()
                    break
                elif(ch==2):
                    pid=input("enter  id to be removed: ")
                    cmd2="delete from ticket where pass_id=%s"
                    L=[pid]
                    cur.execute(cmd2,L)
                    print("record removed successfully")
                    db.commit()
                else:
                    print()
                    print("invalid entry") 
mainmenu()