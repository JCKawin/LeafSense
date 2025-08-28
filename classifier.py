import cvzone
import cv2

def Classify(path):
    # Provide the path to your image
    image_path = path  # Replace with your actual image path

    myClassifier = cvzone.Classifier('MyModel/keras_model.h5', 'MyModel/labels.txt')

    # Read the image from local storage
    img = cv2.imread(image_path)

    if img is not None:
        predictions, index = myClassifier.getPrediction(img)
        print("Predictions:", predictions)
        print("Index:", index)
        
        cv2.imshow("Image", img)
        cv2.waitKey(0)  # Wait for any key press
        cv2.destroyAllWindows()
    else:
        print("Error: Could not load image from", image_path)