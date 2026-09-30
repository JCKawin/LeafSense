# LeafSense

Desktop window that classifies a leaf photo and shows a treatment note from the table in `Gui.py`.

Weights are `converted_keras/keras_model.h5`. The 15 classes are in `converted_keras/labels.txt`: tomato, potato, and bell pepper, healthy and the diseases listed there. Images are resized to 224×224.

```bash
pip install -r requirements.txt
python Gui.py
```

`requirements.txt` pins TensorFlow 2.12 and Keras 2.12. Those wheels need a Python of that era; 3.10 is the one this was set up on.

`python detector.py` runs the same model on `checkimg.JPG` and prints the class scores.

The file dialog accepts `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, and `.tiff`.

GPL-3.0. See `LICENSE`.

- [JCKawin](https://github.com/JCKawin)
- [Guru Kamalesh](https://github.com/guru-kamalesh)
- [Adithiaya](https://github.com/adithiyaks)
- [Raghav](https://github.com/raghavkrishnab2025-max)
