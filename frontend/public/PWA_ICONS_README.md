# PWA Icons - Instructions

## Required Icons

The PWA requires the following icon sizes. Currently, placeholder icons are needed.

### Icon Sizes Needed
1. **pwa-64x64.png** (64x64 pixels) - Favicon
2. **pwa-192x192.png** (192x192 pixels) - Android home screen
3. **pwa-512x512.png** (512x512 pixels) - Splash screen
4. **maskable-icon-512x512.png** (512x512 pixels) - Android adaptive icon
5. **apple-touch-icon.png** (180x180 pixels) - iOS home screen
6. **favicon.ico** (16x16, 32x32, 48x48 multi-size) - Browser tab

## How to Generate Icons

### Option 1: Use Existing Logo
If you have an existing MBAS logo (SVG or PNG):

```bash
cd frontend/public

# If you have mbas-logo.svg:
npx @vite-pwa/assets-generator --preset minimal mbas-logo.svg

# This will generate all required sizes automatically
```

### Option 2: Manual Creation
Use a tool like:
- **Figma**: Design 512x512 icon, export all sizes
- **Adobe Illustrator**: Create vector icon, export at different sizes
- **Online Tool**: https://realfavicongenerator.net/

### Option 3: Use Current MBAS Icon
Copy the existing icon from the Tauri app:

```bash
# From project root
cp mbas_icon.ico frontend/public/favicon.ico

# If you have PNG versions in tauri-app/src-tauri/icons/:
cp tauri-app/src-tauri/icons/icon.png frontend/public/pwa-512x512.png
# Then resize to other sizes using ImageMagick or similar
```

## Icon Design Guidelines

### Safe Zone
For maskable icons (Android), keep important content within the safe zone:
- 512x512 canvas
- Safe zone: 410x410 circle in center
- Content outside this may be cropped on some devices

### Colors
- Use the MBAS brand colors
- Ensure good contrast for visibility
- Test on both light and dark backgrounds

### Style
- Simple, recognizable design
- Avoid fine details (won't show on small sizes)
- Consistent with MBAS branding

## Testing Icons

After adding icons:

1. **Build the app**:
   ```bash
   npm run build
   npm run preview
   ```

2. **Test installation**:
   - Open http://localhost:4173 in Chrome
   - Click "Install" button in address bar
   - Verify icon appears correctly

3. **Test on mobile**:
   - Access from mobile device on same WiFi
   - Tap "Add to Home Screen"
   - Check icon on home screen

## Current Status

⚠️ **ICONS NEEDED**: Placeholder icons must be replaced with actual MBAS branded icons.

Once icons are created, remove this README file.
