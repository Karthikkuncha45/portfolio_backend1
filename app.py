from flask import Flask, render_template, request, redirect
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# PostgreSQL Connection using credentials from .env
db = psycopg2.connect(
    
    "host": "dpg-d071dajuibrs73f1kcs0-a.oregon-postgres.render.com",
    "port": "5432",
    "database": "student_db_tc30",
    "user": "student_db_tc30_user",
    "password": "x3WA2Wfqeg9yOzY3BV7P7INwJxWrimLh"
}

cursor = db.cursor()

@app.route("/")
def index():
    # Redirect to Netlify site
    return redirect("https://karthikkuncha45.netlify.app/home.html")

@app.route("/home", methods=["POST"])
def home():
    visitor_name = request.form["visitor_name"].strip()
    visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("INSERT INTO visitors (name, visit_time) VALUES (%s, %s)", (visitor_name, visit_time))
        db.commit()
        return render_template("home.html", name=visitor_name)
    except Exception as e:
        db.rollback()
        return f"Database error: {str(e)}", 500

@app.route("/submit-form", methods=["GET", "POST"])
def submit_form():
    if request.method == "POST":
        name = request.form.get("name").strip()
        phone = request.form.get("phone").strip()
        message = request.form.get("message").strip()
        submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Validation
        if not name or not phone or not message:
            return "All fields are required.", 400

        if len(phone) != 10 or not phone.isdigit() or not phone.startswith(("6", "7", "8", "9")):
            return "Invalid phone number.", 400

        try:
            cursor.execute(
                "INSERT INTO ContactListOfProfile (name, phone, message, submit_time) VALUES (%s, %s, %s, %s)",
                (name, phone, message, submit_time)
            )
            db.commit()
            return redirect("/home")
        except Exception as e:
            db.rollback()
            return f"Database error: {str(e)}", 500

    return redirect("/home")

@app.route("/education", methods=["GET", "POST"])
def education():
    return render_template("education.html")

if __name__ == "__main__":
    app.run(debug=True)
