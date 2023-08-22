from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
import warnings
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings('ignore')
import sys,os
from sqlalchemy import create_engine,text
from urllib.parse import quote_plus
app = Flask(__name__)

 

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result1',methods=['POST', 'GET'])
def result1():
    output = request.form.to_dict()
    print(output)
    engine = create_engine("mysql+pymysql://root:%s@localhost:3306/pat4" % quote_plus('Praharsh@363'))
    
    Topic = output["Topic"]
    year=output["year"]
    location_abbriviation=output["location abbriviation"]
    location=output["location"]
    Question_to_Doctor=output["Question to Doctor"]
    DataValueUnit=output["DataValueUnit"]
    DataValueType=output["DataValueType"]
    DataValue=output["DataValue"]
    DataValueAlt=output["DataValueAlt"]
    StratificationCategory1=output["StratificationCategory1"]
    Stratification1=output["Stratification1"]
    QuestionID=output["QuestionID"]
    DataValueTypeID=output["DataValueTypeID"]
    StratificationCategoryID1=output["StratificationCategoryID1"]
    StratificationID1=output["StratificationID1"]
    Latitude=output["Latitude"]
    # change the next line and everything should be good.
    sql="INSERT INTO cdi VALUES ('"+year+"','','"+location_abbriviation+"','"+location+"','','"+Topic+"','"+Question_to_Doctor+"','','"+DataValueUnit+"','"+DataValueType+"','"+DataValue+"','"+DataValueAlt+"','','','','','"+StratificationCategory1+"','"+Stratification1+"','','','','','"+Latitude+"','','','','"+QuestionID+"','"+DataValueTypeID+"','"+StratificationCategoryID1+"','"+StratificationID1+"','','','','');"
    print(sql)
    with engine.begin() as conn:
        result = conn.execute(text(sql))
    # for row in result:
    #     print(row)
    
    return render_template('index.html', Topic = Topic)


@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    year=output["year"]
    location_abbriviation=output["location abbriviation"]
    location=output["location"]
    Question_to_Doctor=output["Question to Doctor"]
    DataValueUnit=output["DataValueUnit"]
    DataValueType=output["DataValueType"]
    DataValue=output["DataValue"]
    DataValueAlt=output["DataValueAlt"]
    StratificationCategory1=output["StratificationCategory1"]
    Stratification1=output["Stratification1"]
    QuestionID=output["QuestionID"]
    DataValueTypeID=output["DataValueTypeID"]
    StratificationCategoryID1=output["StratificationCategoryID1"]
    StratificationID1=output["StratificationID1"]
    Latitude=output["Latitude"]
    
    Q = pd.DataFrame(
                    {'YearStart': [year], 'LocationAbbr': [location_abbriviation], 
                      'LocationDesc': [location], 'Question': [Question_to_Doctor],'DataValueUnit': [DataValueUnit],
                      'DataValueType': [DataValueType], 'DataValue': [DataValue], 'DataValueAlt': [DataValueAlt],
                      'StratificationCategory1': [StratificationCategory1], 'Stratification1': [Stratification1], 'QuestionID': [QuestionID],
                      'DataValueTypeID': [DataValueTypeID],'StratificationCategoryID1': [StratificationCategoryID1], 
                      'StratificationID1': [StratificationID1], 'Latitude': [Latitude]}
                    )


    engine = create_engine("mysql+pymysql://root:%s@localhost:3306/pat4" % quote_plus('Praharsh@363'))

    cdi_data1 = pd.read_sql_table("cdi", engine)
    df=cdi_data1
    df['DataValueAlt'] = pd.to_numeric(df['DataValueAlt'])
    df = df.drop(['YearEnd','DataSource','LowConfidenceLimit','HighConfidenceLimit','LocationID',
                'DataValueFootnoteSymbol','DatavalueFootnote','Response','ResponseID', 'StratificationCategory2',
                'StratificationCategory3','Stratification2','Stratification3', 'StratificationCategoryID2',
                'StratificationCategoryID3','StratificationID2','StratificationID3'], axis = 1)

    df['YearStart'] = pd.to_numeric(df['YearStart'])
    df = df[(df['YearStart'] > 2009) & (df['YearStart'] < 2016)]

    df['GeoLocation'] = df['GeoLocation'].str.replace(r"\(","")
    df['GeoLocation'] = df['GeoLocation'].str.replace(r"\)","")
    new = df['GeoLocation'].str.split(",", n = 1, expand = True)
    df["Latitude"] = new[0]
    df.drop(columns=["GeoLocation"], inplace = True)
    df.drop(df[df.LocationDesc == 'United States'].index,inplace = True)
    df = df.dropna()
    df=df.drop(["TopicID"],axis = 1)

    from sklearn import preprocessing
    label_encoder = preprocessing.LabelEncoder()

    df['LocationAbbr']= label_encoder.fit_transform(df['LocationAbbr'])
    df['LocationDesc']= label_encoder.fit_transform(df['LocationDesc'])
    df['Question']= label_encoder.fit_transform(df['Question'])
    df['DataValueUnit']= label_encoder.fit_transform(df['DataValueUnit'])
    df['StratificationCategory1']= label_encoder.fit_transform(df['StratificationCategory1'])
    df['Stratification1']= label_encoder.fit_transform(df['Stratification1'])
    df['QuestionID']= label_encoder.fit_transform(df['QuestionID'])
    df['DataValueTypeID']= label_encoder.fit_transform(df['DataValueTypeID'])
    df['StratificationCategoryID1']= label_encoder.fit_transform(df['StratificationCategoryID1'])
    df['StratificationID1']= label_encoder.fit_transform(df['StratificationID1'])
    df['Latitude']= label_encoder.fit_transform(df['Latitude'])
    df['DataValueType']= label_encoder.fit_transform(df['DataValueType'])

    X =  pd.DataFrame(df.drop(["Topic"],axis = 1))
    y = df.Topic
    
    Q['LocationAbbr']= label_encoder.fit_transform(Q['LocationAbbr'])
    Q['LocationDesc']= label_encoder.fit_transform(Q['LocationDesc'])
    Q['Question']= label_encoder.fit_transform(Q['Question'])
    Q['DataValueUnit']= label_encoder.fit_transform(Q['DataValueUnit'])
    Q['StratificationCategory1']= label_encoder.fit_transform(Q['StratificationCategory1'])
    Q['Stratification1']= label_encoder.fit_transform(Q['Stratification1'])
    Q['QuestionID']= label_encoder.fit_transform(Q['QuestionID'])
    Q['DataValueTypeID']= label_encoder.fit_transform(Q['DataValueTypeID'])
    Q['StratificationCategoryID1']= label_encoder.fit_transform(Q['StratificationCategoryID1'])
    Q['StratificationID1']= label_encoder.fit_transform(Q['StratificationID1'])
    Q['Latitude']= label_encoder.fit_transform(Q['Latitude'])
    Q['DataValueType']= label_encoder.fit_transform(Q['DataValueType'])
    from sklearn.preprocessing import MinMaxScaler
    x_scaler = MinMaxScaler()
    X.columns = X.columns.map(lambda x: x.replace('"', ''))
    x_scaler.fit(X)
    column_names = X.columns
    X[column_names] = x_scaler.transform(X)

    from sklearn.naive_bayes import GaussianNB

    clf = GaussianNB()

    clf.fit(X, y)
    Ans=clf.predict(Q)
    print(Ans.item())
    return render_template('index.html', name = name, Ans=Ans.item())
    




if __name__ == "__main__":
    app.run()