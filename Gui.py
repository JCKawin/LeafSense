from fileinput import filename
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from detector import PlantDiseaseDetector


# Disease Database with Index Keys
DISEASE_DATABASE = {
    0: {  # Tomato_healthy
        "name": "Tomato_healthy",
        "status": "Healthy",
        "description": "No disease detected - plant appears healthy",
        "treatment": "No treatment required",
        "monitoring": "Regular inspection for early disease signs",
        "preventive_care": "Maintain proper watering, nutrition, and spacing",
        "severity": "None",
        "scientific_name": "N/A",
        "urgency": "None"
    },
    
    1: {  # Tomato_Mosaic_virus
        "name": "Tomato_Mosaic_virus",
        "status": "Viral Disease",
        "description": "Mosaic virus causing leaf mottling, yellowing, and plant stunting",
        "immediate_action": "Remove infected plants immediately and dispose by burning",
        "biological_control": "Bacillus amyloliquefaciens foliar spray (90% reduction in viral load)",
        "chemical_treatment": "No direct chemical control; focus on vector control",
        "cultural_practices": [
            "Use resistant varieties (EC-771607, Hisar Anmol)",
            "Sanitize tools with 10% bleach solution",
            "Control aphid vectors with insecticidal soap"
        ],
        "prevention": "Certified virus-free seeds, crop rotation (2-3 years)",
        "severity": "High",
        "scientific_name": "Tomato mosaic virus (ToMV)",
        "urgency": "Immediate"
    },
    
    2: {  # Tomato_YellowLeaf_Curl_Virus
        "name": "Tomato_YellowLeaf_Curl_Virus",
        "status": "Viral Disease",
        "description": "Whitefly-transmitted virus causing leaf yellowing, curling, and stunting",
        "immediate_action": "Remove symptomatic plants in sealed bags",
        "vector_control": [
            "UV-reflective mulch to deter whiteflies",
            "Imidacloprid-based systemic insecticides (Admire Pro, Provado)",
            "Yellow sticky traps"
        ],
        "cultural_practices": [
            "Remove solanaceous weeds within 100m radius",
            "Use whitefly-exclusion screens for high-value crops",
            "Plant TYLCV-resistant varieties"
        ],
        "organic_treatment": "Neem oil spray weekly + mustard oil cake soil amendment",
        "severity": "High",
        "scientific_name": "Tomato yellow leaf curl virus (TYLCV)",
        "urgency": "Immediate"
    },
    
    3: {  # Tomato_Target_Spot
        "name": "Tomato_Target_Spot",
        "status": "Fungal Disease",
        "description": "Fungal disease causing brown spots with concentric rings on leaves",
        "chemical_control": "Azoxystrobin 250g/L SC (10ml/10L water)",
        "alternative_treatment": "Mancozeb 80% WP (20g/10L water)",
        "application": "Weekly sprays during humid conditions",
        "cultural_practices": "Improve air circulation, avoid overhead irrigation",
        "organic": "Acibenzolar-S-methyl (SAR activator) - 42% defoliation reduction",
        "severity": "Medium",
        "scientific_name": "Corynespora cassiicola",
        "urgency": "Within 48 hours"
    },
    
    4: {  # Tomato_spider_mites_Two_spotted
        "name": "Tomato_spider_mites_Two_spotted",
        "status": "Pest Infestation",
        "description": "Two-spotted spider mites causing stippling, webbing, and leaf damage",
        "biological_control": "Tobacco leaf extract spray (most effective organic treatment)",
        "predatory_control": "Predatory mites release (Phytoseiulus persimilis)",
        "cultural_control": "Tomato-onion intercropping (91.2% population reduction)",
        "chemical_control": "Miticides (abamectin, spiromesifen) if biological methods fail",
        "environmental": "Increase humidity, reduce plant stress",
        "severity": "Medium",
        "scientific_name": "Tetranychus urticae",
        "urgency": "Within 1 week"
    },
    
    5: {  # Tomato_Septoria
        "name": "Tomato_Septoria",
        "status": "Fungal Disease",
        "description": "Septoria leaf spot causing small dark spots with light centers",
        "chemical_control": "Azoxystrobin (Quadris), Pyraclostrobin (Cabrio)",
        "secondary_treatment": "Mancozeb, chlorothalonil (Bravo), copper fungicides",
        "organic_control": "Trichoderma spp. bioagent (2g/L water)",
        "cultural_practices": "Crop rotation, remove lower leaves, avoid overhead watering",
        "application_schedule": "Weekly during favorable conditions (warm, humid)",
        "severity": "Medium",
        "scientific_name": "Septoria lycopersici",
        "urgency": "Within 3 days"
    },
    
    6: {  # Tomato_Leaf_Mold
        "name": "Tomato_Leaf_Mold",
        "status": "Fungal Disease",
        "description": "Leaf mold causing yellow patches and fuzzy gray-brown growth",
        "environmental_control": "Maintain RH below 85%, improve ventilation",
        "chemical_treatment": "Amistar (azoxystrobin) - translaminar action",
        "biological_treatment": "Serenade ASO (Bacillus subtilis) - early application",
        "cultural_practices": "Remove lower leaves for better airflow, use resistant varieties",
        "sanitation": "Comprehensive cleanup, disinfect with Hortisept Pro",
        "severity": "Medium",
        "scientific_name": "Passalora fulva",
        "urgency": "Within 5 days"
    },
    
    7: {  # Tomato_Late_blight
        "name": "Tomato_Late_blight",
        "status": "Fungal Disease",
        "description": "Late blight causing dark lesions and white fuzzy growth",
        "chemical_control": "Chlorothalonil (Bravo, Daconil), Mancozeb",
        "organic_treatment": "Fixed copper products (Kocide)",
        "cultural_practices": "Remove volunteer tomatoes and nightshades, avoid sprinkler irrigation",
        "application": "Weekly sprays during wet weather, start at flowering",
        "critical": "Disc fields in fall to eliminate overwintering fungus",
        "severity": "High",
        "scientific_name": "Phytophthora infestans",
        "urgency": "Immediate"
    },
    
    8: {  # Tomato_Early_blight
        "name": "Tomato_Early_blight",
        "status": "Fungal Disease",
        "description": "Early blight causing concentric ring spots on older leaves",
        "most_effective": "Neem oil (73.08% disease reduction, 82.03% yield increase)",
        "alternative_treatment": "Harad powder, Sanay powder",
        "integrated_management": "Carbendazim 12% + Mancozeb 63% WP (0.15% concentration)",
        "cultural_practices": "Crop rotation, proper nutrition (especially nitrogen), certified seed",
        "organic": "Castor oil, Aonla powder applications",
        "severity": "Medium",
        "scientific_name": "Alternaria solani",
        "urgency": "Within 48 hours"
    },
    
    9: {  # Tomato_Bacterial_spot
        "name": "Tomato_Bacterial_spot",
        "status": "Bacterial Disease",
        "description": "Bacterial spot causing small dark spots with yellow halos",
        "chemical_control": "Copper hydroxide (Kocide 3000) 0.75-1.75 lb/acre",
        "enhanced_treatment": "Copper + Mancozeb combination for resistance management",
        "biological_control": "Trichoderma spp., Bacillus subtilis, Pseudomonas fluorescens",
        "cultural_practices": "Use pathogen-free seed, avoid sprinkler irrigation, 3-year crop rotation",
        "application": "10-14 day intervals during warm, moist conditions",
        "severity": "Medium",
        "scientific_name": "Xanthomonas spp.",
        "urgency": "Within 24 hours"
    },
    
    10: {  # Potato_healthy
        "name": "Potato_healthy",
        "status": "Healthy",
        "description": "No disease detected - potato plant appears healthy",
        "treatment": "No treatment required",
        "monitoring": "Regular field scouting, especially during humid conditions",
        "severity": "None",
        "scientific_name": "N/A",
        "urgency": "None"
    },
    
    11: {  # Potato_Late_blight
        "name": "Potato_Late_blight",
        "status": "Fungal Disease",
        "description": "Late blight causing dark lesions and white growth on potato leaves",
        "most_effective": "Azoxystrobin + Tebuconazole (1ml/L water)",
        "standard_treatment": "Mancozeb, chlorothalonil, metalaxyl combinations",
        "cultural_practices": "Plant certified seed tubers, eliminate cull piles and volunteers",
        "harvest_management": "Wait 2-3 weeks after vine death before harvest",
        "critical": "Apply fungicides before infection during favorable conditions",
        "severity": "High",
        "scientific_name": "Phytophthora infestans",
        "urgency": "Immediate"
    },
    
    12: {  # Potato_Early_blight
        "name": "Potato_Early_blight",
        "status": "Fungal Disease",
        "description": "Early blight causing concentric ring spots on potato leaves",
        "primary_treatment": "Carbendazim 12% + Mancozeb 63% WP (0.15%)",
        "alternative": "Hexaconazole 5 EC (most effective systemic)",
        "integrated_management": "Mancozeb seed treatment + foliar hexaconazole + Trichoderma harzianum",
        "cultural_practices": "Crop rotation, proper nitrogen management, fall tillage",
        "application": "Start at tuber initiation stage",
        "severity": "Medium",
        "scientific_name": "Alternaria solani",
        "urgency": "Within 48 hours"
    },
    
    13: {  # Pepper_bell_healthy
        "name": "Pepper_bell_healthy",
        "status": "Healthy",
        "description": "No disease detected - pepper plant appears healthy",
        "treatment": "No treatment required",
        "monitoring": "Weekly scouting for bacterial spot symptoms",
        "severity": "None",
        "scientific_name": "N/A",
        "urgency": "None"
    },
    
    14: {  # Pepper_bell_Bacterial_spot
        "name": "Pepper_bell_Bacterial_spot",
        "status": "Bacterial Disease",
        "description": "Bacterial spot causing dark spots with yellow halos on pepper leaves",
        "seed_treatment": "Hot water treatment (custom by seed company)",
        "alternative_seed": "Sodium hypochlorite (Clorox) treatment",
        "chemical_control": "Fixed copper bactericides (7-10 day schedule)",
        "biological_control": "AgriPhage (bacteriophages) for organic production",
        "cultural_practices": "Use resistant varieties, trickle irrigation only, 3-year crop rotation",
        "field_management": "Scout weekly, rogue infected plants immediately",
        "severity": "Medium",
        "scientific_name": "Xanthomonas spp.",
        "urgency": "Within 24 hours"
    }
}


def get_disease_info(class_index):
    """Get disease information by class index"""
    return DISEASE_DATABASE.get(class_index, {
        "name": "Unknown Disease",
        "status": "Unknown Disease",
        "description": "Disease information not available",
        "treatment": "Consult local agricultural expert",
        "severity": "Unknown",
        "urgency": "Consult expert"
    })


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

        #Initialize Classifier
        self.detector = PlantDiseaseDetector()
        
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
        
        # Add scrollbar to results
        results_container = tk.Frame(self.results_frame, bg="#3a3a3a")
        results_container.pack(fill="both", expand=True)
        
        self.results_text = tk.Text(results_container, bg="#3a3a3a", 
                                   fg=self.text_color, font=("Arial", 11),
                                   border=0, padx=15, pady=15,
                                   wrap="word", state="disabled")
        
        scrollbar = tk.Scrollbar(results_container, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial results text
        self.results_text.config(state="normal")
        self.results_text.insert("1.0", "🤖 Upload an image to see AI analysis results...\n\nWaiting for plant leaf image upload.")
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
            print(f"Selected image path: {self.selected_file}")  # Debug print
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
        """Analyze image with AI model and display comprehensive results"""
        if not self.selected_file:
            messagebox.showwarning("No Image", "Please select an image first.")
            return
        
        # Show loading message
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "🤖 AI is analyzing your image...\nPlease wait...")
        self.results_text.config(state="disabled")
        self.root.update()
        
        # Initialize detector and predict
        
        test_image = self.selected_file
        
        if os.path.exists(test_image):
            result = self.detector.predict(test_image)
            if result:
                # Print to console
                print(f"\n🔍 ANALYSIS COMPLETE")
                print(f"Class: {result['class_name']}")
                print(f"Class Index: {result['class_index']}")
                print(f"Confidence: {result['confidence']:.2%}")
                
                # Display comprehensive results in UI
                self.display_comprehensive_results(result)
                
            else:
                self.show_error_results("Failed to make prediction")
        else:
            self.show_error_results(f"Image file {test_image} not found")
    
    def display_comprehensive_results(self, result):
        """Display comprehensive AI analysis results with treatment information"""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", "end")
        
        class_index = result['class_index']
        confidence_percent = result['confidence'] * 100
        
        # Get disease information from database using index
        disease_info = get_disease_info(class_index)
        
        # Determine confidence status
        if confidence_percent >= 80:
            status_icon = "🟢"
            status_text = "HIGH CONFIDENCE"
        elif confidence_percent >= 60:
            status_icon = "🟡"
            status_text = "MEDIUM CONFIDENCE"
        else:
            status_icon = "🔴"
            status_text = "LOW CONFIDENCE"
        
        # Build comprehensive results text
        results_text = f"""🤖 AI ANALYSIS COMPLETE

{status_icon} DETECTED: {disease_info.get('name', 'Unknown')}
📊 Confidence: {confidence_percent:.1f}% ({status_text})
⚠️ Status: {disease_info.get('status', 'Unknown')}
🧬 Scientific Name: {disease_info.get('scientific_name', 'Unknown')}
🚨 Severity Level: {disease_info.get('severity', 'Unknown')}
⏰ Action Required: {disease_info.get('urgency', 'Consult expert')}

📝 DESCRIPTION:
{disease_info.get('description', 'No description available')}

"""
        
        # Add treatment information based on disease type
        if disease_info.get('status') == 'Healthy':
            results_text += f"""✅ PLANT STATUS: HEALTHY
• {disease_info.get('treatment', 'No treatment required')}
• {disease_info.get('monitoring', 'Continue regular monitoring')}
• {disease_info.get('preventive_care', 'Maintain good growing conditions')}
"""
        else:
            # Add immediate action if available
            immediate_action = disease_info.get('immediate_action')
            if immediate_action:
                results_text += f"""🚨 IMMEDIATE ACTION:
• {immediate_action}

"""
            
            # Add primary treatments
            treatments = []
            for key in ['chemical_control', 'most_effective', 'primary_treatment', 'environmental_control']:
                if disease_info.get(key):
                    treatments.append(disease_info[key])
            
            if treatments:
                results_text += "💊 PRIMARY TREATMENTS:\n"
                for treatment in treatments:
                    results_text += f"• {treatment}\n"
                results_text += "\n"
            
            # Add alternative treatments
            alternatives = []
            for key in ['alternative_treatment', 'secondary_treatment', 'biological_control', 'organic_treatment']:
                if disease_info.get(key):
                    alternatives.append(disease_info[key])
            
            if alternatives:
                results_text += "🌿 ALTERNATIVE TREATMENTS:\n"
                for alt in alternatives:
                    if isinstance(alt, list):
                        for item in alt:
                            results_text += f"• {item}\n"
                    else:
                        results_text += f"• {alt}\n"
                results_text += "\n"
            
            # Add cultural practices
            cultural = disease_info.get('cultural_practices')
            if cultural:
                results_text += "🌱 CULTURAL PRACTICES:\n"
                if isinstance(cultural, list):
                    for practice in cultural:
                        results_text += f"• {practice}\n"
                else:
                    results_text += f"• {cultural}\n"
                results_text += "\n"
            
            # Add application schedule
            application = disease_info.get('application') or disease_info.get('application_schedule')
            if application:
                results_text += f"📅 APPLICATION SCHEDULE:\n• {application}\n\n"
            
            # Add prevention
            prevention = disease_info.get('prevention')
            if prevention:
                results_text += f"🛡️ PREVENTION:\n• {prevention}\n\n"
        
        # Add model confidence breakdown
        results_text += "📈 AI MODEL CONFIDENCE:\n"
        # Show top 5 predictions
        sorted_predictions = sorted(enumerate(result['all_probabilities']), 
                                  key=lambda x: x[1], reverse=True)[:5]
        
        for i, (class_idx, prob) in enumerate(sorted_predictions):
            if class_idx < len(self.detector.class_names):
                class_name = self.detector.class_names[class_idx]
            else:
                class_name = f"Class {class_idx}"
            
            percentage = prob * 100
            bar = "█" * int(percentage / 5)  # Visual bar
            if i == 0:  # Highlight top prediction
                results_text += f"→ {class_name}: {percentage:.1f}% {bar}\n"
            else:
                results_text += f"  {class_name}: {percentage:.1f}% {bar}\n"
        
        # Add technical info and recommendations
        results_text += f"""
🔬 TECHNICAL INFO:
• Model: TensorFlow/Keras Deep Learning
• Classes: {len(self.detector.class_names)} disease types
• Input: 224x224 pixel analysis
• Processing: Real-time CNN analysis

💡 RECOMMENDATIONS:"""
        
        if confidence_percent >= 80:
            results_text += """
• High confidence - proceed with treatment
• Monitor plant response in 3-5 days
• Follow application guidelines strictly"""
        elif confidence_percent >= 60:
            results_text += """
• Medium confidence - consider expert consultation
• Verify with additional symptoms
• Start with safest treatment option"""
        else:
            results_text += """
• Low confidence - seek expert diagnosis
• Retake photo with better conditions
• Consider laboratory testing"""
        
        # Insert all text and disable editing
        self.results_text.insert("1.0", results_text)
        self.results_text.config(state="disabled")
        
        # Show completion message
        if confidence_percent >= 60:
            messagebox.showinfo("Analysis Complete", 
                              f"✅ Analysis completed!\n\n"
                              f"Disease: {disease_info.get('name', 'Unknown')}\n"
                              f"Confidence: {confidence_percent:.1f}%\n"
                              f"Urgency: {disease_info.get('urgency', 'See results')}")
        else:
            messagebox.showwarning("Low Confidence", 
                                 f"⚠️ Low confidence result ({confidence_percent:.1f}%)\n\n"
                                 f"Consider retaking photo or expert consultation.")
    
    def show_error_results(self, error_message):
        """Display error message in results area"""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", "end")
        
        error_text = f"""❌ ANALYSIS ERROR

{error_message}

🔧 TROUBLESHOOTING:
• Check image format (JPG, PNG, JPEG)
• Ensure clear plant leaf image
• Verify image is not corrupted
• Try better lighting conditions
• Restart application if needed

📋 REQUIREMENTS:
• Clear, well-focused leaf image
• Good lighting conditions
• Minimal background distractions
• Supported file formats only

🆘 IF PROBLEMS PERSIST:
• Contact technical support
• Check model files are present
• Verify system requirements"""
        
        self.results_text.insert("1.0", error_text)
        self.results_text.config(state="disabled")
        
        messagebox.showerror("Analysis Error", f"Error: {error_message}")


def main():
    root = tk.Tk()
    app = LeafSenseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
