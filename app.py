from flask import Flask, jsonify
import mysql.connector
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

# Route for serving entrance data
@app.route('/entrance')
def get_entrance_data():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ayesiga@123",
            database="store"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT MAX(serial_number) FROM storage")
        max_serial_number = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({"max_serial_number": max_serial_number})
    except Exception as e:
        # Log the exception
        logging.error("An error occurred while fetching entrance data: %s", str(e))
        return jsonify({"error": "An error occurred while fetching entrance data"}), 500

# Route for serving exit data
@app.route('/exit')
def get_exit_data():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ayesiga@123",
            database="store"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT MAX(serial_number) FROM storage2")
        max_serial_number = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({"max_serial_number": max_serial_number})
    except Exception as e:
        # Log the exception
        logging.error("An error occurred while fetching exit data: %s", str(e))
        return jsonify({"error": "An error occurred while fetching exit data"}), 500

if __name__ == '__main__':
    app.run(port=5000)
