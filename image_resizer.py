import os, sys
from PIL import Image
from flask import Flask, send_from_directory, request
import urllib.request
app = Flask(__name__)

def getImgName(path):
    paths = path.split("/")
    imgName = paths[len(paths)-1].split('.')[0]
    return imgName

def downloadImage(path):
    imgName = getImgName(path)
    urllib.request.urlretrieve('https://%s' % path, "./stored/%s.png" % imgName)
    return "./stored/%s.png" % imgName

def fitImage(path):
    size = 764, 400
    imgName = getImgName(path)
    if os.path.isfile("./cached/%s.png" % imgName):
        return imgName
    else:
        try:
            img = downloadImage(path)
            im = Image.open(img)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save("./cached/%s.png" % imgName, "png")
            try:
                os.remove("./stored/%s.png" % imgName)
            except OSError as oserr:
                print(oserr)
            return imgName
        except IOError:
            print("cannot create thumbnail for '%s'" % imgName)


@app.route('/images')
def get_image():
    pid = request.args.get('url')
    img = fitImage(pid)
    return send_from_directory('./cached/', img+".png")

if __name__ == '__main__':
    app.run(debug=False, port=5000, host="127.0.0.1")
