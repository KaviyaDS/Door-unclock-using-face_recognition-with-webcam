from flask import Flask, request, render_template, redirect, url_for, Response
import os
import cv2

app = Flask(__name__)

# Owner's password (replace with your password)
owner_password = "123"

# Create the "dataset" folder if it doesn't exist
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Capture image flag
capture_image = False

@app.route("/", methods=["GET", "POST"])
def index():
    global capture_image
    password_is_correct = False
    if request.method == "POST":
        entered_password = request.form.get("password")
        if entered_password == owner_password:
            capture_image = True
            password_is_correct = True
            return redirect(url_for("capture"))
        else:
            return "Incorrect password. Access denied."

    return render_template("index.html", capture_image=capture_image)

@app.route("/capture", methods=["GET", "POST"])
def capture():
    global capture_image

    if capture_image:
        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return "Failed to open the webcam."

        if request.method == "POST":
            user_name = request.form.get("user_name")
            if user_name:
                image_path = os.path.join("dataset", f"{user_name}.jpg")
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(image_path, frame)
                    capture_image = False
                    cap.release()
                    return "Image captured and saved successfully."

        return render_template("capture.html", capture_image=capture_image, video_feed="/video_feed")

    return redirect(url_for("index"))

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == "__main__":
    app.run(port=8080)
