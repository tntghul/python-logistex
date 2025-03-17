from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
from user import user_operation
from delivery import delivery_operation
from encryption import Encryption
from validate import myvalidate
from datetime import datetime
import razorpay


app=Flask(__name__)
app.secret_key='hdjdkeloejeldsvc45625'

client = razorpay.Client(auth=("rzp_test_PkxyeF1OLcy3d8", "anNC61WKeRqubB3e5oQIbDbK"))

# Sample in-memory store for delivery partner info (in a real scenario, use a database)
# delivery_partners = []

# Route to serve the HTML
@app.route("/delivery_login", methods=['GET', 'POST'])
def delivery_login():
    if request.method == 'POST':
        del_email = request.form.get('del_email')
        del_pswd = request.form.get('del_pswd')

        # Debugging ke liye print statements
        print(f"Email: {del_email}, Password: {del_pswd}")

        # Dummy authentication (Replace with DB check)
        if del_email == "del1" and del_pswd == "12345":
            session['del_email'] = del_email  # Session set karna
            return redirect(url_for('del_dashboard'))  # Redirect to dashboard
        else:
            flash("Invalid email or password!", "danger")  # Error message
            return redirect(url_for('delivery_login'))  # Wapas login page pe

    return render_template("delivery_login.html") 



@app.route('/del_dashboard')
def del_dashboard():
    ob = delivery_operation()
    records= ob.delivery()
    if 'del_email' not in session:
        return redirect(url_for('delivery_login'))  # Agar session nahi hai to wapas login page pe
    
    return render_template("del_dashboard.html",record=records)

@app.route('/login_all')
def login_all():
        
    ob = user_operation()
    records= ob.login_all(semail,spwd)
    return render_template("login_all.html",record=records)

@app.route("/pickup/<int:bid>", methods=["GET","POST"])
def pickup(bid):
    # Create an instance of delivery_operation
    ob = delivery_operation()
    if request.method == "GET":
    # Call the delivery method and pass the 'bid' to it
        records = ob.delivery_one(bid)

    # Return the template and pass the fetched records
        return render_template("pickup.html",bid=bid, record=records)

    if request.method == "POST":
        status = request.form["status"]
        currentStep = request.form["currentStep"]
        pickup_status = request.form['pickup_status']
        ob.pickup(bid,status,currentStep,pickup_status)
        return redirect(f"/pickup/{bid}")



@app.route('/drop/<int:bid>')
def drop(bid):
    ob = delivery_operation()
    record = ob.drop(bid)
    return render_template('drop.html', record=record)



@app.route("/delivery_update",methods=["GET","POST"])
def delivery_update():
    track_no = request.args.get("track_no")
    if track_no: 
        ob = delivery_operation()
        record = ob.get_delivery_status(track_no) 

        if record:
            return render_template("/delivery_update.html",record=record)
        else:
            return "Tracking number not found", 404

    return render_template("index.html")

# Route to retrieve all delivery partners (for testing purposes)
@app.route('/get_delivery_partners', methods=['GET'])
def get_delivery_partners():
    return jsonify(delivery_partners), 200


# Simulated order data
orders = {
    6152: {
        "currentStep": 0  # Default: "Order Processed"
    }
}

@app.route("/tracker", methods=["GET","POST"])
def tracker(bid):
    ob = delivery_operation()
    record = ob.get_delivery_status(bid)  # Fetch the status from the database
    return render_template("delivery_update.html", record=record)


# Endpoint for delivery partners to update order status
@app.route('/api/order-status/<int:track_no>', methods=['GET'])
def get_order_status(track_no):
    # Simulate fetching the current step index (e.g., from a database)
    status_data = {"currentStep": 2}  # 0-based index: 2 means "Order Shipped"
    return jsonify(status_data)

@app.route('/delivery_update/<int:track_no>')
def order_tracker(order_id):
    # Example data fetched from database or API
    record = {
        "track_no": order_id,
        "currentStep": 2,  # The current step of the order
        "expectedArrival": "01/06/20",
        "trackingCode": "V534HB"
    }
    
    # Pass the `record` dictionary to the template
    return render_template('delivery_update.html', record=record)

@app.route('/',methods=['GET','POST'])
def index():
    if(request.method=='GET'):
        return render_template("index.html")
    elif(request.method=='POST'):
        bname=request.form['bname']
        bemail=request.form['bemail']
        bphone=request.form['bphone']
        origin=request.form['origin']
        destination=request.form['destination']
        content=request.form['content']
        dpackage=request.form['dpackage']
        size=request.form['size']
        price=request.form['price']
        track_no=request.form['track_no']
        origin_p =request.form['origin_p']
        destination_p =request.form['destination_p']

        ob = user_operation()
        ob.book_shipment(bname,bemail,bphone,origin,destination,content,dpackage,size,price,track_no,origin_p,destination_p)


        flash("Message sent successfully!")
        return redirect(url_for('user_details'))
                   
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('index')) 

@app.route('/user_details', methods=["GET", "POST"])
def user_details():
    
    ob = user_operation()
    records= ob.user_details()
    return render_template("user_details.html",record=records)
 
@app.route('/payment',methods=['POST'])
def pay():
    if(request.method=='POST'):   
        bid = request.form.get('bid')
        price = request.form.get('price')

        # Debugging the received bid and price
        print(f"Received bid: {bid}, price: {price}")
        
        session['bid']=bid
        session['price']=price

        print(f"Session Bid: {session.get('bid')}, Session Price: {session.get('price')}")
        # Check if bid and price are not None or empty
        if not bid or not price:
            return "Error: Bid or price not found.", 400

        # Create a Razorpay order
        data = { "amount": int(price) * 100, "currency": "INR" }
        payment = client.order.create(data=data)
        pdata=[price*100, payment["id"]]

        print(f"Sending to HTML - Bid: {bid}, Price: {price}")

        return render_template(("payment.html"),pdata=pdata,bid=bid,price=price )

@app.route('/success')
def success():
    payid = request.args.get('payment_id')
    ord_id=request.args.get("order_id")
    sign=request.args.get("signature")
    bid = request.args.get('bid')
    price = request.args.get('price')
    print(f"Payment ID: {payid}, Order ID: {ord_id}, Signature: {sign}")
    print("data",bid)
    print("data",price)

    if not payid or not ord_id or not sign:
        return "Error: Missing payment ID, order ID, or signature", 400

    ob = user_operation()
    ob.payment(payid, ord_id) 
    r = ob.receipt(payid)

    return render_template('receipt.html', payment_id=payid, order_id=ord_id, signature=sign,receipt=r,bid=bid,price=price)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/who-we-are")
def page():
    return render_template("who-we-are.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/blog-details")
def blogdetails():
    return render_template("blog-details.html")

@app.route("/contact", methods=['GET','POST'])
def contact():
    if(request.method=='GET'):
        return render_template("contact.html")
    elif(request.method=='POST'):
        cname=request.form['cname']
        cemaill=request.form['cemaill']
        cphone=request.form['cphone']
        csubject=request.form['csubject']
        comment=request.form['comment']

        ob = user_operation()
        ob.contact(cname,cemaill,cphone,csubject,comment)
        flash("Message sent successfully!!")
        return redirect(url_for('index'))            
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('index')) 

@app.route('/debug')
def debug():
    return str(session) 


# admin

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    
    if(request.method=='GET'):
        return render_template("admin_login.html")
    elif(request.method=='POST'):
        semail = request.form['semail']
        spwd = request.form['spwd']
        print(semail)
        print(spwd)
        
        e = Encryption()
        spwdd = e.convert(spwd)
        print(spwdd)

        ob = user_operation()
        record=ob.login_all(semail)
        print(record)
        if record:
            email,pswd = record
            print ("Email:",email)
            print("Pswd:",pswd)
            print(record)

            if(semail==email and spwdd ==pswd):
                session['email']=email
                print(f"Session set: {session.get('email')}")
                print("success")
                
                return redirect(url_for('adminindex'))
            else:
                print("false")
                print(f"User entered: {semail} | {spwd}")
                
                print(f"Database returned: {email} | {pswd}")
                flash("invalid input!")
                return redirect(url_for('admin_login'))
            # return session['name']
        else:
            flash("invalid input!")
            return redirect(url_for('admin_login')) 
    flash("invalid input!")
    return redirect(url_for('admin_login'))


@app.route('/adminlogout')
def adminlogout():
    session.clear()  # Poora session clear kar do
    flash("Logged out successfully!")
    return redirect(url_for('admin_login'))

@app.route("/admin_signup",methods=['GET','POST'])
def admin_signup():
    if(request.method=='GET'):
        return render_template("admin_signup.html")
    elif(request.method=='POST'):
        sname=request.form['sname']
        semail=request.form['semail']
        sphone=request.form['sphone']
        spwd=request.form['spwd']

        e = Encryption()
        spwd = e.convert(spwd)

        ob = user_operation()
        ob.signup(sname,semail,sphone,spwd)

        flash("Message sent successfully!!")
        return redirect(url_for('admin_login'))            
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('index'))

@app.route("/adminindex")
def adminindex():
    if "email" not in session:
        return redirect(url_for("admin_login")) 
    ob = user_operation()
    records= ob.admincontact()
    return render_template("adminindex.html",record=records)  # Ensure this template exists


@app.route("/bookadmin")
def bookadmin():
    ob = user_operation()
    records= ob.bookadmin()
    return render_template("bookadmin.html",record=records)

@app.route("/adminprofile",methods=['GET','POST'])
def adminprofile():
    ob = user_operation()
    if request.method == "GET":
        semail = session.get('semail') 
    # Call the delivery method and pass the 'bid' to it
        records = ob.profile_one(semail)

    # Return the template and pass the fetched records
        return render_template("admin_profile.html",semail=semail , record=records)
    # elif request.method=='POST':
    #     sname = request.form['sname']
    #     sphone = request.form['sphone']
    #     spwd = request.form['spwd']
    #     ob = user_operation()
    #     ob.adminprofile(sname,sphone,spwd)

    #     return redirect(url_for('admin_profile'))
    # return render_template("admin_profile.html")

@app.route("/admincontact")
def admincontact():
    ob = user_operation()
    records= ob.admincontact()
    return render_template("admincontact.html",record=records)

@app.route("/deletebook/<int:bid>")
def delete_book(bid):
    ob = user_operation()
    ob.delete_book(bid)
    records = ob.bookadmin() 
    return render_template("bookadmin.html",record=records)

@app.route("/view_book/<int:bid>")
def view_book(bid):
    ob = user_operation()
    records = ob.view_book(bid)
    return render_template("view_book.html",record=records)

@app.route("/deletecontact/<int:id>")
def delete_contact(id):
    ob = user_operation()
    ob.delete_contact(id)
    records = ob.admincontact() 
    return render_template("admincontact.html",record=records)


@app.route('/admindelivery')
def admindelivery():
    ob = delivery_operation()
    records= ob.delivery()
    return render_template("admindelivery.html",record=records)

@app.route('/adminpayment')
def adminpayment():
    ob = delivery_operation()
    records= ob.payment()
    return render_template("adminpayment.html",record=records)

@app.route("/book_update/<int:bid>", methods=['GET', 'POST'])
def book_update(bid):
    ob = user_operation() 
    
    if request.method == 'GET':
        
        # Fetch the current details of the book for the given bid
        record = ob.get_book_by_id(bid) # Implement this method in `user_operation` to fetch book details
        if not record:
            return "Book not found.", 404  # Handle invalid `bid`

        # Render the form with the current book details
        return render_template('book_update.html', record=record)

    elif request.method == 'POST':
        # Handle form submission
        bname = request.form['bname']
        bemail = request.form['bemail']
        bphone = request.form['bphone']
        origin = request.form['origin']
        destination = request.form['destination']
        content = request.form['content']
        dpackage = request.form['dpackage']
        size = request.form['size']
        price = request.form['price']
        track_no = request.form['track_no']
        origin_p = request.form['origin_p']
        destination_p = request.form['destination_p']

        # Update the database
        
        ob.book_update(bid, bname, bemail, bphone, origin, destination, content, dpackage, size, price, track_no, origin_p, destination_p)


        # Fetch updated records for display
        updated_record = ob.get_book_by_id(bid)

        # Redirect to a success page or the admin view
        return render_template('book_update.html', record=updated_record)



if __name__=='__main__':
    app.run(debug=True)    