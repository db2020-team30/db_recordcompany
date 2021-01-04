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

    #κουμπί παραπομπής στην συνάρτηση "show_row" για την προβολή των στοιχείων επικοινωνίας 
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας γραφίστα",font=('times new roman','13'),fg='dark green',command= lambda: basic_functions.select_row_window(5,conn,'epik_graf'))
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
    FROM pelaths left outer join pwleitai on pelaths.afm=pwleitai.afm
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
        if(ans[2] is None):
            eid='-'
            pos='0'
        else:
            eid=ans[2]
            pos=ans[3]
        #αλλαγή του χρώματος background και εκτύπωση των δεδομένων
        if i%2:
            Label(fr,bg='grey96',font=('Lucida Console','12'), text=(f'{ans[0]:9} {ans[1]:50} {eid:7} {pos:<10}')).grid(column=0,row=i,sticky=W)
        else:
            Label(fr,bg='white',font=('Lucida Console','12'),text=(f'{ans[0]:9} {ans[1]:50} {eid:7} {pos:<10}')).grid(column=0,row=i,sticky=W)
        ans=cur.fetchone()
        i=i+1

    #κουμπί παραπομπής στην συνάρτηση "show_row" για την προβολή των στοιχείων επικοινωνίας 
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας πελάτη",font=('times new roman','13'),fg='forest green',command= lambda: basic_functions.select_row_window(5,conn,'epik_pelath'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close()
    return


def album_per_studio(conn): #"Άλμπουμ ανά studio ηχογράφησης"

    #δημιουργία παραθύρου
    fr,root=scrollbar.scroll_window("1610x600")
    root.title('Άλμπουμ ανά studio ηχογράφησης')
    root.config(bg='white')
    #εκτέλεση sql
    cur=conn.cursor()
    cur.execute('''SELECT onoma,album_id, titlos, vinyl_stock, CD_stock, release_date, graf_afm,royalties_prof,rec_start,rec_end,hours,hourly_rate
                   FROM album  right outer join studio on studio_afm=studio.afm
                   ORDER BY onoma,album_id''')
    ans=cur.fetchone()
    i=0
    studio=''

    #εκτύπωση αποτελεσμάτων
    Label(fr,bg='white',font=('Lucida Console','10'), width=183, anchor=W, text=f'{"Κωδ. Άλμπ.":<11} {"Τίτλος":<50} {"Απόθεμα Βινυλ.":<14} {"Απόθεμα CD":<11} {"Ημερ.Κυκλοφ.":<12} {"ΑΦΜ γραφίστα":<12} {"Κέρδη πνευμ.δικ.":<16} {"Ημ.έναρξης ηχογραφήσης":<22} {"Ημ.ολοκλ.":<10} {"Ώρες ηχογραφήσης":<16}',fg="red2").grid(column=0,row=i,sticky=W)
    while(ans is not None):
        i=i+1

        #εκτύπωση του ονόματος και της χρέωσης ανα ώρα του studio
        if(str(ans[0])!=studio):
            studio=str(ans[0])
            Label(fr,bg='grey85',font=('Lucida Console','10'),text='{}, Χρέωση:{} ευρώ/ώρα'.format(studio,str(ans[11])),width=183,anchor=W).grid(column=0,row=i,sticky=W)
            i=i+1
        if i%2:
            color='white'
        else:
            color='grey97'
            
        #μετατροπή δεδομένων date
        date=[]
        for c in [5,8,9]:
            if(ans[c]is None or ans[c]=='0000-00-00'):
                date.append('-')
            else:
                date.append(ans[c].strftime("%Y-%m-%d"))
        if(ans[1] is None):
            Label(fr,bg=color,font=('Lucida Console','10'),text=f"{'-':<11} {'-':<50} {'-':<14} {'-':<11} {date[0]:<12} {'-':<12} {'-':<16} {date[1]:<22} {date[2]:<10} {'-':^16}",width=183, anchor=W).grid(column=0,row=i,sticky=W)
        else:
            Label(fr,bg=color,font=('Lucida Console','10'),text=f'{str(ans[1]):<11} {str(ans[2]):<50} {str(ans[3]):<14} {str(ans[4]):<11} {date[0]:<12} {str(ans[6]):<12} {str(ans[7]):<16} {date[1]:<22} {date[2]:<10} {str(ans[10]):^16}',width=183, anchor=W).grid(column=0,row=i,sticky=W)
        ans=cur.fetchone()
    i=i+1

    #κουμπι για μετάβαση στο "show_row" για την εύρεση των στοιχείων επικοινωνίας
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας studio",font=('times new roman','13'),command= lambda: basic_functions.select_row_window(5,conn,'epik_studio'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close()
    root.mainloop()
    return
