import pymysql
import itertools
from datetime import datetime
from tkinter import*
from tkinter import ttk
import basic_functions
import scrollbar


def choose_song(conn,ch): #επιλογή τραγουδίου
    cur=conn.cursor()
    cur.execute('''SELECT tragoudi.titlos
                    FROM `tragoudi` JOIN anhkei ON tragoudi.song_id=anhkei.song_id
                    WHERE anhkei.album_id in (SELECT album.album_id FROM album WHERE album.titlos='{}')'''.format(ch))
    ep_tuple=cur.fetchall()
    ep=[]
    for i in range(len(ep_tuple)):
        ep.append(ep_tuple[i][0])
    cur.close()
    window=scrollbar.create('350x250',"Επιλογή Τραγουδιού")
    if(ep!=[]): #αν υπαρχουν τραγούδια στο άλμπουμ
        Label(window,bg='white', text='Επιλέξτε Τραγούδι', fg="blue", font=('arial','11')).pack()
        combo=ttk.Combobox(window,values=ep,font=('arial','11'),width=25)
        combo.pack()
        combo.current(0)
        Button(window,bg='white',text="Επιλογή",font=('arial','12'),command=lambda: instruments(conn,combo.get(),window)).pack()
    else: #αν δεν υπάρχουν
        Label(window,bg='white', text='Δεν υπάρχουν τιμές!', fg="red", font=('arial','14')).pack()
    window.mainloop()
    return
        

def songInfo_perAlbum(conn,choice): #"Στοιχεία τραγουδιών ανά άλμπουμ"
    if(choice=='**Όλα τα Άλμπουμ**'):choice=''

    #Δημιουργία παραθύρου
    size="1300x600"
    fr,root=scrollbar.scroll_window(size)
    root.title('Στοιχεία τραγουδιών ανά άλμπουμ')
    root.config(bg='white')
    cur=conn.cursor()
    if choice!='': 
        try: #Εκτέλεση sql για συγκεκριμένο άλμπουμ που είναι αποθηκευμένο στο "choice"
            cur.execute('''
            SELECT album.titlos, anhkei.track_no, tragoudi.titlos, diarkeia, s_language
            FROM tragoudi, anhkei, album
            WHERE anhkei.song_id=tragoudi.song_id AND anhkei.album_id=album.album_id AND album.titlos=%s
            ORDER BY album.titlos, anhkei.track_no, tragoudi.titlos''', choice)
        except pymysql.Error:
             cur.close()
             return
    else: #Εκτέλεση sql για όλα τα άλμπουμ
        cur.execute('''
        SELECT album.titlos, anhkei.track_no, tragoudi.titlos, diarkeia, s_language
        FROM tragoudi, anhkei, album
        WHERE anhkei.song_id=tragoudi.song_id AND anhkei.album_id=album.album_id
        ORDER BY album.titlos, anhkei.track_no, tragoudi.titlos''')
    ans=cur.fetchone()
    album=''
    row_num=0
    color_num=0
    while ans is not None:
        if ans[0]!=album: #Αν δεν έχει ξαναεμφανιστεί το συγκεκριμένο άλμπουμ
            Label(fr,font=('Lucida Console','12'), bg='grey80', width=140, anchor=W, text=ans[0]).grid(sticky=W, column=0,row=row_num)
            row_num=row_num+1
            r='No.'
            r0='Τίτλος Τραγουδιού'
            r1='Ερμηνεία'
            r2='Μουσική'
            r3='Στίχοι'
            r4='Διάρκεια'
            r5='Γλώσσα'
            Label(fr,font=('Lucida Console','10'), bg='white',width=180, anchor=W, text=(f'{r:3} {r0:40} {r1:50} {r2:20} {r3:20} {r4:8} {r5:6}'),fg="magenta").grid(sticky=W, column=0,row=row_num)
            album=ans[0]
            row_num=row_num+1
        
        #Εύρεση του καλλιτεχνικού ονόματος του ερμηνευτή
        cur1=conn.cursor()
        art_num=cur1.execute('''
        SELECT stage_name
        FROM (tragoudi join ermhneyei on tragoudi.song_id=ermhneyei.song_id), persona_group
        WHERE ermhneyei.artist_id=persona_group.artist_id AND tragoudi.titlos=%s''', ans[2])
        a=cur1.fetchone()
        artists=[]
        if(a is None):artists.append(' ')
        while a is not None:
            artists.append(a[0])
            a=cur1.fetchone()

        #Εύρεση των συνθετών ενός τραγουδιού    
        cur2=conn.cursor()
        syn_num=cur2.execute('''
        SELECT lastname
        FROM (tragoudi join synthetei on tragoudi.song_id=synthetei.song_id), symbeblhmenos
        WHERE synthetei.afm=symbeblhmenos.afm AND tragoudi.titlos=%s''', ans[2])
        s=cur2.fetchone()
        synth=[]
        if(s is None):synth.append(' ')
        while s is not None:
            synth.append(s[0])
            s=cur2.fetchone()

        #Εύρεση των στιχουργών ενός τραγουδιού 
        cur3=conn.cursor()
        stix_num=cur3.execute('''
        SELECT lastname
        FROM (tragoudi join grafei on tragoudi.song_id=grafei.song_id), symbeblhmenos
        WHERE grafei.afm=symbeblhmenos.afm AND tragoudi.titlos=%s''', ans[2])
        st=cur3.fetchone()
        stix=[]
        if(st is None):stix.append(' ')
        while st is not None:
            stix.append(st[0])
            st=cur3.fetchone()
   
        diarkeia = str(ans[3])
        
        #Αλλαγή χρώματος background
        if color_num%2:
            color='white'
        else:
            color='grey97'
        
        #Εκτύπωση δεδομένων
        Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{ans[1]:<3} {ans[2]:40} {artists[0]:50} {synth[0]:20} {stix[0]:20} {diarkeia:8}  {ans[4]:^6}').grid(sticky=W, column=0,row=row_num)
        row_num=row_num+1
        i=1
        blank=''
        num=[art_num, syn_num, stix_num]
        num.sort()
        while i<num[2]:
            if i<num[0]:
                Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:45} {artists[i]:50} {synth[i]:20} {stix[i]:20}').grid(sticky=W, column=0,row=row_num)
            elif i<num[1]:
                if art_num==num[0]:
                    Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:95} {synth[i]:20} {stix[i]:20}').grid(sticky=W, column=0,row=row_num)
                elif syn_num==num[0]:
                    Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:45} {artists[i]:50} {blank:20} {stix[i]:20}').grid(sticky=W, column=0,row=row_num)
                elif stix_num==num[0]:
                    Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:45} {artists[i]:50} {synth[i]:20}').grid(sticky=W, column=0,row=row_num)
            else:
                if art_num==num[2]:
                    Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:45} {artists[i]:50}').grid(sticky=W, column=0,row=row_num)
                elif syn_num==num[2]:
                    Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:95} {synth[i]:20}').grid(sticky=W, column=0,row=row_num)
                elif stix_num==num[2]:
                    Label(fr,font=('Lucida Console','10'),bg=color, width=180, anchor=W, text=f'{blank:116} {stix[i]:20}').grid(sticky=W, column=0,row=row_num)
            row_num=row_num+1
            i=i+1
        color_num=color_num+1
        ans=cur.fetchone()
    return

def instruments(conn,song,window): #"Οργανοπαίκτες που συμμετείχαν σε ένα τραγούδι"
    window.destroy() #Καταστροφή προηγούμενου παραθύρου
    cur=conn.cursor()

    #Εκτέλεση sql και διαχείριση λαθών
    try:
        cur.execute('''SELECT organopaikths.afm,organopaikths.fullname,organopaikths.specialty
                        FROM organopaikths 
                        WHERE organopaikths.afm in (SELECT symmetexei.afm
						                            FROM symmetexei JOIN tragoudi ON symmetexei.song_id=tragoudi.song_id
						                            WHERE tragoudi.titlos=%s)
	                ''',song)
    except pymysql.Error:
        print("hi")
        cur.close()
        return
    
    #Δημιουργία παραθύρου
    size="750x500"
    fr,root=scrollbar.scroll_window(size)
    root.title('Οργανοπαίκτες που συμμετείχαν σε ένα τραγούδι')
    root.config(bg='white')
    Label(fr,font=('Lucida Console','11'),bg='grey80', width=80, text=('{}'.format(song))).grid(column=0,row=0)
    Label(fr,font=('Lucida Console','11'),bg='white', text=(f'{"ΑΦΜ":<9} {"ΟΝΟΜΑ":<50} {"ΜΟΥΣΙΚΗ ΙΔΙΟΤΗΤΑ":<10}'),fg="red2").grid(sticky=W,column=0,row=1)
    ans=cur.fetchone()
    i=2
    while(ans is not None):

        #Αλλαγή χρώματος background
        if i%2:
            color='grey97'
        else:
            color='white'

        #Εκτύπωση δεδομένων
        Label(fr,font=('Lucida Console','11'),bg=color, width=80, anchor=W, text=(f'{ans[0]:<9} {ans[1]:<50} {ans[2]:<10}')).grid(sticky=W,column=0,row=i)
        ans=cur.fetchone()
        i=i+1
    
    #κουμπί για παραπομπή στην "show_entry" για την προβολή των στοιχίων επικοινωνίας
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας οργανοπαίκτη",font=('helvetica','11'), command= lambda: basic_functions.select_pleiad(5,conn,'epik_organop'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close()
    root.mainloop()
    return None

def album_per_genre(conn): #"Άλμπουμ ανά μουσικό είδος"
    fr,root=scrollbar.scroll_window("1335x600") #Δημιουργία παραθύρου
    root.title('Άλμπουμ ανά μουσικό είδος')
    root.config(bg='white')
    cur=conn.cursor()
    #Εκτέλεση sql
    cur.execute('''SELECT A.genre,B.album_id, B.titlos, vinyl_stock, CD_stock, release_date, graf_afm,royalties_prof,total
                    FROM
                    (SELECT * FROM ypagetai) AS A
                    JOIN
                    (SELECT album.album_id, album.titlos, vinyl_stock, CD_stock, release_date, graf_afm,royalties_prof,COUNT(anhkei.song_id) AS total
                    FROM (album join anhkei on album.album_id=anhkei.album_id)
                    GROUP BY anhkei.album_id) AS B
                    ON A.album_id=B.album_id
                    ORDER BY genre, album_id''')
    ans=cur.fetchone()
    i=0
    eidos=''

    #Εκτύπωση των ονομάτων των στηλών 
    Label(fr,bg='white',font=('Lucida Console','11'), width=146, anchor=W, text=f'{"Κωδ. Άλμπ.":<11} {"Τίτλος":<50} {"Απόθεμα Βινυλ.":<14} {"Απόθεμα CD":<11} {"Ημερ.Κυκλοφ.":<12} {"ΑΦΜ γραφίστα":<12} {"Κέρδη πνευμ.δικ.":<16} {"Αρ.τραγουδιών":<13}',fg="red2").grid(column=0,row=i,sticky=W)
    while(ans is not None):
        i=i+1

        #εάν το είδος δεν έχει εμφανιστεί ξανά
        if(str(ans[0])!=eidos):
            eidos=str(ans[0])
            cur2=conn.cursor()

            #Εύρεση μέσων πωλήσεων ανά άλμπουμ
            cur2.execute(f'''SELECT round(AVG(Α.total_sales)) FROM
                            (SELECT (SUM(posothta)) as total_sales
                            FROM (ypagetai join pwleitai on ypagetai.album_id=pwleitai.album_id)
                            where genre="{eidos}"
                            GROUP BY pwleitai.album_id) AS Α''')
            Label(fr,bg='grey85',font=('Lucida Console','11'),text='{}, Μέσες πωλήσεις:{}'.format(eidos,str(cur2.fetchone()[0])),width=146,anchor=W).grid(column=0,row=i,sticky=W)
            i=i+1
            cur2.close()

        #Αλλαγή χρώματος background
        if i%2:
            color='white'
        else:
            color='grey97'

        #Διαχείριση δεδομένων date
        if(ans[5]is None or ans[5]=='0000-00-00'):
            date='-'
        else:
            date=ans[5].strftime("%Y-%m-%d")

        #εκτύπωση δεδομένων
        Label(fr,bg=color,font=('Lucida Console','11'),text=f'{str(ans[1]):<11} {str(ans[2]):<50} {str(ans[3]):<14} {str(ans[4]):<11} {date:<12} {str(ans[6]):<12} {str(ans[7]):<16} {str(ans[8]):<13}',width=146, anchor=W).grid(column=0,row=i,sticky=W)
        ans=cur.fetchone()
    cur.close()
    root.mainloop()
    return

def album_per_studio(conn): #"Άλμπουμ ανά studio ηχογράφησης"

    #δημιουργία παραθύρου
    fr,root=scrollbar.scroll_window("1610x600")
    root.title('Άλμπουμ ανά studio ηχογράφησης')
    root.config(bg='white')
    #εκτέλεση sql
    cur=conn.cursor()
    cur.execute('''SELECT onoma,album_id, titlos, vinyl_stock, CD_stock, release_date, graf_afm,royalties_prof,rec_start,rec_end,hours,hourly_rate
                   FROM album join studio on studio_afm=studio.afm
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
            Label(fr,bg='grey85',font=('Lucida Console','10'),text='{}, Χρέωση:{}/ώρα'.format(studio,str(ans[11])),width=183,anchor=W).grid(column=0,row=i,sticky=W)
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
        Label(fr,bg=color,font=('Lucida Console','10'),text=f'{str(ans[1]):<11} {str(ans[2]):<50} {str(ans[3]):<14} {str(ans[4]):<11} {date[0]:<12} {str(ans[6]):<12} {str(ans[7]):<16} {date[1]:<22} {date[2]:<10} {str(ans[10]):<16}',width=183, anchor=W).grid(column=0,row=i,sticky=W)
        ans=cur.fetchone()
    i=i+1

    #κουμπι για μετάβαση στο "show_entry" για την εύρεση των στοιχείων επικοινωνίας
    b1=Button(fr,bg='white', width=40, activebackground='light cyan', highlightcolor='light cyan', text="Στοιχεία επικοινωνίας studio",font=('times new roman','13'),command= lambda: basic_functions.select_pleiad(5,conn,'epik_studio'))
    b1.grid(column=0,row=i,sticky=S)
    cur.close()
    root.mainloop()
    return