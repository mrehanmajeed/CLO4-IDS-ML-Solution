import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import socket
import urllib.parse

# Page config
st.set_page_config(page_title="Network IDS Dashboard", page_icon="🛡️", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 30px;
    }
    .prediction-normal {
        background-color: #2ecc71;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .prediction-attack {
        background-color: #e74c3c;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load model and scaler
@st.cache_resource
def load_model():
    try:
        with open("ids_dt_model.pkl", "rb") as f:
            data = pickle.load(f)
        return data['model'], data['scaler'], data['features']
    except FileNotFoundError:
        return None, None, None

model, scaler, feature_cols = load_model()

# Helper function to parse URL to Hostname
def get_hostname(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc

# Simulation func: Convert Target to NSL-KDD features
# Note: In a real environment, you'd capture live PCAP traffic and route it through a parser.
# Here we simulate network traffic profiling based on the input string to demonstrate the ML model.
def simulate_network_features(target, feature_list):
    np.random.seed(sum([ord(c) for c in target])) # consistent random profile per target
    
    # 0 = Normal-like profile, 1 = Attack-like profile bias
    is_suspicious = np.random.choice([0, 1], p=[0.7, 0.3]) 
    
    fake_data = {}
    for col in feature_list:
        if 'rate' in col or 'error' in col:
            fake_data[col] = np.random.uniform(0.7, 1.0) if is_suspicious else np.random.uniform(0.0, 0.1)
        elif 'count' in col:
            fake_data[col] = np.random.randint(200, 511) if is_suspicious else np.random.randint(1, 20)
        elif 'bytes' in col:
            fake_data[col] = np.random.randint(1000, 50000)
        else:
            fake_data[col] = np.random.uniform(0, 1)
            
    return pd.DataFrame([fake_data])

# Dashboard Layout
st.markdown("<div class='main-header'>🛡️ AI-Powered Network Intrusion Detection</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Real-time traffic simulation & classification using Random Forest</div>", unsafe_allow_html=True)

if model is None:
    st.error("Model not found! Please run the `IDS_ML_Solution.ipynb` notebook completely to generate `ids_dt_model.pkl`.")
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2882/2882121.png", width=100)
    st.header("Scan Target")
    target_input = st.text_input("Enter IP Address or Hostname:", placeholder="e.g., https://bahria.edu.pk or 65.139.32.45")
    scan_btn = st.button("Analyze Target", type="primary")
    
    st.divider()
    st.markdown("### Model Properties")
    st.info(f"**Algorithm:** Random Forest\n\n**Features Expected:** {len(feature_cols)}\n\n**Status:** Online")

# Main Content
if scan_btn and target_input:
    hostname = get_hostname(target_input)
    
    # Simulate resolving
    with st.spinner(f"Resolving & Interrogating {hostname} ..."):
        time.sleep(1.5) # Fake delay
        try:
            ip_address = socket.gethostbyname(hostname)
        except socket.gaierror:
            ip_address = "IP Unresolved (Simulated Mode)"
        
        st.success(f"Successfully profiled target: {hostname} ({ip_address})")
    
    # Generate simulated PCAP features for this target
    st.markdown("### Traffic Telemetry (Simulated)")
    features_df = simulate_network_features(hostname, feature_cols)
    
    # Show some of the simulated features
    st.dataframe(features_df.iloc[:, :8], use_container_width=True)
    
    # Preprocess & Predict
    with st.spinner("Analyzing telemetry with ML Model..."):
        time.sleep(1)
        # Scale
        X = scaler.transform(features_df)
        
        # Predict
        prediction = model.predict(X)[0]
        prob = model.predict_proba(X)[0]
    
    # Display Results
    st.markdown("### Threat Classification Result")
    col1, col2 = st.columns(2)
    
    with col1:
        if prediction == 0:
            st.markdown("<div class='prediction-normal'>✅ NORMAL TRAFFIC</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='prediction-attack'>⚠️ MALICIOUS / ATTACK DETECTED</div>", unsafe_allow_html=True)
    
    with col2:
        st.metric(label="Threat Probability", value=f"{prob[1]*100:.2f}%")
        st.metric(label="Normal Probability", value=f"{prob[0]*100:.2f}%")
        
else:
    st.info("👈 Enter a target URL or IP address in the sidebar and click 'Analyze Target' to begin.")
    
    st.markdown("---")
    st.markdown("""
    ### About this Dashboard
    This application utilizes the model trained in `IDS_ML_Solution.ipynb`. Since full NIDS functionality requires live packet grabbing (e.g., Wireshark/TShark) and complex feature extraction (reconstructing NSL-KDD's 41 dimensions in real-time), this dashboard **simulates** those feature telemetry metrics based on the specific hostname/IP you input to demonstrate the Machine Learning classification in action.
    
    **Requirements:**
    `pip install streamlit pandas numpy scikit-learn`
    
    **Run:**
    `streamlit run app.py`
    """)
    
