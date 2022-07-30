import streamlit as st
import altair as alt
import utils

st.markdown('# Introduction')
st.write("Here we are going to explore European Soccer Database "
 "with a bunch of visualizations that might be insightful to a few people.")


@st.cache
def load_datasets():
    players = utils.load_df('players.feather')
    player_attrs = utils.load_df('player_attrs.feather')
    teams = utils.load_df('teams.feather')
    team_attrs = utils.load_df('team_attrs.feather')
    countries = utils.load_df('countries.feather')
    leagues = utils.load_df('leagues.feather')
    matches = utils.load_df('matches.feather')
    return players, player_attrs, teams, team_attrs, countries, leagues, matches

players, player_attrs, teams, team_attrs, countries, leagues, matches = load_datasets()

st.markdown('### Best and Worst Players')
def top_bottom_X_chart(X=10):
    player_avg_ratings = player_attrs.groupby('player_api_id')[['overall_rating', 'potential']].mean()
    sorted_player_avg_ratings = player_avg_ratings.sort_values('overall_rating', ascending=False)
    top_players_attrs = sorted_player_avg_ratings[:X]
    worst_players_attrs = sorted_player_avg_ratings[-X:]
    top_players = top_players_attrs.merge(players, on='player_api_id')
    worst_players = worst_players_attrs.merge(players, on='player_api_id')

    # Limit Y Axis to 0 to 100 by passing this to the encoding param `scale`
    zero_to_100_axis = alt.Scale(domain=[0, 100])

    # Top
    top_chart = alt.Chart(
        top_players,
        # width=500,
        title=f'Top {X} (Rating)' 
    ).mark_bar().encode(
        y=alt.Y('player_name',sort='-x'),
        x=alt.X('overall_rating', scale=zero_to_100_axis),
    ) 
    top_chart |= alt.Chart(
        top_players,
        # width=500,
        title=f'Top {X} (Potential)'
    ).mark_bar().encode(
        y=alt.Y('player_name',sort='-x'),
        x=alt.X('potential', scale=zero_to_100_axis),
    )

    # Bottom 
    bottom_chart = alt.Chart(
        worst_players,
        # width=500,
        title=f'Worst {X} (Rating)'
    ).mark_bar(color='firebrick').encode(
        y=alt.Y('player_name',sort='-x',),
        x=alt.X('overall_rating', scale=zero_to_100_axis),
    )

    bottom_chart |= alt.Chart(
        worst_players,
        # width=500,
        title=f'Worst {X} (Potential)'
    ).mark_bar(color='firebrick').encode(
        y=alt.Y('player_name',sort='-x',),
        x=alt.X('potential', scale=zero_to_100_axis),
    )
    return top_chart & bottom_chart



# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
add_slider = st.slider(
    'Pick a number to rank',
    0, 20, 10
)

st.altair_chart(top_bottom_X_chart(add_slider))

