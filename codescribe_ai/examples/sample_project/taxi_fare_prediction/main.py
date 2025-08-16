from flask import Flask, render_template, request
import pandas as pd
import pickle
import pandas as pd
import os

app = Flask(__name__)

with open('model.pkl', 'rb') as f: 
    model, feature_names = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
        try:
            form = request.form

            data = {
                'temperature': float(form['temperature']),
                'rainfall': int(form['rainfall']),
                'holiday': float(form['holiday']),
                'hour': float(form['hour']),
                'day_of_week': float(form['day_of_week']),
                
            }

            df=pd.DataFrame([data])


            prediction = model.predict(df)[0]
        except Exception as e:
            return render_template('index.html', error=f"Invalid input. Please enter numeric values. Details: {str(e)}")

        return render_template("result.html", prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
