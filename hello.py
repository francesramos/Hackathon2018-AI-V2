from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    import tensorflow as tf
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

    #Model Libraries
    import keras
    from keras.models import Sequential
    from keras.layers import Dense


    from keras.models import load_model

    #Import the data
    print("Loading data...")
    Data = pd.read_csv("Incidencia_Crime_Map_arrage.csv")
    Data = Data.dropna()
    print("Data loaded")


    #Grab input values
    x = Data.iloc[:,2:5].values
    #Grab label values
    y = Data.iloc[:,-1].values


    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    y = y.reshape(-1, 1) #change into 2d array

    one_hot_encoder = OneHotEncoder(categorical_features = [0])
    y = one_hot_encoder.fit_transform(y).toarray()


    #Split the data Randomly
    print("Creating testing set...")
    X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3)


    #Scalling input values
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)




    print("Loading Model...")
    classifier = load_model('crime_model.h5')
    print("Model Loaded")



    if request.method == 'POST':
        print(request.form['time'])
        print(request.form['latitude'])
        print(request.form['longitude'])
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        user_time = request.form['time']
        global graph_1_x
        global graph_1_y
        graph_1_x = [60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440]
        graph_1_y = []

        for time in graph_1_x:
            graph_1_y.append(classifier.predict(sc.transform([[user_time,latitude,longitude]])))


        print(graph_1_y)
        global graph_2_x
        global graph_2_y
        graph_2_x = label_encoder.classes_ #prints classes
        graph_2_y = []
        graph_2_y.append(classifier.predict(sc.transform([[user_time,latitude,longitude]])))
        print(graph_2_x)
        print(graph_2_y)
#why, the social impact

 #Scale data and predict




    municipios = ["Aguadilla", "Aibonito", "Arecibo", "Bayamon", "Caguas", "Carolina", "Fajardo", "Guayama", "Humacao", "Mayaguez", "Ponce", "San Juan", "Utuado"]
    data_por_municipio = []
    average_por_municipio = []
    percent_diff_por_municipio = []

    global average_puerto_rico
    #Split the data by municipios
    for municipio in municipios:
        data_por_municipio.append(Data[Data['Area Policiaca'].str.contains(municipio)])

    #Calculate the mean values for each municipio
    for i in range(len(data_por_municipio)):
        data_por_municipio[i] = data_por_municipio[i].iloc[:,2:5].values #grab only the input values
        data_por_municipio[i] = classifier.predict(sc.transform(data_por_municipio[i])) #Scale data and predict
        mean = np.mean(data_por_municipio[i], axis=0) #calculate the mean of the values for each category
        average_por_municipio.append(mean)

    #Calculate Puerto Rico average
    average_puerto_rico = np.mean(average_por_municipio, axis=0) #calculate the mean of the values for each category

    #Calculate difference between promedio municipio y average puerto rico
    for array in average_por_municipio:
            percent_diff_por_municipio.append(np.divide(array,average_puerto_rico))

    print(average_puerto_rico*100)



    return render_template('index.html', **globals())



if __name__=='__main__':
    app.run(debug=True)
