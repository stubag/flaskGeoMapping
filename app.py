from flask import Flask, redirect, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from geocoder import geocoder
import uuid

UPLOAD_FOLDER = './uploads'
DOWNLOAD_FOLDER = './downloads'
ALLOWED_EXTENSIONS = {'csv'}


app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER 
app.secret_key = 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/success", methods=["GET", "POST"])
def success():
    if request.method == 'POST':
        # check if the post request has the file part        
        if 'file' not in request.files:
            return render_template("index.html", warning="There was an error please try again")
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html", warning="You did not attach a file")
        if allowed_file(file.filename) != True:
            return render_template("index.html", warning='Please upload a CSV file only')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                 os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = geocoder(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if type(df) == type(False):
                return render_template("index.html", warning='Please add an address column to the file')
            else:
                newfilename =  'file_' + str(uuid.uuid4()) + ".csv"
                df.to_csv(f'./downloads/{newfilename}')
                return render_template("success.html", table=df.to_html(), titles=df.columns.values, filename=newfilename)


@app.route('/download', methods=["POST"])
def download():
    if request.method=="POST":
        print(request.form['filename'])
        filename=request.form['filename']
        path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        return send_file(path, as_attachment=True, download_name="yourfile.csv")
            

if __name__ == "__main__":
    app.run(debug=True)