import os
# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf

class PlantDiseaseDetector:
    def __init__(self, model_path='converted_keras/keras_model.h5', labels_path='converted_keras/labels.txt'):
        """Initialize the detector with model and labels."""
        self.model = load_model(model_path, compile=False)
        self.class_names = self._load_labels(labels_path)
        
    def _load_labels(self, labels_path):
        """Load labels from the text file."""
        with open(labels_path, 'r') as f:
            class_names = [line.strip() for line in f.readlines()]
        return class_names

    def process_image(self, img_path):
        """Process image for prediction."""
        # Load and preprocess the image
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch
        img_array = img_array / 255.0  # Normalize
        return img_array

    def predict(self, img_path):
        """Predict the class of an image."""
        try:
            # Process image
            processed_image = self.process_image(img_path)
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get the predicted class and confidence
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])
            
            # Get the class name
            predicted_class = self.class_names[predicted_class_index]
            
            return {
                'class_name': predicted_class,
                'class_index': predicted_class_index,
                'confidence': confidence,
                'all_probabilities': predictions[0].tolist()
            }
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = PlantDiseaseDetector()
    
    # Test with an image
    test_image = "checkimg.JPG"  # Replace with your image path
    
    if os.path.exists(test_image):
        result = detector.predict(test_image)
        if result:
            print("\nPrediction Results:")
            print(f"Class: {result['class_name']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Class Index: {result['class_index']}")
            print("\nAll class probabilities:")
            for i, prob in enumerate(result['all_probabilities']):
                print(f"Class {i} ({detector.class_names[i]}): {prob:.2%}")
        else:
            print("Failed to make prediction")
    else:
        print(f"Image file {test_image} not found")
