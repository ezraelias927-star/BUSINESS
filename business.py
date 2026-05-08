from flask import Flask,render_template,redirect,url_for,request,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
app=Flask(__name__)
import os
app.secret_key="hhdjjfifgiururuuu7476578686tnfgdye7ee6y3y3n"
UPLOAD_FOLDER='static/images'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import event
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mimi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
from datetime import datetime
    

class bidhaa(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bei=db.Column(db.String)
    maelezo=db.Column(db.String(50),nullable=False)
    tarehe=db.Column(db.String(50))
    picha=db.Column(db.String(50))

@app.route('/')
def home():
    matokeo=bidhaa.query.all()
    return render_template('home.html',matokeo=matokeo)

@app.route('/display')
def display():
    matokeo=bidhaa.query.all()
    return render_template('display.html',matokeo=matokeo)

#About
@app.route('/about')
def about():
    return render_template('about.html')

#Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

#service
@app.route('/service')
def service():
    return render_template('service.html')



#kuingia admin dashboard
@app.route('/admin',methods=['POST','GET'])
def admin():
    return render_template('admin.html')

#kujaza bidhaa
@app.route('/add',methods=['POST','GET'])
def add():
    if request.method=='POST':
     file=request.files.get('file')
     filename=file.filename
     file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
     file.save(file_path)
     bei=request.form.get('bei')
     maelezo=request.form.get('maelezo')
     tarehe=request.form.get('tarehe')
     matokeo=bidhaa(bei=bei,maelezo=maelezo,tarehe=tarehe,picha=filename)
     db.session.add(matokeo)
     db.session.commit()
    return render_template('file.html')

#chagua mechi zote kabisa hapa
@app.route('/adminselect')
def adminselect():
    zote=bidhaa.query.all()
    return render_template('adminselect.html',zote=zote)

#kudelete bidhaa
@app.route('/delete/<int:id>')
def delete(id):
    kitu=bidhaa.query.get(id)
    db.session.delete(kitu)
    db.session.commit()
    return redirect('/adminselect')

#kuupdate bidhaa
@app.route('/update/<int:id>',methods=['POST'])
def adminupdate(id):
    mat=bidhaa.query.get(id)
    bei=request.form.get('bei')
    maelezo=request.form.get('maelezo')
    tarehe=request.form.get('tarehe')
    picha=request.form.get('picha')
    mat.bei=bei
    mat.maelezo=maelezo
    mat.tarehe=tarehe
    mat.picha=picha
    db.session.commit()
    return redirect(url_for('adminselect'))
    

#HAPA NI SEHEMU YA KUJASILI WATUMIAJI
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=5000, debug=False)
