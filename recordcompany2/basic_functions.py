import pymysql
import itertools
from datetime import datetime
from tkinter import*
from tkinter import ttk
import scrollbar
from PIL import ImageTk,Image
import helping_func

def select_row_window(a,conn,table):  # παράθυρο για επιλογή γνωρισμάτων πλειάδας (για διαγραφή, ενημέρωση ή εκτύπωση πλειάδας)
    
    if(a!=5):  #στην διαγραφή και στην ενημέρωση,η επιλογή γίνεται βάσει του primary key
        fields=helping_func.get_primary(table,conn)
    else:  #στην εκτύπωση πλειάδας,η επιλογή γίνεται βάσει οποιουδήποτε γνωρίσματος
        fields=[]
        cur=conn.cursor()
        cur.execute(f'''
        SELECT COLUMN_NAME
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='recordcompany2' 
        AND `TABLE_NAME`="{table}"''')
        c=cur.fetchall()
        for i in range(len(c)):
            fields.append(str(c[i][0]))
        cur.close()

    #δημιουργία παραθύρου
    window=scrollbar.create('500x400','Επιλογή πλειάδας')

    #Εαν γίνεται ενημέρωση, γίνεται έλεγχος για το αν υπάρχουν στοιχεία που δεν ειναι PRIMARY KEY. Αν δεν υπάρχουν, η ενημέρωση ακυρώνεται
    col=[]
    if(a==3):
        cur=conn.cursor()
        cur.execute('''
        SELECT COLUMN_NAME
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_SCHEMA`='recordcompany2' 
        AND `TABLE_NAME`=%s AND `COLUMN_KEY`!="PRI"''',table)
        c=cur.fetchall()
        for i in range(len(c)):
            col.append(c[i][0])
        cur.close()
        if(len(col)==0):
            Label(window,bg='white', text="Δεν μπορείτε να αλλάξετε αυτόν τον πίνακα.\nΔοκιμάστε διαγραφή και εισαγωγή εκ νέου.", fg="red", font=('arial','14')).grid(column=0,row=0,sticky=N)
            return
    

    Label(window,bg='white', text='Επιλέξτε πλειάδα', fg="blue", font=('arial','13')).grid(column=1,row=0,sticky=N)

    #Για καθε στήλη που ειναι primary key, δημιουργείται Combobox με επιλογές τα αποθηκευμένα στοιχεία της στήλης.
    #Για την επιλογή "Εκτύπωση πλειάδας" γίνεται για όλες τις στήλες
    i=1
    combobox_array=[]
    for k in fields:
        #εμφάνιση ονόματος στήλης
        Label(window,bg='white', text=f'{helping_func.greek(k)}:', fg="blue", font=('arial','13')).grid(column=0,row=i,sticky=W,padx=10)
        cur=conn.cursor()
        cur.execute(f'''SELECT DISTINCT {k}
                        FROM {table}''')
        option_tuple=cur.fetchone()
        op=[]

        #αν είναι η επιλογή "εκτύπωση πλειάδας", βαζουμε και την επιλογή '-', ώστε να επιλέγει αυτό ο χρήστης, αμα δεν θέλει να αναζητήσει πλειάδα βάσει αυτού του γνωρίσματος       
        if(a==5):
            op.append('-')
        elif(option_tuple is None): #αλλιώς αν δεν υπάρχουν δεδομένα(σε στήλη που ειναι PRIMARY KEY),εμφανίζεται μήνυμα λάθους
            helping_func.error("Δεν υπάρχουν πλειάδες")
            return

        #δημιουργία επιλογών του Combobox
        while option_tuple is not None:
            op.append(str(option_tuple[0]))
            option_tuple=cur.fetchone()

        #δημιουργία Combobox
        combo=ttk.Combobox(window,values=op,font=('arial','13'),width=25)
        combo.grid(column=1,row=i,columnspan=2)
        combo.current(0)
        combobox_array.append(combo)
        i=i+1
        cur.close()

    #δημιουργία κουμπίων
    if a==5:
        Button(window,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: show_row(table,conn,combobox_array,fields,window)).grid(column=1,row=i,sticky=S)
    elif a==2:
        Button(window,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: delete_row(table,conn,combobox_array,window)).grid(column=1,row=i,sticky=S)
    else:
        Button(window,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: columns_to_update(table,conn,combobox_array,window,col)).grid(column=1,row=i,sticky=S)
    window.mainloop()
    return

def columns_to_update(table,conn,combobox_array,window,col): #επιλογή στηλών προς ενημέρωση
    entry=[]

    #αποθήκευση επιλεγμένης πλειάδας
    for i in combobox_array:
        entry.append(i.get())
    window.destroy() #καταστροφή παραθύρου επιλογής πλειάδας
    cur=conn.cursor()

    #δημιουργία παραθύρου επιλογής στηλών προς ενημέρωση
    check=scrollbar.create('340x350','Επιλογή στοιχείων για ενημέρωση')
    Label(check,bg='white', text='Επιλέξτε ποιές τιμές θέλετε να ενημερώσετε', fg="blue", font=('arial','13')).pack()

    #δημιουργία των "Checkbutton", ένα για κάθε στήλη που δεν είναι PRIMARY KEY 
    ch_arr=[]
    for i in col:
        ch=IntVar()
        c=Checkbutton(check,bg='white',text=f'{helping_func.greek(i)}',variable=ch,font=('arial','13'))
        c.pack()
        ch_arr.append(ch)

    #κουμπί για αποθήκευση επιλογής που παραπέμπει στην "new_data"
    Button(check,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: new_data(3,conn,table,entry,col,check,ch_arr)).pack()
    return

def updating(table,primary,entry,column,data,conn):
    cur=conn.cursor()
    if(data!='NULL'): data="'" +str(data)+"'" #τροποποιουμε το data στην σωστη μορφη

    #δημιουργια εντολής sql
    sql="UPDATE `{}` set `{}`={} where {}={}".format(table,column,data,primary[0],entry[0])
    for i in range(1,len(primary)):
        sql=sql+(' and {}={}'.format(primary[i],entry[i]))
    sql=sql+(';')

    #εκτέλεση εντολής sql και διαχείριση λαθών
    try:
       cur.execute(sql)
    except pymysql.Error:
        cur.close()
        return helping_func.greek(column)
    cur.close()
    conn.commit()
    return 

    
def update_exe(conn,table,entry,entries,columns,new_val): #αποθήκευση επιλογής γνωρισμάτων προς αλλαγή και κλήση της "updating"
    helping_func.error_col=[]

    #επανάληψη για όσα γνωρίσματα θέλει να αλλάξει ο χρήστης
    for i in range(len(columns)):

        #για γνωρισματα που δεν ειναι τυπου date,time
        if(len(entries[i])==1):
            temp1=entries[i][0].get()
            if(temp1==''):temp='NULL' #μετατροπή κενού σε NULL
            a=updating(table,helping_func.get_primary(table,conn),entry,columns[i],temp1,conn) #εκτέλεση ενημέρωσης
        else: #για γνωρισματα τυπου date,time
            temp=[]
            for c in range(3):
                temp.append(entries[i][c].get())
            if('date' not in columns[i] and 'rec' not in columns[i] ):
                a=updating(table,helping_func.get_primary(table,conn),entry,columns[i],temp[0]+':'+temp[1]+':'+temp[2],conn) #εκτέλεση ενημέρωσης για γνωρισματα τυπου time
            else:

                #έλεγχος για το αν η ημερομηνία είναι σωστή
                try :
                    datetime(int(temp[0]),int(temp[1]),int(temp[2]))
                    a=updating(table,helping_func.get_primary(table,conn),entry,columns[i],temp[0]+'-'+temp[1]+'-'+temp[2],conn) #εκτέλεση ενημέρωσης για γνωρισματα τυπου date
                except ValueError :
                    helping_func.error("Λανθασμένη\nημερομηνία!")
                    return
        if(a is not None):
            helping_func.error_col.append(a)

    #προβολή μηνυμάτων σχετικά με την ολοκλήρωση της διαδικασίας   
    if(helping_func.error_col!=[]):
        if len(helping_func.error_col)==1:
            text="Δεν καταχωρήθηκαν\nοι αλλαγές στο {}".format(helping_func.error_col[0])
        else:
            text="Δεν καταχωρήθηκαν\nοι αλλαγές στα:\n{}\n".format(helping_func.error_col[0])
            for i in range(1,len(helping_func.error_col)):
                text=text+"\n{}\n".format(helping_func.error_col[i])
        helping_func.error(text)
        return
    else:
        helping_func.success("Επιτυχής ενημέρωση")
        return
    new_val.destroy()
    return

def new_data(option,conn,table,entry,columns,check='',ch_arr=''): #επιλογή καινούριων δεδομένων
    
    #για ενημέρωση
    if(option==3):

        #δημιουργια αντίγραφου των αρχικών ονομάτων των στηλών
        columns_original=[]
        for item in columns:columns_original.append(item)

        #αφαίρεση απο το "columns" όσων στηλών δεν επιλέχθηκαν 
        for i in range(len(ch_arr)):
            if(ch_arr[i].get()!=1): columns.remove(columns_original[i])

        #εάν δεν επιλέχθηκαν στήλες, εμφάνιση μηνύματος λάθους και ακύρωση της ενημέρωσης
        if(len(columns)==0):
            helping_func.error('Δεν επιλέξατε στοιχεία προς τροποποίηση!')
            return
        else:   #αλλιώς, καταστροφή προηγούμενου παραθύρου
            check.destroy()

    #για εισαγωγή
    if(option==1):

        #δημιουργία λίστας με τις στήλες
        columns=[]
        cur=conn.cursor()
        cur.execute('''SELECT `COLUMN_NAME` 
                       FROM `INFORMATION_SCHEMA`.`COLUMNS` 
                       WHERE `TABLE_SCHEMA`='recordcompany2' 
                       AND `TABLE_NAME`=%s;''',table)
        row=cur.fetchall()
        for i in range(len(row)):
            columns.append(row[i][0])
        cur.close()

    nv=[]
    entries=[]
    new_val=scrollbar.create('500x300','Νέες τιμές') #δημιουργία νέου παραθύρου

    #Εντοπισμός Foreign key
    cur=conn.cursor()
    cur.execute(f'''SELECT 
                    COLUMN_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
                    FROM
                    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                    WHERE
                    REFERENCED_TABLE_SCHEMA = 'recordcompany2' AND
                    TABLE_NAME = "{table}";''')
    fk_tuple=cur.fetchone()
    fk_arr=[]
    fk_col_arr=[]
    while fk_tuple is not None:
        temp=[]
        fk_col_arr.append(str(fk_tuple[0]))
        for i in range(1,3):
            temp.append(str(fk_tuple[i]))
        fk_arr.append(temp)
        fk_tuple=cur.fetchone()
    cur.close()

    #δημιουργία του ανάλογου κουτιού εισαγωγής για κάθε στοιχείο της λίστας "columns"
    for i in range(len(columns)):
        Label(new_val,bg='white', text=f'{helping_func.greek(columns[i])}:', font=('arial','13')).grid(column=0,row=i,columnspan=2)
        if(columns[i] in fk_col_arr): # Για τις στήλες που είναι foreign key
            cur=conn.cursor()
            index=-1
            for c in range(len(fk_col_arr)):
                if(columns[i]==fk_col_arr[c]):
                    index=c
            cur.execute(f'''SELECT DISTINCT {fk_arr[index][1]}
                        FROM {fk_arr[index][0]}''')
            option_tuple=cur.fetchone()
            if(option==1):
                op=['-']
            else:
                op=[]
            if(option_tuple is None and option==3): #αν δεν ύπαρχουν δεδομένα (στην στήλη που δείχνει το foreign key),εμφανίζεται μήνυμα λάθους
                helping_func.error("Δεν υπάρχουν δεδομένα\nγια να αντιστοιχίσετε\nτο foreign key!")
                return

            #δημιουργία επιλογών του Combobox
            while option_tuple is not None:
                op.append(str(option_tuple[0]))
                option_tuple=cur.fetchone()

            #δημιουργία Combobox
            combo=[]
            combo.append(ttk.Combobox(new_val,values=op,font=('arial','13'),width=16))
            combo[0].grid(column=2,row=i,columnspan=2)
            combo[0].current(0)
            entries.append(combo)
            cur.close()

        elif(columns[i]=='order_date'): #για δεδομένα datetime
            entries.append(helping_func.datetime_data(i,new_val))

        elif('date' in columns[i] or 'rec' in columns[i]):#για δεδομένα date
            entries.append(helping_func.date_data(i,new_val))

        elif(columns[i]=='diarkeia'):#για δεδομένα time
            entries.append(helping_func.time_data(i,new_val))

        else:#για όλα τα άλλα δεδομένα
            temp1=[]
            temp1.append(Entry(new_val,font=('times new roman','12'), bg='white', relief='sunken', bd=2))
            entries.append(temp1)
            entries[i][0].grid(column=2,row=i,columnspan=2)

    #δημιουργία κουμπιών για αποθήκευση
    if(option==3):
        Button(new_val,bg='white',text="Αποθήκευση",font=('arial','12'),command=lambda: update_exe(conn,table,entry,entries,columns,new_val)).grid(column=1,row=i+1,columnspan=2)
    else:
        Button(new_val,bg='white',text="Αποθήκευση",font=('arial','12'),command=lambda: insert_row(table,conn,entries,new_val,columns)).grid(column=1,row=i+1,columnspan=2)
    new_val.mainloop()
    return
    
    
def show_table(table,conn): #"Εκτύπωση πίνακα"
    sql='''SELECT * FROM `{}`;'''.format(table) #SELECT όλα τα δεδομένα του πίνακα
    helping_func.printing(table,sql,conn,0) #εκτύπωση(βλ. helping_func.py)
    return

def show_row(table,conn,combobox_array,columns,window):
    entry=[]

    #δημιουργια της λίστας "columns_original", που περιέχει όλες τις στήλες
    columns_original=[]
    for item in columns :columns_original.append(item)

    #αποθήκευση των επιλογών του χρήστη στον πινακα entry. Αφαίρεση απο την λίστα με τις στήλες, όσων τους δόθηκε τιμή "-"
    for i in range(len(combobox_array)):
        entry.append(combobox_array[i].get())
        if(entry[i]=='-'):
            columns.remove(columns_original[i])
    if(len(columns)==0):
        helping_func.error("Δεν επιλέξατε δεδομένα!")
        return
    #δημιουργία εντολής sql
    for i in range(len(columns)):
        index=0
        while(columns[i]!=columns_original[index]):
            index=index+1
        if(i==0):
            sql='''SELECT * FROM `{}` WHERE {}="{}"'''.format(table,columns[i],entry[index])
        else:
            sql=sql+" AND {}='{}'".format(columns[i],entry[index])
    sql=sql+";"

    #εκτύπωση
    helping_func.printing(table,sql,conn,window)
    return

def insert_row(table,conn,entries,new_val,columns):
    cur=conn.cursor()
    flag=0
    sql_input=[]
    columns_original=[]
    for item in columns :columns_original.append(item) #δημιουργια αντίγραφου της αρχικής λίστας "columns"

    #Αποθήκευση δεδομένων προς εισαγωγή
    for i in range(len(entries)):

        #για γνωρισματα που δεν ειναι τυπου date,time,datetime
        if(len(entries[i])==1):
            temp1=entries[i][0].get()
            if(temp1=='' or temp1=='-'):
                columns.remove(columns_original[i]) #αφαίρεση κάθε στήλης, που δεν πήρε τιμή, από τις στήλες
            else: 
                temp1="'" +str(temp1)+"'"
                sql_input.append(temp1)

        #για γνωρισματα τυπου date,time,datetime
        else: 
            temp=[]
            for c in range(len(entries[i])):
                temp.append(entries[i][c].get())
            if ('date' not in columns_original[i] and 'rec' not in columns_original[i]):   #αν είναι τύπου time
                sql_input.append(f"'{str(temp[0])}:{str(temp[1])}:{str(temp[2])}'")
            else:

                #έλεγχος για το αν η ημερομηνία είναι σωστή
                try :
                    datetime(int(temp[0]),int(temp[1]),int(temp[2]))
                    if(len(entries[i])==3): # αν είναι τύπου date
                        sql_input.append(f"'{str(temp[0])}-{str(temp[1])}-{str(temp[2])}'")
                    else: #αν είναι τύπου datetime
                        sql_input.append(f"'{str(temp[0])}-{str(temp[1])}-{str(temp[2])} {str(temp[3])}:{str(temp[4])}:{str(temp[5])}'")
                except ValueError : #διαχείριση λάθους
                    new_val.destroy()
                    helping_func.error("Λανθασμένη\nημερομηνία!")
                    return

    #Δημιουργια Sql:

    if(len(columns)==0): #Αν ο χρήστης δεν συμπλήρωσε καμία τιμή, εμφάνισε μήνυμα λάθους
        new_val.destroy()
        helping_func.error("Δεν βάλατε τιμές!")
        cur.close()
        return

    #Επανάληψη για όλες τις στήλες που έχουν δεδομένα
    sql='''INSERT INTO {} ({}'''.format(table,columns[0])
    for i in range(1,len(columns)): 
        sql=sql+',{}'.format(columns[i])
    sql=sql+') VALUES('

    #Επανάληψη για όλα τα δεδομένα που είναι για εισαγωγή
    for i in range(len(sql_input)):
        if i==0:
            sql=sql+'{}'.format(sql_input[i])
        else:
            sql=sql+',{}'.format(sql_input[i])
    sql=sql+');'

    #έλεγχος για αφαίρεση ποσότητας φυσικής αγοράς από το stock
    index=-1
    flag=0
    if (table=='pwleitai'):

        #Εύρεση της καινούργιας θέσης στην λίστα "columns", της στήλης "eidos"(θα είχε αλλάξει η θέση της αμα δεν είχαν συμπληρωθεί όλες οι τιμές)
        for i in range(len(columns)):
            if('eidos' in columns[i]):
                index=i     
        if(index!=-1):
            if(sql_input[index] not in 'DIGITAL'): # Αν ήταν CD ή VINYL
                d={"'CD'":"CD_stock","'VINYL'":"vinyl_stock"}
                if(sql_input[index] not in d): #Διαχείριση λάθους εισαγωγής "eidous"
                    new_val.destroy()
                    helping_func.error('Μη έγκυρη καταχώρηση.\nΛάθος είδος.')
                    cur.close()
                    return
                
                #Εκτέλεση sql για να βρούμε το διαθέσιμο απόθεμα του είδος για το άλμπουμ που επέλεξε ο χρήστη, και διαχείριση λαθών
                try:
                    cur.execute('''SELECT {} from album where album_id={};'''.format(d[sql_input[index]],sql_input[0]))
                except pymysql.Error:
                    new_val.destroy()
                    helping_func.error('sql helping_func.error')
                    cur.close()
                    return
                result=cur.fetchone()
                if(result is None):
                    helping_func.error("Δεν βρέθηκε το άλμπουμ!")
                    return

                #ορισμός flag για να γίνουν οι κατάλληλες ενέργιες στο τέλος
                stock=int(result[0])
                pos=sql_input[4]
                pos=pos.replace("'","")
                pos=int(pos)
                if(pos>stock):
                    flag=-1
                else:
                    flag=1

    #Εκτέλεση της sql για την εισαγωγή των δεδομένων και διαχείριση των λαθών                
    try:
        cur.execute(sql)
    except pymysql.Error:
        new_val.destroy()
        helping_func.error("Η εισαγωγή απέτυχε!")
        cur.close()
        return
    new_val.destroy()

    #Τροποποίηση αποθέματος, αν χρειάζεται 
    if(flag==1):
        try:
           sql="UPDATE album set {}={} where album_id={};".format(d[sql_input[3]],(stock-pos),sql_input[0])
           cur.execute(sql)
        except pymysql.Error:
            helping_func.error("Η τροποποίηση\nτου αποθέματος απέτυχε!")
            cur.close()
            return
    conn.commit()

    #μήνυμα για την επιτυχία της εισαγωγής
    if(flag==0):
        helping_func.success("Η εισαγωγή\nήταν επιτυχής!")
    else: #μήνυμα για την έλλειψη αποθέματος
        helping_func.success("Η εισαγωγή\nήταν επιτυχής!",1)
    cur.close()
    return


def delete_btn(conn,alert_window,sql,table,entry): #εκτέλεση διαγραφής και διαχείριση των λαθών
    alert_window.destroy()
    cur=conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except pymysql.Error:
        helping_func.error("Ακύρωση διαγραφής!")
        return
    helping_func.success("Επιτυχής διαγραφή!")
    cur.close()
    return        


def delete_row(table, conn, combobox_array, window): ##ΔΙΑΓΡΑΦΗ ΠΛΕΙΑΔΑΣ
    
    entry=[] 

    #Αποθήκευση της επιλογής πλειάδας 
    for i in combobox_array:
        entry.append(i.get())
        
    primary=helping_func.get_primary(table,conn) #Εύρεση του/των γνωρισμάτος/των που αποτελούν το πρωτεύον κλειδί

    cur=conn.cursor()
    sql2='''SELECT * FROM {} WHERE {}="{}"'''.format(table,primary[0],entry[0]) 
    sql1='''DELETE FROM {} WHERE {}="{}"'''.format(table,primary[0],entry[0])
    for i in range(1,len(primary)):
        sql1=sql1+' AND {}="{}"'.format(primary[i],entry[i])
        sql2=sql2+' AND {}="{}"'.format(primary[i],entry[i])
    sql1=sql1+';'
    sql2=sql2+';'

    #ελέγχουμε μήπως δεν υπάρχει η πλειάδα που μας δόθηκε
    cur.execute(sql2)
    if(cur.fetchall() is None):
        helping_func.error("Δεν βρέθηκε!")

    else:
        #Καταστροφή του προηγούμενου παραθύρου και δημιουργία του παραθύρου προειδοποίησης
        cur.close()
        window.destroy()
        alert_window=scrollbar.create('450x250','ALERT')
        i=Image.open("alert.JPG")
        img=ImageTk.PhotoImage(i)
        Label(alert_window,bg='white',image=img).grid(column=0,row=0,sticky=NW,columnspan=2)
        Label(alert_window,bg='white', text="Είστε σίγουροι για την διαγραφή;\nΔεν θα μπορεί να γίνει αναίρεση!", fg="red", font=('arial','14')).grid(column=2,row=0,columnspan=2)
        Button(alert_window,bg='white', text="ΔΙΑΓΡΑΦΗ", relief='flat',font=('arial','14'),command= lambda: delete_btn(conn,alert_window,sql1,table,entry)).grid(column=2,row=1,columnspan=2)
        Button(alert_window,bg='white', text="ΑΚΥΡΩΣΗ", relief='flat', font=('arial','14'),command= lambda: alert_window.destroy()).grid(column=2,row=2,columnspan=2)
        alert_window.mainloop()
    return
