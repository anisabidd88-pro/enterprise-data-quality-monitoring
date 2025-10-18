
import pandas as pd
from sklearn.impute import SimpleImputer

class Imputer:
    def __init__(self, strategy='median'):
        self.strategy = strategy

    def impute_dataframe(self, df, target_cols):
        df = df.copy()
        for col in target_cols:
            if col not in df.columns:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                imputer = SimpleImputer(strategy=self.strategy)
                vals = df[[col]]
                df[col] = imputer.fit_transform(vals)
            else:
                imputer = SimpleImputer(strategy='most_frequent')
                vals = df[[col]].astype(object)
                df[col] = imputer.fit_transform(vals)
        return df
