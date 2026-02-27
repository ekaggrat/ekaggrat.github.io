import os
import json
import re
from datetime import datetime

# --- CONFIGURATION ---
IMAGE_FOLDER = 'images'  # The folder to scan for images and the text file
OUTPUT_FILE = 'gallery.html'
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

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
        body { font-family: 'Manrope', sans-serif; }
    </style>
</head>
<body class="bg-white text-black">
    
    <header class="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-sm z-50 py-6 px-8 flex justify-between items-center border-b border-gray-100">
        <div class="text-2xl font-semibold tracking-[0.2em] uppercase">
            Ekaggrat
        </div>
        <nav class="flex space-x-8 text-xs font-medium tracking-widest uppercase text-gray-500">
            <a href="https://ekaggrat.com" class="hover:text-black transition-colors">Home</a>
        </nav>
    </header>

    <div class="max-w-[1600px] mx-auto pt-32 pb-20 px-4 md:px-12">
        
        <h1 class="text-2xl font-bold tracking-[0.3em] uppercase text-gray-800 mb-12 text-center">
            [PROJECT_TITLE]
        </h1>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
"""

# Template for individual grid items (No hover titles, triggers lightbox)
ITEM_TEMPLATE = """
            <div class="group block cursor-pointer" onclick="openModal([INDEX])">
                <div class="relative w-full aspect-[4/3] overflow-hidden bg-gray-100">
                    <img 
                        src="[FILEPATH]" 
                        alt="[CLEAN_NAME]" 
                        class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:-translate-y-12"
                        onerror="this.onerror=null; this.src='https://placehold.co/640x480/f3f3f3/333?text=IMAGE+NOT+FOUND';"
                    >
                </div>
            </div>
"""

# Footer with Description and My Role section
FOOTER_TEMPLATE = """
        </div>

        <div class="mt-24 max-w-4xl">
            <h2 class="text-xl font-bold tracking-[0.2em] uppercase mb-6">Description</h2>
            <p class="text-sm text-gray-600 leading-relaxed mb-12 whitespace-pre-wrap">[PROJECT_TEXT]</p>
            
            <h3 class="text-sm font-bold tracking-[0.2em] uppercase mb-4 text-gray-800">My Role</h3>
            <p class="text-sm text-gray-600 leading-relaxed">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.
            </p>
        </div>

        <footer class="mt-32 border-t border-gray-200 pt-8 flex flex-col md:flex-row justify-between items-center text-[10px] tracking-widest uppercase text-gray-400">
            <div>&copy; """ + str(datetime.now().year) + """ Ekaggrat Studio</div>
            <div class="mt-4 md:mt-0 space-x-6">
                <a href="#" class="hover:text-black">Instagram</a>
                <a href="#" class="hover:text-black">LinkedIn</a>
                <a href="#" class="hover:text-black">Behance</a>
            </div>
        </footer>
    </div>
"""

# Lightbox HTML and Navigation Logic
MODAL_AND_JS = """
    <div id="lightbox" class="fixed inset-0 z-[100] bg-white/95 hidden flex-col justify-center items-center opacity-0 transition-opacity duration-300" onclick="closeModal()">
        
        <button class="absolute top-8 right-8 text-black hover:text-gray-500 focus:outline-none z-50 transition-colors" onclick="closeModal()">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>

        <button class="absolute left-4 md:left-8 top-1/2 -translate-y-1/2 text-black hover:text-gray-500 focus:outline-none z-50 transition-colors p-4" onclick="prevImage(event)">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
        </button>

        <button class="absolute right-4 md:right-8 top-1/2 -translate-y-1/2 text-black hover:text-gray-500 focus:outline-none z-50 transition-colors p-4" onclick="nextImage(event)">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
        </button>

        <div class="max-w-[90vw] max-h-[90vh] flex justify-center items-center w-full h-full p-12" onclick="event.stopPropagation()">
            <img id="lightbox-img" src="" alt="Enlarged view" class="max-w-full max-h-full object-contain shadow-2xl transition-opacity duration-300">
        </div>
    </div>

    <script>
        // Array of images passed from Python
        const images = [IMAGE_ARRAY_JSON];
        let currentIndex = 0;

        function openModal(index) {
            currentIndex = index;
            const lightbox = document.getElementById('lightbox');
            const img = document.getElementById('lightbox-img');
            
            img.src = images[currentIndex];
            lightbox.classList.remove('hidden');
            
            // Short timeout to allow display block to apply before fading in
            setTimeout(() => {
                lightbox.classList.remove('opacity-0');
            }, 10);
            
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        }

        function closeModal() {
            const lightbox = document.getElementById('lightbox');
            lightbox.classList.add('opacity-0');
            
            // Wait for fade transition to finish before hiding
            setTimeout(() => {
                lightbox.classList.add('hidden');
            }, 300);
            
            document.body.style.overflow = ''; 
        }

        function nextImage(event) {
            if (event) event.stopPropagation();
            currentIndex = (currentIndex + 1) % images.length;
            document.getElementById('lightbox-img').src = images[currentIndex];
        }

        function prevImage(event) {
            if (event) event.stopPropagation();
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            document.getElementById('lightbox-img').src = images[currentIndex];
        }

        // Add keyboard navigation (Escape, Left Arrow, Right Arrow)
        document.addEventListener('keydown', function(event) {
            const lightbox = document.getElementById('lightbox');
            if (!lightbox.classList.contains('hidden')) {
                if (event.key === "Escape") closeModal();
                if (event.key === "ArrowRight") nextImage(null);
                if (event.key === "ArrowLeft") prevImage(null);
            }
        });
    </script>
</body>
</html>
"""

def clean_filename(filename):
    """Removes extensions and replaces separators with spaces."""
    name, _ = os.path.splitext(filename)
    clean = name.replace("-", " ").replace("_", " ")
    clean = clean.replace("(", " ").replace(")", "")
    return clean

def get_sort_key(filename):
    """Extracts the first number found in the filename for sorting.
       If no number is found, returns infinity so it gets sorted to the end."""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def generate_gallery():
    print(f"Scanning folder: {IMAGE_FOLDER}...")
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Folder '{IMAGE_FOLDER}' not found.")
        print("Please create the folder and add images, or change the IMAGE_FOLDER variable.")
        return

    # 1. Grab text file for title and description
    txt_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith('.txt')]
    project_text = "No project description text file found. Please add a .txt file inside your images folder."
    project_title = "UNTITLED PROJECT"
    
    if txt_files:
        text_filename = txt_files[0]
        text_file_path = os.path.join(IMAGE_FOLDER, text_filename)
        
        # Extract title from text filename (removing extension and cleaning)
        project_title = clean_filename(text_filename).upper()
        
        with open(text_file_path, 'r', encoding='utf-8') as tf:
            project_text = tf.read()
            print(f"Loaded project text from: {text_filename}")

    # 2. Grab images and sort them numerically
    files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
    
    if not files:
        print("No images found in the folder.")
        return

    # Sort files using our custom numerical key
    files.sort(key=get_sort_key)

    # 3. Build HTML items and a list of image paths for the JS array
    gallery_items = ""
    image_paths_for_js = []
    
    for index, filename in enumerate(files):
        file_path = f"{IMAGE_FOLDER}/{filename}"
        clean_name = clean_filename(filename)
        
        image_paths_for_js.append(file_path)
        
        item_html = ITEM_TEMPLATE.replace("[FILEPATH]", file_path)
        item_html = item_html.replace("[CLEAN_NAME]", clean_name)
        item_html = item_html.replace("[INDEX]", str(index))
        gallery_items += item_html

    # 4. Assemble full HTML
    header_html = HTML_HEADER.replace("[PROJECT_TITLE]", project_title)
    
    footer_html = FOOTER_TEMPLATE.replace("[PROJECT_TEXT]", project_text)
    
    # Dump Python list into a valid JSON/JS array string
    js_array_string = json.dumps(image_paths_for_js)
    modal_html = MODAL_AND_JS.replace("[IMAGE_ARRAY_JSON]", js_array_string)

    full_html = header_html + gallery_items + footer_html + modal_html
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Success! Generated {OUTPUT_FILE} with {len(files)} images sorted by number.")

if __name__ == "__main__":
    generate_gallery()