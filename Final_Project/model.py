# Random Forest Module
# --------------------
from sklearn.ensemble import RandomForestClassifier
# --------------------


def model_selecting(model_selector):
    model = None

    if model_selector == 'random forest':
        model = RandomForestClassifier(min_samples_leaf=2, n_estimators=1000, random_state=0, verbose=1)
    elif model_selector == 'SVM':
        print(2)
    elif model_selector == 'KNN':
        print(3)
    else:
        print('hello world')

    return model