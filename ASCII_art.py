from PIL import Image
import glob

def get_image_filenames(file_list):
    stripped_paths = []
    for item in file_list:
        not_finished = True
        index = len(item) - 1
        while not_finished:
            if item[index] == "\\":
                not_finished = False
            else:
                index -= 1
        index += 1
        stripped_paths.append(item[index:])
    return stripped_paths
        
def menu(filenames):
    #filter_image_files(files)
    print("\nWhich image file would you like to open?\n")
    for index, image in enumerate(filenames):
        print("-" + str(index) + ": " + image)
    print()
    choice = input("")
    if not choice.isdigit():
        return -1
    else:
        return int(choice)

def print_image(grey_img, width, height):
    """Prints out the image in the console"""
    for y in range(height):
        for x in range(width):
            #prints the value 3 times so the image isn't squashed
            print(grey_img[y][x], end="")
            print(grey_img[y][x], end="")
            print(grey_img[y][x], end="")
        print()

def convert_to_ascii(bright_val, ascii_len):
    """returns the index of the ascii string that fits the brightness value"""
    interval = 255 / ascii_len
    return int(round(bright_val / interval)) - 1

def write_to_file(grey_img, width, height):
    f = open("output.txt", "w")
    for y in range(height):
        for x in range(width):
            #prints the value 3 times so the image isn't squashed
            f.write(grey_img[y][x] * 3)
            #f.write(grey_img[y][x], end="")
            #f.write(grey_img[y][x], end="")
        f.write("\n")
    f.close()

def ascii_art(directory, size_factor=1, inverted=False):
    """creates a text version of an image!!!"""
    files = glob.glob(directory + "*.jpg")
    filenames = get_image_filenames(files)
    index = menu(filenames)

    if index == -1: #make this more forgiving
        print("bad input!")
        return

    #sets up the file for reading data
    img = Image.open(directory + filenames[index])
    #optionally shrinks the image to fit the terminal better
    img = img.resize((img.width // size_factor, img.height // size_factor))
    #img.show()
    img_vals = list(img.getdata())
    grey_scale = []
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    for y in range(img.height): #loads the new array with indexes
        row = []
        for x in range(img.width):
            row.append("")
        grey_scale.append(row)

    for i in range(len(img_vals)): #load 3 digit pixel values into grey-scale values
        y = i // img.width
        x = i % img.width
        #converts the RGB to Grey-scale
        grey_scale_val = (img_vals[i][0] + img_vals[i][1] + img_vals[i][2]) / 3
        #inverts the color if inverted parameter is true
        if inverted:
            grey_scale_val = 255 - grey_scale_val
        #finds the corresponding ascii character
        index = convert_to_ascii(grey_scale_val, len(ascii_chars))
        #applies the ascii
        grey_scale[y][x] = ascii_chars[index]

    write_to_file(grey_scale, img.width, img.height)

    img.close()
    return

ascii_art("C:\\Users\\Ryan Brasseaux\\Desktop\\python-files\\MessAround\\CodingChallenges\\ASCII_art\\Images\\", size_factor=5, inverted=False)