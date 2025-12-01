# attendance.py
from flask import Blueprint, request, jsonify
from .database import SessionLocal  # Use relative import
from .models import Attendance, Employee  # Use relative import
from datetime import datetime

attendance = Blueprint("attendance", __name__, url_prefix="/attendance")


@attendance.post("/in")
def clock_in():
    db = SessionLocal()
    data = request.json

    emp = db.query(Employee).filter_by(id=data["employee_id"]).first()
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    new_record = Attendance(
        employee_id=data["employee_id"],
        login_time=datetime.now()
    )
    db.add(new_record)
    db.commit()

    return jsonify({"message": "Clock-in recorded"})


@attendance.post("/out")
def clock_out():
    db = SessionLocal()
    data = request.json

    record = db.query(Attendance).filter_by(
        employee_id=data["employee_id"],
        logout_time=None
    ).first()

    if not record:
        return jsonify({"error": "User not clocked in"}), 400

    record.logout_time = datetime.now()
    db.commit()

    return jsonify({"message": "Clock-out recorded"})
