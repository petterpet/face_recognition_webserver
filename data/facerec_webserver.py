# Based on: https://github.com/ageitgey/face_recognition/blob/master/examples/web_service_example.py

# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a known face.
# Pictures of known faces must be stored in the specific folder.
# The filename should be the name of the person.

# The result is returned as json. For example:
# {
#  "status": "'OK' or 'ERROR'",
#  "number_of_known_faces": "number",
#  "face_found_in_image": "boolean",
#  "known_face_found_in_image": "boolean",
#  "persons_name": "string"
# }

# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

import face_recognition
from flask import Flask, jsonify, request, redirect
import os

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# Detect known faces
pictures_known_faces = os.listdir("./known_faces/")
known_face_encodings = []
known_persons = []  # List of names of known persons

for picture in pictures_known_faces:
    file = "./known_faces/" + picture
    known_persons.append(picture[0:picture.index('.')])

    picture_loaded = face_recognition.load_image_file(file)
    known_face_encoding = face_recognition.face_encodings(picture_loaded)[0]
    known_face_encodings.append(known_face_encoding)

number_known_faces = len(known_face_encodings)

# Webserver
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Gesichtserkennung</title>
    <h1>Lade ein Foto hoch und du erfährst, ob die Person dem System bekannt ist</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

# Face Recognition
def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    # Initialize some variables
    face_found = False
    known_face_found = False
    name_of_known_face = ""

    if number_known_faces > 0:
        if len(unknown_face_encodings) > 0:
            face_found = True
            # See if the first face in the uploaded image matches a known face
            i = 0
            for known_face_encoding in known_face_encodings:
                match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])

                if match_results[0]:
                    known_face_found = True
                    name_of_known_face = known_persons[i]
                    break
                i += 1

        result = {
            "status": "OK",
            "number_of_known_faces": number_known_faces,
            "face_found_in_image": face_found,
            "known_face_found_in_image": known_face_found,
            "persons_name": name_of_known_face
        }

    else:
        # folder with known faces is empty
        result = {
            "status": "ERROR",
            "number_of_known_faces": number_known_faces
        }

    # Return the result as json
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
