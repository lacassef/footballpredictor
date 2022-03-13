import pandas


# mlp for multi-label classification
from numpy import mean, asarray, std
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler


def get_training_data():
    dataframe = pandas.read_csv("persistence/training.csv")
    dataset = dataframe.drop('awardedMatches', axis=1).drop('id', axis=1).values
    X = dataset[:, 0:98].astype(float)
    y = dataset[:, 98:].astype(int)
    return X, y


def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(90, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(n_outputs, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam')
    # model.fit(X, y, epochs=150, batch_size=10)
    return model


def evaluate_model(X, y):
    results = list()
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # define evaluation procedure
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # enumerate folds
    for train_ix, test_ix in cv.split(X):
        # prepare data
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y[train_ix], y[test_ix]
        # define model
        model = get_model(n_inputs, n_outputs)
        st_x = MinMaxScaler()
        X_train = st_x.fit_transform(X_train)
        X_test = st_x.transform(X_test)
        # fit model
        model.fit(X_train, y_train, verbose=0, epochs=100)
        # make a prediction on the test set
        yhat = model.predict(X_test)
        # round probabilities to class labels
        yhat = yhat.round()
        # calculate accuracy
        acc = accuracy_score(y_test, yhat)
        # store result
        results.append(acc)
    return results


def make_prediction(mat: []) -> []:
    # load dataset
    X, y = get_training_data()
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # get model
    model = get_model(n_inputs, n_outputs)
    # fit the model on all data
    st_x = MinMaxScaler()
    X = st_x.fit_transform(X)
    model.fit(X, y, verbose=0, epochs=100)
    # make a prediction for new data
    # row = [3, 3, 6, 7, 8, 2, 11, 11, 1, 3]
    newX = asarray([mat])
    newX = st_x.transform(newX)
    yhat = model.predict(newX)
    return yhat