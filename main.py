import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
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
        self.analyze_button.configure(state="disabled")  # Disabled until image is uploaded

        # Create main frame for image display
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Image display label
        self.image_label = ctk.CTkLabel(self.main_frame, text="No image selected\nClick 'Upload Image' to begin", 
                                      font=ctk.CTkFont(size=16))
        self.image_label.grid(row=0, column=0, padx=20, pady=20)

        # Status label
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", font=ctk.CTkFont(size=13))
        self.status_label.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="sw")

        self.current_image = None
        self.image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Image Files', '*.png *.jpg *.jpeg *.bmp *.gif')]
        )
        if file_path:
            try:
                # Open and display the image
                image = Image.open(file_path)
                
                # Calculate size to maintain aspect ratio and fit in window
                display_size = (400, 400)
                image.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Update image label
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Keep a reference!
                
                # Store current image and path
                self.current_image = image
                self.image_path = file_path
                
                # Update status and enable analyze button
                self.status_label.configure(text=f"Status: Image loaded - {os.path.basename(file_path)}")
                self.analyze_button.configure(state="normal")
                
            except Exception as e:
                self.status_label.configure(text=f"Error: Failed to load image - {str(e)}")
                self.analyze_button.configure(state="disabled")

    def analyze_image(self):
        if self.current_image:
            Classify(self.current_image)
            # TODO: Add your image analysis code here
            self.status_label.configure(text="Status: Analyzing image...")
            # For now, just show a placeholder message
            self.status_label.configure(text="Status: Analysis complete! (Placeholder)")

if __name__ == "__main__":
    app = App()
    app.mainloop()
