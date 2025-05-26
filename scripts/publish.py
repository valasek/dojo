#!/usr/bin/env python3
"""
publish.py - Website publishing script

This script prepares website files for publishing by:
1. Cleaning the public directory
2. Build Tailwind CSS
3. Copying assets and images directories
4. Processing HTML files with included partials
5. Skipping blacklisted files

Usage: python scripts/publish.py
"""

import shutil
from pathlib import Path
import subprocess


class Publisher:
    """Handles the website publishing process."""

    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.public_dir = self.base_dir / "public"
        self.partials_dir = self.base_dir / "partials"

        # Folders to copy entirely
        self.copy_folders = ["assets", "images"]

        # Files to preserve in public directory during cleanup
        self.cleanup_blacklist = [".keep"]

        # Files to skip (blacklist)
        self.blacklist = ["README.md", "LICENCE", "_template.html"]

        # Partials to replace in HTML files
        self.partials = {
            "<head></head>": "head.html",
            '<div id="header-container"></div>': "menu.html",
            '<div id="footer-container"></div>': "footer.html"
        }

        # Cache for partial contents
        self.partial_contents = {}

    def clean_public_dir(self):
        """Delete all files and folders in the public directory."""
        if self.public_dir.exists():
            for item in self.public_dir.iterdir():
                # Check if item should be preserved
                if item.name in self.cleanup_blacklist:
                    print(f"⊘ Skipped blacklisted file: {item.name} in {self.public_dir} folder")
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        else:
            self.public_dir.mkdir(parents=True)

        print(f"✓ Cleaned public directory: {self.public_dir}")

    def copy_folders_to_public(self):
        """Copy specified folders to the public directory."""
        for folder in self.copy_folders:
            src_path = self.base_dir / folder
            dest_path = self.public_dir / folder

            if src_path.exists():
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
                print(f"✓ Copied folder: {folder}/")
            else:
                print(f"⚠️ Warning: Source folder not found: {folder}/")

    def load_partial(self, partial_name):
        """Load and cache partial file content."""
        if partial_name not in self.partial_contents:
            partial_path = self.partials_dir / partial_name
            try:
                with open(partial_path, 'r', encoding='utf-8') as file:
                    self.partial_contents[partial_name] = file.read()
            except FileNotFoundError:
                print(f"⚠️  Warning: Partial file not found: {partial_path}")
                self.partial_contents[partial_name] = ""

        return self.partial_contents[partial_name]

    def process_html_file(self, file_path):
        """Process an HTML file by replacing placeholder elements with partial content."""
        dest_path = self.public_dir / file_path.name

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace placeholders with partial contents
        for placeholder, partial_name in self.partials.items():
            partial_content = self.load_partial(partial_name)
            content = content.replace(placeholder, partial_content)

        with open(dest_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"✓ Processed HTML file: {file_path.name}")

    def copy_html_files(self):
        """Copy and process HTML files to the public directory."""
        for file_path in self.base_dir.glob("*.html"):
            if file_path.name in self.blacklist:
                print(f"⊘ Skipped blacklisted file: {file_path.name}")
                continue

            self.process_html_file(file_path)

    def build_tailwind_css(self):
        """Build Tailwind CSS from source to minified version."""
        tailwind_cmd = "./tailwindcss-macos-arm64"
        input_css = "./assets/tailwind.css"
        output_css = "./assets/tailwind-min.css"

        try:
            result = subprocess.run(
                [tailwind_cmd, "-i", input_css, "-o", output_css],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ Built Tailwind CSS: {output_css}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error building Tailwind CSS: {e}")
            print(f"Error output: {e.stderr}")
        except FileNotFoundError:
            print(f"❌ Error: Tailwind CSS executable not found: {tailwind_cmd}")

    def publish(self):
        """Run the complete publishing process."""
        print("\n📦 Starting website publishing process...\n")

        self.clean_public_dir()
        self.build_tailwind_css()
        self.copy_folders_to_public()
        self.copy_html_files()

        print("\n✅ Publishing complete! Files ready in public directory.\n")


if __name__ == "__main__":
    publisher = Publisher()
    publisher.publish()
