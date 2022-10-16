from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader

# Load your workbook and sheet as you want, for example
wb = load_workbook('样例.xlsx')
sheet = wb.active

# Put your sheet in the loader
image_loader = SheetImageLoader(sheet)

# And get image from specified cell
image = image_loader.get('H1')

# Image now is a Pillow image, so you can do the following
image.show()

# Ask if there's an image in a cell
if image_loader.image_in('A4'):
    print("Got it!")