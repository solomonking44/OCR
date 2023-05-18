from flask import Flask, render_template, request, send_file
from flask_restful import Resource, Api

#flask app declaration
app = Flask(__name__)

#api configuration
api = Api(app)


#image to text router
@api.resource('/imagetotext')
class ImageToText(Resource):
    def get(self):
        return "GET: Welcome to the Image to text module"
    
    
#pdf to text router
@api.resource('/pdftotext')    
class PDFToText(Resource):
    def get(self):
        return "GET:Welcome to the PDF to text module"
    
    
#selective ocr router   
@api.resource('/selectiveocr')  
class SelectiveOCR(Resource):
    def post(self):
        if request.method == "POST":
            return render_template('thankyou.html')
        else:
            print("Wrong place!")
            

#login router            
@api.resource('/login')            
class User(Resource):
    def get(self):
        print("Welcome to the new world")
        return render_template('login.html')
    
    def post(self):
        username = request.form['username']
        password = request.form['password']
        
        return f"username: {username}\npassword: {password}"


#home router   
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':       
        print(request.form['value'])
        value = request.form['value']
        print(url_for(f'http://localhost:5000/{value}'))
    else:
        return "Error: Wrong method used to access API!"
    
    
#error handler router    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')
    

