import cv2
import face_recognition
import mysql.connector
from datetime import datetime
import time

# Open the default camera (0)
cap = cv2.VideoCapture(0)

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ayesiga@123",
    database="store"
)

# Initialize flag to control camera feed and time of last face detection
camera_on = True
last_detection_time = 0

while True:
    if camera_on:
        # Read the frame from the camera
        ret, frame = cap.read()

        # Convert the frame from BGR to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all face locations in the frame
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")  # Adjust face detection model if necessary

        current_time = time.time()
        if face_locations and current_time - last_detection_time >= 5:
            # If faces are detected and 5 seconds have elapsed since the last detection, save the face
            last_detection_time = current_time

            try:
                # Connect to MySQL and save the face data
                cursor = db_connection.cursor()
                current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                directory_saved = "saved-faces"  # Replace with the actual directory where you want to save images
                encoded_faces = face_recognition.face_encodings(rgb_frame, face_locations)
                for encoded_face in encoded_faces:
                    encoded_face_hex = encoded_face.tobytes().hex()
                    cursor.execute(
                        "INSERT INTO storage (serial_number, file_path, confidence, timestamp_col) VALUES (%s, %s, %s, %s)",
                        (None, directory_saved, 0.0, current_time_str))
                db_connection.commit()
                cursor.close()

                for i, (top, right, bottom, left) in enumerate(face_locations):
                    face_image = frame[top:bottom, left:right]
                    image_path = f"{directory_saved}/face_{i}.jpg"
                    try:
                        cv2.imwrite(image_path, face_image)
                        print(f"Image saved: {image_path}")
                    except Exception as e:
                        print(f"Error saving image: {e}")

                # Draw rectangle and label on the detected faces
                for top, right, bottom, left in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, 'Detected Face', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            except mysql.connector.Error as err:
                print("MySQL Error:", err)

            # Turn off camera feed until next face detection
            camera_on = False

    if not camera_on:
        # Wait for 5 seconds before turning the camera feed back on
        if time.time() - last_detection_time >= 5:
            camera_on = True

    if camera_on:
        cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
