# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Slovak wellness center website built as a static site with a custom Python-based template system. The site serves "DOJO" - a holistic wellness center offering services like coaching, pilates, martial arts training, massages, and group programs.

## Build System and Development Commands

### Building the Site
```bash
# Build entire site (processes templates and compiles CSS)
python scripts/publish.py

# Build Tailwind CSS only
./tailwindcss-macos-arm64 -i assets/tailwind.css -o assets/tailwind-min.css --minify
```

### Development Workflow
1. Run `python scripts/publish.py` to build the site
2. Serve the `/public` directory with a local server
3. Access at `http://127.0.0.1:5500` (or your server's port)

## Architecture

### Template System
The site uses a custom Python build script that processes HTML files by replacing placeholder elements with partials:

- `<head></head>` → `partials/head.html`
- `<div id="header-container"></div>` → `partials/menu.html`
- `<div id="footer-container"></div>` → `partials/footer.html`

### File Structure
- **Source**: Root HTML files (e.g., `index.html`, `kontakt.html`)
- **Partials**: Reusable components in `/partials/`
- **Assets**: CSS, JS, and images in `/assets/` and `/images/`
- **Output**: Built site in `/public/` directory
- **Build Script**: `scripts/publish.py`

### Technology Stack
- Pure HTML5 with semantic structure
- Tailwind CSS (compiled from source with custom config)
- Vanilla JavaScript for interactive features
- Python for build automation
- No front-end framework dependencies

## Key Patterns

### Page Structure
Every page follows this consistent pattern:
```html
<!DOCTYPE html>
<html lang="sk" class="light">
<head></head>
<body>
    <div id="header-container"></div>
    
    <!-- Hero section with gradient background -->
    <section class="pt-32 bg-gradient-to-b from-cyan-900...">
        <h1>Page Title</h1>
    </section>
    
    <!-- Main content section -->
    <section class="py-16 bg-white dark:bg-gray-900">
        <!-- Content here -->
    </section>
    
    <div id="footer-container"></div>
</body>
</html>
```

### Navigation Structure
- **Main sections**: O nás (About), Programy (Programs), Služby (Services), Fotogaléria, Kontakt
- **Service pages**: Individual HTML files for each service offering
- **Team pages**: Personal profiles for practitioners

### Theme System
- Dark/light mode toggle with localStorage persistence
- Theme class applied to `<html>` element (`class="light"` or `class="dark"`)
- All components support both themes via Tailwind dark: modifiers

## Content Management

### Adding New Pages
1. Create HTML file in root directory
2. Use the consistent page structure pattern
3. Include placeholder elements for head, header, and footer
4. Run build script to process templates
5. Add navigation links in `partials/menu.html` if needed

### Modifying Global Elements
- **Site-wide head content**: Edit `partials/head.html`
- **Navigation menu**: Edit `partials/menu.html`
- **Footer content**: Edit `partials/footer.html`

### Assets
- **Custom CSS**: Add to `assets/styles.css`
- **Tailwind config**: Modify `assets/tailwind.css` source file
- **Images**: Store in `/images/` directory with appropriate subdirectories
- **JavaScript**: Edit `assets/scripts.js`

## Important Notes

- The build script skips files starting with `_` (like `_template.html`)
- Always run the build script after making changes to see updates
- The `/public` directory is the output - don't edit files there directly
- Site uses Slovak language primarily with semantic HTML for accessibility