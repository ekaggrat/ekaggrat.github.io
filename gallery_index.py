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
    <title>Ekaggart Singh Kalsi - Selected Works</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;400;600&display=swap');
        body { font-family: 'Manrope', sans-serif; }
    </style>
</head>
<body class="bg-white text-black">
    
    <header class="fixed top-0 left-0 w-full bg-white/90 backdrop-blur-sm z-50 py-6 px-8 flex justify-between items-center border-b border-gray-100">
        <div class="flex items-center gap-4">
            <img src="images/logo.png" alt="Logo" class="h-6 w-auto object-contain">
            <div class="text-2xl font-semibold tracking-[0.2em] uppercase">
                Ekaggart singh Kalsi
            </div>
        </div>
        <nav class="hidden md:flex space-x-8 text-xs font-medium tracking-widest uppercase text-gray-500">
            <a href="https://ekaggrat.com" class="hover:text-black transition-colors">Home</a>
        </nav>
    </header>

    <div class="max-w-[1600px] mx-auto pt-32 pb-20 px-4 md:px-12">
        <h1 class="text-xs font-bold tracking-[0.3em] uppercase text-gray-400 mb-12 text-center md:text-left">
            Selected Works
        </h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
"""

HTML_FOOTER = """
        </div>

        <footer class="mt-32 border-t border-gray-200 pt-8 flex flex-col md:flex-row justify-between items-center text-[10px] tracking-widest uppercase text-gray-400">
            <div>&copy; {year} Ekaggrat Studio</div>
            <div class="mt-4 md:mt-0 space-x-6">
                <a href="{insta_link}" target="_blank" class="hover:text-black">Instagram</a>
                <a href="{linkedin_link}" target="_blank" class="hover:text-black">LinkedIn</a>
                <a href="{hackaday_link}" target="_blank" class="hover:text-black">Hackaday</a>
            </div>
        </footer>
    </div>
</body>
</html>
"""

# HTML template matching the exact basename for folders, links, and titles
ITEM_TEMPLATE = """
            <a href="{basename}/{basename}.html" class="group block cursor-pointer">
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
    """Simply returns the filename without the extension, applying no formatting."""
    name, _ = os.path.splitext(filename)
    return name

def get_social_link(filename):
    """Reads a URL from a text file, returning '#' if it doesn't exist."""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return "#"

def generate_gallery():
    print(f"Scanning folder: {IMAGE_FOLDER}...")
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Folder '{IMAGE_FOLDER}' not found.")
        print("Please create the folder and add images, or change the IMAGE_FOLDER variable.")
        return

    # Filter out logo.png
    files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS and f.lower() != 'logo.png']
    
    if not files:
        print("No images found in the folder.")
        return

    # Sort files by modification date, newest first
    files.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGE_FOLDER, x)), reverse=True)

    gallery_items = ""
    
    for filename in files:
        file_path = f"{IMAGE_FOLDER}/{filename}"
        basename = get_basename(filename)
        title = basename.upper()
        
        gallery_items += ITEM_TEMPLATE.format(
            filepath=file_path,
            basename=basename,
            title=title
        )

    # Grab the links for the footer
    insta_link = get_social_link('instagram.txt')
    linkedin_link = get_social_link('linkedin.txt')
    hackaday_link = get_social_link('hackaday.txt')

    # Format the footer with links and the current year
    footer_html = HTML_FOOTER.format(
        year=datetime.now().year,
        insta_link=insta_link,
        linkedin_link=linkedin_link,
        hackaday_link=hackaday_link
    )

    full_html = HTML_HEADER + gallery_items + footer_html
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Success! Generated {OUTPUT_FILE} with {len(files)} images.")

if __name__ == "__main__":
    generate_gallery()