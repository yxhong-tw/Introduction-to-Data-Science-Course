# Random Forest Module
# --------------------
from sklearn.ensemble import RandomForestClassifier
# --------------------


def model_select(model_selector):
    model = None

    if model_selector == 'Random_Forest':
        model = RandomForestClassifier(min_samples_leaf=2, n_estimators=1000, random_state=0, verbose=1, n_jobs=8)
    elif model_selector == 'SVM':
        # Set SVM model
        print('hello world')
    elif model_selector == 'KNN':
        # Set KNN model
        print('hello world')
    else:
        print('This is impossible case.')

    return model