from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def fetch_largest_serial_number():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ayesiga@123",
        database="store"
    )


    cursor = connection.cursor()
    cursor.execute("SELECT MAX(serial_number) FROM storage")
    largest_serial_number = cursor.fetchone()[0]


    cursor.close()
    connection.close()

    return largest_serial_number

@app.route('/data')
def get_data():

    largest_serial_number = fetch_largest_serial_number()


    return jsonify({"largest_serial_number": largest_serial_number})

if __name__ == '__main__':
    app.run(debug=True)
