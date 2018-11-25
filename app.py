from flask import Flask, render_template,request,url_for
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
Bootstrap(app)


#config
files = UploadSet('files',ALL)
app.config['UPLOADED_FILES_DEST'] = 'static/uploadstorage'
configure_uploads(app,files)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datauploads',methods=['GET','POST'])
def datauploads():
    if request.method == 'POST' and 'csv_data' in request.files:
        file = request.files['csv_data']
        global filename
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/uploadstorage',filename))
        df = pd.read_csv(os.path.join('static/uploadstorage',filename))
        df_table = df

    return render_template('details.html',filename=filename, df_table=df)

@app.route('/eda')
def eda():
    df = pd.read_csv(os.path.join('static/uploadstorage',filename))
    df_shape= df.shape
    df_size = df.size
    return render_template('eda.html', df_shape=df_shape, df_size=df_size)

if __name__ == '__main__':
    app.run(debug=False)
