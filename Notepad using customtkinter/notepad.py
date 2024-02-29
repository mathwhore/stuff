from tkinter import Frame
import customtkinter as ct
import pyodbc
from PIL import Image

cnxn=pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                     r'DBQ=C:\Users\Haider\Downloads\notes.accdb;')

def delNote(data,i):
  crsr=cnxn.cursor()
  crsr.execute(f"Delete from Notes where username='{usrnm.get()}' and noteTitle='{data}'")
  crsr.commit()        
  ct.CTkLabel(notesFrame,text="Note deleted",width=380,height=60,font=('Times',20)).grid(row=i+1,columnspan=3,padx=10,pady=10)

def savenewNotes(data,title):
  crsr=cnxn.cursor()
  crsr.execute(f"Insert into Notes([note],noteTitle,username) Values('{data}','{title}','{usrnm.get()}')")
  crsr.commit()
  ct.CTkLabel(notesAdd,text='Note saved.',font=('Times',20,'bold'),width=30).grid(column=1,row=5,padx=10,pady=5)
  
def saveexistingNotes(data,title):
  crsr=cnxn.cursor()
  crsr.execute(f"Update Notes set [note]='{data}' where noteTitle='{title}' and username='{usrnm.get()}'")
  crsr.commit()
  ct.CTkLabel(notesdisp,text='Note saved.',font=('Times',20,'bold'),width=30,anchor='center').grid(column=1,row=5,padx=10,pady=10)
  

def addNote():
    global notesAdd
    notesAdd=Frame(notes,bg="#363636")
    notesAdd.place(x=0,y=0,width=790,height=530)
    ct.CTkButton(notesAdd,text='',image=img,fg_color="#363636",hover=False,font=('Times',20),width=40,command=notesAdd.destroy).place(x=0,y=7)
    ct.CTkLabel(notesAdd,text='Enter note title.',font=('Arial',20,'bold')).grid(columnspan=2,row=0,padx=10,pady=5)
    title=ct.CTkTextbox(notesAdd,height=50,width=600,font=('Arial',20),undo=True)
    title.grid(columnspan=4,row=1,padx=10,pady=5)
    ct.CTkLabel(notesAdd,text='Enter note.',font=('Arial',20,'bold')).grid(columnspan=2,row=2,padx=10,pady=5)
    disp=ct.CTkTextbox(notesAdd,height=250,width=700,font=('Arial',20),undo=True)
    disp.grid(columnspan=7,row=3,padx=10,pady=5)
    ct.CTkButton(notesAdd,text='Save',width=180,font=('Times',20),command=lambda:savenewNotes(disp.get(1.0,"end"),title.get(1.0,"end"))).grid(row=4,column=1,padx=10,pady=10)
    
    

def dispNote(title):
    global notesdisp
    notesdisp=Frame(notes,bg="#363636")
    notesdisp.place(x=0,y=0,width=790,height=530)
    crsr=cnxn.cursor()
    crsr.execute(f"Select * from Notes where noteTitle='{title}'")
    note=crsr.fetchone()
    ct.CTkButton(notesdisp,text='',image=img,fg_color="#363636",hover=False,font=('Times',20),width=40,command=notesdisp.destroy).place(x=0,y=7)
    ct.CTkLabel(notesdisp,text=title,font=('Arial',20,'bold','underline'),width=30).grid(column=1,row=0,padx=10,pady=10)
    disp=ct.CTkTextbox(notesdisp,insertwidth=1,height=200,width=600,font=('Arial',20),undo=True)
    disp.grid(columnspan=7,row=1,padx=10,pady=10)
    disp.insert(1.0,note[1])
    ct.CTkButton(notesdisp,text='Save',width=180,font=('Times',20),command=lambda:saveexistingNotes(disp.get(1.0,"end"),title)).grid(row=4,column=1,padx=10,pady=10)

def noteWin():
    global notesFrame
    notesFrame=ct.CTkScrollableFrame(notes,width=730,height=400,orientation='vertical',scrollbar_button_color="#082621",scrollbar_button_hover_color="#14695a")
    notesFrame.place(x=0,y=0)
    dlt=Image.open("dlt.png","r")
    img2=ct.CTkImage(dlt,None,(30,30))
    ct.CTkButton(notesFrame,text='Add new note',font=('Times',20),command=addNote).grid(row=0,columnspan=2,padx=10,pady=10)
    crsr=cnxn.cursor()
    crsr.execute(f"Select noteTitle from Notes where username='{usrnm.get()}'")
    note=crsr.fetchall()
    if note==None or len(note)==0:
      ct.CTkLabel(notesFrame,text='No notes found',font=('Times',20)).grid(row=3,column=1,columnspan=2,padx=10,pady=10)
    else:
      for i in range(len(note)):
         ct.CTkLabel(notesFrame,text=f'{i+1}.',font=('Times',20)).grid(row=i+1,column=0,padx=10,pady=10)
         ct.CTkButton(notesFrame,text=note[i][0],width=180,font=('Times',20),command=lambda pi=i:dispNote(note[pi][0])).grid(row=i+1,column=1,padx=10,pady=10)
         ct.CTkButton(notesFrame,text='',image=img2,font=('Times',20),fg_color="#363636",hover=False,command=lambda pi=i:delNote(note[pi][0],pi)).grid(row=i+1,column=2,padx=10,pady=10)

 

def loginCheck():
    crsr=cnxn.cursor()
    crsr.execute(f"Select * from Users where username='{usrnm.get()}'")
    failure=crsr.fetchone()
    if len(usrnm.get())==0 or len(psswrd.get())==0:
      ct.CTkLabel(loginFrame,text='Entries left empty!',font=('Times',20),width=40).grid(columnspan=2,row=8,pady=10)
    else:
      if len(failure)==0 or failure==None:
        ct.CTkLabel(loginFrame,text='Incorrect username',font=('Times',20),width=30).grid(columnspan=2,row=8,pady=10)
      else:
        if psswrd.get()==failure[2]:
         ct.CTkLabel(loginFrame,text='Login Successful!',font=('Times',20),width=50).grid(columnspan=2,row=8,pady=10)
         for widget in notes.winfo_children():
           widget.destroy()
         noteWin()
        else:
         ct.CTkLabel(loginFrame,text='Incorrect password',font=('Times',20),width=30).grid(columnspan=2,row=8,pady=10)

def signupCheck():
    crsr=cnxn.cursor()
    crsr.execute(f"Select * from Users where username='{username.get()}'")
    failure=crsr.fetchall()
    if len(username.get())==0 or len(password.get())==0 or len(cnfrm_password.get())==0:
      ct.CTkLabel(signupFrame,text='Entries left empty!',font=('Times',20),width=30).grid(columnspan=2,row=8,pady=10)
    else:
     if len(failure)==0:
      if password.get()==cnfrm_password.get():
        ct.CTkLabel(signupFrame,text='SIGNUP SUCCESSFULL!',font=('Times',20),width=30).grid(columnspan=2,row=8,pady=10)
        crsr.execute(f"Insert into Users(username,password) Values('{username.get()}','{password.get()}')")
        crsr.commit()
        crsr.close()
        ct.CTkButton(signupFrame,text='Login again',font=('Times',20),command=signupFrame.destroy).grid(row=9,columnspan=2,padx=10,pady=10)
      else:
        ct.CTkLabel(signupFrame,text='Password does not match',font=('Times',20),width=30).grid(columnspan=2,row=8,pady=10)
     else:
        ct.CTkLabel(signupFrame,text='Username taken!',font=('Times',20),width=30).grid(columnspan=2,row=8,pady=10)
       

def signup():
    global signupFrame
    signupFrame=Frame(auth_frm,bg="#363636")
    signupFrame.place(x=0,y=0,width=380,height=530)
    ct.CTkLabel(signupFrame,text='Signup',font=('Times',30)).grid(columnspan=2,row=3,padx=10,pady=10)
    ct.CTkLabel(signupFrame,text='Enter username',font=('Times',20),anchor='center').grid(row=4,padx=10,pady=10)
    ct.CTkLabel(signupFrame,text='Enter password',font=('Times',20),anchor='center').grid(row=5,padx=10,pady=10)
    ct.CTkLabel(signupFrame,text='Confirm password',font=('Times',20),anchor='center').grid(row=6,padx=10,pady=10)
    global username
    username=ct.CTkEntry(signupFrame,font=('Arial',20),width=180)
    username.grid(row=4,column=1,padx=10,pady=10)
    global password
    password=ct.CTkEntry(signupFrame,show="*",font=('Arial',20),placeholder_text='6 characters min.',width=180)
    password.grid(row=5,column=1,padx=10,pady=10)
    global cnfrm_password
    cnfrm_password=ct.CTkEntry(signupFrame,show="*",font=('Arial',20),width=180)
    cnfrm_password.grid(row=6,column=1,padx=10,pady=10)
    ct.CTkButton(signupFrame,text='Signup',font=('Times',30),width=200,command=signupCheck).grid(row=7,columnspan=2,padx=10,pady=10)
    ct.CTkButton(signupFrame,text='',image=img,fg_color="#363636",hover=False,font=('Times',20),width=40,command=signupFrame.destroy).place(x=0,y=7)
    

root=ct.CTk()
root.title('Notepad')
root.geometry('1200x600')
root.iconbitmap('ntpd.ico')
ct.set_appearance_mode("system")
ct.set_default_color_theme(r"C:\Users\Haider\Downloads\CTkTheme_test.json")
btn=Image.open('btn.png','r')
img=ct.CTkImage(btn)
ntbk=Image.open('notebook.png','r')
nt_img=ct.CTkImage(ntbk,None,(80,80))
auth_frm=ct.CTkFrame(root,width=380,height=530)
auth_frm.place(x=10,y=60)
notes=ct.CTkFrame(root,width=790,height=530)
notes.place(x=400,y=60)
loginFrame=ct.CTkFrame(auth_frm,width=380,height=530)
loginFrame.place(x=0,y=0)
Label(root,text='Notepad',background="#262626",font=('Verdana',30),width=30).pack(side='top')
ct.CTkLabel(loginFrame,text='Login',font=('Times',30)).grid(columnspan=2,row=3,padx=10,pady=10)
ct.CTkLabel(loginFrame,text='Enter username',font=('Times',20),anchor='center').grid(row=4,padx=10,pady=10)
ct.CTkLabel(loginFrame,text='Password',font=('Times',20),anchor='center').grid(row=5,padx=10,pady=10)
usrnm=ct.CTkEntry(loginFrame,font=('Arial',20),placeholder_text='eg: Admin',width=180)
usrnm.grid(row=4,column=1,padx=10,pady=10)
psswrd=ct.CTkEntry(loginFrame,show="*",font=('Arial',20),placeholder_text='xxxxxx',width=180)
psswrd.grid(row=5,column=1,padx=10,pady=10)
ct.CTkButton(loginFrame,text='Login',font=('Times',20),width=200,command=loginCheck).grid(row=6,columnspan=2,padx=10,pady=10)
ct.CTkButton(loginFrame,text='''Don't have an account? Sign up.''',font=('Times',20,'underline'),width=180,command=signup).grid(row=7,columnspan=2,padx=10,pady=10)
ct.CTkLabel(notes,text='Your notes will show up here.',font=('Times',25)).place(x=250,y=260)
ct.CTkLabel(notes,text='',image=nt_img).place(x=325,y=150)
root.mainloop()