import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproject.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


@app.route("/")
@login_required
def index():
    """Redirect logged-in users to the dashboard"""
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Signup user"""

    if request.method == "POST":
        # Get form inputs
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # Change this to match the input name
        confirmation = request.form.get("confirm_password")

        # Ensure all fields are provided
        if not username or not email or not password or not confirmation:
            flash("All fields are required.", "danger")
            return render_template("signup.html")

        # Check if passwords match
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        # Check if username already exists
        existing_user = db.execute(
            "SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            flash("Username already exists. Choose a different one.", "danger")
            return render_template("signup.html")

        # Add new user to the database (including email)
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   username, email, hashed_password)

        # Debugging: Print out the username and email to confirm it's being added
        print(f"New user added: {username}, {email}")

        flash("Registration successful! Please log in.", "success")
        return redirect("/")

    # GET request - render the signup page
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # If user is already logged in, redirect to /
    if "user_id" in session:
        print("User already logged in. Redirecting to index.")
        return redirect("/")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for empty fields
        if not username or not password:
            flash("Username and password cannot be empty.", "danger")
            return redirect("/login")

        # Query the database for the user
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Verify user exists and password is correct
        if user and check_password_hash(user[0]["password"], password):
            # Store user ID in session
            session["user_id"] = user[0]["id"]
            print(f"Logged in successfully. session['user_id'] = {
                  session['user_id']}")

            flash("Login successful!", "success")
            return redirect("/")  # Redirect to index
        else:
            flash("Invalid username or password.", "danger")

    # User reached route via GET
    return render_template("login.html")


@app.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():
    """Reset password"""

    if request.method == "POST":
        email = request.form.get("email")

        # TODO: Implement email verification and password reset logic
        flash("A password reset link has been sent to your email.", "info")
        return redirect("/login")

    # GET request - render the reset password page
    return render_template("resetpassword.html")


@app.route("/dashboard")
@login_required
def dashboard():
    total_students = db.execute("SELECT COUNT(*) FROM students")[0]['COUNT(*)']
    total_teachers = db.execute("SELECT COUNT(*) FROM teachers")[0]['COUNT(*)']
    total_courses = db.execute("SELECT COUNT(*) FROM courses")[0]['COUNT(*)']
    total_sections = db.execute("SELECT COUNT(*) FROM sections")[0]['COUNT(*)']
    total_payments = db.execute("SELECT COUNT(*) FROM payments")[0]['COUNT(*)']
    # new_students_weekly = [row['count'] for row in db.execute("SELECT count(*) as count FROM students GROUP BY week ORDER BY week")]
    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        total_sections=total_sections,
        total_payments=total_payments
        # new_students_weekly=new_students_weekly
    )

@app.route("/students")
@login_required
def students():
    """Show list of teachers"""
    students = db.execute(
        """
        SELECT
            students.id,
            students.student_name,
            students.parent_name,
            courses.course_name,
            sections.section_name,
            students.dob,
            students.gender,
            students.mobile,
            students.address
        FROM
            students
        JOIN
            courses ON students.course_id = courses.id,
            sections ON students.section_id = sections.id
        """
    )
    return render_template("students/students.html",students=students)


@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        # Retrieve form data
        student_name = request.form["student_name"]
        parent_name = request.form["parent_name"]
        course_id = request.form["course_name"]
        section_id = request.form["section_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        address = request.form["address"]

        db.execute("""
            INSERT INTO students (student_name, parent_name, course_id, section_id, dob, gender, mobile, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, student_name, parent_name, course_id, section_id, dob, gender, mobile, address)
        flash("Student added successfully!", "success")
        return redirect('/students')

    # Fetch teachers and courses for the form
    sections = db.execute("SELECT * FROM sections")
    courses = db.execute("SELECT * FROM courses")
    return render_template('students/add_student.html', courses=courses, sections= sections)


@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if request.method == 'POST':
        # Retrieve form data
        student_name = request.form["student_name"]
        parent_name = request.form["parent_name"]
        course_id = request.form["course_name"]
        section_id = request.form["section_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        address = request.form["address"]

        db.execute("""
            UPDATE students
            SET student_name = ?, parent_name  = ?, course_id = ?, section_id = ?, dob = ?, gender = ? , mobile = ?, address = ?
            WHERE id = ?
            """,
            student_name, parent_name, course_id, section_id, dob, gender, mobile, address, id)
        flash("Student updated successfully!", "success")
        return redirect('/students')

    # Fetch teachers and courses for the form
    sections = db.execute("SELECT * FROM sections")
    courses = db.execute("SELECT * FROM courses")
    student = db.execute("SELECT * FROM students WHERE id = ?", id)
    return render_template('students/edit_student.html',students=student[0], courses=courses, sections= sections)

@app.route('/students/delete', methods=['POST'])
@login_required
def delete_student():
    """Delete one or more students"""
    # Parse JSON data from the request
    data = request.get_json()
    print(f"Received data: {data}")  # Debugging output

    # Extract section IDs to delete
    student_ids_to_delete = data.get('student_ids', [])

    if not student_ids_to_delete:
        return jsonify({"success": False, "message": "No student IDs provided."}), 400

    # Perform deletion
    for student_id in student_ids_to_delete:
        print(f"Attempting to delete student with ID: {student_id}")  # Debugging output
        db.execute("DELETE FROM students WHERE id = ?", student_id)
        flash("Student deleted successfully!", "danger")
    # If successful, return confirmation
    return jsonify({"success": True, "message": f"Deleted {len(student_ids_to_delete)} student(s)."})


@app.route("/teachers")
@login_required
def teachers():
    """Show list of teachers"""
    teachers = db.execute(
        """
        SELECT
            teachers.id,
            teachers.name,
            teachers.specialization,
            courses.course_name,
            teachers.experience,
            teachers.mobile_phone,
            teachers.address
        FROM
            teachers
        JOIN
            courses ON teachers.course_id = courses.id
        """
    )
    return render_template("teachers/teachers.html", teachers=teachers)


@app.route("/teachers/add", methods=["GET", "POST"])
@login_required
def add_teacher():
    if request.method == "POST":
        # Get form data
        name = request.form['teacher_name']
        specialization = request.form['specilization']
        course_id = request.form['course_name']
        experience = request.form['experience']
        mobile_phone = request.form['mobile']
        address = request.form['address']

        # Insert teacher data into the database
        db.execute(
            """
            INSERT INTO teachers (name, specialization, course_id, experience, mobile_phone, address)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            name, specialization, course_id, experience, mobile_phone , address
        )
        flash("Teacher added successfully!", "success")
        return redirect("/teachers")  # Redirect after processing

    # Fetch the list of courses from the database for the dropdown
    courses = db.execute("SELECT * FROM courses")

    # Render the add_teacher.html template with the courses
    return render_template("teachers/add_teacher.html", courses=courses)


@app.route("/teachers/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_teacher(id):
    if request.method == "POST":
        # Retrieve form data
        name = request.form.get("teacher_name")
        specialization = request.form.get("specilization")
        course_id = request.form.get("course_name")
        experience = request.form.get("experience")
        mobile = request.form.get("mobile")
        address = request.form.get("address")

        # Update the teacher's details
        db.execute("""
            UPDATE teachers
            SET name = ?, specialization = ?, course_id = ?, experience = ?, mobile = ?, address = ?
            WHERE id = ?
            """, name, specialization, course_id, experience, mobile, address, id)
        flash("Teacher updated successfully!", "success")
        return redirect("/teachers")

    # Fetch the teacher details and all courses
    teacher = db.execute("SELECT * FROM teachers WHERE id = ?", id)
    courses = db.execute("SELECT * FROM courses")

    return render_template("teachers/edit_teacher.html", teachers=teacher[0], courses=courses)


@app.route('/teachers/delete', methods=['POST'])
@login_required
def teacher_courses():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging output
        teacher_ids_to_delete = data.get('teacher_ids', [])

        # Perform deletion
        for teacher_id in teacher_ids_to_delete:
            print(f"Attempting to delete teacher with ID: {teacher_id}")  # Debugging output
            db.execute("DELETE FROM teachers WHERE id = ?", (teacher_id,))

        # If successful, return confirmation
        return jsonify({"success": True, "message": f"Deleted {len(teacher_ids_to_delete)} teacher(s)."})

    except Exception as e:
        # Log the error and return a failure response
        print(f"Error during teacher deletion: {e}")
        return jsonify({"success": False, "message": "An error occurred while deleting teachers."}), 500


@app.route("/courses")
@login_required
def courses():
    # Get all courses from the database
    courses = db.execute("SELECT * FROM courses")
    return render_template("courses/courses.html", courses=courses)


@app.route("/courses/add", methods=["GET", "POST"])
@login_required
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        course_fee = request.form["course_fee"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        description = request.form["description"]

        # Insert course into the database
        db.execute(
            """
            INSERT INTO courses (course_name, course_fee, start_date, end_date, start_time, end_time, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            course_name, course_fee, start_date, end_date, start_time, end_time, description
        )
        flash("Course added successfully!", "success")
        return redirect("/courses")

    return render_template("courses/add_course.html")


@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):

    if request.method == 'POST':
        # Get the updated course details from the form
        updated_name = request.form['course_name']
        updated_fee = request.form['course_fee']
        updated_start_date = request.form['start_date']
        updated_end_date = request.form['end_date']
        updated_start_time = request.form['start_time']
        updated_end_time = request.form['end_time']
        updated_description = request.form['description']

        # Update course details in the database
        db.execute(
            """
            UPDATE courses
            SET course_name = ?, course_fee = ?, start_date = ?, end_date = ?, start_time = ?, end_time = ?, description = ?
            WHERE id = ?
            """,
            updated_name, updated_fee, updated_start_date, updated_end_date, updated_start_time, updated_end_time, updated_description, course_id
        )
        flash("Course updated successfully!", "success")
        return redirect('/courses')  # Redirect back to the courses list

    course = db.execute("SELECT * FROM courses WHERE id = ?", id)
    return render_template('courses/edit_course.html', courses=course[0])


@app.route('/courses/delete', methods=['POST'])
@login_required
def delete_courses():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging output
        course_ids_to_delete = data.get('course_ids', [])

        # Validate the incoming data
        if not course_ids_to_delete:
            return jsonify({"success": False, "message": "No course IDs provided."}), 400

        # Perform deletion
        for course_id in course_ids_to_delete:
            print(f"Attempting to delete course with ID: {course_id}")  # Debugging output
            db.execute("DELETE FROM courses WHERE id = ?", (course_id,))

        # If successful, return confirmation
        return jsonify({"success": True, "message": f"Deleted {len(course_ids_to_delete)} course(s)."})

    except Exception as e:
        # Log the error and return a failure response
        print(f"Error during course deletion: {e}")
        return jsonify({"success": False, "message": "An error occurred while deleting courses."}), 500


@app.route("/sections")
@login_required
def sections():
    """Show list of Sections"""
    teachers = db.execute("SELECT * FROM teachers")
    courses = db.execute("SELECT * FROM courses")
    sections = db.execute(
        """
        SELECT
            sections.id,
            sections.section_name,
            courses.course_name,
            teachers.name,
            sections.room_name,
            sections.start_time,
            sections.end_time
        FROM
            sections
        JOIN
            courses ON sections.course_id = courses.id,
            teachers ON sections.teacher_id = teachers.id
        """
    )
    return render_template("sections/sections.html", sections=sections,teachers=teachers,courses=courses)

@app.route('/sections/add', methods=['GET', 'POST'])
@login_required
def add_section():
    if request.method == 'POST':
        # Retrieve form data
        section_name = request.form["section_name"]
        course_id = request.form["course_name"]
        teacher_id = request.form["teacher_name"]
        room_name = request.form["room_name"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]


        db.execute("""
            INSERT INTO sections (section_name, course_id, teacher_id, room_name, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            section_name, course_id, teacher_id, room_name, start_time, end_time
        )
        flash("Section added successfully!", "success")
        return redirect('/sections')

    # Fetch teachers and courses for the form
    teachers = db.execute("SELECT * FROM teachers")
    courses = db.execute("SELECT * FROM courses")
    return render_template('sections/add_section.html', courses=courses, teachers=teachers)


@app.route("/sections/edit/<int:section_id>", methods=["GET", "POST"])
@login_required
def edit_section(section_id):
    """Edit Section"""
    if request.method == "POST":
        # Get form data
        section_name = request.form["section_name"]
        course_id = request.form["course_name"]
        teacher_id = request.form["teacher_name"]
        room_name = request.form["room_name"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]


        # Update the section in the database
        db.execute("""
            UPDATE sections
            SET section_name = ?, course_id = ?, teacher_id = ?, room_name = ?, start_time = ?, end_time = ?
            WHERE id = ?
        """,
        section_name, course_id, teacher_id, room_name, start_time, end_time, section_id)

        flash("Section updated successfully!", "success")
        return redirect("/sections")

    # Fetch related data for dropdowns
    courses = db.execute("SELECT * FROM courses")
    teachers = db.execute("SELECT * FROM teachers")
    section = db.execute("SELECT * FROM sections WHERE id = ?", section_id)

    return render_template("sections/edit_section.html", sections=section[0], courses=courses, teachers=teachers)

@app.route('/sections/delete', methods=['POST'])
@login_required
def delete_section():
    """Delete one or more sections"""
    # Parse JSON data from the request
    data = request.get_json()
    print(f"Received data: {data}")  # Debugging output

    # Extract section IDs to delete
    section_ids_to_delete = data.get('section_ids', [])

    if not section_ids_to_delete:
        return jsonify({"success": False, "message": "No section IDs provided."}), 400

    # Perform deletion
    for section_id in section_ids_to_delete:
        print(f"Attempting to delete section with ID: {section_id}")  # Debugging output
        db.execute("DELETE FROM sections WHERE id = ?", section_id)

    # If successful, return confirmation
    return jsonify({"success": True, "message": f"Deleted {len(section_ids_to_delete)} section(s)."})

@app.route("/payments")
@login_required
def payments():
    """Show list of payments"""
    payments = db.execute("""
    SELECT
        payments.id,
        students.student_name,
        sections.section_name,
        payments.payment_date,
        payments.payment_amount,
        payments.payment_method
    FROM
        payments
    JOIN
        students ON payments.student_id = students.id
    JOIN
        sections ON payments.section_id = sections.id
    """)

    return render_template("payments/payments.html",payments= payments)

@app.route('/payments/add', methods=['GET', 'POST'])
@login_required
def add_payment():
    if request.method == 'POST':
        # Retrieve form data
        student_id = request.form["student_name"]
        section_id = request.form["section_name"]
        payment_date = request.form["payment_date"]
        payment_amount = request.form["payment_amount"]
        payment_method = request.form["payment_method"]

        # Insert into the database
        db.execute("""
            INSERT INTO payments (student_id, section_id, payment_date, payment_amount, payment_method)
            VALUES (?, ?, ?, ?, ?)
        """, student_id, section_id, payment_date, payment_amount, payment_method)

        flash("Payment added successfully!", "success")
        return redirect('/payments')

    # Fetch students and sections for the form
    sections = db.execute("SELECT * FROM sections")
    students = db.execute("SELECT * FROM students")
    return render_template('payments/add_payment.html', sections=sections, students=students)



@app.route('/payments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_payment(id):
    if request.method == 'POST':
        # Retrieve form data
        student_id = request.form["student_name"]
        section_id = request.form["section_name"]
        payment_date = request.form["payment_date"]
        payment_amount = request.form["payment_amount"]
        payment_method = request.form["payment_method"]

        db.execute("""
            UPDATE payments
            SET student_id = ?, section_id = ?, payment_date = ?, payment_amount = ? , payment_method = ?
            WHERE id = ?
            """,
            student_id, section_id, payment_date, payment_amount, payment_method, id)
        flash("Payments updated successfully!", "success")
        return redirect('/payents')

    # Fetch teachers and courses for the form
    sections = db.execute("SELECT * FROM sections")
    students = db.execute("SELECT * FROM students")
    payment = db.execute("SELECT * FROM payments WHERE id = ?", id)
    return render_template('payments/edit_payment.html', payments= payment[0],students=students, sections= sections)

@app.route('/payments/delete', methods=['POST'])
@login_required
def delete_payment():
    """Delete one or more payments"""
    # Parse JSON data from the request
    data = request.get_json()
    print(f"Received data: {data}")  # Debugging output

    # Extract section IDs to delete
    payment_ids_to_delete = data.get('payment_ids', [])

    if not payment_ids_to_delete:
        return jsonify({"success": False, "message": "No payment IDs provided."}), 400

    # Perform deletion
    for payment_id in payment_ids_to_delete:
        print(f"Attempting to delete student with ID: {payment_id}")  # Debugging output
        db.execute("DELETE FROM payments WHERE id = ?", payment_id)

    # If successful, return confirmation
    return jsonify({"success": True, "message": f"Deleted {len(payment_ids_to_delete)} payment(s)."})



@app.route("/logout", methods=["POST"])
def logout():
    print("Logout route accessed")  # Debugging log
    session.clear()
    return redirect("/login")



# Run the app
if __name__ == "__main__":
    app.run()
