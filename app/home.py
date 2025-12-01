# app/home.py
from flask import Blueprint, jsonify

home = Blueprint("home", __name__)

@home.route("/")
def index():
    return jsonify({
        "message": "Attendance System API",
        "endpoints": {
            "auth": {
                "register": "POST /auth/register",
                "login": "POST /auth/login"
            },
            "attendance": {
                "clock_in": "POST /attendance/in",
                "clock_out": "POST /attendance/out"
            }
        }
    })