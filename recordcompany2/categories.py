import pymysql
import itertools
from datetime import datetime
from tkinter import*
from tkinter import ttk
import scrollbar
import basic_functions


def choice(a,conn): #δημιουργία παραθύρου για επιλογή 
    if(a==1): #για την περίπτωση "Στοιχεία συμβολαίων ανά κατηγορία καλλιτεχνών"
        window=scrollbar.create('350x250','Επιλογή Ιδιότητας')
        ep=['*** Όλες ***','Στιχουργοί','Συνθέτες','Μουσικοί']
        label='Επιλέξτε ιδιότητα'
        b=Button(window,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: idiothta(conn,window,combo.get()))
    else: #για την περίπτωση "Συγκροτήματα/Τραγουδιστές"
        window=scrollbar.create('350x250','Επιλογή Κατηγορίας')
        ep=['Συγκροτήματα','Τραγουδιστές']
        label='Επιλέξτε κατηγορία'
        b=Button(window,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: band(conn,window,combo.get()))
    Label(window,bg='white', text=label, fg="blue", font=('arial','13')).pack()
    combo=ttk.Combobox(window,values=ep,font=('arial','13'),width=25)
    combo.pack()
    combo.current(0)
    b.pack()
    window.mainloop()
    return

        
def idiothta(conn,window,choise): #"Στοιχεία συμβολαίων ανά κατηγορία καλλιτεχνών"

    #λεξικό για μετάφραση της εισόδου του χρήστη
    d={}
    d['*** Όλες ***']=['stixourgos', 'syntheths', 'mousikos']
    d['Στιχουργοί']=['stixourgos']
    d['Συνθέτες']=['syntheths']
    d['Μουσικοί']=['mousikos']

    #καταστροφή παραθύρου επιλογής και δημιουργία νέου για τα αποτελέσματα
    window.destroy()
    ch=d[choise]
    cur=conn.cursor()
    size="1000x600"
    fr,root=scrollbar.scroll_window(size)
    root.title('Στοιχεία συμβολαίων ανά κατηγορία καλλιτεχνών')
    root.config(bg='white')
    i=0

    #εκτέλεση επανάληψης για κάθε ιδιότητα. Αν επιλέχθηκε συγκεκριμένη από τον χρήστη, θα εκτελεστεί μόνο μια φορά
    for spec in ch:

        #εκτέλεση ερωτήματος sql
        cur.execute('''
        SELECT {}.afm, firstname, lastname, id_contract, startdate, enddate, pososto
        FROM {} join symbeblhmenos on {}.afm=symbeblhmenos.afm, symbolaio
        WHERE symbeblhmenos.afm=symbolaio.afm 
        ORDER BY {}.afm, enddate DESC
        '''.format(spec, spec, spec, spec))
        ans=cur.fetchone()

        #εκτύπωση ιδιότητας
        if spec=='stixourgos':
            Label(fr,bg='grey80',font=('Lucida Console','13'), width=140, anchor=W, text='ΣΤΙΧΟΥΡΓΟΙ').grid(column=0,row=i)
            i=i+1
        if spec=='syntheths':
            Label(fr,bg='grey80',font=('Lucida Console','13'), width=140, anchor=W, text='ΣΥΝΘΕΤΕΣ').grid(column=0,row=i)
            i=i+1
        if spec=='mousikos':
            Label(fr,bg='grey80',font=('Lucida Console','13'), width=140, anchor=W, text='ΜΟΥΣΙΚΟΙ').grid(column=0,row=i)
            i=i+1

        #εκτύπωση των ονομάτων των στηλών 
        r='ΑΦΜ'
        r0='ΟΝΟΜΑ'
        r1='ΕΠΩΝΥΜΟ'
        r2='ΚΩΔ. ΣΥΜΒ'
        r3='ΗΜ.ΕΝΑΡΞΗΣ'
        r4='ΗΜ.ΛΗΞΗΣ'
        r5='ΠΟΣΟΣΤΟ'
        Label(fr,bg='white',font=('Lucida Console','11'), width=140, anchor=W, text=f'{r:9} {r0:20} {r1:20} {r2:10} {r3:8} {r4:8} {r5:3}',fg="red2").grid(column=0,row=i,sticky=W)
        i=i+1
        blank=''
        afm=''
        while ans is not None:

            #αλλαγή χρώματος background
            if i%2:
                color='white'
            else:
                color='grey97'

            #διαχείρηση δεδομένων date
            if(ans[4] is None):
                data1=''
            else:
                data1=ans[4].strftime("%Y-%m-%d")
            if(ans[5] is None):
                data2=''
            else:
                data2=ans[5].strftime("%Y-%m-%d")

            #εκτύπωση των δεδομένων, αν είναι το πρώτο συμβόλαιο του συμβεβλημένου που εμφανίζεται
            if ans[0]!=afm:
                Label(fr,bg=color, font=('Lucida Console','11'), width=140, anchor=W, text=f'{ans[0]:9} {ans[1]:20} {ans[2]:20} {ans[3]:10} {data1:10} {data2:10} {ans[6]:3}').grid(column=0,row=i,sticky=W)
                i=i+1
                afm=ans[0]

            #εκτύπωση των δεδομένων,αν δεν είναι το πρώτο συμβόλαιο του συμβεβλημένου που εμφανίζεται
            else:
                Label(fr,bg=color, font=('Lucida Console','11'), width=140, anchor=W, text=f'{blank:9} {blank:20} {blank:20} {ans[3]:10} {data1:10} {data2:10} {ans[6]:3}').grid(column=0,row=i,sticky=W)
                i=i+1
            ans=cur.fetchone()
    cur.close()
    Label(fr, bg='white', text='').grid(column=0,row=i,sticky=S)
    i=i+1

    #κουμπί παραπομπής στην συνάρτηση "show_entry" για την προβολή των στοιχείων επικοινωνίας 
    b1=Button(fr,bg='white', width=30, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας συμβεβλημένου",font=('helvetica','11'), command= lambda: basic_functions.select_pleiad(5,conn,'epik_symbebl'))
    b1.grid(column=0,row=i, sticky=W)
    root.mainloop()
    return

def band(conn,window,choise): #"Συγκροτήματα/Τραγουδιστές"
    window.destroy() #καταστροφή προηγούμενου παραθύρου

    #δημιουργία λεξικού για μετατροπή της επιλογής του χρήστη
    d={'Συγκροτήματα':'1','Τραγουδιστές':'2'}
    ch=d[choise]
    cur=conn.cursor()

    #δημιουργία καινούργιου παραθύρου
    size="800x600"
    fr,root=scrollbar.scroll_window(size)
    root.title('Συγκροτήματα/Τραγουδιστές')
    root.config(bg='white')
    i=0

    #ανάλογα με την επιλογή του χρήστη, θέτουμε το "char" και εμφανίζουμε το κατάλληλο μήνυμα 
    if(ch=='1'):
        char='>'
        Label(fr,bg='grey80',font=('Lucida Console','12'),text='Ονόματα συγκροτημάτων και αντίστοιχα μέλη:',width=61, anchor=W).grid(column=0,row=i)
    else:
        char='='
        Label(fr,bg='grey80',font=('Lucida Console','12'),text='Τραγουδιστές:',width=61, anchor=W).grid(column=0,row=i)

    #εκτέλεση sql.Το "char" που ορίστικε παραπάνω, διαμορφώνει κατάλληλα το ερώτημα ανάλογα την επιλογή του χρήστη
    cur.execute('''
    SELECT mousikos.afm, firstname, lastname, specialty,(SELECT stage_name FROM persona_group WHERE persona_group.artist_id=mousikos.artist_id)
    FROM (mousikos JOIN symbeblhmenos ON mousikos.afm=symbeblhmenos.afm)
    WHERE artist_id in (SELECT artist_id FROM mousikos GROUP BY artist_id HAVING count(artist_id){}1)
    ORDER BY artist_id,mousikos.afm
    '''.format(char))
    ans=cur.fetchone()
    band=''
    i=i+1

    #εκτύπωση των ονομάτων των στηλών
    Label(fr,bg='white',font=('Lucida Console','11'),text=f'\n{"ΑΦΜ":<9} {"ΟΝΟΜΑ":<20} {"ΕΠΩΝΥΜΟ":<20} {"ΜΟΥΣΙΚΗ ΙΔΙΟΤΗΤΑ":<16}',fg="red2",width=68, anchor=W).grid(column=0,row=i,sticky=W)
    i=i+1

    #εκτύπωση αποτελεσμάτων
    while ans is not None:

        #Αν το καλλιτεχνικό όνομα δεν έχει ξαναεμφανιστεί, εκτύπωσή του  
        if(band!=ans[4]):
            Label(fr,bg='grey85',font=('Lucida Console','11'),text='{}'.format(ans[4]),width=68,anchor=W).grid(column=0,row=i,sticky=W)
            band=ans[4]
            i=i+1

        #αλλαγή χρώματος background
        if i%2:
            color='white'
        else:
            color='grey97'

        #εκτύπωση των δεδομένων
        Label(fr,bg=color,font=('Lucida Console','11'),text=f'{ans[0]:<9} {ans[1]:<20} {ans[2]:<20} {ans[3]:<16}',width=68, anchor=W).grid(column=0,row=i,sticky=W)
        i=i+1
        ans=cur.fetchone()

    #κουμπί παραπομπής στην συνάρτηση "show_entry" για την προβολή των στοιχείων επικοινωνίας
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας συμβεβλημένου",font=('helvetica','13'),command= lambda: basic_functions.select_pleiad(5,conn,'epik_symbebl'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close()
    root.mainloop()
    return
