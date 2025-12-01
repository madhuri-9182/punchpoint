# app/webui.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.database import SessionLocal
from app.models import Employee, Attendance
from datetime import datetime

webui = Blueprint("webui", __name__)

@webui.route("/")
def dashboard():
    """Main dashboard page"""
    return render_template("dashboard.html")

@webui.route("/register", methods=["GET", "POST"])
def register_page():
    """Registration page"""
    if request.method == "POST":
        db = SessionLocal()
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if email exists
        if db.query(Employee).filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for("webui.register_page"))
        
        # Create new employee - USE password_hash NOT password
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        hashed_pw = bcrypt.generate_password_hash(password).decode()
        
        # FIXED LINE: Use password_hash, not password
        emp = Employee(
            name=name, 
            email=email, 
            password_hash=hashed_pw,  # ← CHANGED FROM password TO password_hash
            active="active"           # ← ADD THIS (required field)
        )
        db.add(emp)
        db.commit()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("webui.login_page"))
    
    return render_template("register.html")

@webui.route("/login", methods=["GET", "POST"])
def login_page():
    """Login page"""
    if request.method == "POST":
        db = SessionLocal()
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = db.query(Employee).filter_by(email=email).first()
        
        if user:
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt()
            # FIXED: Check against password_hash, not password
            if bcrypt.check_password_hash(user.password_hash, password):  # ← CHANGED
                session["employee_id"] = user.id
                session["employee_name"] = user.name
                flash("Login successful!", "success")
                return redirect(url_for("webui.dashboard"))
        
        flash("Invalid credentials", "error")
    
    return render_template("login.html")

@webui.route("/attendance")
def attendance_page():
    """Attendance management page"""
    if "employee_id" not in session:
        return redirect(url_for("webui.login_page"))
    
    db = SessionLocal()
    employee_id = session["employee_id"]
    
    # Get employee's attendance records
    records = db.query(Attendance).filter_by(
        employee_id=employee_id
    ).order_by(Attendance.login_time.desc()).limit(10).all()
    
    # Check if currently clocked in
    current_session = db.query(Attendance).filter_by(
        employee_id=employee_id,
        logout_time=None
    ).first()
    
    return render_template("attendance.html", 
                         records=records, 
                         current_session=current_session,
                         employee_name=session.get("employee_name"))

@webui.route("/clock-in", methods=["POST"])
def clock_in():
    """Clock in from web"""
    if "employee_id" not in session:
        return redirect(url_for("webui.login_page"))
    
    db = SessionLocal()
    employee_id = session["employee_id"]
    
    # Check if already clocked in
    existing = db.query(Attendance).filter_by(
        employee_id=employee_id,
        logout_time=None
    ).first()
    
    if existing:
        flash("You are already clocked in!", "warning")
        return redirect(url_for("webui.attendance_page"))
    
    # Create new attendance record
    new_record = Attendance(
        employee_id=employee_id,
        login_time=datetime.now()
    )
    db.add(new_record)
    db.commit()
    
    flash("Clock-in recorded successfully!", "success")
    return redirect(url_for("webui.attendance_page"))

@webui.route("/clock-out", methods=["POST"])
def clock_out():
    """Clock out from web"""
    if "employee_id" not in session:
        return redirect(url_for("webui.login_page"))
    
    db = SessionLocal()
    employee_id = session["employee_id"]
    
    # Find current session
    record = db.query(Attendance).filter_by(
        employee_id=employee_id,
        logout_time=None
    ).first()
    
    if not record:
        flash("No active clock-in found!", "error")
        return redirect(url_for("webui.attendance_page"))
    
    record.logout_time = datetime.now()
    db.commit()
    
    flash("Clock-out recorded successfully!", "success")
    return redirect(url_for("webui.attendance_page"))

@webui.route("/logout")
def logout():
    """Logout user"""
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("webui.login_page"))