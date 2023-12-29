import mysql.connector

con  = mysql.connector.connect(
    host="localhost", user="root", password="password", database='empd')

## Perfrom CURD create update read delete --> add_employ, promote_employ, check_employ, remove_employ, Display_employ, menu(front)

def add_employ():
     Id = input("Enter Employee Id: ")

     if(check_employ(Id)==True):
         print("Employee already exist")
         menu()

     else:
         Name = input("Enter Employee Name : ")
         Post = input("Enter Employee Post : ")
         Salary = input("Enter Employee Salary : ")
         data = (Id,Name,Post,Salary)

         sql = "insert into empd values(%s,%s,%s,%s)"
         c = con.cursor()
         c.execute(sql,data)
         con.commit()
         print("Employee Added Successfully")
         menu()

def promote_employ():
    Id = input("Enter Employee Id : ")

    if(check_employ == False):
        print("Employee does not exist \n Try Again ")
        menu()
    else:
        Amount = int(input("Enter increase of salary"))

        sql = 'Select salary from the empd where id=%s'
        data = (Id)
        c= con.cursor()
        c.execute(sql,data)
        con.commit()

        r = c.fetchone()
        t = r[0]+Amount
        sql = 'update empd set salary=%s where Id=%s'
        data = (t,Id)
        c.execute(sql,data)
        con.commit()
        print("Employee Salary Updated")
        menu()

def remove_employ():
    Id  = input("Enter Employee Id")

    if(check_employ==False):
        print("Employee Does Not Exist")
    else:
        sql = 'delete from empd where Id=%s'
        data = (Id)
        c = con.cursor()
        c.execute(sql,data)
        con.commit()
        print("The Employee Is Removed")
        menu()

def check_employ(employ_id):
    sql = 'select * from empd where id=%s'
    c = con.cursor(buffered=True)
    data = (employ_id)
    c.execute(sql,data)

    r = c.rowcount
    if r ==1:
        return True
    else:
        return False

def display_employ():
    sql = "select * from empd"
    c = con.cursor()
    c.execute(sql)

    r= c.fetchall()
    for i in r:
        print("Employee Id: ",i[0])
        print("EMployee Name: ",i[1])
        print("Employee Post: ",i[2])
        print("Employee Salary: ",i[3])
        print("---------------------------\
              -----------------------------\
              ------------------------------\
              -----------------------------------")
        menu()

def menu():
    print("Welcome to the employee management record")
    print("Press")
    print("1 to Add Employee ")
    print("2 to Promote Employee ")
    print("3 to Delete Employee ")
    print('4 to Display Employee')
    print("5 to Check Employ")
    print("6 to exit")

    ch = int(input("Enter your choice : "))

    if ch == 1:
        add_employ()
    elif ch == 2:
        promote_employ()
    elif ch == 3:
        remove_employ()
    elif ch == 4:
        display_employ()
    elif ch == 5:
        employ_id = input("Enter Employ id ")
        check_employ(employ_id)
    elif ch == 6:
        exit(0)
    else:
        print("Enter Valid Options")
        menu()


