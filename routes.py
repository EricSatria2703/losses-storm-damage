from flask  import render_template, request, session, redirect, abort, url_for, render_template, make_response
from app import app 
import pickle
import numpy as np
import pandas as pd
import json

jsonData = open('json/state.json', 'r')
stateCategory = json.load(jsonData)

jsonData = open('json/source.json', 'r')
sourceCategory = json.load(jsonData)

mg_typeCategory = {'EG': 0, 'MG': 1}

jsonData = open('json/azimuth.json', 'r')
event_azimuthCategory = json.load(jsonData)

jsonData = open('json/reference-location.json', 'r')
reference_locationCategory = json.load(jsonData)

@app.route("/", methods=["GET"])
def index():
    pred = request.args.get('pred')
    if(pred):
        return render_template('index.html', 
                                pred=pred.split("'")[1].capitalize(),
                                stateCategory=stateCategory, 
                                sourceCategory=sourceCategory,
                                mg_typeCategory=mg_typeCategory,
                                event_azimuthCategory=event_azimuthCategory,
                                reference_locationCategory=reference_locationCategory,
                                )

    print(len(stateCategory))

    return render_template('index.html',
                                stateCategory=stateCategory, 
                                sourceCategory=sourceCategory,
                                mg_typeCategory=mg_typeCategory,
                                event_azimuthCategory=event_azimuthCategory,
                                reference_locationCategory=reference_locationCategory,
                            )


@app.route("/predict", methods=["POST"])
def predictForm():
    state = request.form['state']   
    state_fips_code = request.form['state_fips_code']   
    cz_fips_code = request.form['cz_fips_code']   
    source = request.form['source']   
    magnitude = request.form['magnitude']   
    magnitude_type = request.form['magnitude_type']   
    event_range = request.form['event_range']   
    event_azimuth = request.form['event_azimuth']   
    reference_location = request.form['reference_location']   
    event_latitude = request.form['event_latitude']   
    event_longitude = request.form['event_longitude']   

    X = np.array([
        [
            float(state),
            float(state_fips_code),
            float(cz_fips_code),
            float(source),
            float(magnitude),
            float(magnitude_type),
            float(event_range),
            float(event_azimuth),
            float(reference_location),
            float(event_latitude),
            float(event_longitude),
        ]
    ])


    loaded_model = pickle.load(open('model/dmgPred.pkl', "rb"))
    pred = loaded_model.predict(X)

    return redirect(url_for('index', pred=pred))



@app.route("/docs")
def docs():
    return render_template('docs.html')