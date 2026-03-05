import os
from datetime import datetime

# --- CONFIGURATION ---
IMAGE_FOLDER = 'images'  
OUTPUT_FILE = 'index.html' 
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}

# --- HTML TEMPLATES ---

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ekaggrat Singh Kalsi</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;400;600&display=swap');
        body {{ font-family: 'Manrope', sans-serif; }}
    </style>
</head>
<body class="bg-white text-black">
    
    <header class="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-sm z-50 py-6 px-8 flex justify-between items-center border-b border-gray-100">
        <div class="flex items-center gap-4">
            <img src="images/logo.png" alt="Logo" class="h-6 w-auto object-contain">
            <div class="text-2xl font-semibold tracking-[0.2em] uppercase">
                Ekaggrat Singh Kalsi
            </div>
        </div>
        <nav class="hidden md:flex space-x-8 text-xs font-medium tracking-widest uppercase text-gray-500 items-center">
            <a href="{insta_link}" target="_blank" class="hover:text-black transition-colors">Instagram</a>
            <a href="{linkedin_link}" target="_blank" class="hover:text-black transition-colors">LinkedIn</a>
            <a href="{hackaday_link}" target="_blank" class="hover:text-black transition-colors">Hackaday</a>
            <a href="about/about.html" class="hover:text-black transition-colors">About</a>
        </nav>
    </header>

    <div class="max-w-full mx-auto pt-32 pb-20 px-4 md:px-12">
        
        <div class="flex flex-wrap gap-6 mb-10 justify-center md:justify-start">
            <button onclick="filterGallery('all')" class="text-xs font-bold tracking-widest uppercase text-black hover:text-gray-500 transition-colors">All</button>
            <button onclick="filterGallery('architecture')" class="text-xs font-bold tracking-widest uppercase text-gray-400 hover:text-black transition-colors">Architecture</button>
            <button onclick="filterGallery('interior')" class="text-xs font-bold tracking-widest uppercase text-gray-400 hover:text-black transition-colors">Interior</button>
            <button onclick="filterGallery('products')" class="text-xs font-bold tracking-widest uppercase text-gray-400 hover:text-black transition-colors">Product</button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3" id="gallery-container">
"""

HTML_FOOTER = """
        </div>

        <footer class="mt-32 border-t border-gray-200 pt-8 flex justify-center items-center text-[10px] tracking-widest uppercase text-gray-400">
            <div>&copy; {year} Ekaggrat Studio</div>
        </footer>
    </div>

    <script>
        function filterGallery(category) {{
            const items = document.querySelectorAll('.gallery-item');
            
            items.forEach(item => {{
                if (category === 'all' || item.classList.contains(category)) {{
                    item.classList.remove('hidden');
                }} else {{
                    item.classList.add('hidden');
                }}
            }});
        }}
    </script>
</body>
</html>
"""

ITEM_TEMPLATE = """
            <a href="{basename}/{basename}.html" class="gallery-item {category} group block cursor-pointer">
                <div class="relative w-full aspect-[4/3] overflow-hidden bg-gray-100">
                    <img 
                        src="{filepath}" 
                        alt="{basename}" 
                        class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:-translate-y-12"
                        onerror="this.onerror=null; this.src='https://placehold.co/640x480/f3f3f3/333?text=IMAGE+NOT+FOUND';"
                    >
                    <div class="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-colors duration-500"></div>
                    
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                        <h2 class="text-white text-lg font-semibold tracking-widest uppercase text-center px-4">{title}</h2>
                    </div>
                </div>
            </a>
"""

def get_basename(filename):
    name, _ = os.path.splitext(filename)
    return name

def get_social_link(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return "#"

def generate_gallery():
    print(f"Scanning folder: {IMAGE_FOLDER}...")
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Folder '{IMAGE_FOLDER}' not found.")
        return

    images_data = []

    for root, dirs, files in os.walk(IMAGE_FOLDER):
        for filename in files:
            if os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS and filename.lower() != 'logo.png':
                
                file_path = os.path.join(root, filename).replace('\\', '/')
                
                rel_dir = os.path.relpath(root, IMAGE_FOLDER)
                category = rel_dir.lower() if rel_dir != '.' else 'all'
                category = category.replace(' ', '-') 

                mtime = os.path.getmtime(os.path.join(root, filename))
                
                images_data.append({
                    'filename': filename,
                    'file_path': file_path,
                    'category': category,
                    'mtime': mtime
                })
    
    if not images_data:
        print("No images found in the folder.")
        return

    images_data.sort(key=lambda x: x['mtime'], reverse=True)

    gallery_items = ""
    
    for data in images_data:
        basename = get_basename(data['filename'])
        title = basename.upper().replace('-', ' ').replace('_', ' ')
        
        gallery_items += ITEM_TEMPLATE.format(
            filepath=data['file_path'],
            basename=basename,
            title=title,
            category=data['category']
        )

    insta_link = get_social_link('instagram.txt')
    linkedin_link = get_social_link('linkedin.txt')
    hackaday_link = get_social_link('hackaday.txt')

    # Format the header with the links now
    header_html = HTML_HEADER.format(
        insta_link=insta_link,
        linkedin_link=linkedin_link,
        hackaday_link=hackaday_link
    )

    # Format the footer with just the year
    footer_html = HTML_FOOTER.format(
        year=datetime.now().year
    )

    full_html = header_html + gallery_items + footer_html
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Success! Generated {OUTPUT_FILE} with {len(images_data)} images.")

if __name__ == "__main__":
    generate_gallery()