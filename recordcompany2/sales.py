import pymysql
import itertools
from datetime import datetime
from tkinter import*
from tkinter import ttk

import scrollbar

def cd_or_vinyl(conn): #δημιουργία παραθύρου, για την επιλογή μεταξύ CD και VINYL
    window=scrollbar.create('350x250','Επιλογή Είδους')
    Label(window, text="Επιλέξτε είδος", fg="blue", bg='white', font=('arial','13')).pack()
    combo=ttk.Combobox(window,values=['CD', 'VINYL'],font=('arial','13'))
    combo.pack()
    combo.current(0)
    Button(window,text="Επιλογή",bg='white', font=('arial','12'),command=lambda: physical_sales(conn,window,combo.get())).pack()
    window.mainloop()


def physical_sales(conn,window,eid): #"Φυσικές πωλήσεις"

    #καταστροφή του παραθύρου επιλογής και δημιουργία καινούργιου
    window.destroy()
    size="620x600"
    fr,root=scrollbar.scroll_window(size)
    root.title('Φυσικές πωλήσεις')
    root.config(bg='white')

    #εκτέλεση ερωτήματος sql,ανάλογα με την επιλογή του χρήστη που είναι αποθηκευμένη στο "eid"
    cur=conn.cursor()
    cur.execute(f'''
                SELECT * FROM(
                    (select album.album_id, titlos, sum(posothta) as 'sales'
                    from album join pwleitai on album.album_id=pwleitai.album_id
                    where eidos="{eid}"
                    group by album.album_id)
                
                UNION

                    (select album.album_id, titlos,0 
                    from (album left outer join pwleitai on album.album_id=pwleitai.album_id)
                    where album.album_id NOT IN(SELECT album.album_id FROM album join pwleitai on album.album_id=pwleitai.album_id WHERE eidos="{eid}")
                    group by album.album_id
                )) as A
                ORDER BY sales DESC
    ''')
    ans=cur.fetchone()

    #εκτύπωση των ονομάτων των στηλών
    l=Label(fr,font=('Lucida Console','11'),bg='white', text=f'{"Κωδικός":<8}  {"Τίτλος Άλμπουμ":<40}  {"Πωλήσεις {}":<15}'.format(eid),fg="red2")
    l.grid(sticky=W, column=0,row=0)
    i=1
    while ans is not None:

        #αλλαγή χρώματος background
        if i%2:
            color='grey97'
        else:
            color='white'

        #εκτύπωση δεδομένων
        l=Label(fr,bg=color, text=f'NO.{ans[0]:<5}  {ans[1]:<40}  {ans[2]:<15}',font=('Lucida Console','11')).grid(sticky=W, column=0,row=i)
        i=i+1
        ans=cur.fetchone()
    cur.close()
    root.mainloop()
    return

def profit_per_album(conn): #"Έσοδα ανά άλμπουμ"

    #δημιουργία παραθύρου
    size="620x600"
    fr,root=scrollbar.scroll_window(size)
    root.title('Έσοδα ανά άλμπουμ')

    #εκτέλεση ερωτήματος sql για την εύρεση των συνολικών εσόδων απο τις πωλήσεις κάθε αλμπουμ    
    cur=conn.cursor()
    cur.execute('''
    select album.album_id, titlos, sum(posothta*item_profit) as 'synoliko kerdos'
    from album left outer join pwleitai on album.album_id=pwleitai.album_id
    group by album.album_id''')
    ans=cur.fetchone()

    #αποθήκευση απάντησης σε λίστα
    a=[]
    while ans is not None:
        a.append(list(ans))
        ans=cur.fetchone()
    cur.close()

    #εκτέλεση ερωτήματος sql για την εύρεση του συνολικού ποσού που δαπανήθηκε για την καταχώρηση στα ψηφιακά καταστήματα
    cur2=conn.cursor()
    cur2.execute('''
    select album.album_id, titlos, sum(adm_fee)
    from (album join pwleitai on album.album_id=pwleitai.album_id) join psif_dianomh on pwleitai.afm=psif_dianomh.afm
    group by album.album_id
    order by album.album_id''')
    b=cur2.fetchone()
    i=0
    while b is not None:

        #αφαίρεση του κόστους καταχώρησης από τα συνολικά έσοδα από τις πωλήσεις του άλμπουμ
        if b[2] is not None: a[i][2]=int(a[i][2])-int(b[2])
        b=cur2.fetchone()
        i=i+1
    i=1

    #εκτύπωση των ονομάτων των στηλών
    Label(fr,bg='white',font=('Lucida Console','11'),text=f'{"Κωδικός":<8}  {"Τίτλος Άλμπουμ":<40}  {"Συνολικά έσοδα":<14}',fg="red2").grid(sticky=W, column=0,row=0)
    for i in range(len(a)):

        #αλλαγή του χρώματος background
        if i%2:
            color='grey97'
        else:
            color='white'

        #εκτύπωση αποτελεσμάτων
        if(a[i][2] is None):
            a[i][2]=0
        Label(fr,bg=color,font=('Lucida Console','11'), width=70, anchor=W, text=f'{a[i][0]:<8}  {a[i][1]:<40}  {a[i][2]:<13}').grid(sticky=W, column=0,row=i+2)
    cur2.close()
    root.mainloop()
    return
