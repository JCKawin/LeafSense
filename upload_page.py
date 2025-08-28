import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os
from classifier import Classify

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("LeafSense - Plant Disease Detection")
        self.geometry("800x600")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="LeafSense", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.upload_button = ctk.CTkButton(self.sidebar_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=1, column=0, padx=20, pady=10)

        self.analyze_button = ctk.CTkButton(self.sidebar_frame, text="Analyze Image", command=self.analyze_image)
        self.analyze_button.grid(row=2, column=0, padx=20, pady=10)
        self.analyze_button.configure(state="disabled")

        # Create main frame for image display
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create frame for image display
        self.image_frame = ctk.CTkFrame(
            self.main_frame,
            width=400,
            height=400
        )
        self.image_frame.grid(row=0, column=0, padx=20, pady=20)
        self.image_frame.grid_propagate(False)  # Prevent frame from shrinking

        # Create CTkLabel for image display
        self.display_text = "No image selected\nClick 'Upload Image' to begin"
        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text=self.display_text,
            font=ctk.CTkFont(size=16),
            width=400,
            height=400
        )
        self.image_label.place(relx=0.5, rely=0.5, anchor='center')

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="sw")

        # Store references
        self._image = None
        self._photo = None
        self.current_image = None
        self.image_reference = None  # Add a persistent reference for the image

    def upload_image(self):
        try:
            # Get file path
            file_path = filedialog.askopenfilename(
                filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp *.gif')]
            )
            
            if not file_path:
                return

            # Load and process image
            image = Image.open(file_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save original for analysis
            self.current_image = image.copy()
            
            # Calculate new size maintaining aspect ratio
            width, height = image.size
            max_size = 380  # Slightly smaller to account for padding
            
            if width > height:
                new_width = max_size
                new_height = int(height * max_size / width)
            else:
                new_height = max_size
                new_width = int(width * max_size / height)
            
            # Create display version
            display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create CTkImage and store reference
            self.image_reference = ctk.CTkImage(
                light_image=display_image,
                dark_image=display_image,
                size=(new_width, new_height)
            )

            # Update label with image
            self.image_label.configure(image=self.image_reference, text="")

            # Enable analyze button and update status
            self.analyze_button.configure(state="normal")
            self.status_label.configure(text=f"Status: Image loaded - {os.path.basename(file_path)}")

        except Exception as e:
            self.status_label.configure(text=f"Error: Failed to load image - {str(e)}")
            self.analyze_button.configure(state="disabled")
            self.current_image = None
            self._photo = None
            self.image_reference = None  # Reset reference on error
            
            # Reset label with error message
            self.image_label.configure(image=None, text="Error loading image\nPlease try again")
            self.image_label.configure(width=400, height=400)  # Reset size

    def analyze_image(self):
        if self.current_image:
            self.status_label.configure(text="Status: Analyzing image...")
            try:
                predictions, index = Classify(self.current_image)
                if index != -1:
                    result = f"Prediction: Class {index} - Confidence: {predictions[index]:.2%}"
                    self.status_label.configure(text=f"Status: Analysis complete! {result}")
                else:
                    self.status_label.configure(text="Status: Analysis failed. Please try another image.")
            except Exception as e:
                self.status_label.configure(text=f"Status: Error during analysis - {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
