from flask import Flask, render_template, request,redirect, url_for
import os
from werkzeug.utils import secure_filename
from email.mime import image
from PIL import Image
from pdf2image import convert_from_path
import numpy
def checkImage(fileName):
    images = convert_from_path(os.path.join('C:/wamp64/wamp64/www/TCPC_Flask-project/tempFiles',fileName)) #concat the absoulte path with the file name 
    image = images.pop()
    #Cropping Image
    width, height = image.size
    left = width / 6
    top = height / 6
    right = 5 * width / 6
    bottom = 5 * height / 6
    image = image.crop((left, top, right, bottom))
   # image.show() can be used to show each image after cropping

    #Getting Image RGB Information
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == "RGB": # For RGB Images
        channels = 3
    elif image.mode == "L": # For Gray Scale Images
        channels = 16
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels)) # 2D Array of Image Pixels

    greyscale = True
    rich_Black = True
    for pic in pixel_values:
        for pi in pic:
            r,g,b = pi
            avg = (r+g+b)/3 #Average of RGB Values
            if not (avg == 255):
                if not ( avg <= 25): ## For rich Black Check
                    rich_Black = False
                if not ( (abs(avg-r)<9) and (abs(avg-g)<9) and (abs(avg-b)<9) ): ##to idendify if the image is greyscale or not 
                    greyscale = False

    if rich_Black:
        return "フルカラーまたはリッチブラックなのでモノクロで印刷して良いかお客様に聞いてください"
    elif greyscale:
        return "期待値モノクロ"
    else:
        return "期待値フルカラー"

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='C:/wamp64/wamp64/www/TCPC_Flask-project/tempFiles'
@app.route('/')
def upload_file():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
      f = request.files.getlist("file[]")
      print(f)
      a={}
      for file in f :
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
          a.update({file.filename:checkImage(secure_filename(file.filename))})
          os.chdir(r"C:/wamp64/wamp64/www/TCPC_Flask-project/tempFiles")
          all_files = os.listdir()
          for f in all_files:
            os.remove(f)
          ##a.append(checkImage(secure_filename(file.filename)))
      return render_template('result.html',text=a)
if __name__ == '__main__':
   app.run(debug = True)