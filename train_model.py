"""Train a small landmark classifier from the generated CSV dataset."""
import argparse
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/gesture_dataset.csv")
    parser.add_argument("--output", default="models/gesture_model.joblib")
    args=parser.parse_args()
    data=pd.read_csv(args.csv)
    if "label" not in data or data["label"].nunique()<2:
        raise SystemExit("Dataset must contain a label column and at least two gesture classes.")
    X=data.drop(columns=["label"]); y=data["label"]
    stratify=y if y.value_counts().min() >= 2 else None
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=42,stratify=stratify)
    model=make_pipeline(StandardScaler(),SVC(kernel="rbf",class_weight="balanced",probability=True))
    model.fit(X_train,y_train)
    print(classification_report(y_test,model.predict(X_test),zero_division=0))
    os.makedirs(os.path.dirname(args.output) or ".",exist_ok=True)
    joblib.dump(model,args.output)
    print(f"Saved model: {args.output}")
if __name__=="__main__": main()
