from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pandas as pd
import pickle

app= Flask(__name__)
model=pickle.load(open("flight_preds.pkl", "rb"))

@app.route('/')
@cross_origin()
def homepage():
    return render_template('homepage.html')


# Convert the departure time to fall in 4 intervals of a day
def departtime(x):
    x=x.strip()
    tt=(int)(x.split(':')[0])
    if(tt>=16 and tt<21):
        x=1 # 1- Evening
    elif(tt>=21 or tt<5):
        x=3 # 3- Night
    elif(tt>=5 and tt<11):
        x=2 # 2- Morning
    elif(tt>=11 and tt<16):
        x=0 # 0- Afternoon
    return x

# Convert the duration into total number of minutes
def duration(minutes):
    minutes=minutes.strip()
    total=minutes.split(' ')
    to=total[0]
    hours=int(to[:-1])*60# -1 because last character is h
    if((len(total))==2):
        mins=(int)(total[1][:-1])# -1 because last character is m
        hours=hours+mins
    minutes=str(hours)
    return minutes



@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method=='POST':
        date_dep=request.form['Dep_Time']
        date_arr=request.form["Arrival_Time"]

        # Extracting the date of the journey
        Journey_day=int(pd.to_datetime(date_dep, format='%Y-%m-%dT%H:%M').day)
        Journey_month=int(pd.to_datetime(date_dep, format='%Y-%m-%dT%H:%M').month)

        # Extracting the day of the week
        Weekday=pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").dayofweek
        # Weekday=float(Weekday)
        
        # Extracting the departure and arrival time
        Dep_hour=pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour
        Dep_min=pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute
        Dep_t=str(Dep_hour) + ':' + str(Dep_min)
        Dep_time=departtime(Dep_t)

        Arrival_hour = pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour
        Arrival_min = pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute
        Arrival_t=str(Arrival_hour) + ':' + str(Arrival_min)
        Arrival_time=departtime(Arrival_t)

        # Extracting Duration time
        dur_hour= abs(int(Arrival_hour) - int(Dep_hour))
        dur_min= abs(int(Arrival_min) - int(Dep_min))
        dur=str(dur_hour) + 'h ' + str(dur_min) + 'm'
        total_duration_in_min=duration(dur)
        mean_dur=1.6817561094794662e-16 # Taken directly from the ipynb
        std_dur=1.0000000000000069 # Taken directly from the ipynb
        Duration=(int(total_duration_in_min) - mean_dur)/std_dur
        # The final duration is standardized

        # Total stops
        Total_Stops=int(request.form["Stops"])

        # Airlines.... Air_Asia=0 is not in the column due to get dummies drop first being true.
        airline=request.form['Airline']
        if(airline=='Jet Airways'):
            Jet_Airways = 1
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline=='IndiGo'):
            Jet_Airways = 0
            IndiGo = 1
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 

        elif (airline=='Air India'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 1
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
            
        elif (airline=='Multiple carriers'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 1
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
            
        elif (airline=='SpiceJet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 1
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0 
            
        elif (airline=='Vistara'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 1
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline=='GoAir'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 1
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline=='Multiple carriers Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 1
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline=='Jet Airways Business'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 1
            Vistara_Premium_economy = 0
            Trujet = 0

        elif (airline=='Vistara Premium economy'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 1
            Trujet = 0
            
        elif (airline=='Trujet'):
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 1

        else:
            Jet_Airways = 0
            IndiGo = 0
            Air_India = 0
            Multiple_carriers = 0
            SpiceJet = 0
            Vistara = 0
            GoAir = 0
            Multiple_carriers_Premium_economy = 0
            Jet_Airways_Business = 0
            Vistara_Premium_economy = 0
            Trujet = 0

        # Source
        # Banglore=0...not in column...get dummies...drop first=true 
        Source=request.form['Source']
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        # Destination
        # Banglore=0...not in column...get dummies...drop first=true 
        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        
        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'New_Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        prediction=model.predict([[Dep_time, Arrival_time, 
        Duration, Total_Stops, 
        Journey_day, Journey_month, Weekday, 
        Air_India, GoAir, IndiGo, Jet_Airways, 
        Jet_Airways_Business, Multiple_carriers,
        Multiple_carriers_Premium_economy, SpiceJet,
        Trujet, Vistara, Vistara_Premium_economy,
        s_Chennai, s_Delhi, s_Kolkata, s_Mumbai,
        d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi]])

        output=round(prediction[0], 2)

        return render_template('homepage.html', Predicted_price='Your Flight price is estimated to be ₹{}'.format(output))

    return render_template('homepage.html')
        

if __name__=="__main__":
    app.run(debug=True)