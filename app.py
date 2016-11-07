#!flask/bin/python
from flask import Flask, render_template, request, send_file, redirect, url_for, session
from mandelbrot import renderizaMandelbrot
import os
import random

app = Flask(__name__)
DIR = os.path.dirname(os.path.realpath(__file__))
historial = {}
# historial[username] = []

@app.route("/")
def home():
    hist = []
    try:
        if (session['usuario'] and historial[session['usuario']]):
            hist = historial[session['usuario']]
        return render_template('home.html', rows=hist)
    except:
        return render_template('home.html', rows=[])

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    session['usuario'] = username
    historial[username] = []
    historial[username].append("/login")
    return render_template('home.html')

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('usuario',None)
    return render_template('home.html')

@app.route("/mandelbrotview", methods=['GET'])
def mandelbrotview():
    return render_template('mandelbrotview.html')

@app.route("/mandelbrot", methods=['GET']) # def mandelbrot():
def mandelbrot():
    try:
        username = session['usuario'] 
        historial[username].append("/mandelbrot")
    except:
        username = "anon"
    img_dir = DIR+'/static/img/mandelbrot/'

    x1 = float(request.args['x1'])
    y1 = float(request.args['y1'])
    x2 = float(request.args['x2'])
    y2 = float(request.args['y2'])
    width = int(request.args['width'])
    iterations = int(request.args['iterations'])
    nombreimg = img_dir+str(x1)+str(y1)+str(x2)+str(y2)+str(width)+str(iterations)+".png"
    if(os.path.isfile(nombreimg)):
        print("cacheando fractal")
        return send_file(nombreimg, mimetype='image/gif')
    else:
        print("no esta en cache")
        img=renderizaMandelbrot(x1,y1,x2,y2, width, iterations, nombreimg)
        return send_file(nombreimg, mimetype='image/gif')
    # return render_template('mandelbrotview.html', mandel=img)

@app.route("/composicion", methods=['GET'])
def composicion():
    comp = ""
    try:
        username = session['usuario'] 
        historial[username].append("/composicion de figuras aleatorias ")
    except:
        username = "anon"
    for i in range(1,500):
        recx = random.randint(30,450)
        recy = random.randint(30,450)
        cirx = random.randint(30,450)
        ciry = random.randint(30,450)
        elx = random.randint(30,450)
        ely = random.randint(30,450)
        ancho = random.randint(10,20)
        altura = random.randint(10,20)
        rx = random.randint(1,15)
        ry = random.randint(1,15)
        colores = ['blue','black','grey','pink','red','orange','green']
        color = colores[random.randint(0,len(colores)-1)]
        rectangulo = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}"/>\n'
        circulo = '<circle cx="{}" cy="{}" rx="{}" ry="{}" fill="{}"/>\n'
        elipse = '<ellipse cx="{}" cy="{}" rx="{}" ry="{}" fill="{}"/>\n'
        comp += rectangulo.format(recx, recy,ancho,altura, color, color)
        comp += circulo.format(cirx,ciry,rx,ry,color)
        comp += elipse.format(elx,ely,rx,ry,color)

    return render_template('composicion.html',composicion=comp)

@app.errorhandler(404)
def page_not_found(response):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = 'dai2016'
    app.run(host='0.0.0.0',debug=True)