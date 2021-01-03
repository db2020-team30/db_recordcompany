from tkinter import*
from tkinter import ttk

def create(size,titlos,option=0): #δημιουργία παραθύρου χωρίς scrollbar
    if(option==0): #Αν είναι toplevel (προεπιλογή)
        root=Toplevel()
    else: #Αν δεν είναι 
        root=Tk()
    if(titlos!=''):root.title(f'{titlos}') #ορισμός τίτλου αν έχει δωθεί

    #τοποθέτηση παραθύρου στο κέντρο της οθόνης
    width=root.winfo_screenwidth()
    height=root.winfo_screenheight()
    new_size=size.split('x')
    if(width<int(new_size[0])):
        new_size[0]=width
    if(height<int(new_size[1])):
        new_size[1]=height
    size=str(new_size[0])+'x'+str(new_size[1])
    xpos=int((int(width)-int(new_size[0]))/2)
    ypos=int((int(height)-int(new_size[1]))/2)
    if(xpos>0 and ypos>0):
        size=size+'+'+str(xpos)+'+'+str(ypos)
    root.geometry(f'{size}')
    root.iconbitmap(True, 'images.ico')
    root.config(bg='white')
    return root


def scroll_window(size): #δημιουργία παραθύρου με scrollbar
    root=create(size,'') #δημιουργία απλού παραθύρου

    #δημιουργία main frame
    main_frame=Frame(root)
    main_frame.config(bg='white')
    main_frame.pack(fill=BOTH,expand=1)

    #δημιουργία καμβά
    my_canvas=Canvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

    #προσθήκη scrollbars
    my_scrollbar=ttk.Scrollbar(main_frame, orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)
    scroll_x = ttk.Scrollbar(root, orient="horizontal", command=my_canvas.xview)
    scroll_x.pack(side=BOTTOM,fill=X)

    #Επεξεργασία καμβά
    my_canvas.configure(yscrollcommand=my_scrollbar.set,xscrollcommand=scroll_x.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    my_canvas.config(bg='white')

    #δημιουργία νέου frame μέσα στον καμβά
    second_frame=Frame(my_canvas)
    second_frame.config(bg='white')

    #Προσθήκη του νέου frame σε παράθυρο,μεσα στον καμβά
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")

    return second_frame,root;
