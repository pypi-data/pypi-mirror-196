import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def evaluate_model(model, X, y):
    """
    This function evaluates your model and interprets the regression metrics results in a DataFrame format.
    
    Input
    ---------
    model: Regression Model
    X: Features
    y: Label
        
    Output
    -------
    metric_df: Result DataFrame
    """

    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    adj_r2 = 1 - (1-r2)*(len()-1)/(len(y)-X.shape[1]-1)
    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)

    metric_df = pd.DataFrame([r2, adj_r2, mse, mae]).T
    metric_df.index = "Metrics"
    metric_df.columns = ["R2 Score", "Adjusted R2", "Mean Squared Error", "Mean Absolute Error"]

    return metric_df