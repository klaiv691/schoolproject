from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)


@app.route('/data')
def get_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_database"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table")
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
