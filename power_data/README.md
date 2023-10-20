### The projects have 2 parts
+ Part 1: Data science solution

++ This part focuses on the data statistic analysis and comparing the performance of each algorithm. Try to figure out
the best performance of models based on evaluating the value of MAPE param. After tuning the models, the system points out
the best parameters for the models and re-train model with the given dataset. Then, evaluate the value of MAPE to get the
best model

++ This part test the model prediction with the given date and obtain the forecasting value 



+ Part 2: Machine learning operation solution

++ This part focuses on the Machine learning operation solution. Given the right model (best performance), an API is 
created to make the endpoint of the model and ready to plug-in any layers. On the other hand, a docker file is created
to make sure that the system can run stable and easily scale up as well

++ This part test the model prediction with the POST method of the API
