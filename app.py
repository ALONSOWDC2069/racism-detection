from flask import Flask,render_template,url_for,request
#import pandas as pd 
import pickle
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout ,BatchNormalization,Reshape,Dot,Concatenate,Add,Lambda,Input,Embedding
from tensorflow.keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from keras.layers.recurrent import LSTM
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.tokenize import sent_tokenize
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import string 
from nltk.stem import WordNetLemmatizer
import sqlite3

lstm_model = load_model('lstm_model.h5')

cv=pickle.load(open('transform2.pkl','rb'))
app = Flask(__name__)

@app.route('/home1')
def home1():
	return render_template('home1.html')

@app.route('/predict1',methods=['POST'])
def predict1():


	if request.method == 'POST':
		message = request.form['message']
		data = [message]
		vect = cv.texts_to_sequences(data)
		vect = pad_sequences(vect)
		k=np.zeros((1,39))
		k[0,-vect.shape[1]:]=vect
		my_prediction = lstm_model.predict_classes(np.array(k))
	return render_template('result1.html',prediction = my_prediction)

@app.route('/')
def home():
	return render_template('home.html')

@app.route("/signup")
def signup():
    
    
    name = request.args.get('username','')
    number = request.args.get('number','')
    email = request.args.get('email','')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `detail` (`name`,`number`,`email`, `password`) VALUES (?, ?, ?, ?)",(name,number,email,password))
    con.commit()
    con.close()

    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('name','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from detail where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()
    print(data)

    if data == None:
        return render_template("signup.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("home1.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home1.html")
    else:
        return render_template("signup.html")



@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/notebook')
def notebook():
	return render_template('notebook.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')		

if __name__ == '__main__':
	app.run(debug=False)
