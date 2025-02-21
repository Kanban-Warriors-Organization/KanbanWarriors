#script for generating a card image
#a background, foreground image, title, subtitle and description are needed as parameters
#the values in this script are HARDCODED.
#if you change them around, the resulting card may look very different!
#proceed with caution
#-AGP-

from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

def make_image(background:str, title:str, subtitle:str, font:str, font_bf:str, desc:str, image) -> int:


    try:
        back = Image.open(background) #opens background image
        front = Image.open(image) #opens foreground image
    except FileNotFoundError:
        print("help!")
        return 1
    
    front = front.resize((400,300)) #scales foreground image
    Image.Image.paste(back,front, (100,170)) #pastes image on
    draw = ImageDraw.Draw(back)
    #path:str = str(Path(__file__).parent.absolute())

    bold = ImageFont.truetype(font_bf, 32) #creates font objects that we need 
    st_font = ImageFont.truetype(font, 32)
    reg_font = ImageFont.truetype(font, 16)
    draw.text((80,64), title, font=bold, fill=(16,64,16)) #adds title
    draw.text((80,108), subtitle, font=st_font, fill=(16,64,16)) #adds subtitle

    #oh no
    #turns out there's no nice way to draw text across multiple lines
    #we just have to separate the text into several lines and write each line
    #in terms of font size and line length we just have to guess and check
    MAX_CHARS:int = 54 #ie. how many chars we can have in a line before we wrap around
    
    count:int = 0
    positions = [] #stores positions at which we need to have a newline char
    des_mod:str = ""

    for i in range(0,len(desc)):
        if desc[i] == " ":
            if count > MAX_CHARS:
                positions.append(i)
                count = 0
            else:
                pos = i
                count += 1
        else:
            count += 1

    for i in range(0,len(desc)): #rewrites string but with newlines instead of spaces when needed
        if i in positions:
            des_mod += "\n"
        else:
            des_mod += desc[i]
        
                
    draw.multiline_text((80,512), des_mod, font=reg_font, fill=(0, 128, 64)) #writes description
    #output_path = title.replace(" ", "_") + ".png" #sanitises name
    #back.save(output_path) #saves image out
    print("success!")
    return back #returns to signify success
    
#test

