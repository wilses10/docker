from flask import Flask, render_template, request
from pymysql import connections
import boto3
import os
from config import *

app = Flask(__name__)

# Database Connection
db_conn = connections.Connection(
    host=customhost,
    user=customuser,
    password=custompass,
    db=customdb
)

# S3 Client
s3 = boto3.client('s3')

# Routes
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/adduser", methods=['POST'])
def add_user():
    nom = request.form['nom']
    prenom = request.form['prenom']
    age = request.form['age']
    ville = request.form['ville']  # Ajout du champ ville
    user_file = request.files['user_file']

    if user_file.filename == "":
        return "Please select a file."

    # Insert into the database
    insert_sql = "INSERT INTO matrix (nom, prenom, ville, age) VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()
    try:
        cursor.execute(insert_sql, (nom, prenom, ville, age))
        db_conn.commit()

        # Upload file to S3
        file_key = f"{nom}_{prenom}_{user_file.filename}"
        s3.upload_fileobj(user_file, custombucket, file_key)
    except Exception as e:
        return str(e)
    finally:
        cursor.close()

    return f"User {prenom} {nom} from {ville} added successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

