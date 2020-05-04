from collections import Counter
import numpy as np 
import pandas as pd 
import pickle
from sklearn import svm, model_selection, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


test_size = 0.2

def preprocess_data_for_labels(csv):
    hm_days = 7
    df = pd.read_csv('data/{}.csv'.format(csv), index_col=0)
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{0}_{1}d'.format(csv, i)] = (df['Adj Close'].shift(-i) - df['Adj Close']) / df['Adj Close']
    df.fillna(0, inplace=True)
    return df


def buy_sell_hold(*args):
    cols = [c for c in args]
    buy_requirement = 0.025
    sell_requirement = 0.025
    for col in cols:
        if col > buy_requirement:
            return 1
        if col < -sell_requirement:
            return -1
    return 0


def extract_featuresets(csv):
    df = preprocess_data_for_labels(csv)
    df['{}_target'.format(csv)] = list(map(buy_sell_hold, 
                                           df['{0}_1d'.format(csv)], 
                                           df['{0}_2d'.format(csv)],
                                           df['{0}_3d'.format(csv)],
                                           df['{0}_4d'.format(csv)], 
                                           df['{0}_5d'.format(csv)],
                                           df['{0}_6d'.format(csv)],
                                           df['{0}_7d'.format(csv)]
                                           ))
    vals = df['{}_target'.format(csv)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data Spread: ', Counter(str_vals))
    
    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df['Adj Close'].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    X = df_vals.values
    y = df['{}_target'.format(csv)].values

    return X, y, df

def do_ml(csv, do_pred):
    X, y, df = extract_featuresets(csv)
    X = X.reshape(-1, 1)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X,
                                                                        y,
                                                                        test_size=test_size)
    # clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rf', RandomForestClassifier())])
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)

    filename = 'models/IOZ_model_{}.sav'.format(str(round(confidence, 2)))
    pickle.dump(clf, open(filename, 'wb'))
    print('Accuracy: ', confidence)
    if do_pred:
        pickle.load(open(filename, 'rb'))
        predictions = clf.predict(X_test)
        print('predicted Spread: ', Counter(predictions))

    return confidence


do_ml('IOZ.AX', 1)