import pandas as pd
import altair as alt
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

## Altair

def alt_corr_plot(df: pd.DataFrame, *, corr_limit=0, box_size=100, annot_size=30) -> alt.Chart:
    corrMatrix = df.corr()\
    .reset_index()\
    .melt('index')
    
    corrMatrix.columns = ['var1', 'var2', 'correlation']
    corrMatrix = corrMatrix[corrMatrix['correlation'].abs() >= abs(corr_limit)]
    
    base = alt.Chart(corrMatrix).transform_filter(
        alt.datum.var1 < alt.datum.var2
    ).encode(
        x=alt.X('var1',title=''),
        y=alt.Y('var2',title=''),
    ).properties(
        width=alt.Step(box_size),
        height=alt.Step(box_size)
    )

    rects = base.mark_rect().encode(
        color='correlation'
    )
    
    corr_range = (corrMatrix['correlation'].max().item() + corrMatrix['correlation'].min().item())/2
    text_condition = f"datum.correlation > {corr_range}"
    text = base.mark_text(
        size=annot_size
    ).encode(
        text=alt.Text('correlation', format=".2f"),
        color=alt.condition(
            text_condition,
            alt.value('white'),
            alt.value('black')
        )
    )
    
    return rects + text