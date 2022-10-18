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

@app.route('/display-graph')
def displaygraph():
   fig = Figure()
   ax = fig.add_subplot(1, 1, 1)
   x = [1, 2, 3, 4]
   labels = 'Audi', 'Kia', 'Maruti', 'BMW'
   sizes = [15, 30, 45, 10]
   explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
   
   ax.pie(sizes, explode=explode, labels=labels, autopct='%1d%%',
         startangle=90)
   ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
   fig.savefig(image1, dpi=500, bbox_inches='tight')
   #return Response(output.getvalue(), mimetype='image/png')
   #image1 = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
   return render_template("display-graph.html",user_image = image1)


   

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not-found.html'), 404