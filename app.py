from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_cus.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arr_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arr_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        Deu_hours = abs(Arr_hour - Dep_hour)
        Deu_mins = abs(Arr_min - Dep_min)
        # print("Duration : ", dur_hour, dur_min)

       

         
        company=request.form['airline']
        if (company=='IndiGo'):
            IndiGo = 1
            Air_India = 0
            SpiceJet = 0
            Vistara = 0
            Go_First = 0
            
            
            

        elif (company=='Air India'):
            IndiGo = 0
            Air_India =1
            SpiceJet = 0
            Vistara = 0
            Go_First = 0
            
        elif (company=='SpiceJet'):
            IndiGo = 0
            Air_India =0
            SpiceJet = 1
            Vistara = 0
            Go_First = 0
            
        elif (company=='Vistara'):
            IndiGo = 0
            Air_India =0
            SpiceJet = 0
            Vistara = 1
            Go_First = 0

        else:
            IndiGo = 0
            Air_India =0
            SpiceJet =0
            Vistara = 0
            Go_First = 1

#         BOM    1422
# DEL     606
# BLR     328
# MAA     215
# CCU     186
# HYD     150
        origin = request.form["Source"]
        if ( origin== 'Delhi'):
            s_BOM = 0
            s_CCU = 0
            s_DEL = 1
            s_HYD = 0
            s_BLR=0
            s_MAA=0

        elif (origin == 'Bangalore'):
            s_BOM = 0
            s_CCU = 0
            s_DEL = 0
            s_HYD = 0
            s_BLR= 1
            s_MAA=0


        elif (origin == 'Chennai'):
            s_BOM = 0
            s_CCU = 0
            s_DEL = 0
            s_HYD = 0
            s_BLR= 0
            s_MAA=1

        elif (origin == 'Mumbai'):
            s_BOM = 1
            s_CCU = 0
            s_DEL = 0
            s_HYD = 0
            s_BLR= 0
            s_MAA=0
        elif (origin == 'Kolkata'):
            s_BOM = 0
            s_CCU = 1
            s_DEL = 0
            s_HYD = 0
            s_BLR= 0
            s_MAA=0
        else:
            s_BOM = 0
            s_CCU = 0
            s_DEL = 0
            s_HYD = 1
            s_BLR= 0
            s_MAA=0

        

        
        destination = request.form["Destination"]
        if ( destination== 'Delhi'):
            d_BOM = 0
            d_CCU = 0
            d_DEL = 1
            d_HYD = 0
            d_BLR=0
            d_MAA=0

        elif (destination == 'Bangalore'):
            d_BOM = 0
            d_CCU = 0
            d_DEL = 0
            d_HYD = 0
            d_BLR= 1
            d_MAA=0


        elif (destination == 'Chennai'):
            d_BOM = 0
            d_CCU = 0
            d_DEL = 0
            d_HYD = 0
            d_BLR= 0
            d_MAA=1

        elif (destination == 'Mumbai'):
            d_BOM = 1
            d_CCU = 0
            d_DEL = 0
            d_HYD = 0
            d_BLR= 0
            d_MAA=0
        elif (destination == 'Kolkata'):
            d_BOM = 0
            d_CCU = 1
            d_DEL = 0
            d_HYD = 0
            d_BLR= 0
            d_MAA=0
        else:
            d_BOM = 0
            d_CCU = 0
            d_DEL = 0
            d_HYD = 1
            d_BLR= 0
            d_MAA=0

       
        prediction=model.predict([[
            
            day,
            month,
            Dep_hour,
            Dep_min,
            Arr_hour,
            Arr_min,
            Deu_hours,
            Deu_mins,
            Air_India,
            Go_First,
            IndiGo,
            SpiceJet,
            Vistara,
            s_BOM,
            s_CCU,
            s_DEL,
            s_HYD,
            s_MAA,
            d_BOM,
            d_CCU,
            d_DEL,
            d_HYD,
            d_MAA,
        ]])

        output=round(prediction[0],2)

        return render_template('home.html',prediction_text="Your Flight price is Rs. {}".format(output))


    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=True)

