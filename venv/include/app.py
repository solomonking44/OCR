from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import cv2 as cv
from io import BytesIO
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
        
        
        with app.app_context():
            db.create_all()
            upload = Upload(filename=file.filename, data=file.read())
            db.session.add(upload)
            db.session.commit()
            
            #process the image
            download = Upload.query.filter_by(filename=file.filename).first()
            img = Image.open(file.data)
            # cv.imshow("Hekk", file)
            
        # return "Worked"
    
    return render_template('index.html')
    
if __name__ == '__main__':
    db.create_all()
    app.run()