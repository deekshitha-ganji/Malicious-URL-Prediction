import streamlit as st
import joblib
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
import base64

# Load models and preprocessing functions
final_model1 = joblib.load('final_model1.pkl')
final_model2 = joblib.load('final_model2.pkl')
vectorizer1 = joblib.load('vectorizer1.pkl')
vectorizer2 = joblib.load('vectorizer2.pkl')

# Function to preprocess a single URL
def preprocess_single_url(url):
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    snowball_stemmer = SnowballStemmer('english')
    tokens = tokenizer.tokenize(url)
    stems = [snowball_stemmer.stem(token) for token in tokens]
    return ' '.join(stems)

# Function to predict the label for a single URL
def predict_single_url(url):
    preprocessed_url = preprocess_single_url(url)
    X_tfidf1 = vectorizer1.transform([preprocessed_url])
    X_tfidf2 = vectorizer2.transform([preprocessed_url])
    prediction1 = final_model1.predict(X_tfidf1)[0]
    prediction2 = final_model2.predict(X_tfidf2)[0]
    if prediction1 == 1 or prediction2 == 1:
        return "Bad"
    else:
        return "Good"
    

# Streamlit app
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        img = f.read()
    return base64.b64encode(img).decode()

image = get_img_as_base64("img.png")

bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{image}");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center; /* Center align the image */
}}
[data-testid="stHeader"] {{
    background-color: rgba(0,0,0,0);
}}
/* Custom CSS to style the Streamlit icons */
.streamlit-container .sidebar .css-1lbrv0a.e1xxz1600 > div:nth-child(1) svg, /* Share icon */
.streamlit-container .sidebar .css-1lbrv0a.e1xxz1600 > div:nth-child(2) svg, /* Fullscreen icon */
.streamlit-container .sidebar .css-1lbrv0a.e1xxz1600 > div:nth-child(3) svg {{ /* Menu icon */
    fill: white !important;
}}

.title-container {{
    background-color: rgba(255, 255, 255, 0.5); /* Translucent white background */
    border-radius: 10px; /* Rounded corners */
    padding: 20px; /* Add some padding */
    margin-bottom: 20px; /* Add some margin below the title */
}}

.prediction-container {{
    padding: 10px;
    border-radius: 5px;
    max-width: 300px;
    margin: 0 auto;
}}

h1 {{
    text-align: center;
    color: black;
}}
</style>
"""
st.markdown(bg, unsafe_allow_html=True)

st.write("<div class='title-container'><h1>Malicous URL Predictor</h1></div>", unsafe_allow_html=True)
st.markdown("<br><br><br>", unsafe_allow_html=True)

url = st.text_input('Enter URL:')
if st.button('Predict'):
        prediction = predict_single_url(url)
        if prediction == "Good":
            st.write("<div class='prediction-container' style='background-color: #00FF00;'>It is a legitimate URL</div>", unsafe_allow_html=True)
        else:
            st.write("<div class='prediction-container' style='background-color: #FFA500;'>Beware! It is a malicious URL</div>", unsafe_allow_html=True)
        
