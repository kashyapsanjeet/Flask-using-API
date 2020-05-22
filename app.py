import flask
import requests
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from datetime import datetime

app=Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///entries.db'

db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    API = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.Date(), nullable=False)
    query = db.Column(db.String(50), nullable=False)

@app.route('/',methods=['Get','Post'])
def index():
    if request.method=='POST':
        t = request.form.get('t1')
        if t=='Weather' or t=='weather':
            return redirect("/Weather")
        elif t=='News' or t=='news':
            return redirect('/News')
        elif t=='Stocks' or t=='stocks':
            return redirect('/Stocks')
        else:
            return redirect('/Invalid')

    return render_template('index.html')

@app.route('/Weather',methods=['Get','Post'])
def weather():
    if request.method=='POST':
        now = datetime.now()
        city = request.form.get('Weat')
        new_obj=Entry(API='Weather',Date=now,query=city)
        db.session.add(new_obj)
        db.session.commit()
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=46b07ad99e69de2b7016418734daded5'
        weather_data=[]
        r=requests.get(url.format(city)).json()

        weather ={
        'city':city,
        'temperature':r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon'],
        'humidity':r['main']['humidity'],
        'wind':r['wind']['speed']
        }
        weather_data.append(weather)
        return render_template('Weather.html',weather_data=weather_data)
    else:
        return render_template('Weather.html')

@app.route('/News',methods=['Get','Post'])
def news():
    if request.method=='POST':
        country=request.form.get('Coun')
        now = datetime.now()
        new_obj=Entry(API='News',Date=now,query=country)
        db.session.add(new_obj)
        db.session.commit()
        url = 'http://newsapi.org/v2/top-headlines?country={}&apiKey=bd395893b7e847b691047e61fd6b40c4'
        r=requests.get(url.format(country)).json()
        news_data=[]

        news={
            'name1':r['articles'][0]['source']['name'],
            'title1':r['articles'][0]['title'],
            'desc1':r['articles'][0]['description'],
            'name2':r['articles'][1]['source']['name'],
            'title2':r['articles'][1]['title'],
            'desc2':r['articles'][1]['description'],
            'name3':r['articles'][2]['source']['name'],
            'title3':r['articles'][2]['title'],
            'desc3':r['articles'][2]['description'],
            'name4':r['articles'][3]['source']['name'],
            'title4':r['articles'][3]['title'],
            'desc4':r['articles'][3]['description'],
        }
        news_data.append(news)
        return render_template('News.html',news_data=news_data)
    else:        
        return render_template('News.html')

@app.route('/Stocks',methods=['Get','Post'])
def stocks():
    if request.method=='POST':
        st=request.form.get('Stock')
        now = datetime.now()
        new_obj=Entry(API='Stocks',Date=now,query=st)
        db.session.add(new_obj)
        db.session.commit()
        url='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=1EDLTD4CDKL6EPYA'
        r=requests.get(url.format(st)).json()
        stock_data=[]
        time=r['Meta Data']['3. Last Refreshed']
        stock={
            'name':r['Meta Data']["2. Symbol"],
            'open':r['Time Series (5min)'][time]['1. open'],
            'close':r['Time Series (5min)'][time]['4. close'],
            'high':r['Time Series (5min)'][time]['2. high'],
            'low':r['Time Series (5min)'][time]['3. low'],
            'time':r['Meta Data']['3. Last Refreshed']
        }
        stock_data.append(stock)
        return render_template('Stocks.html',stock_data=stock_data)
    else:
        return render_template('Stocks.html')

@app.route('/Invalid',methods=['Get','Post'])
def Invalid():
    return render_template('invalid.html')


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
