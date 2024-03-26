from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

class TitlePic:

    def __init__(self, text, author, sub):
        self.title = text
        self.author = author
        self.sub = sub

    def generate(self, filename):
        offset = 0
        fontsize = 1
        font = ImageFont.truetype("Roboto-Regular.ttf", fontsize)
        
        im1 = Image.open(f"Base_Images/redditTitle{self.sub}.png")
        img = im1.copy()

        d = ImageDraw.Draw(img)

        fontsize = 51
        font = ImageFont.truetype("Roboto-Medium.ttf", fontsize)

        x=43

        count = 0
        for line in textwrap.wrap(self.title, x):
            count+=1

        for line in textwrap.wrap(self.title, x):
            d.text((50, 154+offset),line, fill=(8, 8, 8),font=font)
            offset+=65

        fontsize = 36
        font = ImageFont.truetype("Verdana.ttf", fontsize)
        d.text((139, 68), 'u/' + str(self.author) + " · " + str(random.randrange(1, 7)) + "d", fill=(120, 120, 120), font=font)
        d.text((139, 68), 'u/' + str(self.author), fill=(23, 104, 159), font=font)

        width, height = img.size

        marginbottom = 30
        left = 0
        right = width
        top = 0
        bottom = offset + 154 + marginbottom

        imgsave = img.crop((left, top, right, bottom))
        
        width, height = imgsave.size
        small = imgsave.resize((int(round(width * 0.80)), int(round(height * 0.80))))
        width, height = small.size

        imgbg = Image.new('RGBA', (1080, 1920), color=(0, 0, 0, 0))

        imgbg.paste(small, (int(round(1080/2 - width/2)), int(round(1920/2-height/2))), mask = small) 

        imgbg.save(filename)
