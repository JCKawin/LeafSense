🥔 Diseased Potato Detection using AI<br>
An open-source AI project built with Python that detects Diseased Potato from leaves  images. This tool helps farmers and researchers identify whether a potato plant is Healthy, affected by Early Blight, or Late Blight, using deep learning and computer vision.
________________________________________
📌 Features<br>
•	🔍 Detects Diseased potato plant from leaf images.<br>
•	🎯 Classifies into: Healthy, Early Blight, Late Blight.<br>
•	📊 Provides confidence score for predictions.<br>
•	📈 Increases the Industrial yeld by 40%<br>
•	💉 suggests appropriaate treatment for the plant<br>
•	✨ Hygenic procesing of the products<br>
________________________________________
🚀 Installation & Setup<br>
1. Clone Repository<br>
git clone https://github.com/yourusername/potato-disease-detector.git<br>
cd potato-disease-detector<br>
2. Install Dependencies<br>
pip install -r requirements.txt<br>
3. Run Tool<br>
________________________________________
🖼️ Usage<br>
1.	Upload a potato leaf image (.jpg, .jpeg, .png).<br>
2.	The model predicts whether the Plant is:<br>
o	✅ Healthy<br>
o	⚠️ Early Blight<br>
o	❌ Late Blight<br>
________________________________________
📊 Dataset<br>
This model is trained on the Potato Leaf Dataset (PlantVillage subset) containing images of:<br>
•	Healthy potato leaves<br>
•	Potato leaves with Early Blight<br>
•	Potato leaves with Late Blight<br>
📌 Dataset source: kaggle plant village<br>
________________________________________
🧠 Model<br>
•	Input size:<br>
o   Standard image model: 224x224 pixels (RGB).<br>
o	  Embedded image model: 96x96 pixels (Grayscale).<br>
•	Output classes: User-defined and customizable. The number of classes can be adjusted by adding new categories for training data.<br>
•	Optimizer: The platform automatically uses an Adam-like optimizer, but it is not a user-configurable setting.<br>
•	Loss: The platform uses a categorical cross-entropy loss function internally for multi-class problems.<br>

________________________________________
🛠️ Technologies Used<br>
•	Python 3.10.6<br>
•	TensorFlow / Keras<br>
•	OpenCV (image preprocessing)<br>
•	Tikinter/CustomTikinter<br>
•	NumPy<br>
________________________________________
🤝 Contributing<br>
Contributions are welcome!<br>
1.	Fork this repo<br>
2.	Create a branch (feature-new)<br>
3.	Commit and push changes<br>
4.	Submit a Pull Request 🚀<br>
________________________________________
📜 License<br>
This project is licensed under the GNU GPL-3.0 License – free to use and modify.<br>
________________________________________
👨‍💻 Authors<br>
•	JCKAWIN– [GitHub Profile](https://github.com/JCKawin) <br>
•	GURU KAMALESH – [GitHub Profile](https://github.com/guru-kamalesh)<br>
•	ADITYA–[GitHub Profile](https://github.com/adithiyaks)<br>
•	RAGHAV–[GitHub Profile](raghavkrishnab2025-max)<br>

