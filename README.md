# HOTEL PRICE - PREDICTION

The task is to predict the prices of hotel for each case

This project was prepared with two steps. The first step consists of EDA, data pre-processing, feature engineering, model training and prediction, while the second step is the service API. The output of machine learning algorithms were written in csv as a file.

In this solution case, you can execute training and prediction via jupyter notebook. After prediction step, there is a separate success measurement notebook according to the RMSE, MAE and MAPE with different threshold.

In this solution, 2 main machine learning algorithms(Naive Bias and Random Forest Regressor) and their calibrated versions were used.


Again after prediction, you can create rest api to see results. "main.py" file under "src" folder was created for rest service. In this step for easy and fast execution, I prefer to dockerize the service. For dockerization, you have to run below commands on terminal.

*** For result service training, you have to run "python src/main.py" on terminal

But I highly recommend to use dockerize flask service version with help of below shell scripts

1) docker build --tag hotel-price-prediction-app:1.0 .
2) docker run -p 1001:1001 --name hotel-price-prediction-app hotel-price-prediction-app:1.0

After this process, you can use Postman to test. You can find postman file under "collection" file. You have to import that json file to the Postman. 

**Service:**

(post_preds) : This service return probability value for every transaction. This method doesn't need any parameter.

For this service, as a security rule, two different users were created. You have two enter username and password in body part of request. User informations were also written in config file:

[User1]
username = user1
password = password1

[User2]
username = user2
password = password2

Services return random 50 rows of dataframe as a json message.
