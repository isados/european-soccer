import pandas as pd
from sklearn.base import TransformerMixin

class DataFrameImputer(TransformerMixin):
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == 'object' else X[c].median() for c in X],
            index=X.columns)
        return self
    def transform(self, X, y=None):
        return X.fillna(self.fill)
    
def remove_columns_like(tbl: pd.DataFrame, like_text: str) -> None:
    """Removes columns with name like 'like_text' from 'tbl'"""
    redundant_columns = filter(lambda x : x.find(like_text)>0, tbl.columns)
    tbl.drop(redundant_columns, axis=1, inplace=True)
    
import pyarrow.feather as feather
folder = './processed/'
def save_df(df, filename):
    feather.write_feather(df, folder+filename)
def load_df(filename) -> pd.DataFrame:
    return feather.read_feather(folder+filename)
# save_df(player_attrs, 'pattrs.feather')
# load_df('pattrs.feather')