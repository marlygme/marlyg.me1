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

    # Regex to find Readymag CDN links in HTML and JS files
    rmcdn_pattern = re.compile(
        r'https?://[ic]-p\.rmcdn1?\.net/.*?/(img|dist|snippets)/',
        re.IGNORECASE
    )

    processed_files_count = 0
    fixed_files_count = 0
    files_to_delete = []

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
                            r'/\1/',
                            content,
                            flags=re.IGNORECASE
                        )
                        
                        # Handle the specific case of the importmap script
                        importmap_pattern = r'"https://st-p.rmcdn1.net/[\w-]+\/"'
                        new_content = re.sub(importmap_pattern, r'"/"', new_content)

                        # Overwrite the original file with the corrected content
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"  ✅ Fixed CDN links in: {filepath}")
                        fixed_files_count += 1
                
                except Exception as e:
                    print(f"  ❌ ERROR processing file {filepath}: {e}")

            # Check for static HTML files that need to be deleted
            if filename.endswith(('.html')) and "snippets" in subdir:
                files_to_delete.append(filepath)

    # Delete all HTML files in the snippets directory
    print("\nStarting to delete redundant HTML files...")
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"  🗑️ Deleted redundant file: {file_path}")
        except OSError as e:
            print(f"  ❌ ERROR deleting file {file_path}: {e}")

    print(f"\nScan complete. Processed {processed_files_count} files, fixed {fixed_files_count} files.")
    print("Please inspect your files and then commit these changes to GitHub.")

if __name__ == "__main__":
    project_root = "." # Start from the current directory
    fix_readymag_paths(project_root)
