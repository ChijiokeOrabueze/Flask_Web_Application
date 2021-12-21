from PIL import Image

im = Image.open('StarWars/static/images/profile_pic/default.jpg')

ot = (125,125)

im.thumbnail(ot)

im.save('StarWars/static/images/profile_pic/default2.png')