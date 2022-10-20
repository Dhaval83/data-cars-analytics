from tkinter import Y
from flask import Flask
from markupsafe import escape
from flask import render_template
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib as plt
from PIL import Image, ImageDraw
import os
from scipy import stats
import matplotlib.pyplot as plt


IMAGES_FOLDER = os.path.join('static', 'images')


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER

def create_app(config_filename):
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    return app

def page_not_found(e):
  return render_template('not-found.html'), 404
  
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/aboutus/')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus/')
def contactus():
    return render_template('contactus.html')

@app.route('/display-piechart')
def displaypiechart():
   fig = Figure()
   ax = fig.add_subplot(1, 1, 1)
   x = [1, 2, 3, 4]
   labels = 'Hyundai', 'Kia', 'Maruti', 'Toyota'
   sizes = [28, 22, 35, 15]
   explode = (0, 0, 0, 0)  
   
   ax.pie(sizes, explode=explode, labels=labels, autopct='%1d%%',
         startangle=90)
   ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'piechart.png')
   fig.savefig(image1, dpi=500, bbox_inches='tight')
   #return Response(output.getvalue(), mimetype='image/png')
   #image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
   return render_template("display-piechart.html",user_image = image1)

@app.route('/display-barchart')
def displaybarchart():
   fig = Figure()
   ax = fig.add_subplot(1, 1, 1)
   x = [1, 2, 3, 4]
   labels = ["Hyundai", "Kia", "Maruti", "Toyota"]
   sizes = [280, 400, 350, 220]
   ax.bar(labels,sizes)
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   image2 = os.path.join(app.config['UPLOAD_FOLDER'], 'barchart.png')
   fig.savefig(image2, dpi=500, bbox_inches='tight')
   #return Response(output.getvalue(), mimetype='image/png')
   #image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
   return render_template("display-barchart.html",user_image2 = image2)

@app.route('/display-linearregression')
def displaylinearregression():
   fig = Figure()
   ax = fig.add_subplot(1, 1, 1)
   x = [1, 2, 3, 4]
   labels = ["Hyundai", "Kia", "Maruti", "Toyota"]
   x = [2, 4, 3, 1]
   sizes = [280, 400, 350, 220]
   slope, intercept, r, p, std_err = stats.linregress(x, sizes)
   def myfunc(x):
      return slope * x + intercept
   mymodel = list(map(myfunc, x))
   ax.scatter(labels, sizes)
   ax.plot(labels, sizes)
   
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   image3 = os.path.join(app.config['UPLOAD_FOLDER'], 'linearregression.png')
   fig.savefig(image3, dpi=500, bbox_inches='tight')
   return render_template("display-linearregression.html",user_image3 = image3)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not-found.html'), 404