import cv2
import numpy as np
import tensorflow as tf

# Load the COCO labels
LABELS = open('coco.names').read().strip().split("\n")

# Load the TensorFlow model
model = tf.saved_model.load('ssd_mobilenet_v2/saved_model')

# Load an image
image = cv2.imread('image.jpg')
height, width, _ = image.shape

# Preprocess the image: resize and normalize
input_tensor = cv2.resize(image, (300, 300))
input_tensor = input_tensor.astype(np.float32)
input_tensor = np.expand_dims(input_tensor, axis=0)

# Perform object detection
detections = model(input_tensor)

# Extract the detection results
boxes = detections['detection_boxes'][0].numpy()
scores = detections['detection_scores'][0].numpy()
classes = detections['detection_classes'][0].numpy().astype(np.int32)

# Draw bounding boxes on the image
for i in range(len(scores)):
    if scores[i] > 0.5:
        box = boxes[i] * np.array([height, width, height, width])
        (startY, startX, endY, endX) = box.astype("int")

        label = f"{LABELS[classes[i]]}: {scores[i]:.2f}"
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
