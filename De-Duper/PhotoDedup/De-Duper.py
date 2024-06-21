
# TO-DO -- LOOK AT ENUMERATE  ------  fix  local folder paths -------
#--------------------------------
from PIL import Image                                               # For converting/manipulating images
import numpy as np                                                  # For making numpy arrays
from skimage.metrics import structural_similarity as compare_ssim   # For Comparing Images (AS NUMPY ARRAYS)
#--------------------------------
import imagehash                 # FOR HASHING IMAGES
#--------------------------------
import os
#--------------------------------
import itertools                  # FOR SIMPLE ITERATION 
#--------------------------------
from datetime import datetime     # FOR THE CSV
import csv
#--------------------------------
from tqdm import tqdm             # FOR THE LOADING BARS
#--------------------------------
import pyodbc                     # FOR SQL DB


#-------------- GLOBAL VARIABLES ------------------             

#folder_path = '/Users/sony/Documents/Sony-Documents/Coding/projects/Bootcamp/SOLO END PROJECT/MAIN-COMPLETE/PhotoDedup/photos' 
#folder_path = '/Users/sony/Documents/Sony-Documents/Coding/projects/Bootcamp/SOLO END PROJECT/MAIN-COMPLETE/PhotoDedup/test2' 

folder_path = '/Users/sony/Documents/Sony-Documents/Coding/projects/Bootcamp/SOLO END PROJECT/MAIN-COMPLETE/PhotoDedup/IMAGES'
default_path = '/Users/sony/Documents/Sony-Documents/Coding/projects/Bootcamp/SOLO END PROJECT/MAIN-COMPLETE/PhotoDedup/IMAGES'
images = os.listdir(folder_path)
unique = {}
duplicates = {}

#------------ DB CREDENTIALS -----------------
def connect_sql():
    try:
        SERVER   = "server"      # CHANGE THESE
        DATABASE = "database"
        USERNAME = "username"
        PASSWORD = "password"     # FOR WINDOWS CHANGE DRIVER TO 'SQL SERVER'
        connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        return conn, cursor
    except:
        print('Could not connect to database')
        input("Press Enter to continue...")
        report_export_menu()


#--------------- CHOOSE FOLDER PATH -- OPTION 1 -----------------

def choose_path():
    global folder_path, images
    path_name = input("Enter the path to your Images: ")
    folder_path = path_name
    print(f"You entered: {folder_path}")
    try:
        images = os.listdir(folder_path) 
        input("Press Enter to continue...")
        main()
    except:
        print('That IS NOT a valid folder path:')
        folder_path = default_path 
        print('Try again or use the default folder path')
        input("Press Enter to continue...")
        main()
        
#---------------- SHOWS CURRENT PATH INFO -- OPTION 2 ----------------

def show_path_info():
    print(f"Current path: {folder_path}")
    items = os.listdir(folder_path) 
    total_items = len(items)
    print(f"There are {total_items} Images in your directory ")
    input("Press Enter to continue...")
    main()


#----------- PROCESSING IMAGES -------- AND POPULATE DUPLICATES DICTIONARY -----

#----------- SSIM COMPARE IMAGES ----------------   8, 0.8

#                                                        # STRUCTURAL SIMILARITY INDEX MEASURE
def SSIM_compare_images(size, ssim_threshold):           # itertools.combinations is used to make every every possible combination of 2
    try:                                                 # tqdm is for making a simple loading bar around a loop  
        for image1, image2 in tqdm(itertools.combinations(images, 2), total=len(list(itertools.combinations(images, 2))), desc="Comparing images"):
            path1 = os.path.join(folder_path, image1)    
            path2 = os.path.join(folder_path, image2)    # Joins the folder path with the image name to create full paths to the images.

            img1 = Image.open(path1).convert('L').resize((size, size))   #  This uses the PIL library to convert the images to 
            img2 = Image.open(path2).convert('L').resize((size, size))   #  greyscale ('L') and resize them with the parameter 'size'

            img1 = np.array(img1)                        # Turns the image into a numpy array, which can be  --- [200, 100] --- e.g. A 2x2 greyscale numpy array
            img2 = np.array(img2)                        # used for pixel by pixel image comparison              [150,  50] ---             0 - 255
            
            ssim_value = compare_ssim(img1, img2)        # compare_ssim from skimage library, compares numpy arrays and             
#                                                        # creates a value from -1 to 1 (1 is identical -1 is very different)      
            if ssim_value > ssim_threshold and path2 not in duplicates:   
                duplicates[path2] = (f" {image1} {ssim_value} = {image2}") # Adds duplicate image paths to correct dictionary                      
    except: 
        print('Something went wrong with comparing the images.')     
        input("Press Enter to continue...")              # SSIM_compare_images(8, 0.8) --- Most accurate
        main()                                           # images14, and 10 have (different images) 0.6560811143923908   13 and 6 had (duplicates) 0.6191506331338925


            
#--------------- COMPARE IMAGES WITH DHASH ----------------- 

def dhash_compare_images(size, hash_threshold):       # 8, 21  
    try:
        for image1, image2 in tqdm(itertools.combinations(images, 2), total=len(list(itertools.combinations(images, 2))), desc="Comparing images"):
            path1 = os.path.join(folder_path, image1)    
            path2 = os.path.join(folder_path, image2)   

            hash1 = imagehash.dhash(Image.open(path1).convert('L'), hash_size = size)
            hash2 = imagehash.dhash(Image.open(path2).convert('L'), hash_size = size)

            hash_difference = hash1 - hash2

            if hash_difference < hash_threshold and path2 not in duplicates:
                duplicates[path2] = f"Has a dHash difference of: {hash_difference} with {image1}"
    except:
        print(f'Something went wrong with comparing the images')


#--------------- POPULATES UNIQUE DICTIONARY ----------------- 
                    
def sort_images():
    for image in images:
        path = os.path.join(folder_path, image)
        if path in duplicates:
            unique.pop(path, '')
        else:
            unique[path] = ''

#---------------- EXPORTS DATA TO HTML FILE ----------------

def generate_html_report(unique, duplicates):
    html_content = "<html>"
    html_content += "<head>"
    html_content += '<link rel="stylesheet" href="styles.css">'
    html_content += "</head>"
    html_content += "<body>"

    html_content += "<div>"
    html_content += "<h1>Unique Images</h1>"
    html_content += '<div class="image-container">'
    for image_path in unique:
        html_content += f'<div>'
        html_content += f'<img src="{image_path}">'
        html_content += f'<p>{os.path.basename(image_path)}</p>'
        html_content += '</div>'
    html_content += "</div>"
    html_content += "</div>"

    html_content += "<div>"
    html_content += "<h1>Duplicate Images</h1>"
    html_content += '<div class="image-container">'
    for image_path in duplicates:
        html_content += f'<div>'
        html_content += f'<img src="{image_path}">'
        html_content += f'<p>{os.path.basename(image_path)}</p>'
        html_content += '</div>'
    html_content += "</div>"
    html_content += "</div>"

    html_content += "</body></html>"

    with open("Automation/Image Comparison Results.html", "w") as file:
        file.write(html_content)


    print('Your report has been saved to *Image Comparison Results.html* ')
    input("Press Enter to continue...")    
    report_export_menu()      


#------ FUNCTION TO ADD DICTIONARIES TO CSV------

def dump_to_csv(csv_file, unique, duplicates):
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            heading = ['Hash', 'Image']
            writer = csv.DictWriter(csvfile, fieldnames=heading)     # writer.writeheader() would write the header
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")           #------  ADDS DATE AND TIME ------
            csvfile.write(f'{now}\n')

            csvfile.write("Unique Images:\n")                            #------  WRITE UNIQUE IMAGES  ------
            for img_hash, img_name in unique.items():
                writer.writerow({'Hash': img_hash, 'Image': img_name})

            csvfile.write("\nDuplicate Images:\n")                       #------  WRITE DUPLICATE IMAGES  ------
            for img_hash, img_name in duplicates.items():
                writer.writerow({'Hash': img_hash, 'Image': img_name})
        print(f'Data dumped to CSV file: {csv_file}')
    except:
        print(f'Error - Unable to write to CSV file:')
    input("Press Enter to continue...")    
    report_export_menu()  


#--------------- POPULATES DATABASE -----------------

def sql_add_image(table_name, paths, conn, cursor):
    try:
        for image_path in tqdm(paths, desc=f"Adding images to {table_name} table"):
            cursor.execute(f"INSERT INTO {table_name} (Image_Path) VALUES (?)", (image_path,))
            conn.commit()
        print(f'Successfully added paths to the {table_name} table')
    except:
        print(f"Couldn't add images to {table_name} table")
    conn.close    

#--------------- PRINTS THE PROCESSED DICTIOANRIES TO THE TERMINAL ----------------- 

def print_paths():
    print("Unique Images:")
    for image_path, state in unique.items():
        print(f"{image_path}: {state}")

    print("\nDuplicate Images:")
    for image_path, ssim_value in duplicates.items():
        print(f"{image_path}: {ssim_value}")  
    input("Press Enter to continue...")
    report_export_menu()


#--------------- DELETES DUPLICATES FROM FOLDER USING OS ----------------- 

def delete_duplicates(duplicates):
    for image_path in duplicates:
        try:
            os.remove(image_path)
            print(f"Deleted {os.path.basename(image_path)}")

        except:
            print(f"Error deleting")
    input("Press Enter to continue...")        


#-------------- ANDREW COLOUR IDENTIFIER --------------------

#-------------------------------- IMAGE REZ - ANDREW

def print_image_resolution_info(folder_path):
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith((".jpg", ".png", ".bmp", ".jpeg", ".gif")):
            image_file = os.path.join(folder_path, file_name)
            with Image.open(image_file) as img:
                width, height = img.size
                image_format = img.format
                print(f"Image: {file_name}")
                print(f"Resolution: {width} x {height} pixels")
                print(f"Format: {image_format}")
                print("-" * 30)
    input("Press Enter to continue...")
    additional_options_menu()
    
#-------------------------------- IDENTIFY COLOURS - ANDREW

def is_color_image(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    w, h = img.size
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Reshape the array to 2D (all pixels, RGB values)
    img_array_2d = img_array.reshape(-1, 3)
    
    # Check if all RGB channels are the same for each pixel
    is_grayscale = np.all(img_array_2d[:, 0] == img_array_2d[:, 1]) and np.all(img_array_2d[:, 0] == img_array_2d[:, 2])
    
    return not is_grayscale

#-------------------------------- ANDREW

def identify_image_colors(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            if is_color_image(file_path):
                print(f"{filename} is a color image.")
            else:
                print(f"{filename} is a black and white image.")

#----------------- MAIN MENU ------------------ 

def main():
    global unique
    global duplicates
    unique = {}
    duplicates = {} 
    os.system("clear")
    print("╔══════════════════════════════════════════════════╗")
    print("║     ____             ____                        ║")
    print("║    / __ \___        / __ \__  ______  ___  ____  ║")
    print("║   / / / / _ \______/ / / / / / / __ \/ _ \/ ___/ ║")
    print("║  / /_/ /  __/_____/ /_/ / /_/ / /_/ /  __/ /     ║")
    print("║ /_____/\___/     /_____/\__,_/ .___/\___/_/      ║")
    print("║                             /_/                  ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║                                                  ║")
    print("║ 1) Choose Path                                   ║")
    print("║ 2) Current Path Info                             ║")
    print("║                                                  ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║                                                  ║")
    print("║              ------ PROCESS ------               ║")
    print("║                                                  ║")
    print("║ 3) Process Images   (reliable but wont catch all)║")
    print("║ 4) Process Images 2    (may cause false positive)║")
    print("║ 5) Process Images dhash  (works but not finished)║")
    print("║                                                  ║")
    print("╚══════════════════════════════════════════════════╝")

    choice = input('Input an Option: ')
    
    if choice == "1":
        choose_path()
    elif choice == "2":
        show_path_info()
    elif choice == "3": 
        SSIM_compare_images(8, 0.8) 
        sort_images() 
        input("Press Enter to continue...") 
        report_export_menu()  
    elif choice == "4":   
        SSIM_compare_images(8, 0.8)          # ACCURATE FOR DETECTING DUPES BUT WONT FIND THEM IF THEY'RE TOO DIFFERENT (NO FALSE POSITIVE)
        SSIM_compare_images(128, 0.3)        # FINDS DUPLICATES THAT LESS SIMILAR, BUT CAN ALSO SOMETIMES GET FALSE POSITIVES
        sort_images() 
        input("Press Enter to continue...") 
        report_export_menu()    
    elif choice == "5":   
        dhash_compare_images(8, 21)          # PLAY WITH THESE VALUES
        sort_images()
        report_export_menu()
    elif choice == "6":   
        SSIM_compare_images(8, 0.8) 
        sort_images() 
        input("Press Enter to continue...") 
        report_export_menu()    
    else:
        input("Please Input Valid Option")
        main() 

#---------------- REPORT MENU ------------------- 

def report_export_menu(): 
    os.system("clear") 
    print('YOUR IMAGES HAVE BEEN PROCESSED, AND DUPLICATES SEPARATED') 
    print("\n")
    print("╔════════════════════════════════════════════╗")
    print("║        ____                        __      ║")
    print("║       / __ \___  ____  ____  _____/ /_     ║")
    print("║      / /_/ / _ \/ __ \/ __ \/ ___/ __/     ║")
    print("║     / _, _/  __/ /_/ / /_/ / /  / /_       ║")
    print("║    /_/ |_|\___/ .___/\____/_/   \__/       ║")
    print("║              /_/                           ║") 
    print("╠════════════════════════════════════════════╣")
    print("║                                            ║")
    print("║ 1) Print Report to Terminal                ║")
    print("║                                            ║")
    print("╠════════════════════════════════════════════╣")
    print("║                                            ║")
    print("║         --------- EXPORT ---------         ║")
    print("║                                            ║")    
    print("║ 2) HTML FILE                               ║")
    print("║ 3) CSV FILE                                ║")
    print("║ 4) LOCAL DB                                ║")
    print("║ 5) DELETE Duplicates                       ║")
    print("║                                            ║")
    print("║ 6) Additional Options...                   ║")
    print("║                                            ║")
    print("║ 7) Main Menu                               ║")
    print("║                                            ║")    
    print("╚════════════════════════════════════════════╝")

    
    choice = input('Input an Option: ')
    
    if choice == "1":
        os.system("clear") 
        print_paths()
    elif choice == "2":
        generate_html_report(unique, duplicates)
    elif choice == "3":
        dump_to_csv('Automation/images.csv', unique, duplicates)
    elif choice == "4":
        conn, cursor = connect_sql()   # connecr_sql returns the values of conn and cursor to be used in the function below
        sql_add_image('unique_images', unique.keys(), conn, cursor)
        sql_add_image('duplicate_images', duplicates.keys(), conn, cursor)
        input("Press Enter to continue...")
        report_export_menu()
    elif choice == "5":
        confirm = input("Are you sure you want to delete the duplicate images? (y/n) ")
        if confirm.lower() == "y":
            delete_duplicates(duplicates)
            print("Duplicate images have been deleted.")
        else:
            print("Duplicate image deletion canceled.")
        report_export_menu()        
    elif choice == "6":
        additional_options_menu()       
    elif choice == "7":
        main()    
    else:
        input("Please Input Valid Option")
        report_export_menu()    


#-------------------------------- ADDITIONAL OPTIONS MENU - ANDREW 

def additional_options_menu():
    os.system("clear")
    print("╔═════════════════════════════════════════╗")
    print("║         Additional Options Menu         ║")
    print("╠═════════════════════════════════════════╣")
    print("║ 1) Print Image Resolution Information   ║")
    print("║ 2) Color and B&W Detection              ║")
    print("║                                         ║")
    print("║ ...                                     ║")
    print("║ 0) Back to Report Menu                  ║")
    print("╚═════════════════════════════════════════╝")

    choice = input('Input an Option: ')

    if choice == "1":
        print_image_resolution_info(folder_path)
    elif choice == "2":
        identify_image_colors(folder_path)
        input("Press Enter to continue...")
        additional_options_menu()
    elif choice == "0":
        report_export_menu()
    else:
        input("Please Input Valid Option")
        additional_options_menu()  


#-------------------------------- EXECUTE

if __name__ == "__main__":
    main()