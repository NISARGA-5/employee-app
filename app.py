from flask import Flask, request, render_template
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "employee_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def index():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            department VARCHAR(100)
        )
    """)

    conn.commit()

    cur.close()
    conn.close()

    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_employee():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO employees(name,email,department)
        VALUES(%s,%s,%s)
        """,
        (name, email, department)
    )

    conn.commit()

    cur.close()
    conn.close()

    return """
    <h2>Employee Added Successfully!</h2>
    <a href="/">Add Another Employee</a>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
