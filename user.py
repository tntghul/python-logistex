import mysql.connector
from flask import session
from datetime import datetime
date = datetime.now()

class user_operation:
    def connection(self):
        con=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="logixstic")
        return con


    def book_shipment(self,bname,bemail,bphone,origin,destination,content,dpackage,size,price,track_no,origin_p,destination_p):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into book_shipment (bname,bemail,bphone,origin,destination,content,dpackage,size,price,track_no,origin_p,destination_p) values (%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
        record=[bname,bemail,bphone,origin,destination,content,dpackage,size,price,track_no,origin_p,destination_p]
        mycursor.execute(sq,record)
        del_insert="insert into delivery (p_name,track_no,origin_pincode,origin_place,destination_pincode,destination_place,contact,price) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        del_record=[bname,track_no,origin,origin_p,destination,destination_p,bphone,price]
        mycursor.execute(del_insert,del_record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def get_book_by_id(self, bid):
        db=self.connection()
        mycursor=db.cursor()  # This will give results as a dictionary
        query = "SELECT * FROM book_shipment WHERE bid = %s"
        mycursor.execute(query, (bid,))
        record = mycursor.fetchone()  # Fetch the first (and only) matching record
        mycursor.close()
        return record

    def book_update(self,bid,bname,bemail,bphone,origin,destination,content,dpackage,size,price,track_no,origin_p,destination_p):
        db=self.connection()
        mycursor=db.cursor()
        sq="update book_shipment set bname=%s,bemail=%s, bphone=%s,origin=%s,destination=%s,content=%s,dpackage=%s,price=%s,size=%s,track_no=%s,origin_p=%s,destination_p=%s where bid=%s"

        record=[bname,bemail,bphone,origin,destination,content,dpackage,size,price,track_no,origin_p,destination_p,bid]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        session['bphone']=bphone
        session['origin']=origin
        session['destination']=destination
        session['content']=content
        session['dpackage']=dpackage
        session['origin_p']=origin_p
        session['destination_p']=destination_p
        
        return  

    def contact(self,cname,cemaill,cphone,csubject,comment):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into contact (cname,cemaill,cphone,csubject,comment) values (%s,%s,%s,%s,%s)"
        record=[cname,cemaill,cphone,csubject,comment]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def signup(self,sname,sphone,semail,spwd):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into signup (sname,semail,sphone,spwd) values (%s,%s,%s,%s)"
        record=[sname,sphone,semail,spwd]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

   

    def login_all(self,semail):
        db = self.connection()  # Establish database connection
        if db.is_connected():
            print("✅ Database Connected")
        else:
            print("❌ Database Connection Failed")
        mycursor = db.cursor()
        sq = "SELECT semail,spwd FROM signup where semail=%s"
        print(semail)
        
        mycursor.execute(sq,(semail,))
        row=mycursor.fetchone()
        print(f"🟢 Fetched Row: {row}")
        print (row)

        if row:
            print("✅ Query executed successfully and data fetched:", row)
        else:
            print("❌ No data found for the provided email.")

        if row:
            email ,pswd = row
            print("Email",email)
            print("Password",pswd)
        else:

            print("False")

        return row
        
        
    def bookadmin(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select * from book_shipment"
        mycursor.execute(sq)
        row=mycursor.fetchall()
        return row

    def profile_one(self,semail):
        db = self.connection() 
        mycursor = db.cursor()
        sq = "SELECT * FROM signup where semail = %s"
        mycursor.execute(sq,(semail,))
        row=mycursor.fetchone()
        return row
        print(row)

    def adminprofile(self,sname,sphone,spwd):
        db=self.connection()
        mycursor=db.cursor()
        sq="update signup set sname =%s, sphone =%s,spwd=%s where email=%s"
        record=[sname,sphone,spwd,session['semail']]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        
        session['sname']=sname
        session['sphone']=sphone
        session['spwd']=spwd
        print(sname)
        return

    def admincontact(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select * from contact"
        mycursor.execute(sq)
        row=mycursor.fetchall()
        return row

    def delete_book(self,bid):
        db=self.connection()
        mycursor=db.cursor()
        sq="delete from book_shipment where bid=%s"
        record=[bid]
        mycursor.execute(sq,record)
        db.commit()

    def view_book(self,bid):
        db=self.connection()
        mycursor=db.cursor()
        sq="select * from book_shipment where bid=%s"
        record=[bid]
        mycursor.execute(sq,record)
        row=mycursor.fetchone()
        return row

    def delete_contact(self,id):
        db=self.connection()
        mycursor=db.cursor()
        sq="delete from contact where id=%s"

        record=[id]
        mycursor.execute(sq,record)
        db.commit()
        
        return 


    def payment(self,payid,ord_id):
        db=self.connection()
        mycursor=db.cursor()
        bid = session.get("bid")
        price = session.get("price")
        print("pass",bid)
        print("pass",price)
        sq="select price from book_shipment where bid=%s"
        mycursor.execute(sq, (bid,))
        
        row=mycursor.fetchone()
        # amt=row[9]
        # payable = price 
        bid = session.get("bid")
        price = session.get("price")
        print("value",bid)
        print("value",price)

        if not bid or not price:
            print("Error: Bid or Price not found in session!")
            return "Error: Bid or Price not found in session."
        sq="insert into payment (payid,ord_id,paydate,bid,amt) values(%s,%s,%s,%s,%s)"
        
        record=[payid,ord_id,date.today(),bid,price]
        print(record)
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return  

    def receipt(self,payid):
        db=self.connection()
        mycursor=db.cursor(dictionary=True)
        sq="select b.bname,b.bphone,b.price,b.track_no,p.payid,p.ord_id,p.paydate from payment p , book_shipment b where p.bid=b.bid and p.payid=%s"
        record =[payid]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        print("Fetched Rows from DB:", row)
        return row

    def user_details(self):
        db=self.connection()
        mycursor=db.cursor(dictionary=True)
        sq="select * from book_shipment order by bid desc limit 1"
        mycursor.execute(sq)
        row=mycursor.fetchone()
        return row
