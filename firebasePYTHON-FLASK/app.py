from wtforms import Form,StringField,PasswordField,validators
from flask import Flask,render_template,redirect,url_for,request
from firebase import Firebase
from google.cloud import firestore
import jwt as jwt
import firebase_admin
from firebase_admin import credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./firebasePYTHON-FLASK/serviceAccountKey.json"

cred = credentials.Certificate("./firebasePYTHON-FLASK/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.Client()

app=Flask(__name__)
app.secret_key="mouz"
app.env="Development"

class registerForm(Form):
    name=StringField("İsim Soyisim", validators=[validators.Length(min=4,max=25)])
    phoneNo=StringField("Telefon", validators=[validators.Length(min=4,max=25)])
    email=StringField("Email Adresi", validators=[validators.Email(message="Geçersiz Email Adresi")])
    dep=StringField("Departman", validators=[validators.Length(min=4,max=25)])

@app.route("/",methods=["GET","POST"])
def index():
    form = registerForm(request.form)
    if request.method=="POST" and form.validate():
        name=form.name.data
        phoneNo=form.phoneNo.data
        email=form.email.data
        dep=form.dep.data
        db.collection(u"calisanlar").add({
            "name":name,
            "phoneNumber":phoneNo,
            "eMail":email,
            "departmant":dep
        })        
        return redirect(url_for("index"))
    else:
        snapshots = list(db.collection(u'calisanlar').order_by("name").get())
        return render_template("index.html",form=form,snapshots=snapshots)
if __name__=="__main__":
    app.run(debug=True)