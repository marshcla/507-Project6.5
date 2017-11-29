# Import statements necessary
from flask import Flask, render_template
from flask_script import Manager
import json
import requests

# Set up application
app = Flask(__name__)

manager = Manager(app)

# Routes

@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {}</h1>'.format(yourname)

@app.route('/showvalues/<name>')
def basic_values_list(name):
    lst = ["hello","goodbye","tomorrow","many","words","jabberwocky"]
    if len(name) > 3:
        longname = name
        shortname = None
    else:
        longname = None
        shortname = name
    return render_template('values.html',word_list=lst,long_name=longname,short_name=shortname)

## PART 1: Add another route /word/<new_word> as the instructions describe.

@app.route('/word/<new_word>')
def data_muse_func(new_word):
    data_response = requests.get("https://api.datamuse.com/words?rel_rhy={}".format(new_word))
    datatxt = data_response.text
    data_results = json.loads(datatxt)

    rhyme = str(data_results[0]['word'])
    return "<p style='color:black; font-family:helvetica; text-align:center; margin-top:25px;'>Here is a word that rhymes with <strong>{}</strong>:</p> <p style='color:#16A085; font-family:helvetica; font-size:20px; font-weight:bold; text-align:center;'>{}</[]>".format(str(new_word),str(rhyme))



## PART 2: Edit the following route so that the photo_tags.html template will render
@app.route('/flickrphotos/<tag>/<num>')
def photo_titles(tag, num):
    # HINT: Trying out the flickr accessing code in another file and seeing what data you get will help debug what you need to add and send to the template!
    # HINT 2: This is almost all the same kind of nested data investigation you've done before!
    FLICKR_KEY = "38db11ee7cd8e604071311d773fe9ba4" # TODO: fill in a flickr key
    baseurl = 'https://api.flickr.com/services/rest/'
    params = {}
    params['api_key'] = FLICKR_KEY
    params['method'] = 'flickr.photos.search'
    params['format'] = 'json'
    params['tag_mode'] = 'all'
    params['per_page'] = num
    params['tags'] = tag
    response_obj = requests.get(baseurl, params=params)
    trimmed_text = response_obj.text[14:-1]
    flickr_data = json.loads(trimmed_text)
    num_photos = flickr_data['photos']['total']
    title_list = []
    for i in flickr_data['photos']['photo']:
        title_list.append(i['title'])

    return render_template('photo_info.html',photo_titles=title_list, num=num_photos)




if __name__ == '__main__':
    manager.run() # Runs the flask server in a special way that makes it nice to debug
