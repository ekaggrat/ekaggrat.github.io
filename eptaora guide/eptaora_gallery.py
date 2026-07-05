import os
import json
import re
from datetime import datetime

# --- CONFIGURATION ---
IMAGE_FOLDER = 'images'  
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

# --- GALLERY SIZING VARIABLES ---
GALLERY_MAX_WIDTH = '1200px'  # Try '100%', '90vw', or specific pixel widths like '1400px'
GALLERY_ASPECT_RATIO = 'aspect-[16/9]' # e.g., 'aspect-video', 'aspect-[4/3]'


# --- HTML TEMPLATES ---

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[PROJECT_TITLE] - EKAGGRAT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;400;600&display=swap');
        body { font-family: 'Manrope', sans-serif; background-color: #ffffff; }
    </style>
</head>
<body class="text-black overflow-x-hidden">
    
    <header class="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-sm z-50 py-6 px-8 flex justify-between items-center border-b border-gray-100">
        <div class="flex items-center gap-4">
            <img src="images/logo.png" alt="Logo" class="h-5 w-auto object-contain" onerror="this.style.display='none'">
            <div class="text-lg font-semibold tracking-[0.2em] uppercase">
                Ekaggart Singh Kalsi
            </div>
        </div>
        <nav class="flex space-x-8 text-xs font-medium tracking-widest uppercase text-gray-500">
            <a href="https://ekaggrat.com" class="hover:text-black transition-colors">Home</a>
        </nav>
    </header>

    <div class="w-full pt-32 pb-10 px-2 md:px-8">
        <h1 class="text-2xl font-bold tracking-[0.3em] uppercase text-gray-800 mb-12 text-center">
            [PROJECT_TITLE]
        </h1>

        <div class="flex items-center justify-center w-full mx-auto gap-2 md:gap-6" style="max-width: [GALLERY_MAX_WIDTH];">
            
            <div class="flex-none">
                <button type="button" onclick="moveSlide(-1)" class="w-10 h-10 md:w-14 md:h-14 flex items-center justify-center bg-gray-50 hover:bg-gray-200 text-black rounded-full border border-gray-300 shadow-sm transition-colors focus:outline-none cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-6 h-6 md:w-8 md:h-8">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                    </svg>
                </button>
            </div>

            <div class="flex-auto min-w-0 relative overflow-hidden bg-gray-100 border border-gray-200 shadow-sm [GALLERY_ASPECT_RATIO]">
                
                <div id="carousel-track" class="flex w-full h-full transition-transform duration-500 ease-out">
"""

ITEM_TEMPLATE = """
                    <div class="flex-none w-full h-full relative">
                        <img 
                            src="[FILEPATH]" 
                            alt="[CLEAN_NAME]" 
                            class="absolute inset-0 w-full h-full object-contain"
                            onerror="this.onerror=null; this.src='https://placehold.co/1920x1080/f3f3f3/333?text=IMAGE+NOT+FOUND';"
                        >
                    </div>
"""

YOUTUBE_TEMPLATE = """
                    <div class="flex-none w-full h-full relative bg-gray-900">
                        <div class="absolute inset-0 flex flex-col items-center justify-center text-center p-4">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-16 h-16 text-white/50 mb-4">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z" />
                            </svg>
                            <span class="text-lg md:text-xl font-bold tracking-widest uppercase text-white/70">YouTube Embed</span>
                            <span class="text-xs md:text-sm text-white/50 mt-2">Replace this wrapper with your standard YouTube <iframe></span>
                        </div>
                    </div>
"""

FOOTER_TEMPLATE = """
                </div>
                
                <div id="carousel-dots" class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 md:gap-3 z-20 bg-white/60 px-4 py-2 rounded-full backdrop-blur-sm shadow-sm border border-white/40">
                    </div>
            </div>

            <div class="flex-none">
                <button type="button" onclick="moveSlide(1)" class="w-10 h-10 md:w-14 md:h-14 flex items-center justify-center bg-gray-50 hover:bg-gray-200 text-black rounded-full border border-gray-300 shadow-sm transition-colors focus:outline-none cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-6 h-6 md:w-8 md:h-8">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                </button>
            </div>

        </div>

        <div class="mt-24 max-w-4xl mx-auto px-4 md:px-0">
            <h2 class="text-xl font-bold tracking-[0.2em] uppercase mb-6">Description</h2>
            <p class="text-sm text-gray-600 leading-relaxed mb-12 whitespace-pre-wrap">[PROJECT_TEXT]</p>
            
            <h3 class="text-sm font-bold tracking-[0.2em] uppercase mb-4 text-gray-800">My Role</h3>
            <p class="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">[MY_ROLE_TEXT]</p>
        </div>

        <footer class="mt-32 border-t border-gray-200 pt-8 flex flex-col md:flex-row justify-between items-center text-[10px] tracking-widest uppercase text-gray-400 max-w-[1600px] mx-auto px-4 md:px-12 pb-12">
            <div>&copy; """ + str(datetime.now().year) + """ Ekaggrat Studio</div>
            <div class="mt-4 md:mt-0 space-x-6">
                <a href="#" class="hover:text-black">Instagram</a>
                <a href="#" class="hover:text-black">LinkedIn</a>
                <a href="#" class="hover:text-black">Behance</a>
            </div>
        </footer>
    </div>
"""

JS_TEMPLATE = """
    <script>
        let currentSlide = 0;
        let totalSlides = 0;
        let track;
        let dotsContainer;

        document.addEventListener('DOMContentLoaded', () => {
            track = document.getElementById('carousel-track');
            dotsContainer = document.getElementById('carousel-dots');
            const slides = document.querySelectorAll('#carousel-track > div');
            totalSlides = slides.length;
            
            // Generate interactive dots
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('button');
                dot.type = 'button';
                dot.className = `w-2 h-2 md:w-3 md:h-3 rounded-full transition-all duration-300 shadow-sm border border-gray-500 focus:outline-none ${i === 0 ? 'bg-black w-6 md:w-8' : 'bg-white hover:bg-gray-300'}`;
                dot.onclick = () => goToSlide(i);
                dotsContainer.appendChild(dot);
            }
        });

        function moveSlide(direction) {
            if (totalSlides === 0) return;
            currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
            updateCarousel();
        }

        function goToSlide(index) {
            if (totalSlides === 0) return;
            currentSlide = index;
            updateCarousel();
        }

        function updateCarousel() {
            if (track) {
                track.style.transform = `translateX(-${currentSlide * 100}%)`;
            }
            
            // Visually update the dots
            const dots = dotsContainer.children;
            for (let i = 0; i < dots.length; i++) {
                if (i === currentSlide) {
                    dots[i].className = 'w-6 h-2 md:w-8 md:h-3 rounded-full transition-all duration-300 bg-black shadow-sm border border-black focus:outline-none';
                } else {
                    dots[i].className = 'w-2 h-2 md:w-3 md:h-3 rounded-full transition-all duration-300 bg-white hover:bg-gray-300 shadow-sm border border-gray-500 focus:outline-none';
                }
            }
        }

        // Keyboard navigation support
        document.addEventListener('keydown', function(event) {
            if (event.key === "ArrowRight") moveSlide(1);
            if (event.key === "ArrowLeft") moveSlide(-1);
        });
    </script>
</body>
</html>
"""

def clean_filename(filename):
    name, _ = os.path.splitext(filename)
    clean = name.replace("-", " ").replace("_", " ")
    clean = clean.replace("(", " ").replace(")", "")
    return clean

def get_sort_key(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def generate_gallery():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_folder_name = os.path.basename(script_dir)
    output_file = f"{parent_folder_name}.html"

    print(f"Detected project folder: {parent_folder_name}")
    print(f"Scanning subfolder: {IMAGE_FOLDER}...")
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Subfolder '{IMAGE_FOLDER}' not found.")
        return

    # 1. Grab text file for title and description
    txt_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith('.txt') and f.lower() != 'myrole.txt']
    project_text = "No project description text file found."
    project_title = parent_folder_name.replace("-", " ").replace("_", " ").upper()
    
    if txt_files:
        text_filename = txt_files[0]
        text_file_path = os.path.join(IMAGE_FOLDER, text_filename)
        project_title = clean_filename(text_filename).upper()
        with open(text_file_path, 'r', encoding='utf-8') as tf:
            project_text = tf.read()

    # Grab 'myrole.txt' for the Role section
    my_role_text = "Role information not found."
    role_file_path = os.path.join(IMAGE_FOLDER, 'myrole.txt')
    if os.path.exists(role_file_path):
        with open(role_file_path, 'r', encoding='utf-8') as rf:
            my_role_text = rf.read()

    # 2. Grab images
    files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS and f.lower() != 'logo.png']
    
    if not files:
        print("No images found in images subfolder.")
        return

    files.sort(key=get_sort_key)

    # 3. Build HTML items
    gallery_items = ""
    
    for index, filename in enumerate(files):
        file_path = f"{IMAGE_FOLDER}/{filename}"
        clean_name = clean_filename(filename)
        
        item_html = ITEM_TEMPLATE.replace("[FILEPATH]", file_path)
        item_html = item_html.replace("[CLEAN_NAME]", clean_name)
        gallery_items += item_html
        
        # Inject YouTube placeholder after every 3rd image
        if (index + 1) % 3 == 0:
            gallery_items += YOUTUBE_TEMPLATE

    # 4. Assemble full HTML
    header_html = HTML_HEADER.replace("[PROJECT_TITLE]", project_title)
    header_html = header_html.replace("[GALLERY_MAX_WIDTH]", GALLERY_MAX_WIDTH)
    header_html = header_html.replace("[GALLERY_ASPECT_RATIO]", GALLERY_ASPECT_RATIO)
    
    footer_html = FOOTER_TEMPLATE.replace("[PROJECT_TEXT]", project_text)
    footer_html = footer_html.replace("[MY_ROLE_TEXT]", my_role_text)

    full_html = header_html + gallery_items + footer_html + JS_TEMPLATE
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Success! Generated '{output_file}'. Both buttons are securely locked in place.")

if __name__ == "__main__":
    generate_gallery()