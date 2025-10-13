import tkinter as tk
from tkinter import PhotoImage, messagebox,ttk
import ADMS_Latest as adms
import mysql.connector
db=mysql.connector.connect(host="localhost",user="root",password="OPEN SQL",database="ADMS")
cur=db.cursor()
class admsapp():
    def __init__(self,root):
        self.root=root
        self.root.title("ADMS")
        self.root.geometry('600x400')
        #self.root.iconbitmap(r"C:\Users\abhij\Downloads\dictionary_book_encyclopaedia_icon-icons.com_66120.ico")
        self.mobno=tk.StringVar()
        self.create_login_widgets()
    def create_login_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        style = ttk.Style(self.root)
        style.configure('TLabel', font = ('calibri', 20, 'bold'), foreground = 'black')
        style.configure('TButton', font = ('calibri', 20, 'bold'), foreground = 'black')
        #bg=PhotoImage(file=r"C:\Users\abhij\OneDrive\Desktop\coding\python\ADMS\ADMS images\plane-taking-off.jpg")
        # label1=Label(self.root)
        # label1.place(x=0,y=0)
        ttk.Label(self.root,text="Welcome to ADMS MKII").pack(pady=20)
        button_frame=tk.Frame(self.root)
        button_frame.pack(pady=10,expand=True,fill='both')
        ttk.Button(button_frame,text="1.Login",command=self.login).pack(pady=5)
        ttk.Button(button_frame,text="2.Register",command=self.register).pack(pady=5)
    def login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root,text="Enter registered mobile number:").pack()
        tk.Entry(self.root,textvariable=self.mobno).pack()
        tk.Button(self.root,text="Login",command=self.login_check).pack()
    def login_check(self):
        mobno=self.mobno.get()
        if adms.passignin(mobno):
            name=adms.getname(mobno)
            messagebox.showinfo("Login Success","Welcome to ADMS "+name)
            self.create_user_widgets()
        else:
            messagebox.showerror("Login Failed","Invalid mobile number")
            self.create_login_widgets()
    def register(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root,text="Thank you for showing interest on ADMS").pack()
        tk.Label(self.root,text="Enter your mobile number:").pack()
        mobno=tk.StringVar()
        tk.Entry(self.root,textvariable=mobno).pack()
        tk.Button(self.root,text="Verify",command=lambda: self.register2(mobno.get())).pack()
    def register2(self,mobno):
        for widget in self.root.winfo_children():
            widget.destroy()
        if(adms.passignin(mobno) or len(mobno)!=10):
            messagebox.showerror("Register Failed","Mobile number already registered or invalid")
            self.create_login_widgets()
        else:
            messagebox.showinfo("Verify Bot","Mobile number verified")
            tk.Label(self.root,text="Enter your name:").pack()
            name=tk.StringVar()
            tk.Entry(self.root,textvariable=name).pack()
            tk.Label(self.root,text="Enter your Address:").pack()
            address=tk.StringVar()
            tk.Entry(self.root,textvariable=address).pack()
            tk.Label(self.root,text="Enter reg.date(YYYY-MM-DD):").pack()
            regdate=tk.StringVar()
            tk.Entry(self.root,textvariable=regdate).pack()
            tk.Button(self.root,text="Register",command=lambda: self.register_user(name.get(),mobno,regdate.get(),address.get())).pack()
    def register_user(self,name,mobno,regdate,address):
        adms.passignup(name,mobno,regdate,address)
        messagebox.showinfo("Register Success","Welcome to ADMS "+name)
        self.create_user_widgets()

    def create_user_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        buttons=["1.Book Ticket","2.Print Boarding Pass ","3.View Flight Status ","4.View Bill","5.Cancel Ticket","6.Logout"]
        for i in range(6):
            tk.Button(self.root,text=buttons[i],command=lambda i=i: self.user_buttons(i)).pack()
    def user_buttons(self,i):
            if(i==0):
                self.book_ticket()
            elif(i==1):
                 self.print_boarding_pass()
            elif(i==2):
                if adms.hasbooked(self.mobno.get()):
                    status=adms.getstatus(adms.getid(self.mobno.get()))
                    messagebox.showinfo("Flight Status","Your flight "+status[0][0]+" from "+status[0][1]+" to "+status[0][2]+" on "+str(status[0][3])+" is currently "+status[0][4])
                else:
                    messagebox.showerror("OOPS!!","No flight booked for your account")
            elif(i==3):
                if(not(adms.hasbooked(self.mobno.get()))):
                    messagebox.showerror("OOPS!!","No flight booked for your account")
                else:
                    self.view_bill()
            elif(i==4):
                self.cancel_ticket()
            else:
                messagebox.showinfo("Logout","Logged out successfully")
                self.create_login_widgets()
    def book_ticket(self):
        if adms.hasbooked(self.mobno.get()):
            messagebox.showerror("Error","Please Cancel Existing Ticket")
            self.create_user_widgets()
        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            tk.Label(self.root,text="Where would you like to fly with us...").pack()
            buttons=["Calicut","Cochin","Trivandrum","Kannur"]
            for i in range(4):
                tk.Button(self.root,text=buttons[i],command=lambda i=i: self.book_ticket2(buttons[i])).pack()
            tk.Button(self.root,text="<---Back",command=self.create_user_widgets).pack()
    def book_ticket2(self,source):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root,text="Available Destinations").pack()
        buttons=adms.getdestinations(source)
        for i in range(len(buttons)):
            tk.Button(self.root,text=buttons[i],command=lambda i=i: self.book_ticket3(source,buttons[i])).pack()
        tk.Button(self.root,text="<---Back",command=self.book_ticket).pack()
    def book_ticket3(self,source,destination):
        self.source=source
        self.destination=destination
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root,text="Available Flights").pack()
        flights=adms.getflights(source,destination)
        tk.Label(self.root,text="Flight ID\t\tDate\t\tStatus").pack()
        for i in range(len(flights)):
            tk.Label(self.root,text=flights[i][0]+"  \t"+str(flights[i][1])+"\t"+flights[i][2]).pack()
            tk.Button(self.root,text="Book",command=lambda i=i: self.book_ticket4(flights[i])).pack()
        tk.Button(self.root,text="<---Back",command=lambda: self.book_ticket2(source)).pack()
    def book_ticket4(self,flight):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root,text="SELECT SEAT TYPE\nCURRENT RATES").pack()
        seats=adms.getclass()
        self.seat_type = tk.StringVar(value="first")
        tk.Radiobutton(self.root, text="First Class\t" +"Rs"+ str(seats[0][2])+"\t\t"+str(adms.getremainingseats(1,flight[0]))+" Vacant", variable=self.seat_type, value="first").pack()
        tk.Radiobutton(self.root, text="Economy Class\t" +"Rs"+str(seats[1][2])+"\t\t"+str(adms.getremainingseats(2,flight[0]))+" Vacant", variable=self.seat_type, value="economy").pack()
        tk.Radiobutton(self.root, text="Business Class\t" +"Rs"+ str(seats[2][2])+"\t\t"+str(adms.getremainingseats(3,flight[0]))+" Vacant", variable=self.seat_type, value="business").pack()
        tk.Label(self.root,text="Number of seats:").pack()
        self.seatno=tk.StringVar()
        tk.Entry(self.root,textvariable=self.seatno).pack()
        tk.Button(self.root,text="Confirm",command=lambda: self.book_ticket5(flight,self.seat_type.get(),int(self.seatno.get()))).pack()
        tk.Button(self.root,text="<---Back",command=lambda: self.book_ticket3(flight[3],(flight[4],))).pack()
    def book_ticket5(self,flight,seat_class,seatno):
        if(seatno<=0 or seatno>12):
            if(seatno>5):
                messagebox.showerror("Entry Restricted","enter valid number of seats")
                self.book_ticket4(flight)
            else:
                messagebox.showerror("Error","Please enter number of seats")
                self.book_ticket4(flight)
        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            seat_type=adms.getseat_info(seat_class)
            seats=adms.getseats(seatno,int(seat_type[0]),flight[0])
            if(seats==[]):
                messagebox.showerror("Error","Seats not available")
                self.book_ticket4(flight)
            else:
                self.seat_id=" ".join(seats)
                response=messagebox.askquestion("Seat Confirmation","Confirm Booking seats "+ self.seat_id+" in "+seat_type[1]+" class for flight "+flight[0]+" from "+flight[3]+" to "+flight[4]+" on "+str(flight[1])+"?")
                if(response=="yes"):
                    self.book_ticket6(flight,seat_type,seatno)
                else:
                    self.book_ticket4(flight)
    def book_ticket6(self,flight,seats,seatno):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.rate=seatno*int(seats[2])
        tk.Label(self.root,text="Total Cost: Rs"+str(self.rate)).pack()
        tk.Label(self.root,text=str(seatno)+" "+seats[1]+" class seats (Rs"+str(seats[2])+"/ticket)").pack()
        tk.Button(self.root,text="Confirm",command=lambda: self.book_ticket7(flight,seats)).pack()
        tk.Button(self.root,text="Cancel",command=lambda: self.book_ticket4(flight)).pack()
    def book_ticket7(self,flight,seats):
        if(adms.booktickets(adms.getid(self.mobno.get()),adms.getname(self.mobno.get()),flight[0],self.source,self.destination[0],seats[1],flight[1],0,0,self.rate,self.rate,self.seat_id)):
            messagebox.showinfo("Booking Success","Ticket Booked Successfully")
        else:
            messagebox.showerror("Booking Failed","Ticket Booking Failed due to SQL error")
        self.create_user_widgets()
    def cancel_ticket(self):
        if(adms.hasbooked(self.mobno.get())):
            for widget in self.root.winfo_children():
                widget.destroy()
            ticket=adms.getticket(adms.getid(self.mobno.get()))
            print(ticket)
            tk.Label(self.root,text="Confirm Cancellation of Flight "+ticket[0][2]+" From "+ticket[0][3]+" to "+ticket[0][4]+" on "+str(ticket[0][6])+" ?").pack()
            tk.Button(self.root,text="Confirm",command=self.cancel_ticket2).pack()
            tk.Button(self.root,text="Cancel",command=self.create_user_widgets).pack()
        else:
            messagebox.showerror("Error","No ticket booked")
            self.create_user_widgets() 
    def cancel_ticket2(self):
        if(adms.cancelticket(adms.getid(self.mobno.get()))):
            messagebox.showinfo("Cancellation Success","Ticket Cancelled Successfully")
        else:
            messagebox.showerror("Cancellation Failed","Ticket Cancellation Failed due to SQL error")
        self.create_user_widgets()
    def view_bill(self):
        for widget in self.root.winfo_children():
                widget.destroy()
        ticket=adms.getticket(adms.getid(self.mobno.get()))
        tk.Label(self.root,text="Flight ID: "+ticket[0][2]).pack()
        tk.Label(self.root,text="From: "+ticket[0][3]).pack()
        tk.Label(self.root,text="To: "+ticket[0][4]).pack()
        tk.Label(self.root,text="Date: "+str(ticket[0][6])).pack()
        tk.Label(self.root,text="Seat Type: "+ticket[0][5]).pack()
        tk.Label(self.root,text="Seats Booked: "+str(len(ticket[0][11].split()))).pack()
        tk.Label(self.root,text="Total Cost: Rs"+str(ticket[0][10])).pack()
        tk.Button(self.root,text="<---Back",command=self.create_user_widgets).pack()
    def print_boarding_pass(self):
        if not adms.hasbooked(self.mobno.get()):
            messagebox.showerror("Oops!", "No flight booked for your account")
        else:
            for widget in self.root.winfo_children():
                widget.destroy()
            
            ticket_data = adms.getticket(adms.getid(self.mobno.get()))[0]
            print(ticket_data)
            flight_name=adms.getflightname(ticket_data[2])

            # Main frame for the boarding pass
            pass_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
            pass_frame.pack(pady=20, padx=10)

            tk.Label(pass_frame, text=flight_name, font=("calibri", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10))

            # Passenger and Flight Info
            tk.Label(pass_frame, text="PASSENGER:", font=("calibri", 10, "italic")).grid(row=1, column=0, sticky="w")
            tk.Label(pass_frame, text=ticket_data[1], font=("calibri", 12, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
            
            tk.Label(pass_frame, text="FLIGHT:", font=("calibri", 10, "italic")).grid(row=1, column=2, sticky="w")
            tk.Label(pass_frame, text=ticket_data[2], font=("calibri", 12, "bold")).grid(row=2, column=2, columnspan=2, sticky="w", padx=5)

            # Departure and Arrival
            tk.Label(pass_frame, text="FROM:", font=("calibri", 10, "italic")).grid(row=3, column=0, sticky="w", pady=(10, 0))
            tk.Label(pass_frame, text=ticket_data[3], font=("calibri", 12, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", padx=5)

            tk.Label(pass_frame, text="TO:", font=("calibri", 10, "italic")).grid(row=3, column=2, sticky="w", pady=(10, 0))
            tk.Label(pass_frame, text=ticket_data[4], font=("calibri", 12, "bold")).grid(row=4, column=2, columnspan=2, sticky="w", padx=5)

            # Date, Class, and Seat
            tk.Label(pass_frame, text=f"DATE: {ticket_data[6]}", font=("calibri", 11)).grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
            tk.Label(pass_frame, text=f"CLASS: {ticket_data[5]}", font=("calibri", 11)).grid(row=5, column=2, columnspan=2, sticky="w", pady=(10, 0))
            tk.Label(pass_frame, text=f"SEAT(S): {ticket_data[11]}", font=("calibri", 12, "bold")).grid(row=6, column=0, columnspan=4, sticky="w", pady=(5, 10))

            tk.Button(self.root, text="<--- Back", command=self.create_user_widgets).pack(pady=10)

if(__name__=="__main__"):
    root=tk.Tk()
    app=admsapp(root)
    root.mainloop()
#new savepoint