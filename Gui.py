from fileinput import filename
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from detector import PlantDiseaseDetector

class LeafSenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LeafSense - AI Disease Detector")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(True, True)
        
        # Colors
        self.bg_color = "#1a1a1a"
        self.card_color = "#2d2d2d"
        self.accent_color = "#00c851"
        self.secondary_color = "#4CAF50"
        self.text_color = "#ffffff"
        self.text_secondary = "#bcbcbc"
        
        # Initialize pages
        self.current_page = None
        self.show_home_page()
        
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_header(self, parent):
        """Create header with navigation"""
        header_frame = tk.Frame(parent, bg=self.card_color, height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.card_color)
        title_frame.pack(side="left", fill="y", padx=20)
        
        title_label = tk.Label(title_frame, text="🌿 LeafSense", 
                              font=("Arial", 24, "bold"), 
                              fg=self.accent_color, bg=self.card_color)
        title_label.pack(side="left", pady=20)
        
        subtitle_label = tk.Label(title_frame, text="AI Disease Detector", 
                                 font=("Arial", 12), 
                                 fg=self.text_secondary, bg=self.card_color)
        subtitle_label.pack(side="left", padx=(10, 0), pady=20)
        
        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg=self.card_color)
        nav_frame.pack(side="right", fill="y", padx=20)
        
        home_btn = tk.Button(nav_frame, text="Home", 
                            font=("Arial", 11, "bold"),
                            bg=self.accent_color if self.current_page == "home" else self.card_color,
                            fg=self.text_color,
                            border=0, padx=20, pady=10,
                            command=self.show_home_page)
        home_btn.pack(side="left", padx=(0, 10), pady=15)
        
        upload_btn = tk.Button(nav_frame, text="Upload & Detect", 
                              font=("Arial", 11, "bold"),
                              bg=self.accent_color if self.current_page == "upload" else self.card_color,
                              fg=self.text_color,
                              border=0, padx=20, pady=10,
                              command=self.show_upload_page)
        upload_btn.pack(side="left", pady=15)
    
    def show_home_page(self):
        """Display the home page"""
        self.current_page = "home"
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame)
        
        # Main content
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Hero section
        hero_frame = tk.Frame(content_frame, bg=self.card_color, height=300)
        hero_frame.pack(fill="x", pady=(0, 20))
        hero_frame.pack_propagate(False)
        
        hero_content = tk.Frame(hero_frame, bg=self.card_color)
        hero_content.pack(expand=True)
        
        # Hero text
        hero_title = tk.Label(hero_content, text="Detect Plant Diseases with AI", 
                             font=("Arial", 32, "bold"), 
                             fg=self.text_color, bg=self.card_color)
        hero_title.pack(pady=(40, 10))
        
        hero_subtitle = tk.Label(hero_content, 
                                text="Upload an image of your plant leaf and get instant AI-powered disease detection", 
                                font=("Arial", 14), 
                                fg=self.text_secondary, bg=self.card_color)
        hero_subtitle.pack(pady=(0, 20))
        
        # CTA button
        cta_button = tk.Button(hero_content, text="Start Detection →", 
                              font=("Arial", 16, "bold"),
                              bg=self.accent_color, fg=self.text_color,
                              border=0, padx=40, pady=15,
                              command=self.show_upload_page)
        cta_button.pack(pady=20)
        
        # Features section
        features_frame = tk.Frame(content_frame, bg=self.bg_color)
        features_frame.pack(fill="both", expand=True)
        
        features_title = tk.Label(features_frame, text="Key Features", 
                                 font=("Arial", 24, "bold"), 
                                 fg=self.text_color, bg=self.bg_color)
        features_title.pack(pady=(0, 30))
        
        # Feature cards
        cards_frame = tk.Frame(features_frame, bg=self.bg_color)
        cards_frame.pack(fill="x")
        
        # Feature 1
        card1 = tk.Frame(cards_frame, bg=self.card_color, width=300, height=200)
        card1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        card1.pack_propagate(False)
        
        tk.Label(card1, text="🔍", font=("Arial", 30), 
                fg=self.accent_color, bg=self.card_color).pack(pady=(30, 10))
        tk.Label(card1, text="AI-Powered Detection", font=("Arial", 16, "bold"), 
                fg=self.text_color, bg=self.card_color).pack(pady=(0, 10))
        tk.Label(card1, text="Advanced machine learning\nalgorithms for accurate\ndisease identification", 
                font=("Arial", 11), fg=self.text_secondary, bg=self.card_color).pack()
        
        # Feature 2
        card2 = tk.Frame(cards_frame, bg=self.card_color, width=300, height=200)
        card2.pack(side="left", fill="both", expand=True, padx=10)
        card2.pack_propagate(False)
        
        tk.Label(card2, text="⚡", font=("Arial", 30), 
                fg=self.accent_color, bg=self.card_color).pack(pady=(30, 10))
        tk.Label(card2, text="Instant Results", font=("Arial", 16, "bold"), 
                fg=self.text_color, bg=self.card_color).pack(pady=(0, 10))
        tk.Label(card2, text="Get disease detection\nresults in seconds with\nconfidence scores", 
                font=("Arial", 11), fg=self.text_secondary, bg=self.card_color).pack()
        
        # Feature 3
        card3 = tk.Frame(cards_frame, bg=self.card_color, width=300, height=200)
        card3.pack(side="left", fill="both", expand=True, padx=(10, 0))
        card3.pack_propagate(False)
        
        tk.Label(card3, text="📊", font=("Arial", 30), 
                fg=self.accent_color, bg=self.card_color).pack(pady=(30, 10))
        tk.Label(card3, text="Detailed Analysis", font=("Arial", 16, "bold"), 
                fg=self.text_color, bg=self.card_color).pack(pady=(0, 10))
        tk.Label(card3, text="Comprehensive reports\nwith treatment\nrecommendations", 
                font=("Arial", 11), fg=self.text_secondary, bg=self.card_color).pack()
    
    def show_upload_page(self):
        """Display the upload page"""
        self.current_page = "upload"
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame)
        
        # Main content
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Upload section
        upload_frame = tk.Frame(content_frame, bg=self.card_color)
        upload_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = tk.Label(upload_frame, text="Upload Plant Image for Analysis", 
                              font=("Arial", 24, "bold"), 
                              fg=self.text_color, bg=self.card_color)
        title_label.pack(pady=(30, 20))
        
        # Content area
        content_area = tk.Frame(upload_frame, bg=self.card_color)
        content_area.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Left side - Upload area
        left_frame = tk.Frame(content_area, bg=self.card_color)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Drag & drop area
        self.upload_area = tk.Frame(left_frame, bg="#3a3a3a", height=300, width=400, bd=2)
        self.upload_area.pack(fill="x", pady=(0, 20))
        self.upload_area.pack_propagate(False)
        
        upload_content = tk.Frame(self.upload_area, bg="#3a3a3a")
        upload_content.pack(expand=True)
        
        # Upload icon and text
        tk.Label(upload_content, text="📁", font=("Arial", 40), 
                fg=self.accent_color, bg="#3a3a3a").pack(pady=(40, 10))
        
        tk.Label(upload_content, text="Drag & Drop your image here", 
                font=("Arial", 14, "bold"), 
                fg=self.text_color, bg="#3a3a3a").pack()
        
        tk.Label(upload_content, text="or", 
                font=("Arial", 12), 
                fg=self.text_secondary, bg="#3a3a3a").pack(pady=10)
        
        # Browse button
        browse_btn = tk.Button(upload_content, text="Browse Files", 
                              font=("Arial", 12, "bold"),
                              bg=self.accent_color, fg=self.text_color,
                              border=0, padx=30, pady=10,
                              command=self.browse_file)
        browse_btn.pack(pady=10)
        
        tk.Label(upload_content, text="Supported formats: JPG, PNG, JPEG", 
                font=("Arial", 10), 
                fg=self.text_secondary, bg="#3a3a3a").pack(pady=(10, 0))
        
        # Upload button
        self.upload_btn = tk.Button(left_frame, text="Analyze Image", 
                                   font=("Arial", 14, "bold"),
                                   bg=self.secondary_color, fg=self.text_color,
                                   border=0, padx=40, pady=15,
                                   state="disabled",
                                   command=self.analyze_image)
        self.upload_btn.pack(fill="x")
        
        # Right side - Preview and results
        right_frame = tk.Frame(content_area, bg=self.card_color)
        right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        # Image preview
        preview_label = tk.Label(right_frame, text="Image Preview", 
                                font=("Arial", 16, "bold"), 
                                fg=self.text_color, bg=self.card_color)
        preview_label.pack(anchor="w", pady=(0, 10))
        
        self.preview_frame = tk.Frame(right_frame, bg="#3a3a3a", height=200)
        self.preview_frame.pack(fill="x", pady=(0, 20))
        self.preview_frame.pack_propagate(False)
        
        self.preview_label = tk.Label(self.preview_frame, text="No image selected", 
                                     font=("Arial", 12), 
                                     fg=self.text_secondary, bg="#3a3a3a")
        self.preview_label.pack(expand=True)
        
        # Results area
        results_label = tk.Label(right_frame, text="Analysis Results", 
                                font=("Arial", 16, "bold"), 
                                fg=self.text_color, bg=self.card_color)
        results_label.pack(anchor="w", pady=(0, 10))
        
        self.results_frame = tk.Frame(right_frame, bg="#3a3a3a")
        self.results_frame.pack(fill="both", expand=True)
        
        self.results_text = tk.Text(self.results_frame, bg="#3a3a3a", 
                                   fg=self.text_color, font=("Arial", 11),
                                   border=0, padx=15, pady=15,
                                   wrap="word", state="disabled")
        self.results_text.pack(fill="both", expand=True)
        
        # Initial results text
        self.results_text.config(state="normal")
        self.results_text.insert("1.0", "Upload an image to see analysis results...")
        self.results_text.config(state="disabled")
        
        self.selected_file = None
    
    def browse_file(self):
        """Open file browser to select image"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Plant Image",
            filetypes=file_types
        )
        
        if filename:
            self.selected_file = filename
            self.display_preview(filename)
            self.upload_btn.config(state="normal", bg=self.accent_color)
    
    def display_preview(self, filename):
        """Display image preview"""
        try:
            # Clear previous preview
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
            
            # Load and resize image
            image = Image.open(filename)
            # Resize image to fit preview area
            image.thumbnail((300, 180), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(self.preview_frame, image=photo, bg="#3a3a3a")
            image_label.image = photo  # Keep a reference
            image_label.pack(expand=True)
            
            # Show filename
            filename_label = tk.Label(self.preview_frame, 
                                     text=os.path.basename(filename), 
                                     font=("Arial", 10), 
                                     fg=self.text_secondary, bg="#3a3a3a")
            filename_label.pack(pady=(5, 10))
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def analyze_image(self):
        """Simulate image analysis"""
        detector = PlantDiseaseDetector()
        test_image = self.selected_file

        if os.path.exists(test_image):
            result = detector.predict(test_image)
            if result:
                print("\n🔍 ANALYSIS COMPLETE")
                print(f"Class: {result['class_name']}")
                print(f"Confidence: {result['confidence']:.2%}")
                
                self.results_text.config(state="normal")
                self.results_text.delete("1.0", "end")

                results=f'''🔍 ANALYSIS COMPLETE 🔍 \n\nClass: {result['class_name']} \n\nConfidence: {result['confidence']:.2%}
                '''

                self.results_text.insert("1.0", results)
                self.results_text.config(state="disabled")
                
            else:
                print("Failed to make prediction")
        else:
            print(f"Image file {test_image} not found")
        
            if not self.selected_file:
                messagebox.showwarning("No Image", "Please select an image first.")
                return
        
        # Simulate analysis (replace with actual AI model)
        
        messagebox.showinfo("Analysis Complete", "Image analysis completed successfully!")

def main():
    root = tk.Tk()
    app = LeafSenseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
