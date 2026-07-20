import os


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    abort,
    send_file
)


from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)


from werkzeug.utils import secure_filename


from werkzeug.security import (
    generate_password_hash
)


from sqlalchemy import func


from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table
)

from reportlab.lib.styles import getSampleStyleSheet



from config import config


from models import (
    db,
    User,
    Document,
    Result,
    Report
)


from utils.validators import (
    allowed_file,
    validate_user_input
)


from utils.pdf_reader import extract_text


from ai.plagiarism import (
    check_plagiarism_against_db
)



# =====================================
# CREATE FLASK APP
# =====================================


app = Flask(__name__)


env = os.environ.get(
    "FLASK_ENV",
    "default"
)


app.config.from_object(
    config[env]
)
# Admin Secret Key
app.config["ADMIN_SECRET_KEY"] = "SHIVU@2026"


# Maximum upload size 16MB

app.config["MAX_CONTENT_LENGTH"] = (
    16 * 1024 * 1024
)



# =====================================
# DATABASE INITIALIZATION
# =====================================


# =====================================
# DATABASE INITIALIZATION
# =====================================

db.init_app(app)


# Create database tables automatically
with app.app_context():

    db.create_all()

    print("✓ Database tables created")


# =====================================
# LOGIN MANAGER
# =====================================


login_manager = LoginManager()


login_manager.init_app(app)


login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )



# =====================================
# FOLDERS
# =====================================


os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


os.makedirs(
    os.path.join(
        app.config["UPLOAD_FOLDER"],
        "pdfs"
    ),
    exist_ok=True
)


os.makedirs(
    os.path.join(
        app.config["UPLOAD_FOLDER"],
        "documents"
    ),
    exist_ok=True
)


os.makedirs(
    app.config["REPORTS_FOLDER"],
    exist_ok=True
)




# =====================================
# TEMPLATE DATE
# =====================================


@app.context_processor
def inject_now():

    from datetime import datetime

    return {
        "now": datetime.utcnow()
    }



# =====================================
# HOME PAGE
# =====================================


@app.route("/")
def index():


    if current_user.is_authenticated:


        if current_user.role == "Admin":

            return redirect(
                url_for(
                    "admin_dashboard"
                )
            )


        elif current_user.role == "Faculty":

            return redirect(
                url_for(
                    "faculty_dashboard"
                )
            )


        else:

            return redirect(
                url_for(
                    "student_dashboard"
                )
            )


    return render_template(
        "index.html"
    )



# =====================================
# REGISTER
# =====================================


@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        admin_key = request.form.get("admin_key")

        # Validate role
        if role not in ["Student", "Faculty", "Admin"]:
            flash("Invalid role selected.", "danger")
            return render_template("register.html")

        # Validate Admin Secret Key
        if role == "Admin":
            if admin_key != app.config["ADMIN_SECRET_KEY"]:
                flash("Invalid Admin Secret Key.", "danger")
                return render_template("register.html")

        # Validate user input
        valid, msg = validate_user_input(
            name,
            email,
            password
        )

        if not valid:
            flash(msg, "danger")
            return render_template("register.html")

        # Check existing email
        exists = User.query.filter_by(
            email=email
        ).first()

        if exists:
            flash(
                "Email already registered",
                "danger"
            )
            return render_template("register.html")

        # Create new user
        user = User(
            fullname=name,
            email=email,
            role=role,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =====================================
# LOGIN
# =====================================


@app.route(
    "/login",
    methods=["GET","POST"]
)

def login():


    if request.method=="POST":


        email=request.form.get(
            "email"
        )


        password=request.form.get(
            "password"
        )



        user=User.query.filter_by(
            email=email
        ).first()



        if user and user.check_password(password):


            login_user(user)



            if user.role=="Admin":

                return redirect(
                    url_for(
                        "admin_dashboard"
                    )
                )


            elif user.role=="Faculty":

                return redirect(
                    url_for(
                        "faculty_dashboard"
                    )
                )


            else:

                return redirect(
                    url_for(
                        "student_dashboard"
                    )
                )



        flash(
            "Invalid email or password",
            "danger"
        )



    return render_template(
        "login.html"
    )



# =====================================
# LOGOUT
# =====================================


@app.route("/logout")
@login_required

def logout():

    logout_user()


    flash(
        "Logged out successfully",
        "info"
    )


    return redirect(
        url_for("index")
    )



# =====================================
# UPLOAD DOCUMENT
# =====================================


@app.route(
    "/upload",
    methods=["GET","POST"]
)
@login_required
def upload():


    # Only Student and Faculty

    if current_user.role not in [
        "Student",
        "Faculty"
    ]:

        flash(
            "Access denied",
            "danger"
        )

        return redirect(
            url_for("login")
        )



    if request.method=="POST":


        if "file" not in request.files:


            flash(
                "No file selected",
                "danger"
            )

            return redirect(
                request.url
            )



        file=request.files["file"]



        if file.filename=="":


            flash(
                "Please select a file",
                "danger"
            )

            return redirect(
                request.url
            )



        if not allowed_file(
            file.filename
        ):


            flash(
                "Only PDF, DOCX and TXT allowed",
                "danger"
            )


            return redirect(
                request.url
            )



        try:



            filename=secure_filename(
                file.filename
            )



            extension=filename.rsplit(
                ".",
                1
            )[1].lower()



            if extension=="pdf":


                folder=os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    "pdfs"
                )


            else:


                folder=os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    "documents"
                )



            os.makedirs(
                folder,
                exist_ok=True
            )



            filepath=os.path.join(
                folder,
                filename
            )



            # avoid duplicate file names

            count=1


            while os.path.exists(filepath):


                name,ext=os.path.splitext(
                    filename
                )


                filename=f"{name}_{count}{ext}"


                filepath=os.path.join(
                    folder,
                    filename
                )


                count+=1




            file.save(filepath)




            # Extract text

            text=extract_text(
                filepath
            )



            if not text:


                flash(
                    "Text extraction failed",
                    "danger"
                )


                return redirect(
                    request.url
                )




            document=Document(

                user_id=current_user.id,

                filename=filename,

                extracted_text=text

            )



            db.session.add(document)

            db.session.commit()




            # plagiarism check

            result=check_plagiarism_against_db(
                document
            )



            # save report


            report=Report(

                user_id=current_user.id,

                filename=filename,

                plagiarism_score=result.plagiarism_percentage,

                ai_score=getattr(
                    result,
                    "ai_score",
                    0
                ),

                similarity_score=getattr(
                    result,
                    "similarity_score",
                    0
                ),

                matched_file=(

                    result.document2.filename

                    if getattr(
                        result,
                        "document2",
                        None
                    )

                    else "No Match"

                ),


                report_path=getattr(
                    result,
                    "report_path",
                    None
                )

            )



            db.session.add(report)


            db.session.commit()




            flash(

                f"Upload successful | "
                f"Plagiarism: "
                f"{result.plagiarism_percentage:.2f}%",

                "success"

            )




            if current_user.role=="Student":


                return redirect(
                    url_for(
                        "student_dashboard"
                    )
                )


            else:


                return redirect(
                    url_for(
                        "faculty_dashboard"
                    )
                )



        except Exception as e:


            db.session.rollback()


            flash(
                f"Upload Error : {str(e)}",
                "danger"
            )


            return redirect(
                request.url
            )



    return render_template(
        "upload.html"
    )





# =====================================
# STUDENT DASHBOARD
# =====================================


@app.route(
    "/student_dashboard"
)

@login_required
def student_dashboard():



    if current_user.role!="Student":


        flash(
            "Access denied",
            "danger"
        )


        return redirect(
            url_for("login")
        )




    total_docs=Document.query.filter_by(

        user_id=current_user.id

    ).count()




    results=(

        Result.query

        .join(
            Document,
            Result.document1_id==Document.id
        )

        .filter(
            Document.user_id==current_user.id
        )

        .all()

    )



    total_results=len(results)




    if total_results:


        avg_plagiarism=round(

            sum(

                r.plagiarism_percentage

                for r in results

            )

            /
            total_results,

            2

        )


    else:

        avg_plagiarism=0




    return render_template(

        "student_dashboard.html",

        total_docs=total_docs,

        total_results=total_results,

        avg_plagiarism=avg_plagiarism

    )






# =====================================
# FACULTY DASHBOARD
# =====================================


@app.route(
    "/faculty_dashboard"
)

@login_required

def faculty_dashboard():



    if current_user.role!="Faculty":


        flash(
            "Access denied",
            "danger"
        )


        return redirect(
            url_for("login")
        )




    search=request.args.get(
        "search",
        ""
    )




    if search:


        students=User.query.filter(

            User.role=="Student",

            (

                User.fullname.ilike(
                    f"%{search}%"
                )

                |

                User.email.ilike(
                    f"%{search}%"
                )

            )

        ).all()



    else:


        students=User.query.filter_by(

            role="Student"

        ).all()





    total_students=User.query.filter_by(

        role="Student"

    ).count()




    total_documents=Document.query.count()



    total_reports=Report.query.count()




    avg_plagiarism=db.session.query(

        func.avg(
            Report.plagiarism_score
        )

    ).scalar()



    if avg_plagiarism is None:

        avg_plagiarism=0





    faculty_reports=Report.query.order_by(

        Report.upload_date.desc()

    ).all()





    return render_template(

        "faculty_dashboard.html",

        students=students,

        total_students=total_students,

        total_documents=total_documents,

        total_reports=total_reports,

        avg_plagiarism=round(
            avg_plagiarism,
            2
        ),

        faculty_reports=faculty_reports

    )

# =====================================
# ANALYTICS
# =====================================

@app.route("/analytics")
@login_required
def analytics():

    if current_user.role != "Faculty":

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    total_students = User.query.filter_by(
        role="Student"
    ).count()


    total_documents = Document.query.count()


    total_checks = Result.query.count()


    avg_plagiarism = db.session.query(
        func.avg(Result.plagiarism_percentage)
    ).scalar() or 0


    student_data = (
        db.session.query(
            User.fullname,
            func.avg(Result.plagiarism_percentage)
        )
        .join(
            Document,
            User.id == Document.user_id
        )
        .join(
            Result,
            Document.id == Result.document1_id
        )
        .group_by(User.id)
        .all()
    )


    student_names = []
    student_scores = []


    for name, score in student_data:

        student_names.append(name)

        student_scores.append(
            round(score or 0, 2)
        )


    return render_template(

        "analytics.html",

        total_students=total_students,

        total_documents=total_documents,

        total_checks=total_checks,

        avg_plagiarism=round(
            avg_plagiarism,
            2
        ),

        student_names=student_names,

        student_scores=student_scores

    )



# =====================================
# VIEW REPORT
# =====================================

@app.route("/report/<int:result_id>")
@login_required
def report(result_id):

    result = Result.query.get_or_404(
        result_id
    )


    # Students can only view their own reports.
    # Faculty and Admin can view all reports.

    if current_user.role == "Student":

        if result.document1.user_id != current_user.id:
            abort(403)

    elif current_user.role not in [
        "Faculty",
        "Admin"
    ]:

        abort(403)


    from ai.plagiarism import (
        find_matching_paragraphs
    )

    from utils.helper import (
        highlight_text
    )


    matching_paragraphs = []


    highlighted_text = (
        result.document1.extracted_text
    )


    if result.document2:


        matching_paragraphs = (
            find_matching_paragraphs(
                result.document1.extracted_text,
                result.document2.extracted_text
            )
        )


        source_paragraphs = [

            paragraph["source_paragraph"]

            for paragraph in matching_paragraphs

        ]


        highlighted_text = highlight_text(

            result.document1.extracted_text,

            source_paragraphs

        )


    return render_template(

        "report.html",

        result=result,

        highlighted_text=highlighted_text,

        matching_paragraphs=matching_paragraphs

    )

# =====================================
# STUDENT REPORTS (FACULTY)
# =====================================

@app.route("/student_reports/<int:student_id>")
@login_required
def student_reports(student_id):

    if current_user.role not in ["Faculty", "Admin"]:

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    student = User.query.get_or_404(student_id)


    results = (

        Result.query

        .join(
            Document,
            Result.document1_id == Document.id
        )

        .filter(
            Document.user_id == student.id
        )

        .order_by(
            Result.created_at.desc()
        )

        .all()

    )


    return render_template(

        "student_reports.html",

        student=student,

        results=results

    )



# =====================================
# DOWNLOAD EXISTING REPORT
# =====================================

@app.route("/report/download/<int:result_id>")
@login_required
def report_download(result_id):

    result = Result.query.get_or_404(
        result_id
    )


    # Student can download only own report

    if current_user.role == "Student":

        if result.document1.user_id != current_user.id:
            abort(403)

    # Faculty/Admin can download all

    elif current_user.role not in [
        "Faculty",
        "Admin"
    ]:

        abort(403)


    if not result.report_path:

        flash(
            "Report not available.",
            "warning"
        )

        return redirect(request.referrer or url_for("index"))


    if not os.path.exists(result.report_path):

        flash(
            "Report file not found.",
            "danger"
        )

        return redirect(request.referrer or url_for("index"))


    directory = os.path.dirname(
        result.report_path
    )

    filename = os.path.basename(
        result.report_path
    )


    return send_from_directory(

        directory,

        filename,

        as_attachment=True

    )



# =====================================
# MY REPORTS
# =====================================

@app.route("/my_reports")
@login_required
def my_reports():

    if current_user.role != "Student":

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    results = (

        Result.query

        .join(
            Document,
            Result.document1_id == Document.id
        )

        .filter(
            Document.user_id == current_user.id
        )

        .order_by(
            Result.created_at.desc()
        )

        .all()

    )


    return render_template(

        "my_reports.html",

        results=results

    )
# =====================================
# ADMIN PAGE
# =====================================

@app.route("/admin")
@login_required
def admin():

    if current_user.role != "Admin":

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    users = User.query.all()

    documents = Document.query.all()

    results = Result.query.all()


    return render_template(

        "admin.html",

        users=users,

        documents=documents,

        results=results

    )



# =====================================
# ADMIN DASHBOARD
# =====================================

@app.route("/admin_dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "Admin":

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    total_users = User.query.count()

    total_students = User.query.filter_by(
        role="Student"
    ).count()

    total_faculty = User.query.filter_by(
        role="Faculty"
    ).count()

    total_documents = Document.query.count()

    total_results = Result.query.count()

    total_reports = Report.query.count()


    users = User.query.order_by(
        User.id.desc()
    ).all()


    return render_template(

        "admin_dashboard.html",

        total_users=total_users,

        total_students=total_students,

        total_faculty=total_faculty,

        total_documents=total_documents,

        total_results=total_results,

        total_reports=total_reports,

        users=users

    )



# =====================================
# DELETE USER
# =====================================

@app.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):

    if current_user.role != "Admin":

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    user = User.query.get_or_404(
        user_id
    )


    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "warning"
        )

        return redirect(
            url_for("admin_dashboard")
        )


    try:

        documents = Document.query.filter_by(
            user_id=user.id
        ).all()


        for doc in documents:

            # Delete plagiarism results
            Result.query.filter(
                Result.document1_id == doc.id
            ).delete(
                synchronize_session=False
            )

            # If your Result model has document2_id,
            # uncomment the following block.

            """
            Result.query.filter(
                Result.document2_id == doc.id
            ).delete(
                synchronize_session=False
            )
            """

            db.session.delete(doc)


        # Delete reports

        Report.query.filter_by(
            user_id=user.id
        ).delete(
            synchronize_session=False
        )


        # Delete user

        db.session.delete(user)

        db.session.commit()


        flash(
            "User deleted successfully.",
            "success"
        )


    except Exception as e:

        db.session.rollback()

        flash(
            f"Delete failed: {str(e)}",
            "danger"
        )


    return redirect(
        url_for("admin_dashboard")
    )

# =====================================
# GENERATE PDF REPORT
# =====================================

@app.route("/download_report/<int:result_id>")
@login_required
def download_report(result_id):

    if current_user.role not in ["Faculty", "Admin"]:

        flash(
            "Access denied!",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    result = Result.query.get_or_404(result_id)


    student = result.document1.owner


    filename = (
        f"Student_Report_{student.id}_{result.id}.pdf"
    )


    report_folder = os.path.join(
        "static",
        "reports"
    )

    os.makedirs(
        report_folder,
        exist_ok=True
    )


    pdf_path = os.path.join(
        report_folder,
        filename
    )


    document = SimpleDocTemplate(
        pdf_path,
        pagesize=letter
    )


    styles = getSampleStyleSheet()

    content = []


    content.append(

        Paragraph(
            "AI Academic Plagiarism Detection Report",
            styles["Title"]
        )

    )

    content.append(
        Spacer(1, 20)
    )


    similarity = (
        result.similarity_score or 0
    )


    data = [

        [
            "Student Name",
            student.fullname
        ],

        [
            "Email",
            student.email
        ],

        [
            "Document",
            result.document1.filename
        ],

        [
            "Compared With",

            result.document2.filename

            if result.document2

            else "No Match"
        ],

        [
            "Similarity Score",
            f"{similarity*100:.2f}%"
        ],

        [
            "Plagiarism Percentage",
            f"{result.plagiarism_percentage:.2f}%"
        ],

        [
            "Date",
            result.created_at.strftime("%d-%m-%Y")
        ]

    ]


    table = Table(data)

    content.append(table)

    content.append(
        Spacer(1, 20)
    )


    if result.plagiarism_percentage < 30:

        status = "Original Document"

    elif result.plagiarism_percentage < 70:

        status = "Moderate Similarity"

    else:

        status = "High Plagiarism Detected"


    content.append(

        Paragraph(

            f"<b>Final Result:</b> {status}",

            styles["Heading2"]

        )

    )


    document.build(content)


    return send_file(
        pdf_path,
        as_attachment=True
    )



# =====================================
# PROFILE
# =====================================

@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )



# =====================================
# APPLICATION START
# =====================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        admin = User.query.filter_by(
            role="Admin"
        ).first()


        if admin is None:

            admin = User(

                fullname="System Admin",

                email="admin@gmail.com",

                password="admin123",

                role="Admin"

            )

            try:
                db.session.add(admin)
                db.session.commit()
                print("✓ Default Admin Created")
            except Exception as e:
                # Handle race conditions / duplicate insert gracefully
                from sqlalchemy.exc import IntegrityError as _IntegrityError

                if isinstance(e, _IntegrityError):
                    db.session.rollback()
                    print("✓ Default Admin already present (IntegrityError handled)")
                else:
                    db.session.rollback()
                    raise

        else:

            print("✓ Admin Already Exists")


    app.run(
        debug=True
    )