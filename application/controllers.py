from flask import Flask, render_template, redirect, request, flash
from flask import current_app as app 
from .models import *
from flask import request, session
import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf')
pdfkit.from_file('input.html', 'output.pdf', configuration=config)

from flask import session, redirect, url_for

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/userlogin')

@app.route('/user/<int:user_id>', methods=["GET","POST"])
def user(user_id):
    user=User.query.get(user_id)
    books = Book.query.all()
    book_details = []
    for book in books:
       section = book.section
       book_details.append({
            "id" : book.id,
            'name': book.name,
            'author': book.author,
            'section': section.name})
    return render_template('user_dashboard.html', username=user.username, book_details=book_details)


@app.route("/userlogin", methods=["GET", "POST"])
def user_login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        this_user=User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password ==password:
                session['user_id'] = this_user.id
                session['username'] = this_user.username
                session['logged_in'] = True
                if this_user.role=="admin":
                    return redirect('/librariandashboard')
                else:
                    return redirect(f'/user/{this_user.id}')
                
            else:
                return "incorrect Password"
        else:
            return "User does not Exist"

    return render_template('user_login.html')

@app.route("/userdashboard", methods=["GET", "POST"])
def user_dashboard():
    
    book_id = request.form.get('book_id')
    username=session.get("username")
    user_id = session.get('user_id')
    if request.method == "POST":
        
        if user_id is None:
            flash('User not logged in.', 'error')
            return redirect('/userlogin')
    
        new_request = Request( 
            user_id = user_id, 
            book_id = book_id, 
            request_date = datetime.utcnow(),
            return_date = Request.get_default_return_date())
        db.session.add(new_request)
        db.session.commit()
        flash('Book request submitted successfully.', 'success')
        return redirect('/user/' + str(user_id))
    return render_template('user_dashboard.html', username=username, user_id=user_id, book_id=book_id)


@app.route("/userregister", methods=["GET", "POST"])
def user_register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        this_user=User.query.filter_by(username=username).first()
        if this_user:
            return "User already exists!"
        else:
            new_user=User(username = username, password= password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/userlogin")
    return render_template('user_register.html')


@app.route("/sectionmanagement", methods=["GET", "POST"])
def section_management():
    librarian_id = session.get('librarian_id')
    sections = Section.query.all()
    
    if request.method == "POST":
        librarian_id = request.form.get('librarian_id')
        section_name = request.form.get("section_name")
        date_str = request.form.get("date_created") 
        description = request.form.get("description")
        if date_str:  
            date_created = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            date_created = None
        image = request.files.get("image")
        if image:
            image.save("uploads/" + image.filename)
        new_section = Section(name=section_name, date_created=date_created, description=description, librarian_id=librarian_id)
        db.session.add(new_section)
        db.session.commit()
        return redirect("/addsections?librarian_id=" + str(librarian_id))
    return render_template("section_management.html", sections=sections, librarian_id=librarian_id)

@app.route("/addsections", methods=["GET", "POST"])
def add_sections():
    sections = Section.query.all()
    if request.method == "POST":
        section_id = request.form.get("section_id")
        if section_id:
            session['section_id'] = section_id
            return redirect("/bookmanagement") 
    return render_template("add_sections.html", sections=sections)



@app.route("/edit_section_page", methods=["GET"])
def edit_section_page():
    section_id = request.args.get("section_id")
    section = Section.query.get(section_id)
    return render_template("edit_section.html", section_id=section_id, section_name=section.name, description=section.description)

@app.route("/update_section", methods=["POST"])
def update_section():
    if request.method == "POST":
        section_id = request.form.get("section_id")
        new_section_name = request.form.get("section_name")
        new_description = request.form.get("description")
        section = Section.query.get(section_id)
        section.name = new_section_name
        section.description = new_description
        db.session.commit()
        return redirect("/addsections")

@app.route("/delete_section", methods=["POST"])
def delete_section():
    if request.method == "POST":
        section_id = request.form.get("section_id")
        section = Section.query.get(section_id)
        db.session.delete(section)
        db.session.commit()
        return redirect("/addsections")

@app.route("/edit_book_page", methods=["GET"])
def edit_book_page():
    book_id = request.args.get("book_id")
    section_id = request.args.get("section_id")
    #section=Section.query.get("section_id")
    book = Book.query.get(book_id)
    return render_template("edit_book.html", book=book,section_id=section_id, content=book.content)

@app.route("/update_book", methods=["POST"])
def update_book():
    if request.method == "POST":
        book_id = request.form.get("book_id")
        section_id = request.form.get("section_id")
        new_book_name = request.form.get("book_name")
        new_content = request.form.get("content")
        new_author = request.form.get("author")
        # Update the section in the database
        book = Book.query.get(book_id)
        book.name = new_book_name
        book.content= new_content
        book.author=new_author
        db.session.commit()
        return redirect(url_for("book_details", section_id=section_id))
      

@app.route("/delete_book", methods=["POST"])
def delete_book():
    if request.method == "POST":
        book_id = request.form.get("book_id")
        section_id = request.form.get("section_id")
        # Delete the section from the database
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for("book_details", section_id=section_id))


@app.route("/bookdetails", methods=["GET", "POST"])
def book_details():
    section_id = request.args.get("section_id")
    section=Section.query.get(section_id)
    books = Book.query.filter_by(section_id=section_id).all()
    return render_template("book_details.html", books=books, section=section, section_id=section_id)

@app.route("/bookmanagement", methods=["GET", "POST"])
def book_management():
    section_id=session.get("section_id")
    books = Book.query.all()
    if request.method == "POST":
        book_name = request.form.get("book")
        author=request.form.get("author")
        date_str = request.form.get("date") 
        date = datetime.strptime(date_str, '%Y-%m-%d') 
        content= request.form.get("content")
        image = request.files.get("image")
        if image:
            image.save("uploads/" + image.filename)
        if section_id is not None:
            new_book = Book(name=book_name, date_issued=date,content=content, section_id=section_id, author=author)
            db.session.add(new_book)
            db.session.commit()
            return redirect("/bookdetails?section_id=" + str(section_id))
        else:
            return "Section ID not found", 400
    return render_template("book_management.html", books=books, section_id=section_id)



@app.route("/librarianlogin", methods=["GET", "POST"])
def librarian_login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        librarian = User.query.filter_by(username=username, password=password, role="admin").first()
      
        if librarian:
            session['librarian_id'] = librarian.id
            return redirect("/librariandashboard") 
    return render_template('librarian_login.html')

@app.route("/librariandashboard", methods=["GET", "POST"])
def librarian_dashboard():
    return render_template('librarian_dashboard.html')


@app.route("/librarianbooks", methods=["GET", "POST"])
def librarian_books():
    librarian=User.query.filter_by(role="admin").first()
    requested_books = Request.query.filter_by(status="requested").all()
    issued_books = Request.query.filter_by(status="issued").all()
    
    requested_books_details = []
    issued_books_details = []

    for request in requested_books:
        #user = request.user
        book = request.book
        section = book.section
        requested_books_details.append({
            "request_id":request.id,
            "book_id":book.id,
            'user':request.user.id,
            'book_title': book.name,
            'section': section.name})
    for request in issued_books:
        book = request.book
        section = book.section
        issued_books_details.append({
            "request_id":request.id,
            "book_id":book.id,
            'user': request.user.id,
            'book_title': book.name,
            'section': section.name})
    return render_template('librarian_books.html', requested_books=requested_books_details,
     issued_books=issued_books_details,librarian=librarian)

@app.route("/userbooks", methods=["GET", "POST"])
def user_books():
    user_id = session.get('user_id')
    username=session.get("username")
    requested_books = Request.query.filter_by(status="requested").all()
    rejected_books = Request.query.filter_by(status="rejected").all()
    issued_books = Request.query.filter_by(status="issued").all()
    paid_books = Request.query.filter_by(status="paid").all()
    
    requested_books_details = []
    issued_books_details = []
    paid_books_details=[]

    for request in requested_books:
        
        book = request.book
        section = book.section
        status = request.status
        requested_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author':book.author,
            'section': section.name,
            "status": status})
    for request in rejected_books:
        
        book = request.book
        section = book.section
        status = request.status
        requested_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author':book.author,
            'section': section.name,
            "status": status})
    for request in issued_books:
        book = request.book
        section = book.section
        issued_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author':book.author,
            'section': section.name})
    for request in paid_books:
        book = request.book
        section = book.section
        paid_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author':book.author,
            'section': section.name})
    return render_template('user_books.html', requested_books=requested_books_details,username=username,
     issued_books=issued_books_details,paid_books=paid_books_details, user_id=user_id, status=status)


@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        book_id = request.form.get('book_id')
        
        if user_id is None:
            flash('User not logged in.', 'error')
            return redirect('/userlogin')

        book_request = Request.query.filter_by(user_id=user_id, book_id=book_id, status='requested').first()
        if book_request:
            book_request.status = 'paid'
            db.session.commit()
            flash('Payment successful. Book request is now paid.', 'success')
        else:
            flash('No requested book found for payment.', 'error')

        return redirect('/userbooks')
    
    username = session.get("username")
    user_id = session.get('user_id')
    book_id = request.args.get('book_id')
    book = Book.query.get(book_id)
    
    return render_template('payment.html', username=username, user_id=user_id, book_id=book_id,book=book)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    username = session.get("username")
    user_id = session.get('user_id')
    book_id = request.args.get('book_id')
    feedback = None  
    rating = None
    
    if request.method == "POST":
        user_id = request.form.get('user_id')
        book_id = request.form.get('book_id')
        rating = int(request.form['rating'])
        comment = request.form['comment']
         
        feedback = Feedback(user_id=user_id, book_id=book_id, rating=rating, comment=comment)
        db.session.add(feedback)
        db.session.commit()

        rating_entry = Rating.query.filter_by(user_id=user_id, book_id=book_id).first()
        if rating_entry:
            rating_entry.rating = rating
        else:
            rating_entry = Rating(user_id=user_id, book_id=book_id, rating=rating)
            db.session.add(rating_entry)
        db.session.commit()

        flash('Thank you for your feedback!', 'success')
        return redirect("/userbooks")
    return render_template('feedback.html', username=username,
     user_id=user_id, book_id=book_id, 
     feedback=feedback,rating=rating)



@app.route("/cancel_request/<int:book_id>", methods=["POST"])
def cancel_request(book_id):
    if request.method == "POST":
        request_to_cancel = Request.query.filter_by(book_id=book_id).first()
        if request_to_cancel:
            db.session.delete(request_to_cancel)
            db.session.commit()
            flash("Request canceled successfully", "success")
        else:
            flash("Request not found", "error")
        return redirect("/userbooks")

@app.route("/review", methods=["GET", "POST"])
def review():
    request_id = request.args.get('request_id')
    this_request = Request.query.get(request_id)
    
    if request.method == "POST":
        action = request.form.get("action")
        if action == "issue":
            this_request.status = "issued"
            db.session.commit()
            flash("Request issued successfully", "success")
        elif action == "reject":
            this_request.status = "rejected"
            db.session.commit()
            flash("Request rejected successfully", "success")
        return redirect("/librarianbooks")
    return render_template('review.html', this_request=this_request)

@app.route("/view_book_content")
def view_book_content():
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    return render_template("book_content.html", book=book)



@app.route("/revoke_request/<int:request_id>", methods=["POST"])
def revoke_request(request_id):
    if request.method == "POST":
        request_to_revoke = Request.query.get(request_id)
        if request_to_revoke:
            db.session.delete(request_to_revoke)
            db.session.commit()
            flash("Request revoked successfully", "success")
        else:
            flash("Request not found", "error")
        return redirect("/librarianbooks")

import pdfkit

#@app.route("/generate_pdf")
#def generate_pdf():
    #book_id = request.args.get("book_id")
    #book = Book.query.get_or_404(book_id)
    #rendered_html = render_template("book_content.html", book=book)
    #pdf_filename = f"{book.name}.pdf"
   #pdfkit.from_string(rendered_html, pdf_filename)
    #return send_file(pdf_filename, attachment_filename=pdf_filename, as_attachment=True)
@app.route("/generate_pdf")
def generate_pdf():
    book_id = request.args.get("book_id")
    book = Book.query.get_or_404(book_id)
    rendered_html = render_template("book_content.html", book=book)
    pdf = pdfkit.from_string(rendered_html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={book.name}.pdf'
    return response
