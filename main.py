import os
# Set TensorFlow environment variables before importing other modules
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

import customtkinter as ctk
from PIL import Image
from upload_page import App as UploadPage

class HomePage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("LeafSense - Welcome")
        self.geometry("1000x600")

        # Set the appearance mode and default color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Background image path (you'll need to place your image in this location)
        self.bg_image_path = os.path.join("assets", "background.jpg")  # You can change the extension based on your image

        # Create welcome text
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome to LeafSense",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.welcome_label.grid(row=0, column=0, pady=(100, 20))

        # Create description
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Your AI-powered plant disease detection assistant",
            font=ctk.CTkFont(size=20)
        )
        self.desc_label.grid(row=1, column=0, pady=(0, 40))

        # Create Get Started button
        self.start_button = ctk.CTkButton(
            self.main_frame,
            text="Get Started",
            command=self.open_upload_page,
            width=200,
            height=50,
            font=ctk.CTkFont(size=20)
        )
        self.start_button.grid(row=2, column=0, pady=20)

        # Try to load and set background image if it exists
        self.set_background_image()

    def set_background_image(self):
        if os.path.exists(self.bg_image_path):
            try:
                # Load and resize background image
                bg_image = Image.open(self.bg_image_path)
                # Resize to fit window while maintaining aspect ratio
                window_width = 1000
                window_height = 600
                aspect_ratio = bg_image.width / bg_image.height
                
                if window_width / window_height > aspect_ratio:
                    new_width = window_width
                    new_height = int(window_width / aspect_ratio)
                else:
                    new_height = window_height
                    new_width = int(window_height * aspect_ratio)
                
                bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                self.bg_image = ctk.CTkImage(
                    light_image=bg_image,
                    dark_image=bg_image,
                    size=(new_width, new_height)
                )
                
                # Create and place background label
                bg_label = ctk.CTkLabel(
                    self.main_frame,
                    image=self.bg_image,
                    text=""
                )
                bg_label.place(relx=0.5, rely=0.5, anchor="center")
                
                # Ensure other widgets stay on top
                self.welcome_label.lift()
                self.desc_label.lift()
                self.start_button.lift()
            except Exception as e:
                print(f"Error loading background image: {e}")

    def open_upload_page(self):
        self.withdraw()  # Hide the current window
        upload_window = UploadPage()
        
        def on_upload_close():
            upload_window.destroy()
            self.deiconify()  # Show the home page again
        
        upload_window.protocol("WM_DELETE_WINDOW", on_upload_close)
        upload_window.mainloop()

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
