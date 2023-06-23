import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

learning_rates = [0.01, 0.005, 0.001, 0.0001]


def read_data(file_name):
    df = pd.read_excel(file_name, header=None)
    return df

def main():
    X_raw = read_data("X.xlsx")
    Y_raw = read_data("Y.xls") 

    Y_raw.replace(99, np.nan, inplace=True)

    average_reviews = Y_raw.mean()
    Y = average_reviews.reset_index(drop=True)
    Y = Y.drop(0)

    model = SentenceTransformer('bert-base-cased')
    X_arr = [x[0] for x in np.asarray(X_raw.to_numpy())]
    X = model.encode(X_arr)

    X = pd.DataFrame(X).drop(Y[Y.isna()].index)
    Y = Y.dropna()

    X_train_valid, X_test, Y_train_valid, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    X_train, X_valid, Y_train, Y_valid = train_test_split(X_train_valid, Y_train_valid, test_size=0.1, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    X_test = scaler.transform(X_test)

    best_score = float("inf")
    best_model = None

    for lr in learning_rates:
        mlp = MLPRegressor(solver = 'sgd', learning_rate = 'constant', learning_rate_init=lr, alpha=0.0) 
        mlp.fit(X_train, Y_train)

        plt.plot(mlp.loss_curve_, label = 'Learning curve')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

        Y_predict = mlp.predict(X_valid)
        train_score = mean_squared_error(Y_predict, Y_valid)

        print("For learning rate " + str(lr) + ", mean squared error on validation data is " + str(train_score))

        if train_score < best_score:
            best_score = train_score
            best_model = mlp
    
    Y_predict = best_model.predict(X_test)
    test_score = mean_squared_error(Y_predict, Y_test)

    print("Mean squared error for the best model on test data:", test_score)


    


if __name__ == "__main__":
    main()