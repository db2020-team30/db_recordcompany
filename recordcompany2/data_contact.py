import pymysql
import itertools
from datetime import datetime
import basic_functions
from tkinter import*
from tkinter import ttk
import scrollbar

def grafistas(conn): #"Γραφίστες και τα άλμπουμ που έχουν επιμεληθεί"

    #δημιουργία παραθύρου
    fr,root=scrollbar.scroll_window("1550x600")
    root.title('Γραφίστες/άλμπουμ')
    root.config(bg='white')

    #εκτέλεση ερωτήματος sql
    cur=conn.cursor()
    cur.execute('''SELECT afm,fullname,amka,address,city,tk,album_id,titlos,release_date
                    FROM grafistas left OUTER JOIN ALBUM on afm=graf_afm
                    ORDER BY afm''')
    graf=cur.fetchone()
    afm=''
    i=0
    a=0

    #εκτύπωση δεδομένων
    while(graf is not None):

        #αν το ΑΦΜ του γραφίστα δεν έχει ξαναεμφανιστεί
        if(afm!=graf[0]):

            #αλλαγή χρώματος background
            if a%2:
                color='grey97'
            else:
                color='white'
            a=a+1
            i=i+1
            afm=graf[0]

            #εκτύπωση των ονομάτων των στηλών                                     
            Label(fr,bg=color,font=('Lucida Console','11'),text=(f'\n{"ΑΦΜ":<9} {"ΟΝΟΜΑ":<50} {"ΑΜΚΑ":<16} {"ΔΙΕΥΘΥΝΣΗ":<30} {"ΠΟΛΗ":<30} {"ΤΚ":<5}\n'),anchor=W, fg='forest green',width=150).grid(column=0,row=i,sticky=W)
            i=i+1

            #εκτύπωση στοιχείων γραφίστα
            Label(fr,bg=color,font=('Lucida Console','11'),text=(f'{graf[0]:<9} {graf[1]:<50} {graf[2]:<16} {graf[3]:<30} {graf[4]:<30} {graf[5]:<5}'),anchor=W, width=150).grid(column=0,row=i,sticky=W)
            i=i+1

            #αν έχει επιμεληθεί άλμπουμ ο γραφίστας, εκτύπωση του κατάλληλου μηνύματος και των αντίστοιχων ονομάτων των στηλών
            if(graf[6] is not None):
                Label(fr,bg=color,font=('Lucida Console','11'),text=("\n\nΑΛΜΠΟΥΜ ΠΟΥ ΕΧΕΙ ΕΠΙΜΕΛΗΘΕΙ:\n"), width=150, anchor=W, fg='forest green').grid(column=0,row=i, sticky=W)
                i=i+1
                Label(fr,bg=color,font=('Lucida Console','11'),text=(f'{"ΚΩΔΙΚΟΣ":<9} {"ΤΙΤΛΟΣ ΑΛΜΠΟΥΜ":<50} {"ΗΜ.ΚΥΚΛΟΦΟΡΙΑΣ":^14}\n'),anchor=W, fg='forest green',width=150).grid(column=0,row=i,sticky=W)
                i=i+1

            #εκτύπωση μηνύματος αν δεν έχει επιμεληθεί άλμπουμ
            else:
                Label(fr,bg=color,font=('Lucida Console','11'),text=("\n\nΔεν έχει επιμεληθεί αλμπουμ\n"),fg='forest green', anchor=W, width=150).grid(column=0,row=i, sticky=W)
                i=i+1   

        #διαχείριση των δεδομένων τύπου date και εκτύπωση των δεδομένων των άλμπουμ που έχει επιμεληθεί
        if(graf[6] is not None):
            data=[]
            data.append(str(graf[6]))
            data.append(str(graf[7]))
            data.append(graf[8].strftime("%Y-%m-%d"))
            Label(fr,bg=color,font=('Lucida Console','11'),text=(f'{data[0]:<9} {data[1]:<50} {data[2]:<16}'), anchor=W, width=150).grid(column=0,row=i,sticky=W)
            i=i+1
        graf=cur.fetchone()

    #κουμπί παραπομπής στην συνάρτηση "show_entry" για την προβολή των στοιχείων επικοινωνίας 
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας γραφίστα",font=('times new roman','13'),fg='dark green',command= lambda: basic_functions.select_pleiad(5,conn,'epik_graf'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close
    return

def pelates(conn): #"Πελάτες και ποσότητες των προϊόντων που προμηθεύτηκαν"

    #δημιουργία παραθύρου
    fr,root=scrollbar.scroll_window("800x600")
    root.title('Πελάτες/Ποσότητα προμήθειας')
    root.config(bg='white')

    #εκτέλεση sql
    cur=conn.cursor()
    cur.execute('''
    SELECT pelaths.afm, pelaths.name, pwleitai.eidos,SUM(pwleitai.posothta)
    FROM pelaths join pwleitai on pelaths.afm=pwleitai.afm
    GROUP BY pelaths.afm, pwleitai.eidos
    ''')
    ans=cur.fetchone()

    #εκτύπωση των ονομάτων των στηλών
    p1='ΑΦΜ'
    p2='Όνομα'
    p3='Είδος'
    p4='Ποσότητα'
    i=0
    Label(fr,bg='white',font=('Lucida Console','12'),text=(f'{p1:9} {p2:50} {p3:7} {p4:10}'),fg="red2").grid(column=0,row=i,sticky=W)
    i=1
    while ans is not None:

        #αλλαγή του χρώματος background και εκτύπωση των δεδομένων
        if i%2:
            Label(fr,bg='grey96',font=('Lucida Console','12'), text=(f'{ans[0]:9} {ans[1]:50} {ans[2]:7} {ans[3]:^10}')).grid(column=0,row=i,sticky=W)
        else:
            Label(fr,bg='white',font=('Lucida Console','12'),text=(f'{ans[0]:9} {ans[1]:50} {ans[2]:7} {ans[3]:^10}')).grid(column=0,row=i,sticky=W)
        ans=cur.fetchone()
        i=i+1

    #κουμπί παραπομπής στην συνάρτηση "show_entry" για την προβολή των στοιχείων επικοινωνίας 
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας πελάτη",font=('times new roman','13'),fg='forest green',command= lambda: basic_functions.select_pleiad(5,conn,'epik_pelath'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close()
    return
