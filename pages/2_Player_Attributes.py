import streamlit as st
import altair as alt
import utils

def _(text):
    "Returns a streamlit markdown object"
    return st.markdown(text)


@st.cache
def load_datasets():
    player_attrs = utils.load_df('player_attrs.feather')
    return player_attrs
player_attrs = load_datasets()

COEFF = 0.9
st.markdown('# Player Attributes 🤸')
st.write("Now a little bit about the players' abilities")
st.write("There's definitely some strong correlation between their attributes, "
"and how one ability could influence another")

_(f'Here are a few attributes with a Pearson coefficient **>= {COEFF}**...')
_('*Note: gk = goalkeeper*')
corr_plot = utils.alt_corr_plot(player_attrs, corr_limit=0.9, box_size=50, annot_size=10)
st.altair_chart(corr_plot)
