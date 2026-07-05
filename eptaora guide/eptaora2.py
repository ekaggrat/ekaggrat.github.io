import os
import json
import re
from datetime import datetime

# --- CONFIGURATION ---
IMAGE_FOLDER = 'images'  
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
PAGE_MARGIN = '20vw' 

# --- HTML TEMPLATES ---

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
        .snap-container {
            scroll-snap-type: y mandatory;
        overflow-y: scroll;
        /* Subtract 100px (or your header's height) from the full viewport height */
        height: calc(100vh - 100px); 
        margin-top: 100px;
        }
        .snap-item {
            scroll-snap-align: start;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        img {
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }
    </style>
</head>
<body class="bg-white text-black overflow-hidden">
    
    <header class="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-sm z-50 py-6 px-8 flex justify-between items-center border-b border-gray-100">
        <div class="flex items-center gap-4">
            <img src="images/logo.png" alt="Logo" class="h-5 w-auto object-contain">
            <div class="text-lg font-semibold tracking-[0.2em] uppercase">
                Ekaggart Singh Kalsi
            </div>
        </div>
        <nav class="flex space-x-8 text-xs font-medium tracking-widest uppercase text-gray-500">
            <a href="https://ekaggrat.com" class="hover:text-black transition-colors">Home</a>
        </nav>
    </header>

    <main class="snap-container pt-120" style="padding-left: [PAGE_MARGIN]; padding-right: [PAGE_MARGIN];">
"""

ITEM_TEMPLATE = """
            <div class="snap-item group block cursor-pointer w-full" onclick="openModal([INDEX])">
                <div class="relative w-full max-h-[80vh] aspect-[4/3] overflow-hidden bg-gray-100 shadow-lg">
                    <img 
                        src="[FILEPATH]" 
                        alt="[CLEAN_NAME]" 
                        class="w-full h-full object-contain"
                        onerror="this.onerror=null; this.src='https://placehold.co/640x480/f3f3f3/333?text=IMAGE+NOT+FOUND';"
                    >
                </div>
            </div>
"""

YOUTUBE_TEMPLATE = """
            <div class="snap-item w-full flex items-center justify-center p-6">
    <div class="w-full aspect-video bg-gray-50">
        <iframe 
            class="w-full h-full" 
            src="https://www.youtube.com/embed/VIDEO_ID" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            referrerpolicy="strict-origin-when-cross-origin" 
            allowfullscreen>
        </iframe>
    </div>
</div>
"""

FOOTER_TEMPLATE = """
        </div>

        <div class="mt-24 max-w-4xl mx-auto">
            <h2 class="text-xl font-bold tracking-[0.2em] uppercase mb-6">Description</h2>
            <p class="text-sm text-gray-600 leading-relaxed mb-12 whitespace-pre-wrap">[PROJECT_TEXT]</p>
            
            <h3 class="text-sm font-bold tracking-[0.2em] uppercase mb-4 text-gray-800">My Role</h3>
            <p class="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">[MY_ROLE_TEXT]</p>
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

MODAL_AND_JS = """
    <div id="lightbox" class="fixed inset-0 z-[100] bg-white hidden flex items-center justify-center opacity-0 transition-opacity duration-300" onclick="closeModal()">
        
        <button class="absolute top-8 right-8 text-black z-[110]" onclick="closeModal()">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>

        <button class="absolute left-8 text-black z-[110] p-4" onclick="prevImage(event)">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
        </button>

        <button class="absolute right-8 text-black z-[110] p-4" onclick="nextImage(event)">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
        </button>

        <div class="w-full h-full flex items-center justify-center p-20" onclick="event.stopPropagation()">
            <img id="lightbox-img" src="" alt="Enlarged view" class="max-w-full max-h-full object-contain">
        </div>
    </div>

    <script>
        const images = [IMAGE_ARRAY_JSON];
        let currentIndex = 0;

        function openModal(index) {
            currentIndex = index;
            const lightbox = document.getElementById('lightbox');
            const img = document.getElementById('lightbox-img');
            img.src = images[currentIndex];
            lightbox.classList.remove('hidden');
            // Small timeout to allow transition to trigger
            requestAnimationFrame(() => { 
                lightbox.classList.remove('opacity-0'); 
            });
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            const lightbox = document.getElementById('lightbox');
            lightbox.classList.add('opacity-0');
            setTimeout(() => { lightbox.classList.add('hidden'); }, 300);
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

        document.addEventListener('keydown', function(event) {
            const lightbox = document.getElementById('lightbox');
            if (!lightbox.classList.contains('hidden')) {
                if (event.key === "Escape") closeModal();
                if (event.key === "ArrowRight") nextImage(null);
                if (event.key === "ArrowLeft") prevImage(null);
            }
        });
    </script>
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

    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Subfolder '{IMAGE_FOLDER}' not found.")
        return

    txt_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith('.txt') and f.lower() != 'myrole.txt']
    project_text = "No project description text file found."
    project_title = parent_folder_name.replace("-", " ").replace("_", " ").upper()
    
    if txt_files:
        text_filename = txt_files[0]
        text_file_path = os.path.join(IMAGE_FOLDER, text_filename)
        project_title = clean_filename(text_filename).upper()
        with open(text_file_path, 'r', encoding='utf-8') as tf:
            project_text = tf.read()

    my_role_text = "Role information not found."
    role_file_path = os.path.join(IMAGE_FOLDER, 'myrole.txt')
    if os.path.exists(role_file_path):
        with open(role_file_path, 'r', encoding='utf-8') as rf:
            my_role_text = rf.read()

    files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS and f.lower() != 'logo.png']
    
    if not files:
        print("No images found.")
        return

    files.sort(key=get_sort_key)

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
        
        if (index + 1) % 3 == 0:
            gallery_items += YOUTUBE_TEMPLATE

    # 4. Assemble full HTML
    header_html = HTML_HEADER.replace("[PAGE_MARGIN]", PAGE_MARGIN)
    # Note: We removed [PROJECT_TITLE] from the body, but kept it in the <title> tag
    header_html = header_html.replace("[PROJECT_TITLE]", project_title)
    
    footer_html = FOOTER_TEMPLATE.replace("[PROJECT_TEXT]", project_text)
    footer_html = footer_html.replace("[MY_ROLE_TEXT]", my_role_text)
    
    js_array_string = json.dumps(image_paths_for_js)
    modal_html = MODAL_AND_JS.replace("[IMAGE_ARRAY_JSON]", js_array_string)

    full_html = header_html + gallery_items + footer_html + modal_html

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header_html + gallery_items + footer_html + modal_html)
        
    print(f"Success! Generated '{output_file}'.")

if __name__ == "__main__":
    generate_gallery()