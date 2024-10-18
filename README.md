# Fog and Haze Video Processor

This project allows you to upload a video and apply fog and haze effects to it. The processed video can be downloaded with the desired fog intensity, haze contrast, and haze blur.

## Features
- Upload a video file in `.mp4` or `.mov` format.
- Apply fog with adjustable intensity.
- Apply haze with customizable contrast and blur.
- Download the processed video with the effects applied.

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.x
- Flask
- OpenCV
- NumPy
- Werkzeug

You can install the required packages using pip:

```bash
pip install flask opencv-python numpy Werkzeug

```

## Getting Started
Follow these steps to run the application locally:

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-folder>
```
2. Create the necessary folders
Ensure the following folders exist (they will store the uploaded and processed videos):

uploads/: Stores the uploaded video files.
outputs/: Stores the processed videos with fog/haze effects.
If these folders don't exist, they will be automatically created when the server starts.

3. Run the application
Run the following command to start the Flask web server:

```bash
python main.py
```

4. Open the application in your browser
Once the server is running, open your browser and go to:

```bash
http://127.0.0.1:5000
```

5. Upload and process a video
On the webpage, upload a video file in .mp4 or .mov format.
Set the parameters for:
Fog Intensity (range: 0 to 1)
Haze Contrast (range: 0 to 1)
Haze Blur (odd numbers only, e.g., 3, 5, 7)

Click the "Process Video" button to generate the output.
Once the video is processed, the processed video will be available for download.

## Video Processing Details
Fog Effect
The fog effect is applied by blending the video frame with a white mask, creating a foggy look. The intensity of the fog is adjustable between 0 and 1.

Haze Effect
The haze effect is applied by modifying the contrast and blurring the video frame. You can control the contrast and blur amount.

Example
Fog Intensity: 0.5
Haze Contrast: 0.5
Haze Blur: 5
These parameters will generate a video with moderate fog and haze.

License
This project is licensed under the MIT License.

This `README.md` includes step-by-step instructions on how to set up and run the application locally. It explains the features, requirements, and detailed instructions for using the video processor with adjustable fog and haze effects.





