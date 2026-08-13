import shutil
from datetime import datetime, timedelta
from pathlib import Path

extension_map = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg"],
    "Code": [".py", ".js", ".html", ".css", ".json"],
}

def get_category(extension):
    for category, extensions in extension_map.items():
        if extension.lower() in extensions:
            return category
    return "Other"

def organize_folder(folder_path, archive_days=None):
    folder = Path(folder_path)
    
    if not folder.is_dir():
        print(f"Error: {folder_path} not found")
        return

    now = datetime.now()
    archive_cutoff = now - timedelta(days=archive_days) if archive_days else None

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        extension = file_path.suffix
        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

        if archive_cutoff and modified_time < archive_cutoff:
            target_folder = folder / "Archive"
        else:
            category = get_category(extension)
            target_folder = folder / category

        target_folder.mkdir(parents=True, exist_ok=True)
        target_path = target_folder / file_path.name

        if target_path.exists():
            base = file_path.stem
            ext = file_path.suffix
            counter = 1
            while target_path.exists():
                target_path = target_folder / f"{base}_{counter}{ext}"
                counter += 1

        shutil.move(file_path, target_path)
        print(f"Moved: {file_path.name} -> {target_folder.name}")

def main():
    default_folder = Path.home() / "Downloads"
    
    folder_input = input(f"Folder [{default_folder}]: ").strip()
    folder_path = Path(folder_input) if folder_input else default_folder

    archive_input = input("Archive days (Enter to skip): ").strip()
    archive_days = int(archive_input) if archive_input.isdigit() else None

    organize_folder(folder_path, archive_days)
    print("Done.")

if __name__ == "__main__":
    main()
