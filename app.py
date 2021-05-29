from flask.helpers import url_for
from flask.templating import render_template
from pytube import YouTube
from flask import Flask,request,flash
from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_resolutions(streams):
  streams = streams.filter(progressive=True)
  x = [str(s).split() for s in streams]
  resolutions = [r[3].strip('res="') for r in x] #creates a list of availiable resolution with audio and video
  return resolutions

def get_stream_for_res(streams, res):
  #Filter on the basis of a given resolution and return a list of filtered streams
  streams = streams.filter(progressive=True)
  stream = list(filter(lambda x: x.resolution == res, streams))
  return stream


@app.route('/', methods=['GET','POST'])
def homepage():

  if request.method == 'POST':
    
    try:
      youtube_obj = YouTube(request.form['link'].strip())
      res =  request.form['res'].strip()

      resolutions = get_resolutions(youtube_obj.streams)

      if res in resolutions:
        req_stream_obj= get_stream_for_res(youtube_obj.streams,res)[0] 
        req_stream_obj.download()
        flash(f"YouTube Video {youtube_obj.title} Download with Resolution {res}")
      else:
        flash('Selected resolution has no Audio')
        return render_template('homepage.html',resolutions=resolutions)

    except:
      flash('Unable to Download try changing the resoltion')
      return redirect(url_for('homepage'))

  return render_template('homepage.html')


