import pymysql
import itertools
from datetime import datetime
from tkinter import*
from tkinter import ttk
import scrollbar
from PIL import ImageTk,Image

def error(t): #Δημιουργία παραθύρου Σφάλματος
    err_window=scrollbar.create('350x150','Σφάλμα')
    i=Image.open("error1.JPG")
    img_err=ImageTk.PhotoImage(i)
    Label(err_window,bg='white',image=img_err).pack(side=LEFT)
    Label(err_window,bg='white', text=t, fg="red", font=('arial','14')).pack(side=LEFT)
    err_window.mainloop()
    return

def success(t,option=0): #Δημιουργία παραθύρου επιτυχίας
    succ_window=scrollbar.create('380x250','Επιτυχία')
    i=Image.open("succ1.JPG")
    img=ImageTk.PhotoImage(i)
    Label(succ_window,bg='white',image=img).pack()
    Label(succ_window,bg='white', text=t, font=('arial','14')).pack()
    if(option==1):
        Label(succ_window,bg='white', text="Προσοχή!\nΔεν υπάρχει αρκετό απόθεμα", font=('arial','14'),fg='red').pack()
    succ_window.mainloop()
    return

def greek(word): #Μετάφραση σε ελληνικά
    translation={'album_id':'Κωδ. Άλμπ.', 'song_id':'Κωδ.Τραγ.', 'track_no':'Track_no', 'genre':'Είδος',
           'organo_afm':'ΑΦΜ οργανοπαίκτη', 'client_afm':'ΑΦΜ πελάτη','studio_id':'Κωδ.στούντιο', 'afm':'ΑΦΜ',
           'order_date':'Ημερ.παραγγελίας','id_contract':'Κωδ.Συμβολαίου', 'titlos':'Τίτλος',
    'vinyl_stock':'Απόθεμα Βινυλ.',
    'CD_stock':'Απόθεμα CD',
    'release_date':'Ημερ.Κυκλοφ.',
    'graf_afm':'ΑΦΜ γραφίστα',
    'royalties_prof':'Κέρδη πνευμ.δικ.',
    'kin1':'Κινητό 1',
    'kin2':'Κινητό 2',
    'stathero':'Σταθερό',
    'email':'Email',
    'socialmedia':'Social media',
    'Manager_id':'Κωδ.μάνατζερ',
    'manager_id':'Κωδ.μάνατζερ',
    'TK':'ΤΚ',
    'address':'Διεύθυνση',
    'city':'Πόλη',
    'fullname':'Όνομα',
    'AMKA':'ΑΜΚΑ',
    'startdate':'Ημ. Έναρξης',
    'enddate':'Ημ. Λήξης',
    'hours':'Ώρες ηχ.',
    'specialty':'Μουσική ιδιότητα',
    'artist_id':'Κωδ.καλλιτέχνη',
    'name':'Όνομα',
    'stage_name':'Καλλ.ονομασία',
    'adm_fee':'Κόστος Καταχώρησης',
    'eidos':'Είδος',
    'posothta':'Ποσότητα',
    'item_profit':'Κέρδος ανά τεμάχιο',
    'hourly_rate':'Χρέωση ανά ώρα',
    'onoma':'Όνομα',
    'firstname':'Όνομα',
    'lastname':'Επώνυμο',
    'sex':'Φύλο',
    'pososto':'Ποσοστό',
    'diarkeia':'Διάρκεια',
    's_language':'Γλώσσα',
    'album':'Άλμπουμ',
    'manager':'Μάνατζερ',
    'studio_afm':'ΑΦΜ studio',
    'rec_start':'Ημ.έναρξης ηχ.',
    'rec_end':'Ημ.ολοκλ.ηχ.'}
    return translation[word]

def get_primary(table,conn): #βρίσκει τα PRIMARY KEY ενός πίνακα
    cur=conn.cursor()
    cur.execute('''SELECT COLUMN_NAME
                    FROM `INFORMATION_SCHEMA`.`COLUMNS` 
                    WHERE `TABLE_SCHEMA`='recordcompany2' 
                    AND `TABLE_NAME`=%s AND `COLUMN_KEY`="PRI"''',table)
    primary_tuple=cur.fetchall()
    primary=[]
    for i in range(len(primary_tuple)):
        primary.append(primary_tuple[i][0])
    cur.close()
    return primary

def generate(a,b): #δημιουργια λίστας με νούμερα σε μορφη string απο το a μέχρι το b
    r=[]
    for i in range(a,b+1):
        if(i<10):
            value='0'+str(i)
        else:
            value=str(i)
        r.append(value)
    return r

def timing_combobox(fr,grid_col,a,st,init): # δημιουργια combobox για δεδομένα τυπου date,datetime,time.
                                   #(frame,grid_column,list of options,seperator of comboboxes,initial value of combobox)
    comb_arr=[]
    for c in range(3):
        combo=ttk.Combobox(fr,values=a[c],font=('arial','13'),width=len(a[c][10]))

        # αν ειναι δεδομενα για ετος columnspan=2, αλλιως default δηλαδη 1
        if(a[c][0]=='1970'):
            combo.grid(column=grid_col,row=0,columnspan=2,sticky=W)
            grid_col=grid_col+1
        else:
            combo.grid(column=grid_col,row=0,sticky=W)
        
        grid_col=grid_col+1
        combo.current(init[c])
        comb_arr.append(combo)
        if(c!=2):
            Label(fr,bg='white', text=f'{st}', fg="blue", font=('arial','13')).grid(column=grid_col,row=0,sticky=W)
            grid_col=grid_col+1
    return comb_arr

def time_data(i,new_val) :#δημιουργια δεδομένων για combobox για δεδομένα time 
    
    #δημιουργια και τοποθέτηση frame
    fr=Frame(new_val)
    fr.grid(column=2,row=i,columnspan=2,rowspan=1,sticky=W)
    
    # δημιουργια πίνακα a(πιθανές επιλογές του combobox) και πίνακα init(αρχική τιμή combobox)
    a=[]
    init=[]
    a.append(generate(0,59))
    a.append(a[0])
    a.append(a[0])
    init.append(0)
    init.append(0)
    init.append(0)
    return timing_combobox(fr,0,a,':',init)

def date_data(i,new_val):#δημιουργια δεδομένων για combobox για δεδομένα date
    
    #δημιουργια και τοποθέτηση frame
    fr=Frame(new_val)
    fr.grid(column=2,row=i,columnspan=2,rowspan=1,sticky=W)
    
    # δημιουργια πίνακα a (πιθανές επιλογές του combobox) και πίνακα init(αρχική τιμή combobox)
    a=[]
    init=[]
    a.append(generate(1970,2100))
    a.append(generate(1,12))
    a.append(generate(1,31))
    init.append(50)
    init.append(0)
    init.append(0)
    return timing_combobox(fr,0,a,'-',init)

def datetime_data(i,new_val):#δημιουργια δεδομένων για combobox για δεδομένα datetime
    now=datetime.now()
    r_date=[]
    r_time=[]
    result=[]
    
    #δημιουργια και τοποθέτηση frame
    fr=Frame(new_val)
    fr.grid(column=2,row=i,columnspan=5,rowspan=1,sticky=W)
    
    # δημιουργια πίνακα a(πιθανές επιλογές του combobox) και πίνακα init(αρχική τιμή combobox), για τα δεδομένα date
    a=[]
    init=[]
    a.append(generate(1970,2100))
    a.append(generate(1,12))
    a.append(generate(1,31))
    init.append(int(now.strftime("%Y"))-1970)
    init.append(int(now.strftime("%m"))-1)
    init.append(int(now.strftime("%d"))-1)
    r_date.append(timing_combobox(fr,0,a,'-',init))
    # δημιουργια πίνακα a(πιθανές επιλογές του combobox) και πίνακα init(αρχική τιμή combobox), για τα δεδομενα time
    Label(fr,bg='white', text=' ', fg="blue", font=('Lucida Console','13')).grid(column=7,row=0,sticky=W)
    a=[]
    init=[]
    a.append(generate(0,23))
    a.append(generate(0,59))
    a.append(generate(0,59))
    init.append(int(now.strftime("%H")))
    init.append(int(now.strftime("%M")))
    init.append(int(now.strftime("%S")))
    r_time.append(timing_combobox(fr,8,a,':',init))

    #Συγχώνευση αποτελεσμάτων σε μία λίστα
    for i in range(6):
        if(i<3):
            result.append(r_date[0][i])
        else:
            result.append(r_time[0][i-3])
    return result

def printing(table,sql,conn,window):#εκτύπωση δεδομένων

    #παίρνουμε τα ονόματα των στηλών και το μέγιστο μέγεθος χαρακτήρων (αν υπάρχει)
    cur=conn.cursor()
    cur.execute('''SELECT COLUMN_NAME,CHARACTER_MAXIMUM_LENGTH
                       FROM `INFORMATION_SCHEMA`.`COLUMNS` 
                       WHERE `TABLE_SCHEMA`='recordcompany2' 
                       AND `TABLE_NAME`=%s ''',table)
    info=cur.fetchall()
    info_arr=[]
    N=len(info)

    #δημιουργία του πίνακα info_arr που θα έχει το μέγιστο μέγεθος χαρακτήρων για κάθε στήλη
    for i in range(N):
        temp=0
        if(info[i][1] is None):
            if(('order_date' not in info[i][0])):
                temp=13
            else:
                temp=19
        else:
            temp=int(info[i][1])
        if(temp>len(greek(info[i][0]))):
            info_arr.append(temp)
        else:
            info_arr.append(len(greek(info[i][0])))

    #εκτέλεση sql και διαχείριση των λαθών
    cur.execute(sql)
    row=cur.fetchone()
    if(row is None):
        error("Δεν βρέθηκε!")
    else:
        #καταστροφή του παλιού παραθύρου,αν υπήρχε
        if(window!=0):window.destroy()
        #δημιουργία νέου παραθύρου
        fr,root=scrollbar.scroll_window("1600x600")
        root.title('Εκτύπωη Δεδομένων')
        #εκτύπωση των ονομάτων των στηλών
        for i in range(N):
            Label(fr,bg='white',font=('Lucida Console','10'),text=f'{greek(info[i][0]):<{info_arr[i]}} ',width=info_arr[i]+1,fg="red2",anchor=W).grid(column=i,row=0,sticky=W)
        c=1
        while row is not None:
            #εναλλαγή χρώματος
            if c%2:
                color='grey97'
            else:
                color='white'
            #μετατροπή δεδομένων σε μορφή str για εκτύπωση
            for i in range(N):
                if row[i] is None or row[i]=='0000-00-00' or row[i]=='0000-00-00 00:00:00':
                    data='-'
                elif('date' not in info[i][0] and 'rec' not in info[i][0]):
                    data=str(row[i])
                else:
                    if('order_date' in info[i][0]):
                        data = row[i].strftime("%Y-%m-%d %H:%M:%S")
                    elif('diarkeia' in info[i][0]):
                        data = row[i].strftime("%H:%M:%S")
                    else:
                        data = row[i].strftime("%Y-%m-%d")
                        
                #εκτύπωση στοιχείων γραμμής
                Label(fr,bg=color,font=('Lucida Console','10'),text=f'{data:<{info_arr[i]}} ',width=info_arr[i]+1,anchor=W).grid(column=i,row=c,sticky=W)
            c=c+1
            row=cur.fetchone()
        cur.close()
    return