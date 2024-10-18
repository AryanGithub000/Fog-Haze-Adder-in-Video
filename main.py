import os
import cv2
import numpy as np
from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fog and Haze Video Processor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        form { display: flex; flex-direction: column; gap: 10px; }
        input, button { padding: 10px; }
    </style>
</head>
<body>
    <h1>Fog and Haze Video Processor</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".mp4,.mov" required>
        <label for="fog_intensity">Fog Intensity (0-1):</label>
        <input type="number" name="fog_intensity" id="fog_intensity" min="0" max="1" step="0.1" value="0.5">
        <label for="haze_contrast">Haze Contrast (0-1):</label>
        <input type="number" name="haze_contrast" id="haze_contrast" min="0" max="1" step="0.1" value="0.5">
        <label for="haze_blur">Haze Blur (odd number):</label>
        <input type="number" name="haze_blur" id="haze_blur" min="1" max="21" step="2" value="5">
        <button type="submit">Process Video</button>
    </form>
</body>
</html>
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_fog(frame, intensity=0.5):
    fog = np.ones_like(frame, dtype=np.uint8) * 255
    foggy_frame = cv2.addWeighted(frame, 1 - intensity, fog, intensity, 0)
    return foggy_frame

def add_haze(frame, contrast=0.5, blur_amount=5):
    haze_frame = cv2.addWeighted(frame, contrast, np.zeros_like(frame, frame.dtype), 0, 0)
    haze_frame = cv2.GaussianBlur(haze_frame, (blur_amount, blur_amount), 0)
    return haze_frame

def process_video(input_video_path, output_video_path, fog_intensity=0.5, haze_contrast=0.5, haze_blur=5):
    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        foggy_frame = add_fog(frame, intensity=fog_intensity)
        foggy_hazy_frame = add_haze(foggy_frame, contrast=haze_contrast, blur_amount=haze_blur)

        out.write(foggy_hazy_frame)

    cap.release()
    out.release()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'processed_' + filename)

            file.save(input_path)

            fog_intensity = float(request.form.get('fog_intensity', 0.5))
            haze_contrast = float(request.form.get('haze_contrast', 0.5))
            haze_blur = int(request.form.get('haze_blur', 5))

            process_video(input_path, output_path, fog_intensity, haze_contrast, haze_blur)

            return send_file(output_path, as_attachment=True)
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
