from PIL import Image
import shutil

def makePDF(img):
    image1 = Image.open(img)
    im1 = image1.convert('RGB')
    im1.save('image.pdf')
    shutil.move('image.pdf','./data/')