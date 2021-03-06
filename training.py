from numpy.random import seed

seed(1)  # keras seed fixing import

import tensorflow

tensorflow.random.set_seed(2)  # tensorflow seed fixing

# mlp for multi-label classification
import pandas as pd
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler


def get_training_data():
    dataframe = pd.read_csv("persistence/training.csv")
    dataset = dataframe.drop('awardedMatches', axis=1).drop('id', axis=1).values
    X = dataset[:, 0:98].astype(float)
    y = dataset[:, 98:].astype(int)
    return X, y


def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(90, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(n_outputs, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    return model


def evaluate_model(X, y):
    results = list()
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    model = get_model(n_inputs, n_outputs)
    # define evaluation procedure
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # enumerate folds
    for train_ix, test_ix in cv.split(X):
        # prepare data
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y[train_ix], y[test_ix]
        st_x = MinMaxScaler()
        X_train = st_x.fit_transform(X_train)
        X_test = st_x.transform(X_test)
        # fit model
        model.fit(X_train, y_train, verbose=0, epochs=200)
        # make a prediction on the test set
        yhat = model.predict(X_test)
        # print(yhat)
        # print(y_test)
        # round probabilities to class labels
        yhat = yhat.round()
        # calculate accuracy
        acc = accuracy_score(y_test, yhat)
        # store result
        results.append(acc)
    return results


def make_prediction(mat: dict) -> []:
    # load dataset
    X, y = get_training_data()
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # get model
    model = get_model(n_inputs, n_outputs)
    # fit the model on all data
    st_x = MinMaxScaler()
    X = st_x.fit_transform(X)
    model.fit(X, y, verbose=0, epochs=200)
    # make a prediction for new data
    # row = [3, 3, 6, 7, 8, 2, 11, 11, 1, 3]
    mat = pd.DataFrame([mat])
    dataset = mat.drop('awardedMatches', axis=1).drop('id', axis=1).values
    newX = dataset[:, 0:98].astype(float)
    # print(newX.shape)
    newX = st_x.transform(newX)
    yhat = model.predict(newX)
    return yhat[0]
