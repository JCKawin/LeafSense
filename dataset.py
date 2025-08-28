# ==============================
# 1. Import Libraries
# ==============================
import kagglehub
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array

# ==============================
# 2. Download Dataset
# ==============================
print("Downloading dataset...")
path = kagglehub.dataset_download("emmarex/plantdisease")
print("Path to dataset files:", path)

# Train/Test folders are inside PlantVillage
train_path = path + "/PlantVillage/Train"
test_path  = path + "/PlantVillage/Test"

# ==============================
# 3. Load Dataset into Keras
# ==============================
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_path,
    image_size=(128, 128),
    batch_size=32
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    test_path,
    image_size=(128, 128),
    batch_size=32
)

class_names = train_ds.class_names
print("Classes found:", class_names)

# ==============================
# 4. Normalize Images
# ==============================
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds   = val_ds.map(lambda x, y: (normalization_layer(x), y))

# ==============================
# 5. Build CNN Model
# ==============================
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')  # output layer
])

# ==============================
# 6. Compile Model
# ==============================
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# ==============================
# 7. Train Model
# ==============================
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)

# ==============================
# 8. Evaluate Model
# ==============================
loss, acc = model.evaluate(val_ds)
print("Validation Accuracy:", acc)

# ==============================
# 9. Save Model
# ==============================
model.save("plant_disease_model.h5")
print("Model saved as plant_disease_model.h5")

# ==============================
# 10. Plot Accuracy/Loss
# ==============================
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.legend()
plt.title("Model Accuracy")
plt.show()

plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()
plt.title("Model Loss")
plt.show()

# ==============================
# 11. Test on a Custom Image
# ==============================
# Example: replace with your own image path
img_path = test_path + "/Tomato___Late_blight/00001.jpg"

img = load_img(img_path, target_size=(128,128))
img_array = img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)
pred_class = class_names[np.argmax(prediction)]

print("Predicted Class:", pred_class)
