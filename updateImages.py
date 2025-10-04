# ======================= Image Updating Script ==========================
# ======================== Written by Sandstorm ==========================
# It assembles all the shiny pokemon, and warns of any palette swap issues

source_dir = "./game_files/live/public/images/pokemon"
# source_dir = "./game_files/beta/public/images/pokemon" # File path for beta pre-load
# The official files from github must be in "game_files/live" folder, in same directory as this script
# Either clone the github repo, or download and unzip the zip file from github

dest_dir = "./website/images"
# Where to put all the processed images

# =============================== Options ================================

overrideSpriteList = []
# Specify a subset of images, rather than running the entire list
# Each entry must be a string, like this: overrideSpriteList = ['692','3-mega']
# Leave blank to run all the images that are found in source_dir

warnMissingColors = 0
# Warns if at least x different colors listed in the json are NOT found in the image
# This helps find redundant or incorrect entries in the json
# Set to 0 to ignore this check, or set to 1 to report all missing colors

warnSimilarColors = 0
# Warns if colors exist that are less than x bits different on all channels (R/G/B)
# This was important when 'fuzzy color matching' was in the game, however, it is no longer relevant
# Set to 0 to ignore this check

warnPureBlackJson = 0
# Warns if pure black is found on a json
# Set to 0 to ignore this check

# Since there is no official static frame, one must be chosen
# By defualt, it chooses the most common frame of the animation 
# However, you can override here to choose a specific frame
overrideFrame = {
    '12':0,
    '49':0,
    '68':0,
    '890':-8
}

# ==================== Do not touch below this line ======================

import re, os, json
import numpy as np
from PIL import Image

# Function to convert hex to RGBA
def hex_to_rgba(hex_code):
    hex_code = hex_code.lstrip("#") # Remove '#' if present
    hex_code = hex_code[:6]
    if len(hex_code) == 6:  # Format #RRGGBB
        hex_code += "FF"    # Add full opacity if alpha is not specified
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4, 6))
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#") # Remove '#' if present
    hex_code = hex_code[:6]
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# Function to do palette swap
def palette_swap(image, json_path, tier):
    if not os.path.isfile(json_path):
        return None
    with open(json_path, "r") as f:
        data = json.load(f)
    tier_key = str(tier - 1)
    if tier_key not in data:
        return None
    hexDict = data[tier_key]
    rgb2rgbaDict = {hex_to_rgb(key): hex_to_rgba(hexDict[key]) for key in hexDict}
    # Check for similar color keys
    if warnSimilarColors or warnPureBlackJson:
        for index, color in enumerate(rgb2rgbaDict.keys()):
            if warnPureBlackJson and color == (0,0,0):
                print("Pure black found in:",json_path.split('/')[-1])
            if warnSimilarColors:
                for index2, color2 in enumerate(rgb2rgbaDict.keys()):
                    if color != color2 and index2 > index:
                        diff = [abs(color[i] - color2[i]) <= warnSimilarColors for i in [0,1,2]]
                        if all(diff):
                            print('Similar colors:',color,color2,'\n',json_path.split('/')[-1])
    colorFound = {key: 0 for key in rgb2rgbaDict}
    image = image.convert("RGBA") # Ensure the image is in RGBA mode
    # Convert to NumPy array
    data = np.array(image)  # shape: (height, width, 4)
    # Mask for non-transparent pixels (alpha != 0)
    alpha_mask = data[:, :, 3] != 0
    # Iterate only over keys in rgb2rgbaDict
    for rgb, new_rgba in rgb2rgbaDict.items():
        # Create a mask for matching RGB where alpha != 0
        match = np.all(data[:, :, :3] == rgb, axis=-1) & alpha_mask
        colorFound[rgb] = match.any() # Note that the color was found
        data[match] = new_rgba # Assign new RGBA
        alpha_mask[match] = False # Prevent a swapped color from swapping again
    image = Image.fromarray(data, mode="RGBA") # Convert back to PIL image
    if len(colorFound) - sum(colorFound.values()) >= warnMissingColors and warnMissingColors:
        print('Missing',len(colorFound) - sum(colorFound.values()),'colors from',json_path.split('/')[-1])
    return image

def getBestFrame(thisImgPath, altJsonPath=''):
    # This looks at all the frames in the animation sheet, and crops to the most common one
    thisImage = Image.open(f'{thisImgPath}.png')
    if not os.path.isfile(f'{thisImgPath}.json'): # If there is no specific json
        thisImgPath = altJsonPath
    if not os.path.isfile(f'{thisImgPath}.json'): # If there is no default json
        input('json error')
    with open(f'{thisImgPath}.json', "r") as f:
        jsonLoad = json.load(f)
    if 'textures' in jsonLoad:
        allFrames = jsonLoad['textures'][0]['frames']
    else:
        allFrames = jsonLoad['frames']
    indFrames = [line['frame'] for line in allFrames] # Each frame
    # If the pokemon has an override frame, only use that frame
    if thisImgPath.split('/')[-1] in overrideFrame:
        if len(indFrames) >= abs(overrideFrame[thisImgPath.split('/')[-1]]):
            indFrames = [indFrames[overrideFrame[thisImgPath.split('/')[-1]]]]
    frameCount = [0 for line in indFrames]
    for line in indFrames:
        for i in range(len(indFrames)):
            if line['x'] == indFrames[i]['x'] and line['y'] == indFrames[i]['y']:
                if line['w'] == indFrames[i]['w'] and line['h'] == indFrames[i]['h']:
                    frameCount[i] += 1 # Count how many times each frame occurs
    for i in range(len(indFrames)):
        if frameCount[i] == max(frameCount): # Choose the first most common frame
            x,y,w,h = indFrames[i]['x'], indFrames[i]['y'], indFrames[i]['w'], indFrames[i]['h']
            return thisImage.crop((x, y, x+w, y+h))

# Function to do palette swap NEWWWWWWWWWWWWWWWWWWWWWWWWWWW
def new_palette_swap(image, json_path, tier):
    if not os.path.isfile(json_path):
        return None
    with open(json_path, "r") as f:
        data = json.load(f)
    tier_key = str(tier - 1)
    if tier_key not in data:
        return None
    hexDict = data[tier_key]
    rgb2rgbDict = {hex_to_rgb(key): hex_to_rgb(hexDict[key]) for key in hexDict}
    # Check for similar color keys
    if warnSimilarColors or warnPureBlackJson:
        for index, color in enumerate(rgb2rgbDict.keys()):
            if warnPureBlackJson and color == (0,0,0):
                print("Pure black found in:",json_path.split('/')[-1])
            if warnSimilarColors:
                for index2, color2 in enumerate(rgb2rgbDict.keys()):
                    if color != color2 and index2 > index:
                        diff = [abs(color[i] - color2[i]) <= warnSimilarColors for i in [0,1,2]]
                        if all(diff):
                            print('Similar colors:',color,color2,'\n',json_path.split('/')[-1])

    # Access the palette (returns a flat list of RGB triples)
    palette = image.getpalette()  # length is 256*3 internally

    # Modify the first few colors (used colors)
    for i in range(0,len(palette),3):
        key = (palette[i],palette[i+1],palette[i+2])
        if key in rgb2rgbDict:
            palette[i],palette[i+1],palette[i+2] = rgb2rgbDict[key]

    # Apply the modified palette back
    image.putpalette(palette)
    return image

def addPartnerHeart(img): # Adds a heart image onto the partner pokemon image
    # Expand the original image width, more for eevee
    widthAdd = 5+10*(img.width < 40) 
    new_size = (img.width + widthAdd, img.height)
    expanded_image = Image.new("RGBA", new_size, (0, 0, 0, 0))
    expanded_image.paste(img, (0, 0))
    # Open the second image to paste
    overlay_image = Image.open("website/ui/partnerheart.png")
    overlay_pos = (new_size[0] - overlay_image.width, new_size[1] - overlay_image.height)
    # Create a temporary layer for blending
    temp_layer = Image.new("RGBA", expanded_image.size, (0, 0, 0, 0))  # Transparent layer
    temp_layer.paste(overlay_image, overlay_pos)  # Paste the image onto the temp layer
    expanded_image = Image.alpha_composite(expanded_image, temp_layer)
    return expanded_image

def convert_to_exact_palette(img: Image.Image) -> Image.Image:
    """
    Convert an RGBA/RGB image into P mode with an exact palette.
    Preserves all unique colors, avoids quantization shifts.
    """

    # Ensure RGBA
    arr = np.array(img.convert("RGBA"))
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 4)
    for i in range(len(pixels)): # Make transparent pixels actually zero
        if pixels[i][3] == 0:
            pixels[i][:3] = np.array([0,0,0])

    # Collect unique colors
    unique_colors = np.unique(pixels, axis=0)

    if len(unique_colors) > 256:
        raise ValueError(f"Too many colors ({len(unique_colors)}). Cannot fit into P-mode (max 256).")

    # Build palette (R,G,B only)
    palette = []
    for rgba in unique_colors:
        r, g, b, a = rgba
        palette.extend([r, g, b])

    # Pad palette to 256 entries (768 values) (doesn't affect file size)
    while len(palette) < 768:
        palette.extend([0, 0, 0])

    # Create P image
    p_img = Image.new("P", (w, h))
    p_img.putpalette(palette)

    # Map colors to indices
    color_to_index = {tuple(rgba): idx for idx, rgba in enumerate(unique_colors)}
    indices = np.array([color_to_index[tuple(rgba)] for rgba in pixels], dtype=np.uint8)
    indices = indices.reshape(h, w)
    p_img.putdata(indices.flatten())

    # Handle transparency
    if (0, 0, 0, 0) in color_to_index:
        p_img.info['transparency'] = color_to_index[(0, 0, 0, 0)]

    return p_img

def processImage(spriteIndex, shinyIndex, femIndex):
    thisPath = source_dir
    varPath = f'{source_dir}/variant'
    defPath = source_dir
    simpleName = f'{spriteIndex}_{shinyIndex}'
    if shinyIndex == 1:
        thisPath = f'{thisPath}/shiny'
    elif shinyIndex > 1:
        thisPath = f'{thisPath}/variant'
    if femIndex == 1:
        thisPath = f'{thisPath}/female'
        varPath = f'{varPath}/female'
        defPath = f'{defPath}/female'
        simpleName = f'{simpleName}f'
    thisPath = f'{thisPath}/{spriteIndex}'
    varPath = f'{varPath}/{spriteIndex}'
    defPath = f'{defPath}/{spriteIndex}'
    savePath = f'{dest_dir}/{simpleName}'
    sliced_img = None
    if shinyIndex and os.path.isfile(f'{varPath}_{shinyIndex}.png'): 
        # Check for custom shiny first
        sliced_img = getBestFrame(f'{varPath}_{shinyIndex}',defPath)
    elif shinyIndex and os.path.isfile(f'{varPath}.json'): 
        # Check for palette swap (sometimes even T1)
        sliced_img = getBestFrame(defPath)
        if sliced_img.mode != 'P':
            sliced_img = convert_to_exact_palette(sliced_img)
        sliced_img = new_palette_swap(sliced_img, f'{varPath}.json', shinyIndex)
    if not sliced_img and os.path.isfile(f'{thisPath}.png'):
        # If not custom, use official shiny
        sliced_img = getBestFrame(thisPath,defPath)
    if sliced_img:
        # Add partner heart to pika and eevee
        if 'partner' in spriteIndex: 
            sliced_img = addPartnerHeart(sliced_img)

        # Crop to a bounding box of solid pixels
        pixels = np.array(sliced_img)
        if sliced_img.mode == 'P':
            for x in range(len(pixels)):
                for y in range(len(pixels[x])):
                    pixels[x][y] = (pixels[x][y] != sliced_img.info['transparency'])
        sliced_img = sliced_img.crop(Image.fromarray(pixels, mode=sliced_img.mode).getbbox())

        # Strip the color profile to save space (it is useless for pixel art)
        sliced_img.info.pop('icc_profile', None)

        if sliced_img.mode != 'P':
            sliced_img = convert_to_exact_palette(sliced_img)

        # Check for differences with the previous image
        prev_img = Image.open(f"{savePath}.png")
        arr_new = np.array(sliced_img.convert("RGBA"))
        arr_old = np.array(prev_img.convert("RGBA"))
        if arr_new.shape != arr_old.shape:
            print('Size changed in',simpleName)
        else:
            changed_mask = np.any(arr_new[:, :, :3] != arr_old[:, :, :3], axis=-1)  # Compare RGB only
            alpha_mask = arr_new[:, :, 3] > 0  # Only count pixels that are not fully transparent
            pixelsChanged = np.sum(changed_mask & alpha_mask)
            if pixelsChanged: print(pixelsChanged,'pixels changed in',simpleName)

        # Save the image to the website folder
        sliced_img.save(f"{savePath}.png", optimize=True, compress_level=9)
        # sliced_img.save(f"{savePath}.png")
        
        global biggestH, biggestW # Update the largest dimensions
        biggestH = max(biggestH, sliced_img.height)
        biggestW = max(biggestW, sliced_img.width)
    else: # There is no image
        if shinyIndex < 2 and femIndex == 0: # If it should exist, show an error
            print('Could not find any tier',shinyIndex,'shiny for',spriteIndex)

os.makedirs(dest_dir, exist_ok=True) # Ensure the directory exists

# List the dex no of all the sprite files, this is IMPORTANT for assigning dex numbers
print('\nReading all regional dex numbers...')
# List all files in the current directory
files = [file for file in os.listdir(source_dir) if file.lower().endswith('.png')]
baseFormFiles = []
# Define the pattern to match
pattern1 = lambda filename: filename.endswith("s.png") and filename[-6].isdigit()
pattern2 = re.compile(r'\d+s-')
pattern3 = re.compile(r'\d+_\d')
pattern4 = re.compile(r'sub.png')
# Loop through files and create the list of files that are only base species
for file in files:
    if not pattern1(file) and not pattern2.search(file) and not pattern3.search(file) and not pattern4.search(file):
        baseFormFiles.append(file)
filenames = [re.sub(r'-.*','',file) for file in baseFormFiles] # Remove form names
filenames = [re.sub(r'_.*','',file) for file in filenames]     # Remove form names
filenames = [re.sub(r'.png','',file) for file in filenames]    # Remove file extensions
filenames = [int(file) for file in filenames]
filenames.sort()
regionalFormNumbers = [str(file) for file in filenames if file > 1025]
output_file = "./local_files/my_json/regionalformnumbers.txt"
try:
    with open(output_file, 'w') as file:
        file.write("\n".join(regionalFormNumbers))
    print(f"List of regional form numbers saved to {output_file}")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")

# Assemble the list of all images to be processed
png_files = [file for file in os.listdir(source_dir) if file.lower().endswith('.png') and not file.lower().endswith('sub.png')]
spriteNames = [re.sub('.png','',file) for file in png_files]
biggestW, biggestH = 0, 0
# Use override list if applicable, instead of the full list
if overrideSpriteList: 
    spriteNames = [str(name) for name in overrideSpriteList]
    print('\n***** Running with override sprite list *****')
    print(f'\nProcessing {len(overrideSpriteList)} images...')
else:
    print('\nProcessing all images...')

# Loop through each sprite in the list
for thisSpriteName in spriteNames:
    for thisShinyIndex in [0,1,2,3]:
        for thisFemIndex in [0,1]:
            processImage(thisSpriteName, thisShinyIndex, thisFemIndex)

if overrideSpriteList: 
    print(f'\nFinished processing {len(overrideSpriteList)} images')
else:
    print('\nFinished processing all the images')
print('Largest width:' ,biggestW) # usually 115
print('Largest height:',biggestH) # usually 119
print('\n======= ALL DONE =======\n')

# ********* Reminder for what colors and indices are used
# color     yellow      blue        red   
# hex       0xf8c020    0x20f8f0    0xe81048
# rgb       (248,192,32)(32,248,240)(232,16,72)
# tier      1           2           3
# _#.png    1           2           3
# json[#]   0           1           2