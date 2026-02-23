from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATA_FILE = "reports.csv"

# Create CSV file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Location", "Disaster", "Severity", "Description", "Time"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report", methods=["POST"])
def report():
    name = request.form.get("name")
    location = request.form.get("location")
    disaster = request.form.get("disaster")
    severity = request.form.get("severity")
    description = request.form.get("description")

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not name or not location or not disaster or not severity:
        flash("Please fill all required fields!")
        return redirect(url_for("home"))

    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, location, disaster, severity, description, time])

    flash("Report submitted successfully!")
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    reports = []
    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            reports.append(row)

    return render_template("admin.html", reports=reports)


if __name__ == "__main__":
    app.run(debug=True)