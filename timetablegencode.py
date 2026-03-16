#finaltimetablecode
import tkinter as tk
import mysql.connector as mc
from tkinter import messagebox
from tkinter import ttk

#making db
db = mc.connect(host='localhost',user = 'root', passwd='123456')
cur=db.cursor()

cur.execute('CREATE DATABASE IF NOT EXISTS timetable')
cur.execute('SHOW DATABASES')
fetched=cur.fetchall()
#making db, fetched is for checking if required db is in list later below
cur.execute('use timetable')
#cur.execute('drop table if exists subject')
cur.execute('create table if not exists subject (subject_code int primary key, subject_name varchar(20) unique not null)')
#cur.execute('drop table if exists professor')
cur.execute('create table if not exists professor (professor_code int primary key, professor_name varchar(20) unique not null,s_code int unique not null , foreign key(s_code) references subject(subject_code) on delete restrict)')
#cur.execute('drop table if exists thours')
cur.execute('create table if not exists thours (p_code int primary key, teaching_hours varchar(20) not null, foreign key(p_code) references professor(professor_code) on delete restrict)')

db.commit()


def subject():#subject variable screen
    s=tk.Tk() #create the screen
    s.resizable(0,0)
    s.geometry('1000x550')
    s.title('View/Modify Subjects') #screen window title
    tk.Label(s,text='SUBJECTS',font=('Times New Roman',30, 'bold')).pack() #text in screen, parameters are, screen var, text,font, place is for location in screen

    tk.Label(s,text='Subject Code',font=('Times New Roman',20)).place(x=140,y=75)
    sub=tk.StringVar()
    na=tk.StringVar()
    t = tk.Entry(s,textvariable=sub,font=('Times New Roman',20))#textbox kinda thing, value stored in sub
    t.place(x=300,y=75)
    tk.Label(s,text='Subject Name',font=('Times New Roman',20)).place(x=140,y=135)
    b = tk.Entry(s,textvariable=na,font=('Times New Roman',20))
    b.place(x=300,y=135)
    
    
    tk.Label(s,text='Subjects',font=('Times New Roman',20)).place(x=740,y=60,anchor='center')

    content= tk.Listbox(s,font=('Times New Roman',15))#create the listbox which will be in scrollbar so we scroll and see content
    list= tk.Scrollbar(s)#create scrollbar
    content.place(x=620,y=75,width=250,height=250)
    list.place(x=870,y=75,height=250)

    content.config(yscrollcommand=list.set)
    list.config(command=content.yview)#connecting this listbox thing to the scrollbar
    
    # now make listbox display records from DB
    cur.execute('select * from subject')
    for i in cur.fetchall():
        content.insert('end',' '.join(str(value)for value in i))#list comprehension because smol




    from tkinter import messagebox
    def add():
        try:
            h=int(t.get())
            i=b.get()
            query=f"INSERT INTO subject (subject_code,subject_name) values({h},'{i}')" #inserts values into db for later use(generating)
            cur.execute(query)
            db.commit()#finalise insert
        except mc.errors.IntegrityError:
            messagebox.showerror('ERROR','Please do not enter duplicate Name')
        except ValueError:
            messagebox.showerror('ERROR','Please enter a value')
        else:
            content.insert('end',t.get()+' '+b.get())#inserts into listbox
        t.delete(0,tk.END)#deletes content in entry widget (clears it up, can type newly without first deleting existing content)
        b.delete(0,tk.END)
        
    def dele():
        try:#checks for index error i.e no selection made (curselection returns index of value in listbox)
            hi=int(content.get(content.curselection()[0]).split()[0])
            #content.curselection()returns tuple of indices, first element is index of selected so [0],now to get this value from listbox we use listbox.get(content.get here)
            # we know in listbox we inserted as str so to convert back to int we se int()
            query=f"delete from subject where subject_code={hi}" #delete values in db 
            cur.execute(query)
            content.delete(content.curselection()[0])#whichever selected in listbox will delete
            db.commit()
        except IndexError:#when no selection made, a message box comes up
            messagebox.showerror('ERROR','please select an item from list')#message box, syntax is window name,text in window,.showerror or whatever way popup u want
    
    u=tk.LabelFrame(s,text='Edit subjects',font=('Times New Roman',30, 'bold'),pady=10)#anotherframe like subheading
    u.place(x=250,y=200)
    a = tk.Button(u,text='Add Subject',font=('Times New Roman',20),command=add)#creating button
    a.pack(fill='both')
    tk.Button(u,text='Delete subject',font=('Times New Roman',20),command=dele).pack(fill='both')


    s.mainloop()
def professor():
    p=tk.Tk() #create the screen
    p.resizable(0,0)
    p.geometry('1000x700')
    p.title('View/Modify Teachers') #screen window title
    tk.Label(p,text='TEACHERS',font=('Times New Roman',30, 'bold')).pack(anchor='center') #text in screen, parameters are, screen var, text,font, place is for location in screen
    #TEXTBOX
    tk.Label(p,text='Teacher No.',font=('Times New Roman',20)).place(x=140,y=75)
    sub=tk.StringVar()
    na=tk.StringVar()
    code=tk.StringVar()
    t = tk.Entry(p,textvariable=sub,font=('Times New Roman',20))#textbox kinda thing, value stored in sub
    t.place(x=300,y=75)
    tk.Label(p,text='Teacher Name',font=('Times New Roman',20)).place(x=140,y=135)
    b = tk.Entry(p,textvariable=na,font=('Times New Roman',20))
    b.place(x=300,y=135)
    tk.Label(p,text='Subject Code',font=('Times New Roman',20)).place(x=140,y=195)
    c=tk.Entry(p,textvariable=code,font=('Times New Roman',20))
    c.place(x=300,y=195)
    
    def clear_entry(ev):
        if t.get()=='Eg. 101,102,...':
            t.delete(0,tk.END)
    t.insert(tk.END,'Eg. 101,102,...')
    t.config(foreground='grey')
    t.bind('<KeyPress>', clear_entry) 
    def starttype(ev):
        t.config(foreground='black')
    t.bind('<KeyRelease>',starttype)




    #SCROLLBAR,LISTBOX
    tk.Label(p,text='Subjects',font=('Times New Roman',20)).place(x=370,y=300,anchor='center')
    tk.Label(p,text='Teachers',font=('Times New Roman',20)).place(x=640,y=300,anchor='center')
    content= tk.Listbox(p,font=('Times New Roman',15))#create the listbox which will be in scrollbar so we scroll and see content
    list= tk.Scrollbar(p)#create scrollbar
    c2=tk.Listbox(p,font=('Times New Roman',15))#anonther listbox to show subject codes
    c2.config(yscrollcommand=list.set)
    c2.place(x=240,y=325,width=250,height=250)
    content.config(yscrollcommand=list.set)
    content.place(x=520,y=325,width=250,height=250)
    list.place(x=495,y=325,height=250)
    list.config(command=content)#connecting this listbox thing to the scrollbar

    cur.execute('select * from professor')
    for i in cur.fetchall():
        content.insert('end',' '.join(str(value)for value in i))#list comprehension because smol
    cur.execute('select * from subject')
    for i in cur.fetchall():
        c2.insert('end',' '.join(str(value)for value in i))


    #FUNCTIONS FOR BUTTON
    from tkinter import messagebox
    def add():
        try:
            h=int(t.get())
            i=b.get()
            j=int(c.get())
            query=f"INSERT INTO professor (professor_code,professor_name,s_code) values({h},'{i}',{j})" #inserts values into db for later use(generating)
            cur.execute(query)
            db.commit()
        except mc.errors.IntegrityError:
            messagebox.showerror('ERROR','Please do not enter duplicate Name/Select Subject Code from given list.')
        except ValueError:
            messagebox.showerror('ERROR','Please enter a value')
        else:
            content.insert('end',t.get()+' '+b.get()+' '+c.get())#inserts into listbox
        t.delete(0,tk.END)
        b.delete(0,tk.END)
        c.delete(0,tk.END)
        #deletes content in entry widget (clears it up, can type newly without first deleting existing content)
    def dele():
        try:#checks for index error i.e no selection made
            hi=content.get(content.curselection()[0]).split()[0]
            print(hi)
            query=f"delete from professor where professor_code={hi}" #delete values in db 
            cur.execute(query)
            content.delete(content.curselection()[0])#whichever selected in listbox will delete
            db.commit()
        except IndexError:#when no selection made, a message box comes up
            messagebox.showerror('ERROR','please select an item from list')#message box, syntax is window name,text in window,.showerror or whatever way popup u want
    #BUTTONS
    u=tk.LabelFrame(p,text='Edit Teachers',font=('Times New Roman',30, 'bold'),pady=10)#anotherframe like subheading
    u.place(x=600,y=145,anchor='w')
    a = tk.Button(u,text='Add Teacher',font=('Times New Roman',20),command=add)#creating button
    a.pack(fill='both')
    tk.Button(u,text='Delete Teacher',font=('Times New Roman',20),command=dele).pack(fill='both')
    #SCREEN 
    p.mainloop()
def thours():
    t=tk.Tk() #create the screen
    t.resizable(0,0)
    t.geometry('1000x550')
    t.title('View/Modify Teaching Hours') #screen window title
    tk.Label(t,text='TEACHING HOURS',font=('Times New Roman',30, 'bold')).pack() #text in screen, parameters are, screen var, text,font, place is for location in screen
    #TEXTBOX
    tk.Label(t,text='Teacher No.',font=('Times New Roman',20)).place(x=150,y=75)
    sub=tk.StringVar()
    thrs=tk.StringVar()
    h = tk.Entry(t,textvariable=sub,font=('Times New Roman',20),foreground='grey')#textbox kinda thing, value stored in sub
    h.place(x=300,y=75)
    tk.Label(t,text='Teacher timing',font=('Times New Roman',20)).place(x=135,y=135)
    b = tk.Entry(t,textvariable=thrs,font=('Times New Roman',20),foreground='grey')
    b.place(x=300,y=135)
    
    
    def clear_entry(ev):#argument here because otherwise some positional argument error comes up
        if b.get()=='Eg. 13:00-14:00 (24h clock)':
            b.delete(0,tk.END)
    b.insert(tk.END,'Eg. 13:00-14:00 (24h clock)')#this is used as default text in entry widget 
    b.bind('<KeyPress>', clear_entry)   #this will delete the default text as soon as we start typing
        
    def clear_entry(ev):
        if h.get()=='Eg. 101,102,...':
            h.delete(0,tk.END)
    h.insert(tk.END,'Eg. 101,102,...')
    h.bind('<KeyPress>', clear_entry) 

    def starttype(ev):
        b.config(foreground='black')
    b.bind('<KeyRelease>',starttype)# this will change colour of default text as soon as we start typing
    def starttype(ev):
        h.config(foreground='black')
    h.bind('<KeyRelease>',starttype)

    #SCROLLBAR
    tk.Label(t,text='Teaching Hours',font=('Times New Roman',20)).place(x=730,y=60,anchor='center')
    content= tk.Listbox(t,font=('Times New Roman',15))#create the listbox which will be in scrollbar so we scroll and see content
    list= tk.Scrollbar(t)#create scrollbar
    content.config(yscrollcommand=list.set)
    content.place(x=620,y=75,width=250,height=250)
    list.place(x=870,y=75,height=250)
    list.config(command=content)#connecting this listbox thing to the scrollbar
    #FUNCTIONS FOR BUTTON
    cur.execute('select * from thours')
    for i in cur.fetchall():
        content.insert('end',' '.join(str(value)for value in i))#list comprehension because smol    


    from tkinter import messagebox
    def add():
        try:
            
            j=int(h.get())
            i=b.get()
            query=f"INSERT INTO thours (p_code,teaching_hours) values({j},'{i}')" #inserts values into db for later use(generating)
            cur.execute(query)
            db.commit()
        except mc.errors.IntegrityError:
            messagebox.showerror('ERROR','Please do not enter duplicate Teacher No./Enter Valid Teacher No.')
        except ValueError:
            messagebox.showerror('ERROR','Please enter a value')
        else:
            content.insert('end',h.get()+' '+b.get())#inserts into listbox
        h.delete(0,tk.END)
        b.delete(0,tk.END)
    def dele():
        try:#checks for index error i.e no selection made
            hi=int(content.get(content.curselection()[0]).split()[0])
            query=f"delete from thours where p_code={hi}" #delete values in db 
            cur.execute(query)
            content.delete(content.curselection()[0])#whichever selected in listbox will delete
            db.commit()
        except IndexError:#when no selection made, a message box comes up
            messagebox.showerror('ERROR','please select an item from list')
    #BUTTONS
    u=tk.LabelFrame(t,text='Edit teaching hours',font=('Times New Roman',30, 'bold'),pady=10)#anotherframe like subheading
    u.place(x=200,y=200)
    a = tk.Button(u,text='Add Time',font=('Times New Roman',20),command=add)#creating button
    a.pack(fill='both')
    tk.Button(u,text='Delete Time',font=('Times New Roman',20),command=dele).pack(fill='both')
    #SCREEN 
    t.mainloop()

#CONNECTION TO DB PENDING, EITHER MYSQL.CONNECTOR OR SQLLITE3

def generate():
    g=tk.Tk()
    g.geometry('500x500')
    g.title('View/Modify Timetable') #screen window title
    tk.Label(g,text='TIMETABLE',font=('Times New Roman',60, 'bold')).pack(fill='x')
    #database connection to start displaying
    
    headers=['Subject Name','Professor Name','Teaching Hours']
    style = ttk.Style(g)
    style.theme_use('clam')
    style.configure('Treeview.Heading',foreground='black',background='#FFC5C5',font=('Times New Roman',15))

    treeview=ttk.Treeview(g,columns=headers,show='headings')
    
    for i,header in enumerate(headers): 
        treeview.heading(i,text=header)
        treeview.column(i,width=160,anchor='center')

    treeview.bind('<Motion>', 'break')
    treeview.pack(expand=True,fill='y')
    
    cur.execute('select subject_name,professor_name,teaching_hours from subject,professor,thours where subject.subject_code=professor.s_code and thours.p_code=professor.professor_code;')
    data=cur.fetchall()

    timeslots=["8:00-9:00","9:00-10:00","10:00-11:00","11:00-12:00","13:00-14:00","14:00-15:00","15:00-16:00"]
    teachers = {}
    for i in range(len(data)):
        teachers.setdefault((data[i][1],data[i][0]),data[i][2])
    #print(teachers)
# Create an empty timetable
    timetable = {}
    import random
    import datetime as dt
# Randomly assign teachers to timeslots while adhering to their available timeslots
    for t in timeslots:
        b=[tuple(t.split('-')[0].split(':')),tuple(t.split('-')[1].split(':'))]
        #print(b)
        a,c=dt.time(int(b[0][0]),int(b[0][1])),dt.time(int(b[1][0]),int(b[1][1]))
        #print(a,c)
        av_tea = []

        for tea, av_t in teachers.items():
            #print(tea,av_t)
            d=[tuple(av_t.split('-')[0].split(':')),tuple(av_t.split('-')[1].split(':'))]

            e,f=dt.time(int(d[0][0]),int(d[0][1])),dt.time(int(d[1][0]),int(d[1][1]))
            if (e<=a and a<=f) and (e<=c and c<=f) :
                
                av_tea.append(tea)
        if av_tea:
            teacher = random.choice(av_tea)
            timetable[t] = teacher
    #print(timetable)

# Print the timetable
    final = []
    for i in timetable: #for i in dict means i is key when traversing thats why we do dict[i]=value
        final.append((timetable[i][1],timetable[i][0],i))
    
    for i in range(len(final)):#i=0 data[0] [(),(),()]
        treeview.insert('','end',values=final[i],tag=i)
        if i % 2:
            treeview.tag_configure(i,foreground='black', background='#C7DCA7',font=('Times New Roman',15))
        else:
            treeview.tag_configure(i,foreground='black', background='#FFEBD8',font=('Times New Roman',15))
    treeview.insert('',4,values=('Break','N/A','12:00-13:00'),tag=a)
    treeview.tag_configure(a,foreground='black', background='#89B9AD',font=('Times New Roman',15))

    
    def delete():
        try:#checks for index error i.e no selection made
            treeview.delete(treeview.selection()[0])
        except IndexError:#when no selection made, a message box comes up
            messagebox.showerror('ERROR','please select an item from list')
    
    import csv
    import os
    def export():
        data2=[]
        for i in treeview.get_children():
            data2.append(treeview.item(i)['values'])
        file=open('timetable.csv','w',newline='')
        wo=csv.writer(file)
        wo.writerow(headers)
        wo.writerows(data2)
        file.close()
        import tkinter.filedialog as fd
        
        
        filename = fd.askopenfilename(title="Select File", filetypes=[("CSV files", "*.csv")])
        if filename:
            # Process the selected file
            try:
                os.startfile(filename)
                print("Selected file:", filename)
            except Exception as e:
                messagebox.showerror('ERROR',e)
            




    u=tk.LabelFrame(g,text='Edit Timetable',font=('Times New Roman',40, 'bold'),pady=10)#anotherframe like subheading
    u.pack(fill='y')
    tk.Button(u,text='Remove Class',font=('Times New Roman',20, 'bold'),command=delete).pack(fill='both')
    tk.Button(u,text='Export as file',font=('Times New Roman',20, 'bold'),command=export).pack(fill='both')
    
    g.mainloop()


main=tk.Tk() #create the screen
main.resizable(0,0)
main.geometry('1000x700')
main.title('timetable generator') #screen window title
tk.Label(text='TIMETABLE',font=('Times New Roman',60, 'bold')).pack() #text in screen
#pack() or grid() or place()

a=tk.LabelFrame(main,text='Edit Timetable',font=('Times New Roman',40, 'bold'),pady=10)#making a subpart
a.pack(fill='y',anchor='center')
tk.Button(a,text='Subject',font=('Times New Roman',20, 'bold'),command= subject).pack(fill='both')#making buttons
tk.Button(a,text='Teacher',font=('Times New Roman',20, 'bold'),command= professor).pack(fill='both')
tk.Button(a,text='Teaching Hours',font=('Times New Roman',20, 'bold'),command=thours).pack(fill='both')
b=tk.LabelFrame(main,text='Generate Timetable',font=('Times New Roman',40, 'bold'),pady=10)#another subpart
b.pack(fill='y',anchor='center')
tk.Button(b,text='Generate',font=('Times New Roman',20, 'bold'),command=generate).pack(fill='both')

main.mainloop()