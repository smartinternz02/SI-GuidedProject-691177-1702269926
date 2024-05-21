from flask import Flask, render_template, url_for, request, redirect, session
import pickle
import os
import re
import numpy as np
#from newsapi import NewsApiClient



app = Flask(__name__)
app.secret_key = 'bhhgvycyuklmlijuggyj'

model=pickle.load(open('smoking.pkl','rb'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process the initial details from the 'index' page
        name = request.form['name']
        # Save 'name' in the session or any other appropriate place
        
        # Redirect to the 'general_info' page
        return render_template('gen_info.html')
    return render_template('index.html')

@app.route('/gen_info', methods=['GET', 'POST'])
def gen_info():
    if request.method == 'POST':
        id=float(request.form['id'])
        Gender = float(request.form['Gender'])
        Age = float(request.form['Age'])
        Height = float(request.form[ 'Height'])
        Weight = float(request.form['Weight'])
        Eyesight_right = float(request.form['Eyesight_right'])
        Eyesight_left = float(request.form['Eyesight_left'])
        Hearing_right = float(request.form['Hearing_right'])
        Hearing_left = float(request.form['Hearing_left'])
        Waist = float(request.form['Waist'])
        print(float(id),float(Gender), float(Age), float(Height), float(Weight),
                        float(Eyesight_right), float(Eyesight_left), float(Hearing_right),
                        float(Hearing_left), float(Waist))
                # Convert the collected data to the format expected by your model
        pred = np.array([[float(id), float(Gender), float(Age), float(Height), float(Weight),
                        float(Eyesight_right), float(Eyesight_left), float(Hearing_right),
                        float(Hearing_left), float(Waist)]])
        
                # Make predictions using the model
        prediction = model.predict(pred)

                # Define label mapping
        #label_mapping = {'low': 0, 'high': 1}        
        label_mapping = {1:'Smoke', 0: 'No Smoke'}
        predicted_label = label_mapping[prediction[0]]


        # Store the prediction result in the session
        session['predicted_label'] = predicted_label

        # Redirect to the 'result' page
        return render_template('result.html')

    return render_template('gen_info.html')


@app.route('/result')
def result():
    # Retrieve the prediction result from the session
    predicted_label = session.get('predicted_label', None)

    # Check if there's a prediction result
    if predicted_label is None:
        # Handle the case where no result is found, you can redirect or show an error message
        return "No prediction result found. Please enter health-related details first."

    return render_template('result.html', predicted_label=predicted_label)
    #output=predicted_label
    #return render_template('result.html',prediction_text='The chance of churn based on given customer info is {}'.format(output))

if __name__ == '__main__':
    app.run(debug=True)
    