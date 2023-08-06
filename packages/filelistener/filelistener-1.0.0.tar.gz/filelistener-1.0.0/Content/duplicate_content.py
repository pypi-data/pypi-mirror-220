import os
import argparse
import platform
import subprocess
from collections import defaultdict
from Content.modules.duplicate_zip_files import print_duplicate_zip_files


def get_file_hash(file_path):
    """Calculate the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.

    """
    try:
        if platform.system() == "Darwin":
            # macOS (use md5 command)
            md5_output = subprocess.check_output(["md5", file_path], universal_newlines=True)
            file_hash = md5_output.split()[-1]  # Extract the hash from the output
            return file_hash
        else:
            # Linux/Unix-based systems (use md5sum command)
            md5sum_output = subprocess.check_output(["md5sum", file_path], universal_newlines=True)
            file_hash = md5sum_output.split()[0]  # Extract the hash from the output
            return file_hash
    except subprocess.CalledProcessError as e:
        # Handle any errors that might occur during the md5sum command execution
        print(f"Error calculating hash for {file_path}: {e}")
        return None
    

def check_files_in_folder(folder_path, calculate_file_sizes):
    """Check for duplicate files in a folder.

    This function traverses through the specified folder and its subdirectories,
    calculates the MD5 hash of each file, and identifies duplicate files by their hashes.

    Args:
        folder_path (str): The path to the folder.

    """
    # Using collections module defaultdict
    # Using a single dictionary to store duplicate files based on hash and size
    duplicate_files = defaultdict(lambda: defaultdict(list))
    
    # Traverse through the folder and its subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = get_file_hash(file_path) # Calculate the hash of the file
            # file_hashes[file_hash].append(file_path) # Store the file path with its hash
            
            if calculate_file_sizes:
                file_size = os.path.getsize(file_path)
                file_info = (file_path, file_hash)  # Create a tuple with file_path and file_hash
                duplicate_files[file_size][file_hash].append(file_info)
                
            # Store the file path with its hash in the dictionary
            duplicate_files[file_hash]['file_paths'].append(file_path)
        
        for subfolder in dirs:
            subfolder_path = os.path.join(root, subfolder)
            check_files_in_folder(subfolder_path, calculate_file_sizes)  # Recursive call to check files in nested folder

    # Iterate over the file hashes and their corresponding file paths
    for size, hash_dict in duplicate_files.items():
        for file_hash, file_info_list in hash_dict.items():
            if file_hash == 'file_paths':
                continue
                
            if len(file_info_list) > 1: # Check if there are multiple file paths with the same hash
                print(f"Duplicate files with hash {file_hash} and size {size} bytes:")
                for file_info in file_info_list:
                    file_path, _ = file_info  # Unpack the tuple, but we only need the file_path
                    print(f"Name: {os.path.basename(file_path)}")
                    print(f"Absolute Path: {file_path}")
                print()

    if not calculate_file_sizes:
        for file_hash, file_paths in duplicate_files.items():
            if file_hash == 'file_paths':
                continue

            if len(file_paths) > 1:
                print(f"Duplicate files with hash {file_hash}:")
                for file_path in file_paths:
                    print(file_path)
                print()
def main():
    parser = argparse.ArgumentParser(description='Check for duplicate files in a folder.')
    parser.add_argument('-f', '--folder', required=True, help='Path to the folder')
    parser.add_argument('-s', '--calculate-sizes',required=True, action='store_true', help='Calculate duplicate file sizes')
    args = parser.parse_args()

    folder_path = args.folder
    calculate_sizes = args.calculate_sizes

    check_files_in_folder(folder_path, calculate_sizes)

    # After checking for duplicate files in the folder, print duplicate zip files
    print_duplicate_zip_files(folder_path)

if __name__ == '__main__':
    main()
    