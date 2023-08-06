import os
import hashlib
import zipfile

def process_zip_file(zip_file_path):
    """Process a zip file and store partial hashes in a bloom filter."""
    if not zipfile.is_zipfile(zip_file_path):
        print(f"Error: {zip_file_path} is not a valid zip file.")
        return set()

    # Create the bloom filter or use any other suitable data structure
    bloom_filter = set()

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            # Extract a chunk of data from each file in the zip archive
            with zip_file.open(file_name) as file:
                partial_data = file.read(1024)  # Adjust the chunk size as needed

            # Calculate the MD5 hash of the partial data
            partial_hash = hashlib.md5(partial_data).hexdigest()

            # Store the partial hash in the bloom filter
            bloom_filter.add(partial_hash)

    return bloom_filter

def print_duplicate_zip_files(folder_path):
    """Print duplicate files in zip archives in the specified folder."""
    # Traverse through the folder and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.endswith('.zip'):
                zip_bloom_filter = process_zip_file(file_path)
                print(f"Duplicate Zip files with name {file_name}:")
                for file_path in zip_bloom_filter:
                    print(f"Duplicate Hashes: {file_path}")
                print()
