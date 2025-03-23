"""
Generates a card image to represent a given card.
The values for this are HARDCODED.
If you change them, the cards will look completely different.
Proceed with the utmost caution!

"""
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

def make_image(background:str, title:str, desc:str, image, env:float, beauty:float, cost:float):

    """
        Written by Adam
        script for generating card images in the backend

        Args:
        background: a path to the background image for the card, represented as a string
        title: the name of the card
        subtitle: the text below the name of the card
        font: a path to a font used to write text on the card
        font_bf: a path to a bold font used to write text on the card
        desc: the description of the card, written to a box below the image
        image: either a string representing a path to an image, or a django ImageField object

    Returns:
    a PIL image file representing the card image
    """

    try:
        #Opens and resizes the background image.
        back = Image.open(background)
        back = back.resize((1200,1600))
        front = Image.open(image)
    except FileNotFoundError:
        print("help!")
        return 1
    
    #Scales foreground image and pastes it on to the background.
    front = front.resize((885,618))
    Image.Image.paste(back,front, (156,210))
    draw = ImageDraw.Draw(back)

    title_font = ImageFont.truetype("static/card_gen/font/Kanit-Bold.ttf", 84)
    stat_font = ImageFont.truetype("static/card_gen/font/Kanit-Bold.ttf", 84)
    desc_font = ImageFont.truetype("static/card_gen/font/Kanit-Regular.ttf", 50)

    stat_line = "Impact: "+str(env) + "\nCost: "+str(cost) + "\nBeauty: "+str(beauty)
    draw.text((160,72), title, font=title_font, fill=(255,255,255)) #adds title

    #Turns out there's no nice way to draw text across multiple lines.
    #We just have to separate the text into several lines and write each line.
    #In terms of font size and line length we just have to guess and check.

    MAX_CHARS:int = 32   #Defines how many chars we can have in a line before we wrap around.
    count:int = 0
    positions = []   #Stores positions at which we need to have a newline char.
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
    #Rewrites string but with newlines instead of spaces where required.
    for i in range(0,len(desc)):
        if i in positions:
            des_mod += "\n"
        else:
            des_mod += desc[i]
        
    #Writes description onto the card.
    draw.multiline_text((160,860), des_mod, font=desc_font, fill=(0,0,0))
    draw.text((160,1200), stat_line, font=stat_font, fill=(0,0,0))
    #Returns the generated image.
    return back    

