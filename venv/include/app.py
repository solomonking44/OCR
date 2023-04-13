from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import cv2 as cv
from io import BytesIO
import pytesseract
from PIL import Image
import random

#flask app declaration
app = Flask(__name__)

#configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create the extension
db = SQLAlchemy(app)

#Database model
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        
    def __repr__(self):
        return f"Filename is {self.filename}"
    

#route traffic from '/' to 
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # random_number = random.randint(0,99999999)
    
    #if it is a POST method
    if request.method == 'POST':
        
        #store image name in variable
        file = request.files['image']
        
        #Everything with access to flask app
        with app.app_context():
            
            #
            ## PART ONE ## - STORE IMAGE IN DB 
            #
            
            #create tables
            db.create_all()
            
            #create an object
            upload = Upload(filename=file.filename, data=file.read())
            
            #create the database session
            db.session.add(upload)
            
            #save the information
            db.session.commit()
            
            #
            ## PART TWO ## - PROCESS IMAGE ##
            #
            
            #fetch info from table filter by filename
            download = Upload.query.filter_by(filename=random_number).first()
            
            #store image in uploads
            with open(f"./uploads/{download.filename}.png", "wb") as f:
                f.write(download.data)

            #read image in opencv
            image = cv.imread(f'./uploads/{download.filename}.png',0)
                
            #read the text from the image
            text = pytesseract.image_to_string(image)
            
            #store filename in variable
            file_name = download.filename
            
            #extract the file name from the file type
            cut_name = file_name.split(".", 1)[0]
            
            #delete that record from db
            delete = Upload.query.filter_by(filename=file.filename).delete()
            
            #open .txt file 
            image_text = open(f'./text_files/{cut_name}.txt', 'w')
            
            #write text in file
            image_text.write(text)
            
            #testing#
            records = Upload.query.all()
            # print(records)
            for record in records:
                print(record)
            print(text)
            print(download.filename)
      
            #return the file to download
            return send_file(f"./text_files/{cut_name}.txt", as_attachment=True)
        
    #return index page
    return render_template('index.html')

    