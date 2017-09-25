from flask import Flask, render_template, request, send_file
import pandas # do not need to iterate
from geopy.geocoders import Nominatim # geopy library has module geocoders
import datetime

app=Flask(__name__)

@app.route("/") # homepage
def home():
    return render_template("home.html") # renders the homepage

@app.route("/success", methods = ['POST']) # default is GET method - HTTP
def success():
    global filename
    if request.method == 'POST':
        # request method below can upload file into browser
        file=request.files["file"] # for users to upload a file into the website, stores a file object
        # print(type(f)) - werkzeug.datastructure.FileStorage type
        try: # in case the user uploads a csv filethat has no Address column
            df = pandas.read_csv(file.filename)
            # print(df)
            nom = Nominatim(scheme="http")
            # nom.geocode("address") - address format should be like in dataframe
            #apply method in pandas - passes Address column into nom.geocode
            df["Coordinates"] = df["Address"].apply(nom.geocode)
            # get Location datatype in Coordinate column of df with lat and longitude; some scenarios get a None datatype
            # Add 2 columns to store Latitude and longitude
            df["Latitude"]=df["Coordinates"].apply(lambda x: x.latitude if x != None else None)
            df["Longitude"]=df["Coordinates"].apply(lambda x: x.longitude if x != None else None)
            # delete the Coordinates column - drop method
            df = df.drop("Coordinates",1)
            # print(df)
            # create a folder "uploads" and saves the new csv file and download for later
            filename=datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            df.to_csv(filename, index=None)
            # display on site using .to_html()
            return render_template("home.html", btn="download.html", data = df.to_html())
        except:
            return render_template("home.html", text="please make sure you have an Address column in your csv file.")
@app.route('/download')
def download():
    # For project send email instead of downloading
    # send_file method below sends file to browser for downloading
    return send_file(filename, attachment_filename="newfile.csv", as_attachment=True)

if __name__=='__main__':
    app.debug=True
    app.run()
