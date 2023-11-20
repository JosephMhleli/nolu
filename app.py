from flask import Flask, render_template,request,make_response,jsonify,session,redirect, url_for
import jwt
from datetime import datetime,timedelta,timezone
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c87793cf26c24a759e75c3713de80466'    

def token_required(func):
     @wraps(func)
     def decorated(*args,**kwargs):
      token = request.args.get('token')

      if not token:
          return jsonify({'Alert!':'Token is missing!'})
      try:  
       payload = jwt.decode(token,app.config['SECRET_KEY']) 
      except:
          return jsonify({'Alert!':'Invalid Token!'})
     return decorated
      
@app.route('/')     # for the public anyone can access this side......
def index():
    if not session.get('logged in'):
      return render_template('index.html' )
    else :
        return 'Logged in Currently!'
    
    
@app.route('/login')
def show_login():
    return render_template('LoginPage.html')   

@app.route('/login', methods = ['POST'])
def login():
    try:
        if request.form['username'] and request.form['password'] == '123456':
            session['logged_in'] = True
            expiration_time = datetime.now(timezone.utc) + timedelta(seconds=120)
            token = jwt.encode({'user': request.form['username'], 'expiration': str(expiration_time)},
                               app.config['SECRET_KEY'])
            
          
            return redirect(url_for('index'))
        else:
            return make_response('Unable to verify', 403)
    except Exception as e:
        return make_response(str(e), 500)

    # This line is not reachable
    return jsonify({'token': token})

@app.route('/register')
def register():
    return render_template('Register.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index.html'))

@app.route('/SelectBook',methods = ['GET'])

def myBook():
     return 'View Book'


@app.route('/Add2Cart',methods = ['POST','GET','DELETE'])
@token_required
def addtocart():
     return 'added to cart!'


@app.route('/Favorites',methods = ['POST','GET','DELETE'])
@token_required
def myFavorites():
     return 'My favorites!'



if __name__ == '__main__':
    app.run(debug=True)
