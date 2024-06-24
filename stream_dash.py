from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px


# Load the pickled data

track_to_recommendation = pickle.load(open('track_to_recommendation.pkl', 'rb'))
rec_track_to_album_art = pickle.load(open('rec_track_to_album_art.pkl', 'rb'))
my_track_to_album_art = pickle.load(open('my_track_to_album_art.pkl', 'rb'))
song_url=pickle.load(open('my_songs_preview_url.pkl', 'rb'))
my_song_feature_array_dict=pickle.load(open('my_song_feature_array_dict.pkl','rb'))
train_song_feature_array_dict=pickle.load(open('train_song_feature_array_dict.pkl','rb'))


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

]

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
selected_song_url= song_url[selected_song]

st.write(f"Selected Song: {selected_song}")

if selected_song_url:
    st.audio(selected_song_url)

# Display selected song


if selected_song in my_track_to_album_art:
    st.sidebar.image(my_track_to_album_art[selected_song], width=250)
else:
    st.sidebar.write("No album art available for the selected song.")



# Display recommendations for selected song
st.write('**Recommendations:**')
recommendations = track_to_recommendation[selected_song]

# Create columns for recommendations
num_recommendations = len(recommendations)
num_columns = 3  # Number of columns in each row
num_rows = -(-num_recommendations // num_columns)  # Ceiling division to get the number of rows

for i in range(num_rows):
    row_recommendations = recommendations[i * num_columns: (i + 1) * num_columns]
    cols = st.columns(num_columns)
    for col, recommendation in zip(cols, row_recommendations):
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
        # recommendation_url = song_url.get(recommendation)
        # if recommendation_url:
        #     st.audio(recommendation_url)
        # else:
        #     col.write("No preview available for this recommendation.")   


st.title('Feature Analysis')


features=['danceability', 'energy', \
       'loudness', 'speechiness', \
        'acousticness', 'instrumentalness', \
       'liveness', 'valence', 'tempo']
# Get audio features for selected song
selected_song_features = np.array(my_song_feature_array_dict[selected_song]).reshape(1, -1)

# Get audio features for recommended songs
recommended_song_features = [train_song_feature_array_dict[rec] for rec in recommendations]

# Create DataFrame for easier comparison
selected_song_df = pd.DataFrame(selected_song_features,columns=features)
recommended_songs_df = pd.DataFrame(recommended_song_features,columns=features)


# Display audio features
num_features = len(features)
data = {
    'Features' : features,
    'Selected Track': selected_song_features.flatten(),
}
for i, recommended_track_data in enumerate(recommended_song_features):
    data[recommendations[i]] = recommended_track_data.flatten()

df = pd.DataFrame(data)


# st.sidebar.subheader('Selected Track Features Heatmap')
# plt.figure(figsize=(8, 6))
# sns.heatmap(selected_song_df.T, annot=True, cmap='coolwarm', fmt='.2f', cbar=False, linewidths=.5)
# plt.xlabel('Features')
# plt.ylabel('Selected Track')
# st.sidebar.pyplot(plt)



# Interactive Plotly plot
@st.cache_data
def get_plot(feature):
    fig = px.scatter(df.melt(id_vars=['Features', 'Selected Track'], var_name='Track', value_name='Scaled Values'),
                     x='Track', y='Scaled Values', color='Features',
                     title=f'{feature} - Selected Track vs Recommended Tracks',
                     template='plotly_white')
    
    # Filter the data based on the selected feature
    fig.update_traces(visible='legendonly')
    fig.for_each_trace(lambda trace: trace.update(visible=True) if trace.name == feature else trace.update(visible='legendonly'))
    
    # Customize the plot
    fig.update_traces(marker=dict(size=10, symbol='circle'), selector=dict(mode='markers'))
    fig.update_traces(marker=dict(size=10, symbol='diamond'), selector=dict(mode='markers', name='Selected Track'))
    fig.update_layout(xaxis_tickangle=-45)
    
    return fig

# Dropdown for selecting feature
selected_feature = st.selectbox('Select Feature', features)
if selected_feature:
    fig = get_plot(selected_feature)
    st.plotly_chart(fig,use_container_width=True,theme='streamlit')