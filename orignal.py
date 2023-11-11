import mysql.connector
from datetime import date,timedelta
connection = mysql.connector.connect(host="localhost",user="root",password="Vasundhara@403",database="management")
cursor = connection.cursor()

def main():
    cursor.execute("select book_id from books")
    bookid_list=[] #empty list to store all book id's
    for i in cursor:
        bookid_list.append(i[0])
    print("1- Show Tables\n2- Alter Library Books\n3- Issue Book\n4- Return Book\n5- Exit")
    choice=int(input("\nEnter your choice- "))
    if choice==1:
        show_tables()
    elif choice==2:
        alter_library(bookid_list)
    elif choice==3:
        issue_book(bookid_list)
    elif choice==4:
        return_book(bookid_list)
    elif choice==5:
        print("Thanks for using !!!")
        exit()
    else:
        print("\nWrong input !!!\n")
        main()


def show_tables():
    print("\nWhich table would you like to see ?\n1- Collection of Books\n2- Borrowed Books\n3- Borrowing History")
    choice=int(input("\nEnter choice- "))
    if choice==1:
        print("\n( Book Id , Book Name , Author Name , Quantity)\n")
        cursor.execute("select * from books")
        for x in cursor:
            print("(",x[0],",",x[1],",",x[2],",",x[3],")")
        print("\n")
    elif choice==2:
        print("\n(Std ID , Book ID , Date of Issue , Due Date)\n")
        cursor.execute("select * from currently_borrowed")
        for x in cursor:
            print("(",x[0],",",x[1],",",x[2],",",x[3],")")
        print("\n")
    elif choice==3:
        print("\n(Std ID , Book ID , Date of Issue , Due Date , Fine)\n")
        cursor.execute("select * from borrowing_history")
        for x in cursor:
            print("(",x[0],",",x[1],",",x[2],",",x[3],",",x[4],")")
        print("\n")
    else:
        print("\nWrong Inpur !!!\n")
        show_tables()

    ch=input("Would you like to continue? (Y/N)- ")
    print("\n")
    if ch.upper()=="Y" or ch.upper()=="YES":
        main()
    elif ch.upper()=="N" or ch.upper()=="NO":
        print("Thanks for using !!!")
        exit()
    else:
        print("\nWrong input !!!\n")
        main()


def issue_book(bookid_list):
    std=int(input("Enter Student ID- "))
    cursor.execute("select count(student_id) from currently_borrowed where student_id= %s",(std,))
    data=cursor.fetchone()
    if data[0]>=3:
        print("\nMaximum limit reached for ID ",std,". No more books can be issued.\n")
        main()
    else:
        available_books=[]
        cursor.execute("select book_id from books where quantity>0")
        for i in cursor:
            available_books.append(i[0])
        print("3 total books can be issued with 1 ID. Press N to stop\n")
        cursor.execute("select book_id,book_name from books where quantity>0")
        print("Book id ---> Book name")
        for i in cursor:
            print(i[0],"--->",i[1])
        print("\n")
        choice=input("Press N to cancel or any other key to continue- ")
        while choice.upper()!='N' and choice.upper()!="NO":
            cursor.execute("select book_id from currently_borrowed where student_id=%s",(std,))
            already_issued=[]
            for i in cursor:
                already_issued.append(i[0])
            bid=int(input("Enter Book Id to issue- "))
            if bid not in bookid_list:
                print("No such book available in library !!!")
                choice=input("Click N to stop issuing- ")
            elif bid in already_issued:
                print("This book is already with you.")
                choice=input("Click N to stop issuing- ")
            elif bid in bookid_list and bid not in available_books:
                print("Sorry !!! This book is currently out of stock. Comeback later for this book.")
                choice=input("Click N to stop issuing- ")
            else:
                issuedate=date.today()
                returndate=issuedate+timedelta(30)
                cursor.execute("insert into currently_borrowed values(%s,%s,%s,%s)",(std,bid,issuedate,returndate))
                cursor.execute("update books set quantity=quantity-1 where book_id=%s",(bid,))
                connection.commit()
                print("\nBook issued successfully !!!\n")
                cursor.execute("select count(student_id) from currently_borrowed where student_id= %s",(std,))
                data=cursor.fetchone()
                if data[0]>=3:
                    print("\nMaximum limit reached for ID ",std,". No more books can be issued.\n")
                    main()
                else:
                    choice=input("Click N to stop issuing- ")
        ch=input("Would you like to continue? (Y/N)- ")
        if ch.upper()=="Y" or ch.upper()=="YES":
            main()
        elif ch.upper()=="N" or ch.upper()=="NO":
            print("Thanks for using !!!")
            exit()
        else:
            print("\nWrong input !!!\n")
            main()


def return_book(bookid_list):
    std=int(input("Enter Student ID- "))
    cursor.execute("select count(student_id) from currently_borrowed where student_id= %s",(std,))
    data=cursor.fetchone()
    if data[0]==0:
        print("\nNo books are with",std,"\n")
        main()
    else:
        choice=input("Press N to cancel return or any other key to continue- ")
        while choice.upper()!='N' and choice.upper()!="NO":
            issued_books=[]
            cursor.execute("select book_id from currently_borrowed where student_id=%s",(std,))
            for i in cursor:
                issued_books.append(i[0])
            print("Books to return are- ")
            for i in issued_books:
                print(i)
            print("\n")
            bid=int(input("Enter Book Id to return- "))
            if bid not in bookid_list:
                print("No such book available in library !!!")
                choice=input("Click N to stop returning- ")
            elif bid in bookid_list and bid not in issued_books:
                print("You don't have this book with you.")
                choice=input("Click N to stop returning- ")
            else:
                cursor.execute("select * from currently_borrowed where student_id=%s and book_id=%s",(std,bid))
                data=cursor.fetchone()
                issuedate=data[2]
                returndate=data[3]
                todaydate=date.today()
                diff=(todaydate-returndate).days
                if diff<=0:
                    print("Thankyou for returning book on time. Have a nice day!!!")
                    fine=0
                else:
                    fine=diff*5
                    print("Book returned successfully !!!")
                cursor.execute("update books set quantity=quantity+1 where book_id=%s",(bid,))
                cursor.execute("delete from currently_borrowed where student_id=%s and book_id=%s",(std,bid))
                cursor.execute("insert into borrowing_history values(%s,%s,%s,%s,%s)",(std,bid,issuedate,todaydate,fine))
                connection.commit()
                cursor.execute("select count(student_id) from currently_borrowed where student_id= %s",(std,))
                data=cursor.fetchone()
                if data[0]==0:
                    print("\nNo books are with",std,"\n")
                    main()
                else:
                    choice=input("Press N to cancel return or any other key to continue- ")
    
    ch=input("Would you like to continue? (Y/N)- ")
    if ch.upper()=="Y" or ch.upper()=="YES":
        main()
    elif ch.upper()=="N" or ch.upper()=="NO":
        print("Thanks for using !!!")
        exit()
    else:
        print("\nWrong input !!!\n")
        main()


def alter_library(bookid_list):
    print("\nWhat would you like to do ?\n1- Update current book stock\n2- Add new books")
    choice=int(input("\nEnter choice- "))
    if choice==1:
        up=int(input("\nEnter Book ID whose stock is to be updated- "))
        if up not in bookid_list:
            print("No such Book exists in record !!!")
        else:
            num=int(input("Enter amount to be updated- "))
            cursor.execute("update books set Quantity= Quantity+%s where Book_ID= %s",(num,up))
            connection.commit()
            print("Data updated successfully !!!")

    elif choice==2:
        choice=input("Press N to cancel or any other key to continue- ")
        while choice.upper()!='N' and choice.upper()!="NO":
            id=int(input("\nEnter book ID- "))
            if id in bookid_list:
                print("Book already exists in record !!!\n")
            else:
                book=input("Enter Book name- ")
                author=input("Enter Author name- ")
                num=int(input("Enter quantity- "))
                cursor.execute("insert into books value(%s,%s,%s,%s)",(id,book,author,num))
                connection.commit()
                print("\nData added successfully !!!\n")
            choice=input("Would you like to add more records ? (Y/N)- ")
    else:
        print("\nWrong input !!!\n")
        main()

    ch=input("Would you like to continue? (Y/N)- ")
    if ch.upper()=="Y" or ch.upper()=="YES":
        main()
    elif ch.upper()=="N" or ch.upper()=="NO":
        print("Thanks for using !!!")
        exit()
    else:
        print("\nWrong input !!!\n")
        main()

#calling main function to start the program
main()