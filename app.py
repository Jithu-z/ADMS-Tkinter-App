import tkinter as tk
from tkinter import PhotoImage, messagebox,ttk
import functions as adms
import mysql.connector
db=mysql.connector.connect(host="localhost",user="root",password="OPEN SQL",database="ADMS")
cur=db.cursor()
class admsapp():
    def __init__(self,root):
        self.root=root
        self.root.title("ADMS - Airline Database Management System")
        self.root.geometry('600x400')
        self.root.configure(bg='#f0f0f0')
        try:
            self.root.iconbitmap(r"C:\Users\abhij\Downloads\dictionary_book_encyclopaedia_icon-icons.com_66120.ico")
        except tk.TclError:
            print("Icon not found, skipping.")

        self.mobno=tk.StringVar()

        # --- Centralized Style Configuration ---
        style = ttk.Style(self.root)
        style.theme_use('clam')
        
        style.configure('TLabel', font=('calibri', 12), background='#f0f0f0', foreground='black')
        style.configure('Title.TLabel', font=('calibri', 20, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('calibri', 14, 'bold'), background='#f0f0f0')
        style.configure('TButton', font=('calibri', 12, 'bold'), foreground='black', padding=5)
        style.configure('TEntry', font=('calibri', 12), padding=5)
        style.configure('TRadiobutton', font=('calibri', 11), background='#f0f0f0')

        self.create_login_widgets()

    def _clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_widgets(self):
        self._clear_widgets()
        #bg=PhotoImage(file=r"C:\Users\abhij\OneDrive\Desktop\coding\python\ADMS\ADMS images\plane-taking-off.jpg")
        # label1=Label(self.root)
        # label1.place(x=0,y=0)
        ttk.Label(self.root,text="Welcome to ADMS", style='Title.TLabel').pack(pady=40)
        
        button_frame=ttk.Frame(self.root)
        button_frame.pack(pady=10,expand=True)
        
        ttk.Button(button_frame,text="Login",command=self.login, width=20).pack(pady=10)
        ttk.Button(button_frame,text="Register",command=self.register, width=20).pack(pady=10)

    def login(self):
        self._clear_widgets()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        ttk.Label(frame,text="Enter registered mobile number:").pack(pady=(0,5))
        ttk.Entry(frame,textvariable=self.mobno, width=30).pack(pady=5)
        ttk.Button(frame,text="Login",command=self.login_check).pack(pady=20)
        ttk.Button(frame,text="<--- Back",command=self.create_login_widgets).pack()

    def login_check(self):
        mobno=self.mobno.get()
        if adms.passignin(mobno):
            name=adms.getname(mobno)
            messagebox.showinfo("Login Success","Welcome to ADMS "+name)
            self.mobno.set(mobno)
            self.create_user_widgets()
        else:
            messagebox.showerror("Login Failed","Invalid mobile number")
            self.create_login_widgets()

    def register(self):
        self._clear_widgets()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        ttk.Label(frame,text="Thank you for showing interest in ADMS").pack(pady=10)
        ttk.Label(frame,text="Enter your mobile number:").pack(pady=(10,5))
        mobno=tk.StringVar()
        ttk.Entry(frame,textvariable=mobno).pack(pady=5)
        ttk.Button(frame,text="Verify",command=lambda: self.register2(mobno.get())).pack(pady=20)
        ttk.Button(frame,text="<--- Back",command=self.create_login_widgets).pack()

    def register2(self,mobno):
        if(adms.passignin(mobno) or len(mobno)!=10):
            messagebox.showerror("Register Failed","Mobile number already registered or invalid")
            self.create_login_widgets()
        else:
            self._clear_widgets()
            messagebox.showinfo("Verify Bot","Mobile number verified")
            frame = ttk.Frame(self.root, padding="20")
            frame.pack(expand=True)

            ttk.Label(frame,text="Enter your name:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
            name=tk.StringVar()
            ttk.Entry(frame,textvariable=name, width=30).grid(row=0, column=1, pady=5, padx=5)

            ttk.Label(frame,text="Enter your Address:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
            address=tk.StringVar()
            ttk.Entry(frame,textvariable=address, width=30).grid(row=1, column=1, pady=5, padx=5)
            
            ttk.Button(frame,text="Register",command=lambda: self.register_user(name.get(),mobno,address.get())).grid(row=2, column=0, columnspan=2, pady=20)

    def register_user(self,name,mobno,address):
        adms.passignup(name,mobno,address)
        messagebox.showinfo("Register Success","Welcome to ADMS "+name)
        self.mobno.set(mobno) # Set the mobile number for the logged-in session
        self.create_user_widgets()

    def create_user_widgets(self):
        self._clear_widgets()
        ttk.Label(self.root, text="Main Menu", style='Title.TLabel').pack(pady=20)
        
        frame = ttk.Frame(self.root)
        frame.pack(expand=True)

        buttons=[
            ("Book Ticket", 0), ("Print Boarding Pass", 1), ("View Flight Status", 2),
            ("View Bill", 3), ("Cancel Ticket", 4), ("Logout", 5)
        ]
        
        for i, (text, val) in enumerate(buttons):
            ttk.Button(frame, text=text, command=lambda v=val: self.user_buttons(v), width=20).grid(row=i//2, column=i%2, padx=10, pady=10)

    def user_buttons(self,i):
        if i == 0:
            self.book_ticket()
        elif i == 1:
            self.print_boarding_pass()
        elif i == 2:
            booked = adms.hasbooked(self.mobno.get())
            if booked:
                status=adms.getstatus(adms.getid(self.mobno.get()))
                # Handle multiple tickets
                status_messages = [f"Flight {s[0]} from {s[1]} to {s[2]} on {str(s[3])} is {s[4]}" for s in status]
                messagebox.showinfo("Flight Status", "\n".join(status_messages))
            else:
                messagebox.showerror("OOPS!!","No flight booked for your account")
        elif i == 3:
            if not adms.hasbooked(self.mobno.get()):
                messagebox.showerror("OOPS!!","No flight booked for your account")
            else:
                self.view_bill()
        elif i == 4:
            self.cancel_ticket()
        elif i == 5:
            messagebox.showinfo("Logout","Logged out successfully")
            self.create_login_widgets()

    def book_ticket(self):
        booked_tickets = adms.hasbooked(self.mobno.get())
        if len(booked_tickets) >= 2:
            messagebox.showerror("Booking Limit Reached", "You can only have one outbound and one return ticket at a time. Please cancel an existing ticket to book a new one.")
            self.create_user_widgets()
        elif len(booked_tickets) == 1:
            # User has one ticket, so the next must be a return ticket.
            first_ticket = booked_tickets[0]
            return_source = first_ticket[4]      # Arrival of the first ticket
            return_destination = first_ticket[3] # Departure of the first ticket
            
            if messagebox.askyesno("Book Return Ticket", f"You have a booking from {return_destination} to {return_source}. Would you like to book a return flight?"):
                self.book_ticket3(return_source, (return_destination,))
            else:
                self.create_user_widgets()
        else:
            # No tickets booked, start the normal booking flow
            self.book_ticket_start()

    def book_ticket_start(self):
        """Displays the initial departure location choices."""
        self._clear_widgets()
        ttk.Label(self.root,text="Where would you like to fly with us...", style='Header.TLabel').pack(pady=20)
        frame = ttk.Frame(self.root)
        frame.pack(expand=True)
        buttons=["Calicut","Cochin","Trivandrum","Kannur"]
        for i in range(4):
            ttk.Button(frame,text=buttons[i],command=lambda b=buttons[i]: self.book_ticket2(b)).pack(pady=5)
        ttk.Button(self.root,text="<--- Back",command=self.create_user_widgets).pack(pady=20)

    def book_ticket2(self,source):
        self._clear_widgets()
        ttk.Label(self.root,text="Available Destinations", style='Header.TLabel').pack(pady=20)
        frame = ttk.Frame(self.root)
        frame.pack(expand=True)
        buttons=adms.getdestinations(source)
        for i in range(len(buttons)):
            ttk.Button(frame,text=buttons[i][0],command=lambda b=buttons[i]: self.book_ticket3(source,b)).pack(pady=5)
        ttk.Button(self.root,text="<--- Back",command=self.book_ticket_start).pack(pady=20)

    def book_ticket3(self,source,destination):
        self.source=source
        self.destination=destination
        self._clear_widgets()
        ttk.Label(self.root,text="Available Flights", style='Header.TLabel').pack(pady=20)
        
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, padx=20, pady=10)

        flights=adms.getflights(source,destination)
        ttk.Label(frame,text="Flight ID", font=('calibri', 11, 'bold')).grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(frame,text="Date", font=('calibri', 11, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame,text="Status", font=('calibri', 11, 'bold')).grid(row=0, column=2, padx=10, pady=5)
        
        for i in range(len(flights)):
            ttk.Label(frame,text=flights[i][0]).grid(row=i+1, column=0, padx=10, pady=5)
            ttk.Label(frame,text=str(flights[i][1])).grid(row=i+1, column=1, padx=10, pady=5)
            ttk.Label(frame,text=flights[i][2]).grid(row=i+1, column=2, padx=10, pady=5)
            ttk.Button(frame,text="Book",command=lambda f=flights[i]: self.book_ticket4(f)).grid(row=i+1, column=3, padx=10, pady=5)
        
        ttk.Button(self.root,text="<--- Back",command=lambda: self.book_ticket2(source)).pack(pady=20)

    def book_ticket4(self,flight):
        self._clear_widgets()
        ttk.Label(self.root,text="SELECT SEAT TYPE & QUANTITY", style='Header.TLabel').pack(pady=20)
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(expand=True)

        seats=adms.getclass()
        self.seat_type = tk.StringVar(value="first")
        
        ttk.Radiobutton(frame, text=f"First Class\tRs{seats[0][2]}\t({adms.getremainingseats(1,flight[0])} Vacant)", variable=self.seat_type, value="first").pack(anchor='w', pady=5)
        ttk.Radiobutton(frame, text=f"Economy Class\tRs{seats[1][2]}\t({adms.getremainingseats(2,flight[0])} Vacant)", variable=self.seat_type, value="economy").pack(anchor='w', pady=5)
        ttk.Radiobutton(frame, text=f"Business Class\tRs{seats[2][2]}\t({adms.getremainingseats(3,flight[0])} Vacant)", variable=self.seat_type, value="business").pack(anchor='w', pady=5)
        
        entry_frame = ttk.Frame(frame)
        entry_frame.pack(pady=20)
        ttk.Label(entry_frame,text="Number of seats:").pack(side='left', padx=5)
        self.seatno=tk.StringVar()
        ttk.Entry(entry_frame,textvariable=self.seatno, width=5).pack(side='left')

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame,text="Confirm",command=lambda: self.book_ticket5(flight,self.seat_type.get(),self.seatno.get())).pack(side='left', padx=10)
        ttk.Button(btn_frame,text="<--- Back",command=lambda: self.book_ticket3(flight[3],(flight[4],))).pack(side='left', padx=10)

    def book_ticket5(self,flight,seat_class,seatno):
        try:
            num_seats = int(seatno)
            if not (0 < num_seats <= 5):
                messagebox.showerror("Invalid Quantity", "Please enter a valid number of seats (1-5).")
                return
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Input", "Please enter a number for seats.")
            return

        self._clear_widgets()
        try:
            seat_type=adms.getseat_info(seat_class)
            seats=adms.getseats(num_seats,int(seat_type[0]),flight[0])
            if(seats==[]):
                messagebox.showerror("Error","Seats not available")
                self.book_ticket4(flight)
            else:
                self.seat_id=" ".join(seats)
                response=messagebox.askquestion("Seat Confirmation","Confirm Booking seats "+ self.seat_id+" in "+seat_type[1]+" class for flight "+flight[0]+" from "+flight[3]+" to "+flight[4]+" on "+str(flight[1])+"?")
                if(response=="yes"):
                    self.book_ticket6(flight,seat_type,num_seats)
                else:
                    self.book_ticket4(flight)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.book_ticket4(flight)

    def book_ticket6(self,flight,seats,seatno):
        self._clear_widgets()
        self.rate=seatno*int(seats[2])
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame,text=f"Total Cost: Rs {self.rate}", style='Header.TLabel').pack(pady=10)
        ttk.Label(frame,text=f"{seatno} {seats[1]} class seats (Rs{seats[2]}/ticket)").pack(pady=5)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame,text="Confirm and Finish",command=lambda: self.book_ticket9(flight,seats)).pack(side='left', padx=10)
        ttk.Button(btn_frame,text="Add Luggage",command=lambda: self.book_ticket7(flight,seats)).pack(side='left', padx=10)
        ttk.Button(btn_frame,text="Cancel",command=lambda: self.book_ticket4(flight)).pack(side='left', padx=10)

    def book_ticket7(self,flight,seats):
        self._clear_widgets()
        ttk.Label(self.root,text="Select Luggage Option", style='Header.TLabel').pack(pady=20)
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(expand=True)

        luggage=adms.get_luggage(0)
        self.luggage_var = tk.IntVar(value=1) # Default to the first luggage option
        for i in range(len(luggage)):
            ttk.Radiobutton(frame, text=f"{luggage[i][1]} (Rs {luggage[i][2]})", variable=self.luggage_var, value=(i+1)).pack(anchor='w', pady=5)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame,text="Confirm",command=lambda: self.book_ticket8(flight,seats,self.luggage_var.get())).pack(side='left', padx=10)
        ttk.Button(btn_frame,text="Cancel",command=lambda: self.book_ticket6(flight,seats,len(self.seat_id.split()))).pack(side='left', padx=10)

    def book_ticket8(self,flight,seats,luggage):
        lug=adms.get_luggage(luggage)
        total_cost = self.rate + int(lug[2])
        
        self._clear_widgets()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame,text=f"Total Cost: Rs {total_cost}", style='Header.TLabel').pack(pady=10)
        ttk.Label(frame,text=f"{len(self.seat_id.split())} {seats[1]} class seats (Rs{seats[2]}/ticket)").pack(pady=5, anchor='w')
        ttk.Label(frame,text=f"{lug[1]} (Rs{lug[2]})").pack(pady=5, anchor='w')
        extra_lug, lug_rate = lug[1], lug[2]

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame,text="Confirm and Finish",command=lambda: self.book_ticket9(flight,seats,extra_lug,lug_rate,total_cost)).pack(side='left', padx=10)
        ttk.Button(btn_frame,text="Cancel",command=lambda: self.book_ticket6(flight,seats,len(self.seat_id.split()))).pack(side='left', padx=10)

    def book_ticket9(self,flight,seats,extra_lug="Nill",lug_rate=0,total_cost=0):
        if(lug_rate==0):
            total_cost=self.rate
        if(adms.booktickets(adms.getid(self.mobno.get()),adms.getname(self.mobno.get()),flight[0],flight[3],flight[4],seats[1],flight[1],extra_lug,lug_rate,self.rate,total_cost,self.seat_id)):
            messagebox.showinfo("Booking Success","Ticket Booked Successfully")
            # Ask to book a return ticket
            if len(adms.hasbooked(self.mobno.get())) < 2:
                if messagebox.askyesno("Book Return Ticket", "Would you like to book a return ticket?"):
                    self.book_return_ticket(self.destination[0], self.source)
                    return
        else:
            messagebox.showerror("Booking Failed","Ticket Booking Failed due to SQL error")
        self.create_user_widgets()

    def book_return_ticket(self, source, destination):
        """Initiates the booking process for a return flight."""
        self.source = source
        self.destination = (destination,) # Make it a tuple to match expected format
        self.book_ticket3(source, self.destination)

    def cancel_ticket(self):
        booked_tickets = adms.hasbooked(self.mobno.get())
        if booked_tickets:
            self._clear_widgets()
            
            ttk.Label(self.root, text="Select a ticket to cancel", style='Header.TLabel').pack(pady=20)

            if len(booked_tickets) == 1:
                t = booked_tickets[0]
                ttk.Label(self.root,text=f"Flight {t[2]} from {t[3]} to {t[4]} on {t[6]}").pack(pady=10)
                ttk.Button(self.root, text="Confirm Cancellation", command=lambda: self.cancel_ticket2(t[2])).pack(pady=10)
            else: # Multiple tickets
                # Sort tickets by date to identify outbound and return
                sorted_tickets = sorted(booked_tickets, key=lambda x: x[6])
                outbound_ticket = sorted_tickets[0]
                return_ticket = sorted_tickets[1]

                # Button to cancel outbound (and implicitly return)
                ttk.Button(self.root, text=f"Cancel Outbound: {outbound_ticket[3]} -> {outbound_ticket[4]} on {outbound_ticket[6]}", 
                          command=lambda: self.confirm_outbound_cancellation(outbound_ticket, return_ticket)).pack(pady=5)
                
                # Button to cancel only the return
                ttk.Button(self.root, text=f"Cancel Return: {return_ticket[3]} -> {return_ticket[4]} on {return_ticket[6]}", 
                          command=lambda: self.confirm_single_cancellation(return_ticket)).pack(pady=5)

            ttk.Button(self.root, text="<--- Back", command=self.create_user_widgets).pack(pady=20)
        else:
            messagebox.showerror("Error","No ticket booked")
            self.create_user_widgets() 

    def confirm_outbound_cancellation(self, outbound, inbound):
        if messagebox.askyesno("Confirm Full Trip Cancellation", f"Cancelling your outbound flight from {outbound[3]} to {outbound[4]} will also cancel your return flight. Are you sure you want to proceed?"):
            self.cancel_ticket2([outbound[2], inbound[2]]) # Pass a list of flight IDs

    def confirm_single_cancellation(self, ticket_to_cancel):
        if messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel flight {ticket_to_cancel[2]} from {ticket_to_cancel[3]} to {ticket_to_cancel[4]}?"):
            self.cancel_ticket2(ticket_to_cancel[2])

    def cancel_ticket2(self, flight_id_to_cancel):
        if(adms.cancelticket(adms.getid(self.mobno.get()), flight_id_to_cancel)):
            messagebox.showinfo("Cancellation Success","Ticket Cancelled Successfully")
        else:
            messagebox.showerror("Cancellation Failed","Ticket Cancellation Failed due to SQL error")
        self.create_user_widgets()

    def view_bill(self):
        self._clear_widgets()
        tickets = adms.getticket(adms.getid(self.mobno.get()))

        ttk.Label(self.root, text="Bill Details", style='Title.TLabel').pack(pady=20)

        bill_frame = ttk.Frame(self.root)
        bill_frame.pack(padx=20, pady=10, fill="x")

        for i, ticket in enumerate(tickets):
            num_seats = len(ticket[11].split())
            seat_rate_total = ticket[9]
            cost_per_seat = seat_rate_total // num_seats if num_seats > 0 else "N/A"

            # --- Create a frame for each ticket's bill ---
            ticket_frame = ttk.Frame(bill_frame, relief="groove", padding=15)
            ticket_frame.pack(pady=10, fill="x")

            ttk.Label(ticket_frame, text=f"Ticket {i+1}: {ticket[3]} to {ticket[4]}", font=('calibri', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
            ttk.Label(ticket_frame, text=f"Seats ({num_seats} x Rs {cost_per_seat}):").grid(row=1, column=0, sticky="w", padx=5)
            ttk.Label(ticket_frame, text=f"Rs {seat_rate_total}").grid(row=1, column=1, sticky="e", padx=5)
            ttk.Label(ticket_frame, text=f"Luggage ({ticket[7]}):").grid(row=2, column=0, sticky="w", padx=5)
            ttk.Label(ticket_frame, text=f"Rs {ticket[8]}").grid(row=2, column=1, sticky="e", padx=5)
            ttk.Label(ticket_frame, text="Total Cost:", font=('calibri', 11, 'bold')).grid(row=3, column=0, sticky="w", padx=5, pady=(10, 0))
            ttk.Label(ticket_frame, text=f"Rs {ticket[10]}", font=('calibri', 11, 'bold')).grid(row=3, column=1, sticky="e", padx=5, pady=(10, 0))

        ttk.Button(self.root, text="<--- Back", command=self.create_user_widgets).pack(pady=20)

    def print_boarding_pass(self):
        if not adms.hasbooked(self.mobno.get()):
            messagebox.showerror("Oops!", "No flight booked for your account")
        else:
            self._clear_widgets()
            tickets = adms.getticket(adms.getid(self.mobno.get()))
            if len(tickets) == 1:
                self.display_boarding_pass(tickets[0])
            else:
                ttk.Label(self.root, text="Select Boarding Pass to Print", style='Header.TLabel').pack(pady=20)
                for t in tickets:
                    ttk.Button(self.root, text=f"Flight: {t[3]} -> {t[4]} on {t[6]}", command=lambda current_ticket=t: self.display_boarding_pass(current_ticket)).pack(pady=10)
                ttk.Button(self.root, text="<--- Back", command=self.create_user_widgets).pack(pady=20)

    def display_boarding_pass(self, ticket_data):
            self._clear_widgets()
            flight_name=adms.getflightname(ticket_data[2])

            # Main frame for the boarding pass
            pass_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10, bg="white")
            pass_frame.pack(pady=20, padx=10)

            tk.Label(pass_frame, text=flight_name, font=("Helvetica", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky="ew")

            # Passenger and Flight Info
            tk.Label(pass_frame, text="PASSENGER NAME", font=("Helvetica", 8, "italic"), bg="white").grid(row=1, column=0, sticky="w")
            tk.Label(pass_frame, text=ticket_data[1], font=("Helvetica", 14, "bold"), bg="white").grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))
            
            tk.Label(pass_frame, text="FLIGHT", font=("Helvetica", 8, "italic"), bg="white").grid(row=1, column=2, sticky="w")
            tk.Label(pass_frame, text=ticket_data[2], font=("Helvetica", 14, "bold"), bg="white").grid(row=2, column=2, columnspan=2, sticky="w", padx=5, pady=(0,5))

            # Departure and Arrival
            tk.Label(pass_frame, text="FROM", font=("Helvetica", 8, "italic"), bg="white").grid(row=3, column=0, sticky="w", pady=(10, 0))
            tk.Label(pass_frame, text=ticket_data[3], font=("Helvetica", 16, "bold"), bg="white").grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))

            tk.Label(pass_frame, text="TO", font=("Helvetica", 8, "italic"), bg="white").grid(row=3, column=2, sticky="w", pady=(10, 0))
            tk.Label(pass_frame, text=ticket_data[4], font=("Helvetica", 16, "bold"), bg="white").grid(row=4, column=2, columnspan=2, sticky="w", padx=5, pady=(0,5))

            # Date, Class, and Seat
            tk.Label(pass_frame, text=f"DATE: {str(ticket_data[6])}", font=("Helvetica", 11), bg="white").grid(row=5, column=0, sticky="w", pady=(15, 0))
            tk.Label(pass_frame, text=f"CLASS: {ticket_data[5]}", font=("Helvetica", 11), bg="white").grid(row=5, column=1, columnspan=2, sticky="w", pady=(15, 0), padx=10)
            tk.Label(pass_frame, text=f"SEAT(S): {ticket_data[11]}", font=("Helvetica", 12, "bold"), bg="white").grid(row=6, column=0, columnspan=4, sticky="w", pady=(5, 10), padx=5)

            ttk.Button(self.root, text="<--- Back", command=self.create_user_widgets).pack(pady=20)

if(__name__=="__main__"):
    root=tk.Tk()
    app=admsapp(root)
    root.mainloop()
#svaepoint sp1