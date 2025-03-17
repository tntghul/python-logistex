import mysql.connector
from flask import session

class delivery_operation:
    def connection(self):
        con=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="logixstic")
        return con

    def delivery(self):
        db = self.connection()  # Establish database connection
        mycursor = db.cursor()
        sq = "SELECT * FROM delivery"
        mycursor.execute(sq)
        row=mycursor.fetchall()
        return row
        
    def payment(self):
        db = self.connection()  # Establish database connection
        mycursor = db.cursor()
        sq = "SELECT * FROM payment"
        mycursor.execute(sq)
        row=mycursor.fetchall()
        return row

    def delivery_one(self,bid):
        db = self.connection() 
        mycursor = db.cursor()
        sq = "SELECT * FROM delivery where bid = %s"
        mycursor.execute(sq,(bid,))
        row=mycursor.fetchone()
        return row

    def pickup(self,bid,status,currentStep,pickup_status):
        db = self.connection() 
        mycursor=db.cursor()
        
        sq = "UPDATE delivery SET status = %s, currentStep= %s,pickup_status =%s WHERE bid = %s"
        
        mycursor.execute(sq,(status,currentStep,pickup_status,bid))
        db.commit()
        mycursor.close()
        db.close()
        session['bid']=bid
        return

    def get_delivery_status(self,track_no):
        db = self.connection()
        mycursor = db.cursor(dictionary=True)
        mycursor.execute("SELECT track_no AS orderNumber, status, currentStep FROM delivery WHERE track_no=%s ",(track_no,))
        record = mycursor.fetchone()
        return record
        cursor.close()
        db.close()

    def drop(self,bid):
        db = self.connection() 
        mycursor=db.cursor()
        
        sq = "SELECT * FROM book_shipment WHERE bid = %s"
        
        mycursor.execute(sq,(bid))
        db.commit()
        mycursor.close()
        db.close()
        session['bid']=bid
        return