import streamlit as st
import pandas as pd
import pickle

# Load the pickled data
track_to_recommendation = pickle.load(open('track_to_recommendation.pkl', 'rb'))
rec_track_to_album_art = pickle.load(open('rec_track_to_album_art.pkl', 'rb'))
my_track_to_album_art = pickle.load(open('my_track_to_album_art.pkl', 'rb'))

# Apply custom CSS for dark theme with card layout
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
        font-family: 'Orbitron', sans-serif;
        color: #fff;
    }}
    .css-1d391kg {{
        background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e) !important;
        color: #fff;
    }}
    .css-145kmo2 h1 {{
        color: #ff4b1f;
        background: linear-gradient(to right, #ff9068, #fd746c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .css-1v0mbdj, .css-145kmo2 {{
        color: #fff;
    }}
    .card {{
        background-color: rgba(40, 40, 40, 0.8);
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        transition: transform 0.3s, background-color 0.3s;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }}
    .card:hover {{
        transform: scale(1.05);
        background-color: rgba(255, 75, 31, 0.8);
    }}
    .card img {{
        border-radius: 10px;
        width: 100px;
        height: 100px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# Create Streamlit UI
st.image('spotlog.jpg',width=100)
st.title('Song Recommendation System')
st.sidebar.title('Select a Song')

# Dropdown to select a song
selected_song = st.sidebar.selectbox('Select a song', list(track_to_recommendation.keys()))

# Display selected song
st.write(f"Selected Song: {selected_song}")

if selected_song in my_track_to_album_art:
    st.sidebar.image(my_track_to_album_art[selected_song], width=250)
else:
    st.sidebar.write("No album art available for the selected song.")

# Display recommendations for selected song
st.write('**Recommendations:**')
recommendations = track_to_recommendation[selected_song]

# Create columns for recommendations
num_recommendations = len(recommendations)
cols = st.columns(num_recommendations)

for col, recommendation in zip(cols, recommendations):
    with col:
        st.markdown(
            f"""
            <div class="card">
                <p>{recommendation}</p>
                {'<img src="' + (rec_track_to_album_art[recommendation] or '') + '" width="100">'}
            </div>
            """,
            unsafe_allow_html=True
        )   