# app/auth.py
from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Employee
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.post("/register")
def register():
    db = SessionLocal()
    data = request.json

    if db.query(Employee).filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode()

    # FIXED: Use password_hash, not password
    emp = Employee(
        name=data["name"],
        email=data["email"],
        password_hash=hashed_pw,  # ← CHANGED
        active="active"           # ← ADD THIS
    )
    db.add(emp)
    db.commit()

    return jsonify({"message": "Employee registered successfully"})


@auth.post("/login")
def login():
    db = SessionLocal()
    data = request.json

    user = db.query(Employee).filter_by(email=data["email"]).first()

    # FIXED: Check against password_hash
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):  # ← CHANGED
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "employee_id": user.id})