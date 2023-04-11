from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import cv2 as cv
from io import BytesIO
import pytesseract
#create the app
from PIL import Image
app = Flask(__name__)

#configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create the extension
db = SQLAlchemy(app)


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        
    def __repr__(self):
        return f"Filename is {self.filename}"
    

# def download(upload_id)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        
        # text = ''
        with app.app_context():
            db.create_all()
            upload = Upload(filename=file.filename, data=file.read())
            db.session.add(upload)
            db.session.commit()
            
            #process the image
            download = Upload.query.filter_by(filename=file.filename).first()
            with open(f"./uploads/{download.filename}.png", "wb") as f:
                f.write(download.data)
                # image = cv.imread(f.write(download.data),0)
                # text = pytesseract.image_to_string(f.write(download.data))
            image = cv.imread(f'./uploads/{download.filename}.png',0)
            # if image:
                
            text = pytesseract.image_to_string(image)
                
                # grey = cv.COLOR_BGR2GREY(image)
            
        return send_file(open(f"{download.filename}.txt", 'w'))
    
    return render_template('index.html')
    
if __name__ == '__main__':
    db.create_all()
    app.run()