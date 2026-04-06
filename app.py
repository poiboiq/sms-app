from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymysql
import os

app = Flask(__name__)
app.secret_key = 'sms-secret-key-2026'

# Database configuration - edit these when deploying
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'smsuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'smspassword123')
DB_NAME = os.environ.get('DB_NAME', 'smsdb')

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# ─── HOME ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) as c FROM students")
        students_count = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) as c FROM courses")
        courses_count = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) as c FROM enrollments")
        enrollments_count = cur.fetchone()['c']
    db.close()
    return render_template('index.html',
                           students_count=students_count,
                           courses_count=courses_count,
                           enrollments_count=enrollments_count)

# ─── STUDENTS ────────────────────────────────────────────────────────────────
@app.route('/students')
def students():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM students ORDER BY created_at DESC")
        students = cur.fetchall()
    db.close()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO students (name, email, phone, department) VALUES (%s, %s, %s, %s)",
                    (name, email, phone, department)
                )
            db.commit()
            flash('Student added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            db.close()
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        try:
            with db.cursor() as cur:
                cur.execute(
                    "UPDATE students SET name=%s, email=%s, phone=%s, department=%s WHERE id=%s",
                    (name, email, phone, department, id)
                )
            db.commit()
            flash('Student updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            db.close()
        return redirect(url_for('students'))
    with db.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cur.fetchone()
    db.close()
    return render_template('edit_student.html', student=student)

@app.route('/students/delete/<int:id>')
def delete_student(id):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM enrollments WHERE student_id=%s", (id,))
            cur.execute("DELETE FROM students WHERE id=%s", (id,))
        db.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        db.close()
    return redirect(url_for('students'))

# ─── COURSES ─────────────────────────────────────────────────────────────────
@app.route('/courses')
def courses():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM courses ORDER BY created_at DESC")
        courses = cur.fetchall()
    db.close()
    return render_template('courses.html', courses=courses)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        credits = request.form['credits']
        instructor = request.form['instructor']
        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO courses (name, code, credits, instructor) VALUES (%s, %s, %s, %s)",
                    (name, code, credits, instructor)
                )
            db.commit()
            flash('Course added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            db.close()
        return redirect(url_for('courses'))
    return render_template('add_course.html')

@app.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        credits = request.form['credits']
        instructor = request.form['instructor']
        try:
            with db.cursor() as cur:
                cur.execute(
                    "UPDATE courses SET name=%s, code=%s, credits=%s, instructor=%s WHERE id=%s",
                    (name, code, credits, instructor, id)
                )
            db.commit()
            flash('Course updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            db.close()
        return redirect(url_for('courses'))
    with db.cursor() as cur:
        cur.execute("SELECT * FROM courses WHERE id=%s", (id,))
        course = cur.fetchone()
    db.close()
    return render_template('edit_course.html', course=course)

@app.route('/courses/delete/<int:id>')
def delete_course(id):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM enrollments WHERE course_id=%s", (id,))
            cur.execute("DELETE FROM courses WHERE id=%s", (id,))
        db.commit()
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        db.close()
    return redirect(url_for('courses'))

# ─── ENROLLMENTS ─────────────────────────────────────────────────────────────
@app.route('/enrollments')
def enrollments():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT e.id, s.name as student_name, s.email, c.name as course_name,
                   c.code, e.grade, e.enrolled_at
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
            ORDER BY e.enrolled_at DESC
        """)
        enrollments = cur.fetchall()
    db.close()
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    db = get_db()
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        grade = request.form.get('grade', '')
        try:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)",
                    (student_id, course_id, grade)
                )
            db.commit()
            flash('Enrollment added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        finally:
            db.close()
        return redirect(url_for('enrollments'))
    with db.cursor() as cur:
        cur.execute("SELECT id, name FROM students ORDER BY name")
        students = cur.fetchall()
        cur.execute("SELECT id, name, code FROM courses ORDER BY name")
        courses = cur.fetchall()
    db.close()
    return render_template('add_enrollment.html', students=students, courses=courses)

@app.route('/enrollments/delete/<int:id>')
def delete_enrollment(id):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM enrollments WHERE id=%s", (id,))
        db.commit()
        flash('Enrollment removed successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    finally:
        db.close()
    return redirect(url_for('enrollments'))

# ─── API ENDPOINTS (for test cases) ──────────────────────────────────────────
@app.route('/api/students')
def api_students():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
    db.close()
    return jsonify(students)

@app.route('/api/courses')
def api_courses():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
    db.close()
    return jsonify(courses)

@app.route('/api/enrollments')
def api_enrollments():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT e.id, s.name as student_name, c.name as course_name, e.grade
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
        """)
        enrollments = cur.fetchall()
    db.close()
    return jsonify(enrollments)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
