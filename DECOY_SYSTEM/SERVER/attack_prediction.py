import pickle
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd
# import warnings
# warnings.filterwarnings("ignore")


with open(file="trained_models/RandomForestClassifier_model.pkl", mode="rb") as file:
    model = pickle.load(file=file)

with open(file="trained_models/scaler.pkl", mode="rb") as file:
    scaler = pickle.load(file=file)

with open(file="trained_models/selected_features.pkl", mode="rb") as file:
    useful_cols = pickle.load(file=file)

class_labels = ['Benign', 'ddos', 'dos',
                'injection', 'password', 'scanning', 'xss']


def predict():
    input_ = 'in_folder/test.csv'
    input_ = pd.read_csv(input_)
    print("input_ : ", input_)

    input_ = input_[useful_cols]

    inp_cols = input_.columns
    scaled_input_ = scaler.transform(input_.values)
    input_df = pd.DataFrame(data=scaled_input_, columns=inp_cols)

    model_pred_class = model.predict(input_df.values)[0]
    model_pred_label = class_labels[model_pred_class]

    print("model_pred_class : ", model_pred_class)
    print("model_pred_label : ", model_pred_label)

    return model_pred_label
