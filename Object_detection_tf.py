# Import required libraries
import os
import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter
from flask import Flask, render_template, Response
import tensorflow as tf
# Define object detection function using TensorFlowLite
"""def detect_objects(interpreter, frame):
    # Get input details
    input_details = interpreter.get_input_details()
    # Preprocess input image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    input_data = np.expand_dims(image_resized, axis=0)
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # Run inference
    interpreter.invoke()
    # Get output details
    output_details = interpreter.get_output_details()
    # Get detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    # Filter out low confidence detections
    detections = [box for i, box in enumerate(boxes) if scores[i] > 0.5]
    return detections"""

# Define object detection function using TensorFlowLite
def detect_objects(interpreter, frame):
    # Get input details
    input_details = interpreter.get_input_details()
    # Preprocess input image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
    input_data = np.expand_dims(image_resized, axis=0)
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)
    # Run inference
    interpreter.invoke()
    # Get output details
    output_details = interpreter.get_output_details()
    # Get detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0].astype(np.uint8)
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    # Filter out low confidence detections
    detections = [(box, class_idx) for class_idx, box in enumerate(boxes) if scores[class_idx] > 0.5]
    # Read labels from file
    with open('/home/pi/Sample_TFLite_model/labelmap.txt', 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    # Assign labels to classes
    labeled_detections = []
    for detection in detections:
        box, class_idx = detection
        ymin, xmin, ymax, xmax = box
        xmin = int(xmin * frame.shape[1])
        xmax = int(xmax * frame.shape[1])
        ymin = int(ymin * frame.shape[0])
        ymax = int(ymax * frame.shape[0])
        label = labels[class_idx]
        labeled_detections.append(((xmin, ymin, xmax, ymax), label))
    return labeled_detections


# Define Flask app
app = Flask(__name__)

# Define video capture function
"""def capture_video():
    # Open video capture device
    cap = cv2.VideoCapture(0)
    # Load TensorFlowLite model
    interpreter = Interpreter(model_path='/home/pi/Sample_TFLite_model/detect.tflite')
    interpreter.allocate_tensors()
    # Loop through frames
    while True:
        # Read frame from video capture device
        ret, frame = cap.read()
        # Detect objects in frame using TensorFlowLite
        detections = detect_objects(interpreter, frame)
        # Draw bounding boxes around detected objects
        for detection in detections:
            ymin, xmin, ymax, xmax = detection
            xmin = int(xmin * frame.shape[1])
            xmax = int(xmax * frame.shape[1])
            ymin = int(ymin * frame.shape[0])
            ymax = int(ymax * frame.shape[0])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        # Display frame with detected objects
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')"""

# Define video capture function
def capture_video():
    # Open video capture device
    cap = cv2.VideoCapture(0)
    # Load TensorFlowLite model and labels
    model_path = '/home/pi/Sample_TFLite_model/detect.tflite'
    labels_path = os.path.join(os.path.dirname(model_path), 'labelmap.txt')
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    # Loop through frames
    while True:
        # Read frame from video capture device
        ret, frame = cap.read()
        # Detect objects in frame using TensorFlowLite
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
        input_data = np.expand_dims(image_resized, axis=0)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        # Get detection results
        boxes = interpreter.get_tensor(output_details[0]['index'])[0]
        classes = interpreter.get_tensor(output_details[1]['index'])[0]
        scores = interpreter.get_tensor(output_details[2]['index'])[0]
        # Filter out low confidence detections
        detections = [i for i in range(len(scores)) if scores[i] > 0.5]
        # Draw bounding boxes and labels around detected objects
        for i in detections:
            ymin, xmin, ymax, xmax = boxes[i]
            xmin = int(xmin * frame.shape[1])
            xmax = int(xmax * frame.shape[1])
            ymin = int(ymin * frame.shape[0])
            ymax = int(ymax * frame.shape[0])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            label = f'{labels[int(classes[i])]}: {scores[i]:.2f}'
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Display frame with detected objects
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Define Flask route for video stream
@app.route('/video_feed')
def video_feed():
    return Response(capture_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Define Flask route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)