from tkinter import *
import pyodbc
import random
from tkinter import messagebox
import dominate
from dominate.tags import *
from pyhtml2pdf import converter
import os


global conn_str
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Haider\Downloads\Quiz_testing.accdb;'
    )


# Triggering the single question data collector for the first time 
def question_uploader(x,data):
    global max_no_of_questions
    max_no_of_questions = x
    single_Question(x, data)



# Saving the question Data in the database 
def save_question_to_database(x,data):
    active = "Yes"
    if len(ques_var.get())==0 or len(opt_a_var.get())==0 or len(opt_b_var.get())==0 or len(opt_c_var.get())==0 or len(opt_d_var.get())==0:
         lbl=Label(ques_frame,text="One or more entries left empty!",font=("Verdana",15,"bold"), bg="#A4CEFC",fg="#0F3375")
         lbl.place(x=200,y=450)
    else:
        ques_frame.destroy()
        x = x-1
        cnxn = pyodbc.connect(conn_str)
        crsr = cnxn.cursor()
        crsr.execute(f"INSERT INTO Questions(Question, OptionA, OptionB, OptionC, OptionD, Correct, Course, Active, IsPDFAvailable,QuizNo) VALUES ('{ques_var.get()}', '{opt_a_var.get()}', '{opt_b_var.get()}', '{opt_c_var.get()}', '{opt_d_var.get()}',{correct_var.get()},'{data[4]}', {active}, {'Yes' if pdf_var.get() == True else 'No'}),{quiz_id_var.get()}")
        crsr.commit()
        single_Question(x, data)
     


# # Getting Data of a single question from the user 
def single_Question(x, data):
    global ques_frame
    ques_frame=Frame(right_frame,bg="#A4CEFC")
    ques_frame.place(x=20,y=20,height=600,width=700)
    for widget in left_frame.winfo_children():
        widget.destroy()
    if x==0:
         lbl=Label(ques_frame,text="Questions have been uploaded successfully",font=("Verdana",15,"bold"),anchor="center", bg="#A4CEFC",fg="#0F3375")
         lbl.grid(row=0,padx=10, pady=10,column=0)
    else:
        option_question = ["A", "B", "C", "D"]
        global correct_var
        global ques_var
        global opt_a_var
        global opt_b_var
        global opt_c_var
        global opt_d_var
        correct_var = IntVar()
        correct_var.set(1)
        opt_a_var=StringVar()
        opt_b_var=StringVar()
        opt_c_var=StringVar()
        opt_d_var=StringVar()
        ques_var=StringVar()
        Label(ques_frame,text=f"Question {max_no_of_questions-x+1}:",font=("Verdana",20),fg="#0F3375",bg="#A4CEFC").grid(row=0,padx=10, pady=10,column=0)
        ques=Entry(ques_frame,textvariable=ques_var,font=("Verdana",15),width=40)
        ques.grid(row=0,padx=10, pady=10,column=1,columnspan=2)
        Label(ques_frame,text="Option A",font=("Verdana",15),bg="#A4CEFC",fg="#0F3375").grid(row=1,padx=10, pady=10,column=0)
        Label(ques_frame,text="Option B",font=("Verdana",15),bg="#A4CEFC",fg="#0F3375").grid(row=2,padx=10, pady=10,column=0)
        Label(ques_frame,text="Option C",font=("Verdana",15),bg="#A4CEFC",fg="#0F3375").grid(row=3,padx=10, pady=10,column=0)
        Label(ques_frame,text="Option D",font=("Verdana",15),bg="#A4CEFC",fg="#0F3375").grid(row=4,padx=10, pady=10,column=0)
        opt_a=Entry(ques_frame,textvariable=opt_a_var,font=("Verdana",15),width=15)
        opt_a.grid(row=1,padx=10, pady=10,column=1)
        opt_b=Entry(ques_frame,textvariable=opt_b_var,font=("Verdana",15),width=15)
        opt_b.grid(row=2,padx=10, pady=10,column=1)
        opt_c=Entry(ques_frame,textvariable=opt_c_var,font=("Verdana",15),width=15)
        opt_c.grid(row=3,padx=10, pady=10,column=1)
        opt_d=Entry(ques_frame,textvariable=opt_d_var,font=("Verdana",15),width=15)
        opt_d.grid(row=4,padx=10, pady=10,column=1)
        for i in range(1, 5):
                r=5
                c=0
                if i> 2:
                    r = 6
                    c = -2
                options = Radiobutton(ques_frame, text=option_question[i-1], font=["comic sans", 15], value=i, variable=correct_var, anchor="center", width=10,bg="#A4CEFC",fg="#0F3375")
                options.grid(row= r, padx=10, pady=10,column= c+i-1)
        go=Button(ques_frame,text="Next",font=("Verdana",15),width=20,fg="#A4CEFC",bg="#0F3375",command=lambda: save_question_to_database(x,data))
        go.grid(row=7,padx=10, pady=10,column=1)

def select_result(data):
    slct_frm=Frame(right_frame,bg="#A4CEFC")
    slct_frm.place(x=20,y=20,height=600,width=650)
    cnxn = pyodbc.connect(conn_str)
    crsr1 = cnxn.cursor()
    crsr1.execute(f"select Distinct QuizNo from Questions where Course='{data[4]}'")
    quizes = crsr1.fetchall()
    for i in range(len(quizes)):
           Radiobutton(slct_frm,variable=quiz_chk_var,anchor="center",width=20,text=quizes[i][0],value=quizes[i][0],font=["comic sans", 20,"bold"],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=i, padx=10, pady=10)   

    Button(slct_frm,anchor="center",width=20,text='Proceed',font=["comic sans", 20,"bold"],bg="#A4CEFC",fg="#0F3375",command=lambda:generate_result_pdf(data,quiz_chk_var.get())).grid(column=0,row=len(quizes)+1,padx=10,pady=10)

def quiz_info(data):
    info = Frame(right_frame,bg="#A4CEFC")
    info.place(x=20,y=20,height=500,width=700)
    global pdf_var
    global no_ques_var
    no_ques_var=IntVar()
    pdf_var=BooleanVar(value=False)
    Label(info,text="Question Maker",font=("Verdana",25,"bold"),anchor="center",width=20,bg="#A4CEFC",fg="#0F3375").grid(row=0,column=0,columnspan=2)
    Label(info,text="Enter the number of questions",font=("Verdana",15,"bold"),anchor="center",width=30,bg="#A4CEFC",fg="#0F3375").grid(row=1,column=0)
    Label(info,text="Enter QuizID:",font=("Verdana",15,"bold"),anchor="center",width=30,bg="#A4CEFC",fg="#0F3375").grid(row=2,column=0)
    Radiobutton(info,text="Would you like to provide\nsolution pdf to students?",font=("Verdana",15),anchor="center",width=30,value=True,variable=pdf_var,bg="#A4CEFC",fg="#0F3375").grid(row=3,column=0)
    no_ques=Entry(info,textvariable=no_ques_var,width=10,font=("Verdana",15))
    no_ques.grid(row=1,column=1,padx=10,pady=10)
    Entry(info,textvariable=quiz_id_var,width=10,font=("Verdana",15)).grid(row=2,column=1,padx=10,pady=10)
    Button(info,text="Next",font=("Verdana",15),fg="#A4CEFC",bg="#0F3375",width=10,command=lambda:question_uploader(no_ques_var.get(),data)).grid(row=3,column=1,padx=10,pady=10)

# Entering the number of questions in the test 
def teacher_window(data):
    global Data
    Data = Frame(right_frame,bg="#A4CEFC")
    Data.place(x=20,y=20,height=500,width=700)
    k=Button(Data,text="Generate student result",font=("Verdana",15),width=25,fg="#A4CEFC",bg="#0F3375", command=lambda:select_result(data)).grid(row=2,column=0,columnspan=2,padx=10,pady=10)   
    Button(Data,text="Create a quiz",font=("Verdana",15),width=25,fg="#A4CEFC",bg="#0F3375", command=lambda:quiz_info(data)).grid(row=1,column=0,columnspan=2,padx=10,pady=10)   


# Check the courses 
def teacher_checker_window(data):
    global student_data
    student_data = data
    global conn_str
    global teacher_checker
    teacher_checker = Frame(right_frame, bg="#A4CEFC")
    teacher_checker.place(x=0,y=20,height=600,width=700)
    course_check_Heading = Label(teacher_checker, anchor="center",width=25,text="Select Course", font=["comic sans", 25,"bold"],bg="#A4CEFC",fg="#0F3375")
    course_check_Heading.grid(column=0, row=0, padx=10, pady=10)
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    crsr.execute(f"select * from users where isTeacher=True")
    teacher_data = crsr.fetchall()
    for i in range(len(teacher_data)):
        course_button=Button(teacher_checker,fg="#A4CEFC",bg="#0F3375", text=teacher_data[i][4], command=lambda i=i:check_quiz_available(teacher_data[i][4]),width=25)
        course_button.grid(column=0, row=i+1, padx=10, pady=10)



def quiz_checker(quiz_id):       
    cnxn = pyodbc.connect(conn_str)
    crsr2 = cnxn.cursor()
    quiz = Frame(right_frame,bg="#A4CEFC")
    quiz.place(x=20,y=20,height=600,width=650)
    crsr2.execute(f"select * from Result where Course='{Course_name}' AND UserID={student_data[0]} and QuizNo='{quiz_id}'")
    result_data = crsr2.fetchone()
    if result_data == None:
        crsr1 = cnxn.cursor()
        crsr1.execute(f"select Question,OptionA, OptionB, OptionC, OptionD, Correct from Questions where Course='{Course_name}' and QuizNo='{quiz_id}'")
        global quiz_ques
        quiz_ques = crsr1.fetchall()
        if len(quiz_ques) == 0:
            Label(quiz,anchor="center",width=25,text=f"There are no Quizes Available",font=('Verdana',18,"bold"),bg="#A4CEFC",fg="#0F3375").grid(column=0, row=0, padx=10, pady=10)
        else:
            global result
            result = 0
            global no_of_questions
            no_of_questions = len(quiz_ques)
            random.shuffle(quiz_ques)
            question_generator(quiz_ques,quiz_id)
    else:
        Label(quiz,anchor="center",width=40,text=f"You Have Already Attempted This Test\n You got {result_data[1]}/{result_data[4]}",font=["comic sans", 20,"bold"],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=0, padx=10, pady=10)
        Button(quiz,anchor="center",width=20,text=f"Check for another quiz",font=["comic sans", 20,"bold"],bg="#A4CEFC",fg="#0F3375",command=lambda:check_quiz_available(Course_name)).grid(column=0, row=1, padx=10, pady=10)
        
# This is to generate the result 
def check_ans(correct, checked):
    if correct == checked:
        global result
        result = result + 1
    del quiz_ques[0]
    single_question_frame.destroy()
    question_generator(quiz_ques,quiz_chk_var.get()) 

# # Student Portal
def check_quiz_available(course_data):
    global Course_name 
    Course_name = course_data
    global check_quiz
    check_quiz = Frame(right_frame,bg="#A4CEFC")
    check_quiz.place(x=20,y=20,height=600,width=650)
    cnxn = pyodbc.connect(conn_str)
    crsr1 = cnxn.cursor()
    crsr1.execute(f"select Distinct QuizNo from Questions where Course='{Course_name}'")
    quiz_chk = crsr1.fetchall()
    if len(quiz_chk) == 0:
      Label(check_quiz,anchor="center",width=25,text=f"There are no Quizes Available",font=('Verdana',18,"bold"),bg="#A4CEFC",fg="#0F3375").grid(column=0, row=0, padx=10, pady=10) 
    else:
       for i in range(len(quiz_chk)):
          Radiobutton(check_quiz,variable=quiz_chk_var,anchor="center",width=20,text=quiz_chk[i][0],value=quiz_chk[i][0],font=["comic sans", 20,"bold"],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=i, padx=10, pady=10) 
       Button(check_quiz,anchor="center",width=20,text='Proceed',font=["comic sans", 20,"bold"],bg="#A4CEFC",fg="#0F3375",command=lambda:quiz_checker(quiz_chk_var.get())).grid(column=0,row=len(quiz_chk)+1,padx=10,pady=10)
       

# # This is to display the questions to the student
def question_generator(question,quiz_id):
    if len(question) == 0:
        cnxn = pyodbc.connect(conn_str)
        crsr = cnxn.cursor()
        crsr.execute(f"insert into Result(Result, UserID, Course, MaxMarks,QuizNo) values ({result},{student_data[0]},'{Course_name}',{no_of_questions},'{quiz_id}')")
        crsr.commit()
        crsr1 = cnxn.cursor()
        crsr1.execute(f"select isPDFAvailable from Questions where Course = '{Course_name}' and QuizNo='{quiz_id}'")
        isPDFAvailable = crsr1.fetchone()
        result_frame=Frame(right_frame,bg="#A4CEFC")
        result_frame.place(x=50,y=50,height=300,width=500)
        Label(result_frame, text=f"Result\nYou got:{result}/{no_of_questions}",font=('Verdana',25,"bold"),bg="#A4CEFC", anchor="center", width=18,fg="#0F3375").grid(row=0, column=0, padx=10, pady=10)
        if isPDFAvailable[0] == True:
            Button(result_frame, text="Generate PDF", anchor="center", fg="#A4CEFC",bg="#0F3375",width=25, command=lambda:generate_pdf(quiz_id)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    else:
        global single_question_frame
        single_question_frame = Frame(right_frame,bg="#A4CEFC")
        single_question_frame.place(x=0,y=0,height=680,width=780)
        var1 = IntVar()
        question_gen = Label(single_question_frame, text=question[0][0], anchor="center", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(row=0, column=0, padx=10, pady=10)
        for i in range(1, 5):
            options = Radiobutton(single_question_frame, text=question[0][i], font=["comic sans", 15], value=i, variable=var1, anchor="center", width=40,bg="#A4CEFC",fg="#0F3375").grid(row=i, column=0, padx=10, pady=10)
        confirm_button = Button(single_question_frame,fg="#A4CEFC",bg="#0F3375", text="Confirm Answer", anchor="center", width=40, command=lambda: check_ans(question[0][5], var1.get()))
        confirm_button.grid(row=6, column=0, padx=10, pady=10)


# This is to generate PDF using HTML 
def generate_pdf(quiz_id):
    cnxn = pyodbc.connect(conn_str)
    crsr1 = cnxn.cursor()
    crsr1.execute(f"select Question,OptionA, OptionB, OptionC, OptionD, Correct from Questions where Course='{Course_name}'and QuizNo='{quiz_id}'")
    quiz_ques_pdf = crsr1.fetchall()
    doc = dominate.document(title='Solution to the Quiz')
    ans = ["A", "B", "C", "D"]
    with doc.head:
        link(rel='stylesheet', href='style.css')
    with doc:
        with div(id='heading'):
            h1("Solution to the Quiz")
            h2(f'{Course_name}')

        for i in range(len(quiz_ques_pdf)):
            with div():
                attr(cls='ques')
                p(f'Q{i+1}: {quiz_ques_pdf[i][0]}')
            for j in range(1,5):
                if j==quiz_ques_pdf[i][5]:
                    with div():
                        attr(cls="correct_ans")
                        p(f"({ans[j-1]}) {quiz_ques_pdf[i][j]}")
                else:
                    with div():
                        attr(cls="ans")
                        p(f"({ans[j-1]}) {quiz_ques_pdf[i][j]}")
        with div():
            attr(cls="result")
            h3(f"Your Result is: {result}/{no_of_questions}".upper())
    f = open("htmlTempFile.html", "w")
    f.write(str(doc))
    f.close()
    path = os.path.abspath('htmlTempFile.html')
    converter.convert(f'file:///{path}', 'Solution.pdf')
    os.remove("htmlTempFile.html")


# # This is to generate pdf for teacher 
def generate_result_pdf(data,quiz_id):
    marks = []
    Data.destroy()
    cnxn = pyodbc.connect(conn_str)
    crsr1 = cnxn.cursor()
    crsr1.execute(f"select * from Result where Course='{data[4]}' and QuizNo='{quiz_id}'")
    all_student_result = crsr1.fetchall()
    doc = dominate.document(title=f"Student Result ({data[4]})")
    with doc.head:
        link(rel='stylesheet', href='style.css')
    with doc:
        with div(id='heading'):
            h1(f"Compiled Result for Quiz {quiz_id}")
        with div():
            attr(cls="table-div")
            with table():
                attr(cls="result_table")
                with thead():
                    th("Username")
                    th("Marks Obtained")
                    th("Total Marks")
                    th("Course")
                for i in all_student_result:
                    marks.append(i[1])
                    cnxn1 = pyodbc.connect(conn_str)
                    crsr = cnxn1.cursor()
                    crsr.execute(f"select Username from users where UserID={i[2]}")
                    name = crsr.fetchone()
                    with tbody():
                        td(name[0])
                        td(i[1])
                        td(i[4])
                        td(data[4])
        with div():
            attr(cls="average")
            h3(f"Class Average: {round(sum(marks)/len(marks),2)}")
    f = open("htmlTempFile.html", "w")
    f.write(str(doc))
    f.close()
    path = os.path.abspath('htmlTempFile.html')
    converter.convert(f'file:///{path}', 'Compiled_Result.pdf')
    os.remove("htmlTempFile.html")



# THIS IS REGARDING THE AUTHENTICATION 
    
# This is to Signup
def signupCheck():
    global conn_str
    isTeacher = "No"
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    crsr.execute(f"select Username from users where Username='{signup_username_var.get()}'")
    isUsernameTaken = crsr.fetchone()
    if len(signup_username_var.get())==0 or len(signup_password_var.get())==0 or len(signup_confirmPassword_var.get())==0 or len(security_question_var.get())==0:
        Label(Signup, anchor="center",width=30,text="Entries left empty!", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=9, columnspan=2, padx=10, pady=10)
    else:
        if isUsernameTaken != None:
            Label(Signup, anchor="center",width=30,text="Username Already Taken", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=9, columnspan=2, padx=10, pady=10)
        else:
            if signup_password_var.get() == signup_confirmPassword_var.get():
                if Teacher.get() == True:
                 isTeacher = "Yes"
                Label(Signup, anchor="center",width=30,text="Registered Successfully", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=9, columnspan=2, padx=10, pady=5)
                cnxn = pyodbc.connect(conn_str)
                crsr = cnxn.cursor()
                crsr.execute(f"insert into Users(Username, Password, IsTeacher, Course, SQans) values ('{signup_username_var.get()}', '{signup_password_var.get()}', {isTeacher}, '{signup_course_var.get()}','{security_question_var.get()}')")
                cnxn.commit()
                cnxn.close()
            else:
                Label(Signup, anchor="center",width=30,text="Incorrect Credentials", font=["comic sans", 15], bg="#A4CEFC",fg="#0F3375").grid(column=0, row=9, columnspan=2, padx=10, pady=10)


# This is to Login
def loginCheck():
    global conn_str
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    crsr.execute(f"select * from users where Username='{login_username_var.get()}'")
    isAuthenticUser = crsr.fetchone()
    if len(login_username_var.get())==0 or len(login_password_var.get())==0:
        Label(Login, anchor="center",width=20,text="Entries left empty!", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=5, columnspan=2, padx=10,pady=10)
    else:
        if isAuthenticUser == None:
           Label(Login, anchor="center",width=20,text="This User Does Not Exist", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=5, columnspan=2, padx=10, pady=10)
        else:
            if isAuthenticUser[2]==login_password_var.get():
              Label(Login, anchor="center",width=20,text="The User is Authorized", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=5, columnspan=2, padx=10, pady=10)
            #   Signup_login_frame.destroy()

              for widget in Signup_login_frame.winfo_children():
                  widget.destroy()
              
              if isAuthenticUser[3] == False:
                  teacher_checker_window(isAuthenticUser)
              else:
                    teacher_window(isAuthenticUser)
            else:
                Label(Login, anchor="center",width=20,text="Incorrect Password", font=["comic sans", 15], bg="#A4CEFC",fg="#0F3375").grid(column=0, row=5, columnspan=2, padx=10, pady=10)
    


# # This is to get the security question to change the password 
def sq_check():
    global security_question_var_chck
    global sqn_check
    sqn_check = Frame(Signup_login_frame,bg="#A4CEFC")
    sqn_check.place(x=0,y=0,height=500,width=390)
    
    security_question_var_chck = StringVar()
    
    security_question = Label(sqn_check, anchor="center", width=20, text="Enter your mother's name",fg="#0F3375",bg="#A4CEFC", font=["comic sans", 15]).grid(column=0, row=0, padx=10, pady=10)
    security_question_entry = Entry(sqn_check, width=20, textvariable=security_question_var_chck)
    security_question_entry.grid(column=1, row=0, padx=10, pady=10)
    sqbutton = Button(sqn_check, text="Verify", font=["comic sans", 15], anchor="center", width=10, command=verify,fg="#A4CEFC",bg="#0F3375")
    sqbutton.grid(column=0, row=1, padx=10, pady=10, columnspan=2)



# This is to update the password 
def update():
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    query = "UPDATE Users SET Password=? WHERE Username=?"
    crsr.execute(query, (new_password_entry_var.get(), login_username_var.get()))
    crsr.commit()
    Label(sqn_check, anchor="center", width=22, text="Password updated\nPlease try logging in again", font=["comic sans", 15,"bold"],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=5, padx=10, pady=10)


# This is to verify the security code 
def verify():
    global new_password_entry_var
    new_password_entry_var=StringVar()
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    crsr.execute(f"select * from users where Username='{login_username_var.get()}'")
    sq_authentic = crsr.fetchone()
    if sq_authentic[5] == security_question_var_chck.get():
        Label(sqn_check, anchor="center", width=20, text="Correct", font=["comic sans", 15,"bold"],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=2, padx=10, pady=10)
        Label(sqn_check, anchor="center", width=20, text="Enter new password", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=3, padx=10,pady=10)
        security_question_entry = Entry(sqn_check, width=20, textvariable=new_password_entry_var)
        security_question_entry.grid(column=1, row=3, padx=10, pady=10)
        Button(sqn_check, text="Update", font=["comic sans", 15],fg="#A4CEFC",bg="#0F3375", anchor="center", width=10,command=update).grid(column=0, row=4, padx=10, pady=10, columnspan=2)

    else:
        k=Label(sqn_check, anchor="center", width=20, text="Wrong answer", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=2, padx=10 ,pady=10)


# Login Window 
def login():
    global Login
    Login = Frame(Signup_login_frame,bg="#A4CEFC")
    Login.place(x=0,y=0,height=500,width=390)
    global login_username_var
    global login_password_var
    login_username_var = StringVar()
    login_password_var = StringVar()
    global quiz_id_var
    global quiz_chk_var
    quiz_chk_var=StringVar()
    quiz_id_var=StringVar()
    loginHeading = Label(Login, anchor="center",width=10,text="Login", font=["comic sans", 30,"bold"],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=0, columnspan=2, padx=10, pady=10)
    login_username = Label(Login, anchor="center",width=13,text="Username", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=1, padx=10, pady=10)
    login_password = Label(Login, anchor="center",width=13,text="Password", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=2, padx=10, pady=10)
    login_username_entry = Entry(Login, width=30, textvariable=login_username_var)
    login_username_entry.grid(column=1, row=1, padx=10, pady=10)
    login_password_entry = Entry(Login, width=30, textvariable=login_password_var)
    login_password_entry.grid(column=1, row=2, padx=10, pady=10)
    login_button = Button(Login,text="Login",font=["comic sans", 15],anchor="center",fg="#A4CEFC",bg="#0F3375",width=10, command = loginCheck).grid(column=0, row=3, padx=10, pady=10, columnspan=2)
    forget_button = Button(Login,text="Forgot password?",font=["comic sans", 15],anchor="center",width=20,command=sq_check,fg="#A4CEFC",bg="#0F3375").grid(column=0, row=4, padx=10, pady=10, columnspan=2)


# This is to show the course name entry when we are signing in as a teacher 
def show_course_name():
    if Teacher.get() == True:
        signup_course = Label(Signup, anchor="center",width=15,text="Course Name", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=5, padx=10, pady=10)
        signup_course_entry = Entry(Signup, width=20, textvariable=signup_course_var)
        signup_course_entry.grid(column=1, row=5, padx=10, pady=10)
    else:
        Label(Signup, anchor="center",width=15,text="", font=["comic sans", 10],bg="#A4CEFC").grid(column=0, row=5, padx=10, pady=10)
        Label(Signup, anchor="center",width=15,text="", font=["comic sans", 10],bg="#A4CEFC").grid(column=1, row=5, padx=10, pady=10)


# Signup Window 
def signup():
    global Signup
    Signup = Frame(Signup_login_frame,bg="#A4CEFC")
    Signup.place(x=0,y=0,height=500,width=390)
    global Teacher
    global signup_username_var
    global signup_password_var
    global signup_confirmPassword_var
    global signup_course_var
    global security_question_var
    security_question_var = StringVar()
    signup_course_var = StringVar()
    signup_username_var = StringVar()
    signup_password_var = StringVar()
    signup_confirmPassword_var = StringVar()
    Teacher= BooleanVar()
    signupHeading = Label(Signup,bg="#A4CEFC", anchor="center",width=10,text="Signup", font=["comic sans", 30,"bold"],fg="#0F3375").grid(column=0, row=0, columnspan=2, padx=10, pady=10)
    signup_username = Label(Signup, anchor="center",width=10,text="Username", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=1, padx=10, pady=10)
    signup_password = Label(Signup, anchor="center",width=10,text="Password", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=2, padx=10, pady=10)
    signup_confirmPassword = Label(Signup, anchor="center",width=15,text=" Confirm Password", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=3, padx=10, pady=10)
    security_question = Label(Signup, anchor="center",width=20,text="Enter your mother's name", font=["comic sans", 15],bg="#A4CEFC",fg="#0F3375").grid(column=0, row=4, padx=10, pady=10)
    signup_username_entry = Entry(Signup, width=20, textvariable=signup_username_var)
    signup_username_entry.grid(column=1, row=1, padx=10, pady=10)
    signup_password_entry = Entry(Signup, width=20, textvariable=signup_password_var)
    signup_password_entry.grid(column=1, row=2, padx=10, pady=10)
    signup_confirmpassword_entry = Entry(Signup, width=20, textvariable=signup_confirmPassword_var)
    signup_confirmpassword_entry.grid(column=1, row=3, padx=10, pady=5)
    security_question_entry = Entry(Signup, width=20, textvariable=security_question_var)
    security_question_entry.grid(column=1, row=4, padx=10, pady=5)
    signup_teacher =Radiobutton(Signup, text="Teacher",font=["comic sans", 15], value=True,variable=Teacher,command=show_course_name,bg="#A4CEFC",fg="#0F3375")
    signup_teacher.grid(column=0, row=6 ,padx=10, pady=5)
    signup_student =Radiobutton(Signup, text="Student",font=["comic sans", 15], value=False,variable=Teacher,command=show_course_name,bg="#A4CEFC",fg="#0F3375")
    signup_student.grid( column=0, row=7 ,padx=10, pady=5)
    signup_button = Button(Signup,text="Signup",font=["comic sans", 15],anchor="center",width=10,command = signupCheck,fg="#A4CEFC",bg="#0F3375").grid(column=0, row=8, padx=10, pady=5, columnspan=2)
    Signup.mainloop()


# Login or Signup Window 
auth = Tk()
auth.title("Login or Signup")
auth.geometry("1200x724")
auth.config(bg="#0F3375")
auth.resizable(False,False)
heading_data = Label(auth,text="Quiz Management System", font=["Verdana", 30,"bold" ],bd=10,bg="#A4CEFC",highlightbackground="#0F3375", highlightthickness=5,fg="#0F3375").pack(side=TOP,fill=X)
left_frame = Frame(auth,bg="#A4CEFC",bd=10,highlightbackground="#0F3375",highlightthickness=5,highlightcolor="#0F3375")
left_frame.place(x=0,y=74,width=400,height=645)
right_frame = Frame(auth,bg="#A4CEFC",bd=10,highlightbackground="#0F3375",highlightthickness=5,highlightcolor="#0F3375")
right_frame.place(x=400,y=74,width=800,height=645)
devs=Label(right_frame,text="Developed By:\nFESE-019: Muzzammil Ahmed\nFESE-024: Kaif Nathani\nFESE-021: Haider Shahid",font=('verdana',22,"bold"),bg="#A4CEFC",fg="#0F3375")
devs.place(x=160,y=200,height=250,width=500)
heading = Label(left_frame,text="Login Or Signup", font=["Verdana", 20,"bold" ],bg="#A4CEFC",fg="#0F3375").place(x=65,y=20)
loginbutton = Button(left_frame,text="Login", command= login, font=["Verdana", 15],fg="#A4CEFC",bg="#0F3375").place(x=95,y=80)
signupbutton = Button(left_frame,text="Signup", command= signup, font=["Verdana", 15],fg="#A4CEFC",bg="#0F3375").place(x=190,y=80)
Signup_login_frame = Frame(left_frame,bg="#A4CEFC")
Signup_login_frame.place(x=0,y=150,height=450,width=350)

auth.mainloop()