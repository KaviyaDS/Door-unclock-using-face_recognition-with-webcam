import face_recognition
import cv2
import os

# Load known faces from the "dataset" folder
known_face_encodings = []
known_face_names = []

for filename in os.listdir("dataset"):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(os.path.join("dataset", filename))
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

# Initialize the camera
video_capture = cv2.VideoCapture(0)

# Initialize door status
door_open = False

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Assume the door is closed until a recognized face is detected
    door_status = "Door closed"

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        if True in matches:
            # If a known face is detected, get the name of the recognized person
            name = known_face_names[matches.index(True)]
            door_status = f"Door opened for {name}"
            door_open = True
            break

    if not door_open:
        door_status = "Door closed"

    print(door_status)

    # If door is open, you can trigger any action here

    # Display the resulting image
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()