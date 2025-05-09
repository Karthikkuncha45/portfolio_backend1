from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Karthik@143",
    database="mydb"
)
cursor = db.cursor()

@app.route("/")
def index():
    return render_template("home.html")

# Route to store visitor's name and redirect to home.html
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

# Route to handle contact form submission
@app.route("/submit-form", methods=["GET", "POST"])
def submit_form():
    if request.method == "POST":
        name = request.form.get("name").strip()
        phone = request.form.get("phone").strip()
        message = request.form.get("message").strip()
        submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Server-side validation
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
            return redirect("/home")  # Redirect to home page after successful submission
        except Exception as e:
            db.rollback()
            return f"Database error: {str(e)}", 500
    
    # If the user accesses this route with GET, redirect them to home instead of error
    return redirect("/home")

@app.route("/education", methods=["GET","POST"])
def education():
    return render_template("education.html")


if __name__=="__main__":
    app.run(debug=True)