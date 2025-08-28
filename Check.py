from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# Load model
model = load_model("plant_disease_model.h5")

# Use the same class names from training
class_names = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
    "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
    "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

# Function to classify custom image
def predict_image(image_path):
    img = load_img(image_path, target_size=(128,128))      # Resize
    img_array = img_to_array(img) / 255.0                  # Normalize
    img_array = np.expand_dims(img_array, axis=0)          # Add batch dimension

    predictions = model.predict(img_array)
    pred_index = np.argmax(predictions)
    pred_class = class_names[pred_index]
    confidence = np.max(predictions)

    print(f"Predicted class: {pred_class} ({confidence*100:.2f}% confidence)")

# Example usage
test_image = "C:\\Users\\edeep\\Desktop\\LeafSense\\LeafSense\\checkimg.JPG"
predict_image(test_image)
