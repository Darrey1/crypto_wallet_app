from tkinter import* 
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import sys
import os
from .dashboard import dashboard_page
script_directory = os.path.dirname(os.path.abspath(__file__))
# path = os.path.join(script_directory, "img")


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both dev and PyInstaller bundle """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class Login:
    def __init__(self,wind):
        self.main_root = wind
        self.root=wind
        self.root.title("Crypto Wallet App")
        self.root.geometry("900x600") 
        path = resource_path("UI/img")
        self.bg=Image.open(os.path.join(path, "bg.jpg"))
        self.bg=ImageTk.PhotoImage(file=os.path.join(path, "bg.jpg"))
        
        lb1_bg=Label(self.root,image=self.bg)
        lb1_bg.place(x=0,y=0, relwidth=1,relheight=1)

        frame1= Frame(self.root,bg="#002B53")
        frame1.place(relx=0.5, rely=0.5, anchor=CENTER,width=340,height=450)  
        #frame1.place(x=(screen_height/2),y=(screen_height/2),width=340,height=450)

        img1=Image.open(os.path.join(path, "log1.png"))
        img1=img1.resize((100,100),Image.ADAPTIVE)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lb1img1 = Label(image=self.photoimage1,bg="#002B53")
        lb1img1.place(relx=0.5, rely=0.33, anchor=CENTER, width=100,height=100)

        get_str = Label(frame1,text="Login",font=("arial",20,"bold"),fg="white",bg="#002B53")
        get_str.place(x=140,y=100)

        #label1 
        username =lb1= Label(frame1,text="Email:",font=("arial",10,"bold"),fg="white",bg="#002B53")
        username.place(x=30,y=160)

        #entry1 
        txtuser=ttk.Entry(frame1,font=("arial",17,"bold"))
        txtuser.place(x=33,y=190,width=270)


        #label2 
        pwd =lb1= Label(frame1,text="Password:",font=("arial",10,"bold"),fg="white",bg="#002B53")
        pwd.place(x=30,y=230)

        #entry2 
        txtpwd=ttk.Entry(frame1,font=("arial",17,"bold"),show="*")
        txtpwd.place(x=33,y=260,width=270)
        loginbtn=Button(frame1,text="Login",command=lambda:self.login(txtuser.get(),txtpwd.get()),font=("arial",15,"bold"),bd=0,relief=RIDGE,fg="#002B53",bg="white",activeforeground="white",activebackground="#007ACC")
        loginbtn.place(x=33,y=325,width=270,height=35)


        # Creating Button Registration
        loginbtn=Button(frame1,text="Register",font=("arial",10,"bold"),bd=0,relief=RIDGE,fg="white",bg="#002B53",activeforeground="orange",activebackground="#002B53")
        loginbtn.place(x=33,y=420,width=50,height=20)


        # Creating Button Forget
        loginbtn=Button(frame1,text="Forget",font=("arial",10,"bold"),bd=0,relief=RIDGE,fg="white",bg="#002B53",activeforeground="orange",activebackground="#002B53")
        loginbtn.place(x=90,y=420,width=50,height=20)

    def show_password(self):
        if self.txtpwd['show'] == "*":
            self.txtpwd.config(show="")
        else:
            self.txtpwd.config(show="*")
    def reg(self):
        self.new_window=Toplevel(self.root)
        # self.app=Register(self.new_window)


    def login(self,email,pwd):
        print(email)
        print(pwd)
        if (email=="" or pwd==""):
            messagebox.showerror("Error","All Field Required!")
        elif str(email).capitalize() =='Admin' and pwd == '1234':
            # self.root.withdraw()
            self.root.destroy()
            dashboard_page()
            
        else:
            messagebox.showerror("Error","Invalid crediential!")
            
            
#=======================Reset Passowrd Function=============================
    def reset_pass(self,email,answer,new_password):
        if email == "":
            messagebox.showerror("Error","Please Enter your email!")
            return
        if answer == "":
            messagebox.showerror("Error","Please Enter your security answer!")
            return
        if new_password == "":
            messagebox.showerror("Error","Please Enter your new Password!")
            return
        else:
            reset =""
            if reset:
                self.root2.withdraw()
                messagebox.showinfo("Success","Password reset successfull!")
            else:
                messagebox.showerror("Invalid Credientials!","Please provide a valid information !")
                



# =====================Forget window=========================================
    def forget_pwd(self):
        self.root2=Toplevel()
        self.root2.title("Forget Password")
        self.root2.geometry("400x400+610+170")
        l=Label(self.root2,text="Forget Password",font=("arial",30,"bold"),fg="#002B53",bg="gainsboro")
        l.place(x=0,y=10,relwidth=1)
        # -------------------fields-------------------
        #label1 
        ssq =lb1= Label(self.root2,text="Enter your Email:",font=("arial",15,"bold"),fg="#002B53",bg="gainsboro")
        ssq.place(x=70,y=80)
        #Combo Box1
        #self.combo_security = ttk.Combobox(self.root2,textvariable=self.var_ssq,font=("arial",15,"bold"),state="readonly")
        #self.combo_security["values"]=("Select","Your Date of Birth","Your Nick Name","Your Favorite Book")
        #self.combo_security.current(0)
        self.email=ttk.Entry(self.root2,font=("arial",15,"bold"))
        self.email.place(x=70,y=110,width=270)
        #label2 
        sa =lb1= Label(self.root2,text="Your Security Answer:",font=("arial",15,"bold"),fg="#002B53",bg="gainsboro")
        sa.place(x=70,y=150)
        #entry2 
        self.txtpwd=ttk.Entry(self.root2,font=("arial",15,"bold"),show="*")
        self.txtpwd.place(x=70,y=180,width=270)
        #label2 
        new_pwd =lb1= Label(self.root2,text="New Password:",font=("arial",15,"bold"),fg="#002B53",bg="gainsboro")
        new_pwd.place(x=70,y=220)
        #entry2 
        self.new_pwd=ttk.Entry(self.root2,font=("arial",15,"bold"),show="*")
        self.new_pwd.place(x=70,y=250,width=270)
        # Creating Button New Password
        loginbtn=Button(self.root2,command=lambda:self.reset_pass(self.email.get(),self.txtpwd.get(),self.new_pwd.get()),text="Reset Password",font=("arial",15,"bold"),bd=0,relief=RIDGE,fg="#fff",bg="#002B53",activeforeground="white",activebackground="#007ACC")
        loginbtn.place(x=70,y=300,width=270,height=35)
        
