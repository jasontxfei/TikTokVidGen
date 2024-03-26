from PIL import Image, ImageDraw, ImageFont

class Imager:
    def __init__(self, mainCom, author, title):
        self.mainCom = mainCom
        self.author = author
        self.title = title

    def generate(self, filename):
        fontsize = 1
        font = ImageFont.truetype("Verdana.ttf", fontsize)

        img = Image.new('RGBA', (1080, 1920), color=(0, 0, 0, 0))

        d = ImageDraw.Draw(img)

        fontsize = 100
        font = ImageFont.truetype("Verdana Bold.ttf", fontsize)

        width, height = d.textsize(self.mainCom, font = font)

        while width > 1910:
            fontsize += -10
            width, height = d.textsize(self.mainCom, font = font)
        
        width, height = d.textsize(self.mainCom, font = font)

        d.text((1080/2 - width/2, 1920/2 - height/2), self.mainCom, stroke_width=10, stroke_fill=(0, 0, 0), fill=(252, 227, 3),font=font)
    
        img.save(filename)