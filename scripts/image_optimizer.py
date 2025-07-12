#!/usr/bin/env python3
"""
Image Optimization Script for Web
Optimizes images by reducing file size, converting formats, and creating responsive versions.

Usage with uv:
    uv run image_optimizer.py [input_folder] [options]
"""

import os
import sys
from PIL import Image, ImageOps
from PIL.Image import Resampling
import pillow_heif
from pathlib import Path
import argparse

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

class ImageOptimizer:
    def __init__(self, input_folder, output_folder=None, quality=85):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder) if output_folder else self.input_folder / "optimized"
        self.quality = quality
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.heic', '.heif'}
        
        # Create output directory if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)
        
        # Responsive breakpoints (width in pixels)
        self.breakpoints = {
            'small': 480,
            'medium': 768,
            'large': 1200,
            'xlarge': 1920
        }
    
    def get_optimal_size(self, original_width, original_height):
        """Determine the optimal size category for an image"""
        if original_width <= 600:
            return ['small']
        elif original_width <= 900:
            return ['small', 'medium']
        elif original_width <= 1400:
            return ['small', 'medium', 'large']
        else:
            return ['small', 'medium', 'large', 'xlarge']
    
    def optimize_image(self, image_path):
        """Optimize a single image"""
        try:
            print(f"Processing: {image_path.name}")
            
            # Open and process image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (for JPEG output)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background for transparent images
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Auto-orient based on EXIF data
                img = ImageOps.exif_transpose(img)
                
                # Get original dimensions
                original_width, original_height = img.size
                original_size = image_path.stat().st_size
                
                print(f"  Original: {original_width}x{original_height} ({original_size/1024/1024:.1f} MB)")
                
                # Determine which sizes to create
                sizes_to_create = self.get_optimal_size(original_width, original_height)
                
                # Generate optimized versions
                base_name = image_path.stem
                total_savings = 0
                
                for size_name in sizes_to_create:
                    target_width = self.breakpoints[size_name]
                    
                    # Skip if original is smaller than target
                    if original_width <= target_width:
                        target_width = original_width
                        size_name = 'original'
                    
                    # Calculate new dimensions maintaining aspect ratio
                    if original_width > target_width:
                        ratio = target_width / original_width
                        new_width = target_width
                        new_height = int(original_height * ratio)
                        resized_img = img.resize((new_width, new_height), Resampling.LANCZOS)
                    else:
                        resized_img = img
                        new_width, new_height = original_width, original_height
                    
                    # Save WebP version (best compression)
                    webp_name = f"{base_name}_{size_name}.webp" if size_name != 'original' else f"{base_name}.webp"
                    webp_path = self.output_folder / webp_name
                    resized_img.save(webp_path, 'WebP', quality=self.quality, method=6)
                    webp_size = webp_path.stat().st_size
                    
                    # Save JPEG version (fallback)
                    jpg_name = f"{base_name}_{size_name}.jpg" if size_name != 'original' else f"{base_name}.jpg"
                    jpg_path = self.output_folder / jpg_name
                    resized_img.save(jpg_path, 'JPEG', quality=self.quality, optimize=True)
                    jpg_size = jpg_path.stat().st_size
                    
                    # Calculate savings
                    webp_savings = ((original_size - webp_size) / original_size) * 100
                    jpg_savings = ((original_size - jpg_size) / original_size) * 100
                    
                    print(f"    {size_name}: {new_width}x{new_height}")
                    print(f"      WebP: {webp_size/1024:.1f} KB ({webp_savings:.1f}% smaller)")
                    print(f"      JPEG: {jpg_size/1024:.1f} KB ({jpg_savings:.1f}% smaller)")
                    
                    total_savings += (original_size - min(webp_size, jpg_size))
                
                print(f"  Total savings: {total_savings/1024/1024:.1f} MB\n")
                return True
                
        except Exception as e:
            print(f"Error processing {image_path.name}: {str(e)}")
            return False
    
    def generate_html_examples(self):
        """Generate HTML examples for using responsive images"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Optimized Images Examples</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .image-example { margin: 20px 0; padding: 20px; border: 1px solid #ddd; }
        .responsive-img { max-width: 100%; height: auto; }
        code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Responsive Image Examples</h1>
    
    <div class="image-example">
        <h2>Method 1: Using &lt;picture&gt; element with WebP and JPEG fallback</h2>
        <pre><code>&lt;picture&gt;
  &lt;source srcset="image_small.webp 480w, 
                  image_medium.webp 768w, 
                  image_large.webp 1200w" 
          type="image/webp"&gt;
  &lt;source srcset="image_small.jpg 480w, 
                  image_medium.jpg 768w, 
                  image_large.jpg 1200w" 
          type="image/jpeg"&gt;
  &lt;img src="image_medium.jpg" alt="Description" class="responsive-img"&gt;
&lt;/picture&gt;</code></pre>
    </div>
    
    <div class="image-example">
        <h2>Method 2: Simple srcset with sizes</h2>
        <pre><code>&lt;img srcset="image_small.webp 480w, 
             image_medium.webp 768w, 
             image_large.webp 1200w"
     sizes="(max-width: 480px) 480px, 
            (max-width: 768px) 768px, 
            1200px"
     src="image_medium.webp" 
     alt="Description" 
     class="responsive-img"&gt;</code></pre>
    </div>
    
    <div class="image-example">
        <h2>CSS for responsive images</h2>
        <pre><code>.responsive-img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* Lazy loading with intersection observer */
.lazy-img {
  opacity: 0;
  transition: opacity 0.3s;
}

.lazy-img.loaded {
  opacity: 1;
}</code></pre>
    </div>
</body>
</html>"""
        
        html_path = self.output_folder / "responsive_examples.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML examples saved to: {html_path}")
    
    def process_folder(self):
        """Process all images in the input folder and subfolders"""
        print(f"Starting optimization of images in: {self.input_folder}")
        print(f"Output folder: {self.output_folder}")
        print(f"Quality setting: {self.quality}%")
        print("Processing all subfolders recursively...\n")
        
        # Find all image files recursively
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(self.input_folder.rglob(f"*{ext}"))
            image_files.extend(self.input_folder.rglob(f"*{ext.upper()}"))
        
        # Filter out files in the output directory itself
        image_files = [f for f in image_files if not str(f).startswith(str(self.output_folder))]
        
        if not image_files:
            print("No supported image files found!")
            return
        
        print(f"Found {len(image_files)} image files to process\n")
        
        # Group files by subfolder for better organization
        files_by_folder = {}
        for image_path in sorted(image_files):
            folder_name = image_path.parent.name
            if folder_name not in files_by_folder:
                files_by_folder[folder_name] = []
            files_by_folder[folder_name].append(image_path)
        
        # Process each folder
        successful = 0
        failed = 0
        
        for folder_name, files in files_by_folder.items():
            print(f"📁 Processing folder: {folder_name} ({len(files)} files)")
            print("-" * 40)
            
            # Create subfolder in output directory
            folder_output = self.output_folder / folder_name
            folder_output.mkdir(exist_ok=True)
            
            # Temporarily change output folder for this batch
            original_output = self.output_folder
            self.output_folder = folder_output
            
            for image_path in files:
                if self.optimize_image(image_path):
                    successful += 1
                else:
                    failed += 1
            
            # Restore original output folder
            self.output_folder = original_output
            print()
        
        # Generate HTML examples in main output folder
        self.generate_html_examples()
        
        # Summary
        print("=" * 50)
        print("OPTIMIZATION COMPLETE")
        print("=" * 50)
        print(f"Successfully processed: {successful} images")
        print(f"Failed: {failed} images")
        print(f"Output folder: {self.output_folder}")
        print(f"HTML examples: {self.output_folder}/responsive_examples.html")


def main():
    parser = argparse.ArgumentParser(description="Optimize images for web use")
    parser.add_argument("input_folder", nargs='?', default="./images", 
                       help="Folder containing images to optimize (default: ./images)")
    parser.add_argument("-o", "--output", default="./images/output",
                       help="Output folder (default: ./images/output)")
    parser.add_argument("-q", "--quality", type=int, default=85, 
                       help="JPEG/WebP quality (1-100, default: 85)")
    
    args = parser.parse_args()
    
    # Convert to absolute paths
    input_path = Path(args.input_folder).resolve()
    output_path = Path(args.output).resolve()
    
    # Validate input folder
    if not input_path.exists():
        print(f"Error: Input folder '{input_path}' does not exist!")
        sys.exit(1)
    
    # Create optimizer and process images
    optimizer = ImageOptimizer(input_path, output_path, args.quality)
    optimizer.process_folder()


if __name__ == "__main__":
    # If running without command line arguments, use default paths
    if len(sys.argv) == 1:
        # Default to ./images folder, output to ./images/output
        script_dir = Path(__file__).parent
        images_dir = script_dir.parent / "images"
        output_dir = images_dir / "output"
        
        print(f"No arguments provided. Using default paths:")
        print(f"  Images folder: {images_dir}")
        print(f"  Output folder: {output_dir}")
        
        if not images_dir.exists():
            print(f"Error: Default images folder '{images_dir}' does not exist!")
            print("Please create the ./images folder or specify a different path.")
            sys.exit(1)
        
        optimizer = ImageOptimizer(images_dir, output_dir)
        optimizer.process_folder()
    else:
        main()