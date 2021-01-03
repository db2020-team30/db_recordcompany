import pymysql
import itertools
from datetime import datetime
import sys
import os
import tkinter
from tkinter import ttk
from PIL import ImageTk,Image

dir_path=os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import basic_functions
import categories
import sales
import song_info
import data_contact
import scrollbar

class HoverBtn(tkinter.Button): #κλάση για την αλλαγή του χρώματος των κουμπιών, όταν ο κέρσορας περνάει από πάνω τους  
    def __init__(self, master, **kw):
        tkinter.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background']=self['activebackground']

    def on_leave(self, e):
        self['background']=self.defaultBackground

def choose(a,conn): # επιλογή πίνακα(για ερωτήματα 1-5) ή άλμπουμ μεσα από combobox(για τα υπόλοιπα)
    if(a<6):
        ep=['Άλμπουμ', 'Ανήκει', 'Μουσικό Είδος', 'Επικ. Γραφίστα',
      'Επικ. Μάνατζερ','Επικ. Οργανοπαίκτη','Επικ. Πελάτη',
      'Επικ. Στούντιο','Επικ. Συμβεβλημένου','Ερμηνείες', 'Φυσική Διανομή',
      'Γράφει','Ψηφιακή Διανομή','Γραφίστες',
      'Μάνατζερ','Μουσικοί','Οργανοπαίκτες','Πελάτες',
      'Περσόνες/γκρουπ','Πωλήσεις','Στιχουργοί',
      'Στούντιο','Συμβεβλημένοι', 'Συμβόλαια', 'Συμμετέχει','Συνθέτει','Συνθέτες',
      'Τραγούδια','Υπάγεται']
        label="Επιλέξτε πίνακα"
        titlos='Επιλογή Πίνακα'
    else:
        titlos='Επιλογή Άλμπουμ'
        label='Επιλέξτε Άλμπουμ'
        cur=conn.cursor()
        cur.execute('''SELECT titlos FROM album''')
        titloi=cur.fetchall()
        if(a==6):
            ep=['**Όλα τα Άλμπουμ**']
        else:
            ep=[]
        for i in range(len(titloi)):
            ep.append(titloi[i][0])
        cur.close()
    window=scrollbar.create('350x250',titlos)
    tkinter.Label(window, bg='white', text=label, fg="blue", font=('times new roman','14')).pack()
    combo=ttk.Combobox(window,values=ep,font=('times new roman','14'))
    combo.pack()
    combo.current(0)
    tkinter.Button(window,bg='white', text="Επιλογή",font=('times new roman','12'),command=lambda: save_choice(a,conn,window,combo.get())).pack()
    window.mainloop()
    return

def save_choice(a,conn,combo,selected_option): # αποθήκευση επιλογής πίνακα και παραπομπή στην σωστή συνάρτηση
    combo.destroy()
    dict={'Άλμπουμ':'album', 'Ανήκει':'anhkei', 'Μουσικό Είδος':'eidos', 'Επικ. Γραφίστα':'epik_graf',
      'Επικ. Μάνατζερ':'epik_manager','Επικ. Οργανοπαίκτη':'epik_organop','Επικ. Πελάτη':'epik_pelath',
      'Επικ. Στούντιο':'epik_studio','Επικ. Συμβεβλημένου':'epik_symbebl','Ερμηνείες':'ermhneyei', 'Φυσική Διανομή':'fys_dianomh',
      'Γράφει':'grafei','Ψηφιακή Διανομή':'psif_dianomh','Γραφίστες':'grafistas',
      'Μάνατζερ':'manager', 'Μουσικοί':'mousikos','Οργανοπαίκτες':'organopaikths','Πελάτες':'pelaths',
      'Περσόνες/γκρουπ':'persona_group','Πωλήσεις':'pwleitai', 'Στιχουργοί':'stixourgos',
      'Στούντιο':'studio', 'Συμβεβλημένοι':'symbeblhmenos', 'Συμβόλαια':'symbolaio', 'Συμμετέχει':'symmetexei','Συνθέτει':'synthetei','Συνθέτες':'syntheths',
      'Τραγούδια':'tragoudi', 'Υπάγεται':'ypagetai'}
    if(a==1):
        basic_functions.new_data(1,conn,dict[selected_option],[],[])
    elif(a==2):
        basic_functions.select_pleiad(2,conn,dict[selected_option])
    elif(a==3):
        basic_functions.select_pleiad(3,conn,dict[selected_option])
    elif(a==4):
        basic_functions.show_table(dict[selected_option],conn)
    elif(a==5):
        basic_functions.select_pleiad(5,conn,dict[selected_option])
    elif(a==6):
        song_info.songInfo_perAlbum(conn,selected_option)
    else:
        song_info.choose_song(conn,selected_option)
    return

def homescreen(conn): #δημιουργία αρχικής οθόνης
    
    main=scrollbar.create("700x550",'Αρχική',1)
    
    #δημιουργία μενού
    menubar=tkinter.Menu(main)
    edit=tkinter.Menu(menubar, tearoff=0) 
    edit.add_command(label='Εισαγωγή...', command=lambda: choose(1,conn))
    edit.add_command(label='Διαγραφή...', command=lambda: choose(2,conn))
    edit.add_command(label='Αλλαγή στοιχείων...', command=lambda: choose(3,conn))
    
    edit.add_separator()  
    edit.add_command(label="Έξοδος", command=main.destroy)
    menubar.add_cascade(label="Επεξεργασία", menu=edit)

    show=tkinter.Menu(menubar, tearoff=0) 
    show.add_command(label='Εκτύπωση πίνακα...', command=lambda: choose(4,conn))
    show.add_command(label='Εκτύπωση πλειάδας...', command=lambda: choose(5,conn))
    menubar.add_cascade(label="Εκτύπωση", menu=show)
    
    main.config(menu=menubar)

    i=Image.open("logo.PNG")
    img=ImageTk.PhotoImage(i)
    tkinter.Label(main,bg='white',image=img).pack()
    
    #δημιουργία κουμπίων
    btn1=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Φυσικές πωλήσεις",font=('helvetica','14'),command=lambda: sales.physical_sales(conn))
    btn2=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Έσοδα ανά άλμπουμ",font=('helvetica','14'),command=lambda: sales.profit_per_album(conn))
    btn3=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Στοιχεία τραγουδιών ανά άλμπουμ",font=('helvetica','14'),command=lambda: choose(6,conn))
    btn4=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Συγκροτήματα/Τραγουδιστές",font=('helvetica','14'),command=lambda: categories.choice(2,conn))
    btn5=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Στοιχεία συμβολαίων ανά κατηγορία καλλιτεχνών",font=('helvetica','14'),command=lambda: categories.choice(1,conn))
    btn6=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Οργανοπαίκτες που συμμετείχαν σε ένα τραγούδι",font=('helvetica','14'),command=lambda: choose(7,conn))
    btn7=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Πελάτες και ποσότητες των προϊόντων που προμηθεύτηκαν",font=('helvetica','14'),command=lambda: data_contact.pelates(conn))
    btn8=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Γραφίστες και τα άλμπουμ που έχουν επιμεληθεί",font=('helvetica','14'),command=lambda: data_contact.grafistas(conn))
    btn9=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Άλμπουμ ανά μουσικό είδος",font=('helvetica','14'),command=lambda: song_info.album_per_genre(conn))
    btn10=HoverBtn(main,bg='white',width=500, activebackground='light cyan', relief='flat',text="Άλμπουμ ανά studio ηχογράφησης",font=('helvetica','14'),command=lambda: song_info.album_per_studio(conn))
    
    btn1.pack()
    btn2.pack()
    btn3.pack()
    btn4.pack()
    btn5.pack()
    btn6.pack()
    btn7.pack()
    btn8.pack()
    btn9.pack()
    btn10.pack()
    main.mainloop()


    
def connect(_event=None): #δημιουργία σύνδεσης
    global errors
    u=e1.get()
    p=e2.get()
    if (u>'\u0080' and u<'\u03ce') or (p>'\u0080' and p<'\u03ce'): #λάθος,γιατί δεν αποτελείται μόνο απο λατινικούς χαρακτήρες η είσοδος
        if(errors!=1):
            if(errors!=0):err.destroy()
            err=tkinter.Label(parent, bg='white', text="Το όνομα χρήστη και ο κωδικός πρόσβασης\nπρέπει να έχουν μόνο λατινικούς χαρακτήρες.", fg="red", font=('arial','11'))
            err.pack()
            errors=1
    else:
        try:
            conn = pymysql.connect(
                host='localhost',
                user='{}'.format(u),
                password='{}'.format(p),
                db='recordcompany2',
                )
            parent.destroy()
            homescreen(conn)
            
        except pymysql.Error: #Λάθος όνομα χρήστη ή κωδικός
            if(errors<2):
                if(errors!=0):err.destroy()
                err=tkinter.Label(parent, bg='white', text="Λάθος όνομα χρήστη ή κωδικός. \nΑποτυχία σύνδεσης.", fg="red", font=('arial','11'))
                err.pack()
                errors=2   
    return

#δημιουργία παραθύρου για την εισαγωγή όνομα χρήστη και κωδικός
global errors
errors=0
parent=scrollbar.create("350x170",'Σύνδεση',1)

name=tkinter.Label(parent,text="Userame",font=('times new roman','12'), bg='white').pack()  
e1=tkinter.Entry(parent,font=('times new roman','11'), bg='white', relief='sunken', bd=2)
e1.pack()  
password=tkinter.Label(parent,text = "Password",font=('times new roman','12'), bg='white').pack()  
e2=tkinter.Entry(parent,font=('times new roman','11'), relief='sunken', bd=2,show="*")
e2.pack()
submit=HoverBtn(parent,text="Submit",font=('times new roman','13'), command=lambda: connect(), relief='flat', bg='white')
submit.pack()
parent.bind('<Return>', connect)

parent.mainloop()


