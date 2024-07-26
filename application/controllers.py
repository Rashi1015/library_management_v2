from flask import render_template, redirect, flash, url_for, make_response, request, session
from flask import current_app as app 
from application.models import *
import pdfkit
from sqlalchemy import func, or_
from flask_security import hash_password, auth_required, roles_accepted, current_user
import uuid
from .sec import user_datastore


config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def create_view(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/userlogin')

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
                    return redirect('/userdashboard')
                
            else:
                return "incorrect Password"
        else:
            return "User does not Exist"

        return render_template('user_login.html')

    @app.route('/userregister', methods=['GET', 'POST'])
    def user_register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
        # Generate a unique fs_uniquifier
            fs_uniquifier = str(uuid.uuid4())
        # Create the user
            user_datastore.create_user(
                username=username, 
                password=hash_password(password),
                active=True,
                fs_uniquifier=fs_uniquifier,
                roles=['user']  
        )
            db.session.commit()
            return redirect("/userlogin")
        return render_template('user_register.html')


    @app.route('/userdashboard', methods=["GET", "POST"])
    @auth_required('session', 'token')
    def user_dashboard():
        user_id = session.get('user_id')
        username = session.get('username')
        if not user_id or not username:
            flash('Please log in to access your dashboard.', 'warning')
            return redirect('/userlogin') 
            search_word = request.args.get('search_word', '')
        if search_word:
            search_word = "%" + search_word + "%"
            books_by_name = Book.query.filter(Book.name.ilike(search_word)).all()
            books_by_author = Book.query.filter(Book.author.ilike(search_word)).all()
            books_by_section = Book.query.join(Section).filter(Section.name.ilike(f'%{search_word}%')).all()
            books = books_by_name + books_by_author + books_by_section
        else:
            books = Book.query.all()
    
        book_details = []
        for book in books:
            section = book.section
            book_details.append({
            "id": book.id,
            'name': book.name,
            'author': book.author,
            'section': section.name
        })
    
        if request.method == "POST":
            requested_books_count = Request.query.filter_by(user_id=user_id, status='requested').count()
            issued_books_count = Request.query.filter_by(user_id=user_id, status='issued').count()
            total_books_count = requested_books_count + issued_books_count

            if total_books_count >= 5:
                flash('You cannot have more than 5 books in requested or issued status.', 'warning')

            else:
                book_id = request.form.get('book_id')
                new_request = Request(
                   user_id=user_id,
                book_id=book_id,
                request_date=datetime.utcnow(),
                return_date=Request.get_default_return_date()
            )
                db.session.add(new_request)
                db.session.commit()
                flash('Book request submitted successfully.', 'success')
                return redirect('/userbooks') 

        return render_template('user_dashboard.html', username=username,  book_details=book_details, search_word=search_word)

create_view(app)

@app.route("/userbooks", methods=["GET", "POST"])
def user_books():
    if 'user_id' not in session:
        flash('User not logged in.', 'error')
        return redirect('/userlogin')
    
    user_id = session.get('user_id')
    username = session.get("username")
    
    search_word = request.args.get('search_word', '')

    if search_word:
        requested_books = Request.query.filter(
            Request.user_id == user_id,
            Request.status.in_(['requested']),
            (Request.book.has(Book.name.ilike(f'%{search_word}%')) |
             Request.book.has(Book.author.ilike(f'%{search_word}%')) |
             Request.book.has(Book.section.has(Section.name.ilike(f'%{search_word}%'))))
        ).all()
        
        rejected_books = Request.query.filter(
            Request.user_id == user_id,
            Request.status.in_(['rejected']),
            (Request.book.has(Book.name.ilike(f'%{search_word}%')) |
             Request.book.has(Book.author.ilike(f'%{search_word}%')) |
             Request.book.has(Book.section.has(Section.name.ilike(f'%{search_word}%'))))
        ).all()

        issued_books = Request.query.filter(
            Request.user_id == user_id,
            Request.status == 'issued',
            (Request.book.has(Book.name.ilike(f'%{search_word}%')) |
             Request.book.has(Book.author.ilike(f'%{search_word}%')) |
             Request.book.has(Book.section.has(Section.name.ilike(f'%{search_word}%'))))
        ).all()

        paid_books = Request.query.filter(
            Request.user_id == user_id,
            Request.status == 'paid',
            (Request.book.has(Book.name.ilike(f'%{search_word}%')) |
             Request.book.has(Book.author.ilike(f'%{search_word}%')) |
             Request.book.has(Book.section.has(Section.name.ilike(f'%{search_word}%'))))
        ).all()
    else:
        requested_books = Request.query.filter_by(user_id=user_id, status="requested").all()
        rejected_books = Request.query.filter_by(user_id=user_id, status="rejected").all()
        issued_books = Request.query.filter_by(user_id=user_id, status="issued").all()
        paid_books = Request.query.filter_by(user_id=user_id, status="paid").all()

    requested_books_details = []
    issued_books_details = []
    paid_books_details = []

    for req in requested_books:
        book = req.book
        section = book.section
        status = req.status
        requested_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author': book.author,
            'section': section.name,
            "status": status
        })
    
    for req in rejected_books:
        book = req.book
        section = book.section
        status = req.status
        requested_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author': book.author,
            'section': section.name,
            "status": status
        })


    for req in issued_books:
        book = req.book
        section = book.section
        issued_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author': book.author,
            'section': section.name
        })

    for req in paid_books:
        book = req.book
        section = book.section
        paid_books_details.append({
            'book_id': book.id,
            'book_title': book.name,
            'author': book.author,
            'section': section.name
        })

    return render_template('user_books.html', requested_books=requested_books_details, 
                           username=username, issued_books=issued_books_details,
                           rejected_books=requested_books_details,
                           paid_books=paid_books_details, user_id=user_id, search_word=search_word)


@app.route("/userstats", methods=["GET", "POST"])
def user_stats():
    user_id = session.get('user_id')

    requested_count = Request.query.filter_by(user_id=user_id, status="requested").count()
    rejected_count = Request.query.filter_by(user_id=user_id, status="rejected").count()
    issued_count = Request.query.filter_by(user_id=user_id, status="issued").count()
    paid_count = Request.query.filter_by(user_id=user_id, status="paid").count()

    # Render the template with the statistics
    return render_template('user_stats.html', user_id=user_id,
                           requested_count=requested_count, rejected_count=rejected_count,
                           issued_count=issued_count, paid_count=paid_count)



@app.route("/sectionmanagement", methods=["GET", "POST"])
@roles_accepted('admin')
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
@roles_accepted('admin')
def add_sections():
    search_word = request.args.get('search_word', '')
    
    if search_word:
        sections = Section.query.filter(
            Section.name.ilike(f'%{search_word}%') |
            Section.description.ilike(f'%{search_word}%')
        ).all()
    else:
        sections = Section.query.all()
        
    if request.method == "POST":
        section_id = request.form.get("section_id")
        if section_id:
            session['section_id'] = section_id
            return redirect("/bookmanagement")
    
    return render_template("add_sections.html", sections=sections, search_word=search_word)




@app.route("/edit_section_page", methods=["GET"])
@roles_accepted('admin')
def edit_section_page():
    section_id = request.args.get("section_id")
    section = Section.query.get(section_id)
    return render_template("edit_section.html", section_id=section_id, section_name=section.name, description=section.description)

@app.route("/update_section", methods=["POST"])
@roles_accepted('admin')
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
@roles_accepted('admin')
def delete_section():
    if request.method == "POST":
        section_id = request.form.get("section_id")
        section = Section.query.get(section_id)
        db.session.delete(section)
        db.session.commit()
        return redirect("/addsections")

@app.route("/edit_book_page", methods=["GET"])
@roles_accepted('admin')
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
            if librarian.password == password:
                session['librarian_id'] = librarian.id
                session['username'] = librarian.username
                session['logged_in'] = True
                return redirect("/librariandashboard")
            else:
                return "incorrect Password" 
        else:
            return "Librarian does not Exist!"
    return render_template('librarian_login.html')

@app.route("/librariandashboard", methods=["GET", "POST"])
def librarian_dashboard():
    return render_template('librarian_dashboard.html')


@app.route("/librarianbooks", methods=["GET", "POST"])
def librarian_books():
    librarian = User.query.filter_by(role="admin").first()
    search_word = request.args.get('search_word', '')

    if search_word:
        requested_books = Request.query.join(Book).join(Section).filter(
            Request.status == 'requested',
            (Book.name.ilike(f'%{search_word}%') | 
             Section.name.ilike(f'%{search_word}%') |
             User.username.ilike(f'%{search_word}%'))
        ).all()
        issued_books = Request.query.join(Book).join(Section).filter(
            Request.status == 'issued',
            (Book.name.ilike(f'%{search_word}%') | 
             Section.name.ilike(f'%{search_word}%') |
             User.username.ilike(f'%{search_word}%'))
        ).all()
    else:
        requested_books = Request.query.filter_by(status="requested").all()
        issued_books = Request.query.filter_by(status="issued").all()

    requested_books_details = []
    issued_books_details = []

    for req in requested_books:
        book = req.book
        section = book.section
        requested_books_details.append({
            "request_id": req.id,
            "book_id": book.id,
            "user": req.user_id,
            "book_title": book.name,
            "section": section.name
        })

    for req in issued_books:
        book = req.book
        section = book.section
        issued_books_details.append({
            "request_id": req.id,
            "book_id": book.id,
            "user": req.user_id,
            "book_title": book.name,
            "section": section.name
        })
    
    return render_template('librarian_books.html', requested_books=requested_books_details,
                           issued_books=issued_books_details, librarian=librarian, search_word=search_word)

#@app.route('/', methods=['GET', 'POST'])
#def index():
    if request.method == 'POST':
        search_word = request.form.get('search_word', '')
        return redirect(url_for('search_results', search_word=search_word))
    return render_template('librarian_books.html')  

#@app.route('/search_results')
#def search_results():
    search_word = request.args.get('search_word', '')
    
    # Perform search across relevant entities (example: User, Book, etc.)
    users = User.query.filter(User.username.ilike(f'%{search_word}%')).all()
    books = Book.query.filter(Book.name.ilike(f'%{search_word}%')).all()
    sections = Section.query.filter(Section.name.ilike(f'%{search_word}%')).all()
    requests = Request.query.filter(Request.status == 'requested').all()  # Example filter condition
    
    return render_template('librarian_books.html', users=users, books=books, sections=sections, requests=requests, search_word=search_word)



#@app.route('/librariansearch')
#def text_search_L():
    
    search_word = request.args.get("search_word")
    search_word = "%" + search_word + "%"
    
    # Search requests by book name
    requests_by_name = Request.query \
        .join(Book) \
        .filter(Book.name.like(f'%{search_word}%')) \
        .filter(or_(Request.status == 'requested', Request.status == 'issued')) \
        .all()
    
    # Search requests by section name
    requests_by_section = Request.query \
        .join(Book) \
        .join(Section) \
        .filter(Section.name.like(f'%{search_word}%')) \
        .filter(or_(Request.status == 'requested', Request.status == 'issued')) \
        .all()

    # Combine and remove duplicates
    requests = requests_by_name + requests_by_section
    
    return render_template('librarian_search.html', requests=requests)


@app.route("/librarianstats")
def librarian_stats():
    
    requested_count = Request.query.filter_by(status="requested").count()
    issued_count = Request.query.filter_by(status="issued").count()

    return render_template('librarian_stats.html', requested_count=requested_count, issued_count=issued_count)

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
            if datetime.utcnow() > request_to_revoke.return_date:
                db.session.delete(request_to_revoke)
                db.session.commit()
               
            else:
                db.session.delete(request_to_revoke)
                db.session.commit()
                flash("Request revoked successfully", "success")
        else:
            flash("Request not found", "error")
        return redirect("/librarianbooks")

@app.route("/generate_pdf")
def generate_pdf():
    book_id = request.args.get("book_id")
    book = Book.query.get_or_404(book_id)
    rendered_html = render_template("view_pdf.html", book=book)
    pdf = pdfkit.from_string(rendered_html, False, configuration=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'))
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={book.name}.pdf'
    return response
