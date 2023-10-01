import os
from flask import Flask, render_template, request
import cv2
import face_recognition
import numpy as np

app = Flask(__name__)

# All data will be stored in the static folder
if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

if not os.path.exists('static/faces'):
    os.makedirs('static/faces')

if not os.path.exists('static/results'):
    os.makedirs('static/results')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    upload_file = request.files.get('image')
    faces = []

    if upload_file and upload_file.filename != '':
        img_path = os.path.join("static/uploads", upload_file.filename)
        upload_file.save(img_path)
        img = face_recognition.load_image_file(img_path)

        # Convert the image to RGB format
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect Faces
        face_locations = face_recognition.face_locations(img_rgb)
        img_with_boxes = img_rgb.copy()

        for index, face_location in enumerate(face_locations):
            top, right, bottom, left = face_location
            cv2.rectangle(img_with_boxes, (left, top), (right, bottom), (0, 255, 0), 2)

            # Crop and save each face
            face_img = img_rgb[top:bottom, left:right]
            face_filename = f"static/faces/face_{index}_{upload_file.filename}"
            cv2.imwrite(face_filename, face_img)
            faces.append((face_filename, f"img{index + 1}"))

        # Save the resultant image
        result_image_path = "static/results/result_" + upload_file.filename
        cv2.imwrite(result_image_path, img_with_boxes)

        return render_template('index.html', user_image=result_image_path, faces=faces)

    return render_template('index.html', user_image=None, faces=None)


if __name__ == "__main__":
    app.run(debug=True)
