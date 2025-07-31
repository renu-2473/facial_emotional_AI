from flask import Flask, render_template, request
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create uploads folder if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    emotion_result = None
    image_path = None
    emotion_scores = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            try:
                result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
                emotion_scores = result[0]['emotion']
                emotion_result = result[0]['dominant_emotion']
                print("Emotion scores:", emotion_scores)
            except Exception as e:
                emotion_result = f"Error: {str(e)}"

    return render_template('index.html', emotion=emotion_result, emotions=emotion_scores, image=image_path)

if __name__ == '__main__':
    app.run(debug=True)
