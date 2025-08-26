import os
import re

def fix_readymag_paths(root_dir):
    """
    Scans HTML, CSS, and JS files to replace hardcoded Readymag CDN URLs
    with local, relative paths (e.g., /img/ or /dist/).
    This fixes issues where the exported site fails to load resources
    because it's still looking for them on Readymag's servers.
    """
    print("Starting to fix Readymag CDN paths in all files...")

    # Regex to find two types of CDN links:
    # 1. Image CDN: https://i-p.rmcdn.net/.../img/...
    # 2. Scripts CDN: https://c-p.rmcdn1.net/.../dist/...
    # It captures the "img" or "dist" part to use it in the replacement.
    rmcdn_pattern = re.compile(
        r'(https?://[ic]-p\.rmcdn1?\.net/.*?/)(img|dist|snippets)/',
        re.IGNORECASE
    )

    processed_files_count = 0
    fixed_files_count = 0

    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            # Only process relevant file types
            if filename.endswith(('.html', '.css', '.js')):
                filepath = os.path.join(subdir, filename)
                processed_files_count += 1
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Find all matches for the CDN pattern in the file content
                    if re.search(rmcdn_pattern, content):
                        # Replace the CDN part with a relative root path (e.g., /img/)
                        new_content = re.sub(
                            r'https?://[ic]-p\.rmcdn1?\.net/.*?/(img|dist|snippets)/',
                            r'/\2/',  # Use the captured group 2 ("img", "dist", or "snippets")
                            content,
                            flags=re.IGNORECASE
                        )

                        # Overwrite the original file with the corrected content
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"  ✅ Fixed CDN links in: {filepath}")
                        fixed_files_count += 1
                
                except Exception as e:
                    print(f"  ❌ ERROR processing file {filepath}: {e}")

    print(f"\nScan complete. Processed {processed_files_count} files, fixed {fixed_files_count} files.")
    print("Please inspect your files and then commit these changes to GitHub.")

if __name__ == "__main__":
    project_root = "." # Start from the current directory
    fix_readymag_paths(project_root)
