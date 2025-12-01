import streamlit as st
import pandas as pd
import joblib
import datetime, random
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize session state for navigation and dynamic content
if 'started' not in st.session_state:
    st.session_state.started = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# ── Konfigurasi halaman ───────────────────────────────────────
st.set_page_config(
    page_title="Good Health & Well-Being App",
    page_icon="❤️‍🩹",
    layout="wide",
)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Panggil CSS
local_css("style.css")

# Sidebar dengan profil pengguna
with st.sidebar:
    st.image("profil.png", width=100)  # Ganti dengan path gambar profil
    st.markdown("### **Good Health & Well Being**")
    st.markdown("Memonitor dan Mewaspadai Kesehatan Pasien secara Real-time")
    st.markdown("---")
    

# ── Sidebar navigasi ──────────────────────────────────────────
with st.sidebar:
    # Navigation items
    menu_items = ["🏠 Home", "📊 EDA", "📈 Health Prediction", "🌿 Well-Being Tips"]
    selected = st.radio(
        "Navigasi",
        menu_items,
        key='nav_radio',
        index=menu_items.index(st.session_state.current_page)
    )
    
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()
# Custom CSS untuk warna dan styling
    st.markdown("""
    <style>
    /* Background utama */
    .main {
        background-color: #FAF3E0;
        color: #4B3F2F;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #E2725B;
        color: #FAF3E0;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        color: #FAF3E0;
    }

    /* Sidebar link / radio button text */
    [data-testid="stRadio"] label {
        color: #FAF3E0;
    }

    /* Judul */
    h1, h2, h3, h4 {
        color: #4B3F2F;
    }

    /* Button */
    .stButton > button {
        background-color: #D36B00;
        color: #FAF3E0;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #DDB892;
        color: #4B3F2F;
    }

    /* Cards di kolom */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        color: #4B3F2F;
        margin-bottom: 20px;
    }

    .card img {
        margin-bottom: 15px;
    }

    .caption {
        color: #4B3F2F;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* Divider custom */
    .css-1v3fvcr {
        border-top: 2px solid #E2725B !important;
        margin: 2rem 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Wrap semua konten dalam div utama biar background warna jalan
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
# ── Muat model & scaler (tampilkan peringatan bila belum ada) ─
try:
    model  = joblib.load("stacking_model.pkl")
    pt     = joblib.load("power_transfromer.pkl")
    scaler = joblib.load("scaler.pkl")
except FileNotFoundError:
    model = pt = scaler = None
    st.sidebar.warning("⚠️ Berkas model *.pkl* tidak ditemukan. UI tetap bisa diuji.")

# =============================================================
# 1) HOME ─ About + EDA
# =============================================================
def show_home():
        # Header Halaman Utama
    st.markdown(
        """
        <div style='background-color: #FAF3E0; padding: 3% 5%; border-radius: 15px;'>
            <h1 style='color: #E2725B;'>Good Health & Well Being</h1>
            <h3 style='color: #4B3F2F;'>AI-Based Health Monitoring and Early Warning System</h3>
            <p style='font-size: 18px;'>A smart platform to monitor patient data in real-time and provide early warnings of dangerous health risks, to improve the quality of health services.</p>
            <div style='margin-top: 15px;'>
                <span style='background-color: #DDB892; color: #4B3F2F; padding: 6px 12px; border-radius: 20px; margin-right: 10px;'>Responsive</span>
                <span style='background-color: #DDB892; color: #4B3F2F; padding: 6px 12px; border-radius: 20px;'>Easy to Use</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Tombol aksi ──────────────────────────────────────────
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #D36B00;  /* Burnt orange */
            color: white;
            border-radius: 12px;
            font-weight: bold;
            padding: 0.6em 1.2em;
        }
        div.stButton > button:hover {
            background-color: #b35900;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── Tombol CTA ──────────────────────────────────────────
    if 'started' not in st.session_state:
        st.session_state.started = False
        
    st.markdown("<div style='margin-top: 3rem;'>", unsafe_allow_html=True)
    if st.button("Start Explore Good Health & Well Being", key="start_button_landing", use_container_width=True):
        st.session_state.current_page = "📈 Health Prediction"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
#-----------------------------------
    # Section: Welcome & About
    st.markdown("<h1 style='color:#63533e;'>About Our App</h1>", unsafe_allow_html=True)

    st.markdown("""
    <p style='color:#4B3F2F; font-size:16px; line-height:1.6;'>
    The <strong>Good Health and Well-Being Prediction App</strong> helps users gain insight into their <strong>daily habits</strong> and <strong>work-life balance</strong>.  
    Powered by an <strong>ensemble AI model</strong>, the app analyzes your daily activity data to deliver a personalized <strong>balance score</strong> and actionable lifestyle improvements.  
    Aligned with <strong>UN SDG 3</strong>, this app supports a healthier, more productive life for all.
    </p>
    """, unsafe_allow_html=True)
    st.divider()

    # Section: How It Works
    st.markdown("<h1 style='color:#63533e;'>How It Works</h1>", unsafe_allow_html=True)
    st.markdown("""
    <ul style='color:#4B3F2F; font-size:16px; line-height:1.8;'>
    <li><strong>Input your activity data</strong> – Fill a simple form with your daily habits.</li>
    <li><strong>Model processes the data</strong> – Our AI predicts your work-life balance score instantly.</li>
    <li><strong>Get personalized suggestions</strong> – Discover insights and tips to improve your balance.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.divider()

    # Section: Products
    st.markdown("<h1 style='text-align: center; color:#63533e;'>Our Products</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background-color: #FAF3E0; padding: 30px; border-radius: 16px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/2886/2886873.png" width="60"/>
                <div style="font-size: 24px; font-weight: 600; color: #4B3F2F; margin-top: 12px;">Work-Life Score</div>
                <div style="font-size: 16px; color: #4B3F2F; margin-top: 6px;">Predict your balance instantly</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background-color: #FAF3E0; padding: 30px; border-radius: 16px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); text-align: center;">
                <img src="https://cdn-icons-png.flaticon.com/128/10322/10322736.png" width="60"/>
                <div style="font-size: 24px; font-weight: 600; color: #4B3F2F; margin-top: 12px;">Lifestyle Insights</div>
                <div style="font-size: 16px; color: #4B3F2F; margin-top: 6px;">Tailored tips to improve habits</div>
            </div>
        """, unsafe_allow_html=True)
    st.divider()

    # Section: SDG 3
    st.markdown("<h1 style='text-align: center; color:#63533e;'>In Support of SDG 3</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center;">
            <img src="https://sdgs.un.org/sites/default/files/goals/E_SDG_Icons-03.jpg" width="120"/>
            <p style="color: #4B3F2F; font-size: 14px; margin-top: 8px;">
                This app contributes to the United Nations Sustainable Development Goal 3.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Section: Team
    st.markdown("<h1 style='text-align:center; color:#63533e;'>Our Team</h1>", unsafe_allow_html=True)

    team_cards = [
        {
            "number": "1",
            "name": "Eduard Mario Kayesa",
            "role": "Machine Learning Engineer",
            "desc": "Handles model training and performance tuning."
        },
        {
            "number": "2",
            "name": "I Kadek Defa Danuarta",
            "role": "Data Scientist",
            "desc": "Leads data preprocessing and feature selection."
        },
        {
            "number": "3",
            "name": "Gabriela Safira Cristiananda",
            "role": "UI/UX Designer",
            "desc": "Crafts smooth and inclusive user experiences."
        },
        {
            "number": "4",
            "name": "Faradilla Alfaira Chandra",
            "role": "UI/UX Designer",
            "desc": "Designs intuitive, mobile-friendly interfaces."
        }
    ]

    cols = st.columns(4)
    for idx, member in enumerate(team_cards):
        with cols[idx]:
            st.markdown(f"""
                <div style='background-color:#FAF3E0; padding:24px; border-radius:16px; box-shadow:0 4px 10px rgba(0,0,0,0.05); text-align:center;'>
                    <div style='background-color:#E2725B; color:white; font-weight:bold; font-size:18px; width:40px; height:40px; line-height:40px; border-radius:50%; margin:auto;'>{member["number"]}</div>
                    <div style='font-size:18px; font-weight:600; color:#4B3F2F; margin-top:10px;'>{member["name"]}</div>
                    <div style='font-size:14px; font-weight:500; color:#4B3F2F;'>{member["role"]}</div>
                    <div style='font-size:13px; color:#4B3F2F; margin-top:6px;'>{member["desc"]}</div>
                </div>
            """, unsafe_allow_html=True)

# =============================================================
# 2) EDA
# =============================================================
def show_eda():
    st.markdown("""
        <div style='background-color: #FAF3E0; padding: 1.5rem; border-radius: 12px;'>
            <h1 style='color: #E2725B;'>Dokumentasi EDA</h1>
            <p style='color: #4B3F2F;'>Analisis data eksploratif untuk memahami distribusi, pola, dan insight dari data terkait keseimbangan hidup.</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    df = pd.read_csv("datasets_wellbeing.csv")
    
    st.markdown("""<h2 style='color:#63533e;'>Dataset Overview</h2>""", unsafe_allow_html=True)
    st.dataframe(df.head())
    st.markdown(f"Total data: {df.shape[0]} baris dan {df.shape[1]} kolom.")
    st.divider()

    st.markdown("""<h2 style='color:#63533e;'>Informasi Tipe Data</h2>""", unsafe_allow_html=True)
    st.write(df.dtypes)
    st.divider()

    st.markdown("""<h2 style='color:#63533e;'>Data Cleaning Process</h2>""", unsafe_allow_html=True)
    if 'Timestamp' in df.columns:
        df.drop(columns=['Timestamp'], inplace=True)
        st.write("✓ Kolom 'Timestamp' telah dihapus.")
        st.caption("Kolom dihapus karena tidak terlalu berhubungan dengan target")

    missing = df.isnull().sum().sum()
    if missing > 0:
        df.dropna(inplace=True)
        st.write(f"✓ {missing} missing values ditemukan dan telah dihapus.")
    else:
        st.write("✓ Tidak ada missing values.")

    duplikat = df.duplicated().sum()
    if duplikat > 0:
        df.drop_duplicates(inplace=True)
        st.write(f"✓ {duplikat} baris duplikat ditemukan dan telah dihapus.")
    else:
        st.write("✓ Tidak ada data duplikat.")

    fitur_numerik = df.select_dtypes(include='number').columns.tolist()
    total_outliers = 0

    for fitur in fitur_numerik:
        Q1 = df[fitur].quantile(0.25)
        Q3 = df[fitur].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        before = df.shape[0]
        df = df[(df[fitur] >= lower) & (df[fitur] <= upper)]
        after = df.shape[0]
        removed = before - after
        total_outliers += removed
        if removed > 0:
            st.write(f"✓ {removed} outlier dihapus pada fitur '{fitur}'.")

    if total_outliers == 0:
        st.write("✓ Tidak ada outlier yang ditemukan.")

    # Tampilkan data akhir
    st.markdown("---")
    st.markdown("""<h2 style='color:#63533e;'>Data Setelah Dibersihkan</h2>""", unsafe_allow_html=True)
    st.write(df.head())
    st.divider()
    st.write(f"Jumlah data setelah pembersihan: {df.shape[0]} baris dan {df.shape[1]} kolom")

    st.markdown("""<h2 style='color:#63533e;'>Statistik Deskriptif</h2>""", unsafe_allow_html=True)
    st.write("Berikut statistik ringkasan untuk fitur numerik setelah proses pembersihan data:")
    st.dataframe(df.describe())

    st.caption("Setelah Data Cleaning, Explore distribusi data, hubungan, dan korelasi sebelum membangun model.")
    st.divider()
    st.markdown("""
        <div style='margin-top: 2rem; background-color: #FAF3E0; padding: 1rem; border-radius: 10px;'>
            <h1 style='color: #D36B00;'>Explorasi Data</h1>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📈 Distribusi Data", "🔗 Fitur vs Target", "🧩 Korelasi"])

    with tab1:
        st.markdown("""<h1 style='color:#63533e;'>Distribusi Data Fitur – Target</h1>""", unsafe_allow_html=True)
        st.write("Histogram untuk melihat distribusi data target dan fitur (Numerik dan Kategori).")
        st.divider()
        st.markdown("""<h2 style='color:#63533e;'>Distribusi Data Target</h2>""", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8,4))
        sns.histplot(df["WORK_LIFE_BALANCE_SCORE"], kde=True, ax=ax, color = 'Teal')
        ax.set_title("Distribusi Work-Life Balance Score")
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("Distribusi Fitur Numerik")
        fitur_numerik = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        fitur_numerik = [col for col in fitur_numerik if col != 'WORK_LIFE_BALANCE_SCORE']
        feat_scatter = st.selectbox("Pilih fitur numerik:", fitur_numerik, key="selectbox_numerik")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[feat_scatter], kde=True, ax=ax, color='salmon')
        ax.set_xlabel(fitur)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        st.markdown("---")
        st.subheader("Distribusi Fitur Kategorik")
        fitur_kategorikal = df.select_dtypes(include='object').columns.tolist()
        selected_cat = st.selectbox("Pilih fitur kategorik:", fitur_kategorikal, key="selectbox_kategori")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x=selected_cat, order=df[selected_cat].value_counts().index, ax=ax, color = 'lightblue')
        ax.set_title(f"Distribusi kategori pada fitur {selected_cat}")
        st.pyplot(fig)


    with tab2:
        st.markdown("<h1 style='color:#63533e;'>Hubungan Fitur – Target</h1>", unsafe_allow_html=True)
        st.write("Scatter plot dan boxplot untuk melihat pengaruh fitur terhadap skor WLB (Work-Life Balance Score).")
        st.divider()
        st.markdown("<h2 style='color:#63533e;'>Scatter Plot Fitur Numerik - Target</h2>", unsafe_allow_html=True)
        fitur_numerik = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        fitur_numerik = [col for col in fitur_numerik if col != 'WORK_LIFE_BALANCE_SCORE']

        st.write("Scatter plot untuk melihat pengaruh fitur numerik terhadap skor WLB.")
        feat_scatter = st.selectbox("Pilih fitur numerik:", fitur_numerik, key="scatter_numerik")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.regplot(data=df, x=feat_scatter, y="WORK_LIFE_BALANCE_SCORE",
                    scatter_kws={'alpha': 0.5, 'color':'lightblue'},
                    line_kws={'color':'red'}, ax=ax)
        ax.set_title(f"{feat_scatter} vs Work-Life Balance Score")
        st.pyplot(fig)

        st.markdown("---")
        st.markdown("<h2 style='color:#63533e;'>Boxplot Fitur Kategorikal - Target</h2>", unsafe_allow_html=True)
        fitur_kategorikal = df.select_dtypes(include='object').columns.tolist()
        st.write("Boxplot untuk melihat pengaruh fitur kategori terhadap skor WLB.")
        feat_box = st.selectbox("Pilih fitur kategorikal:", fitur_kategorikal, key="boxplot_kategori")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x=feat_box, y="WORK_LIFE_BALANCE_SCORE", ax=ax, palette='Pastel1')
        ax.set_title(f"Distribusi Work-Life Balance Score berdasarkan {feat_box}")
        st.pyplot(fig)


    with tab3:
        st.markdown("<h1 style='color:#63533e;'>Korelasi Antar Fitur</h1>", unsafe_allow_html=True)
        st.write("Heatmap untuk melihat korelasi semua fitur numerik dengan target.")
        st.divider()

        st.markdown("<h2 style='color:#63533e;'>Analisis Korelasi terhadap Work-Life Balance Score</h2>", unsafe_allow_html=True)
        def plot_correlation_heatmap(df):
            plt.figure(figsize=(12, 8))
            correlation = df.select_dtypes(include='number').corr()
            sns.heatmap(correlation[['WORK_LIFE_BALANCE_SCORE']].sort_values(by='WORK_LIFE_BALANCE_SCORE', ascending=False),
                        annot=True, cmap='coolwarm')
            plt.title("Korelasi Fitur dengan WORK_LIFE_BALANCE_SCORE")
            st.pyplot(plt)
            
        plot_correlation_heatmap(df)
        st.divider()
        st.write("Hasil visualisasi ditampilkan dalam bentuk **heatmap** dengan rentang nilai dari -1 hingga 1. **Insight yang diperoleh:**")
        st.write("**-  Korelasi Positif Tinggi**") 
        st.write("Fitur `ACHIEVEMENT`, `SUPPORTING_OTHERS`, dan `TODO_COMPLETED` memiliki korelasi sebesar **0.53–0.55** terhadap skor work-life balance. Artinya, **pencapaian pribadi, membantu orang lain, dan menyelesaikan tugas** berkontribusi positif terhadap keseimbangan hidup.")
        st.write("**- Dukungan Sosial dan Aktivitas Pribadi**")
        st.write("Fitur `PLACES_VISITED`, `TIME_FOR_PASSION`, dan `CORE_CIRCLE` juga menunjukkan korelasi positif (≥ 0.5), menandakan bahwa **rekreasi dan hubungan sosial** penting untuk keseimbangan hidup.") 
        st.write("**- Korelasi Negatif**")
        st.write("`LOST_VACATION` memiliki korelasi negatif tertinggi (-0.26), diikuti `BMI_RANGE` (-0.25) dan `DAILY_SHOUTING` (-0.21). Ini menunjukkan bahwa **tidak mengambil cuti, kesehatan yang kurang ideal, serta kebiasaan marah** dapat menurunkan skor work-life balance.")
        st.write("**- Korelasi Lemah**")
        st.write("`SLEEP_HOURS` hanya berkorelasi 0.17 terhadap work-life balance, sehingga meskipun penting, **tidur** tidak menjadi faktor utama dalam dataset ini.")
        st.write("Kesimpulannya, skor work-life balance paling banyak dipengaruhi oleh **pencapaian pribadi, hubungan sosial, dan aktivitas positif**, serta dapat menurun karena **stres, kurangnya liburan, atau kondisi fisik yang kurang baik**.")

# =============================================================
# 3) PREDIKSI KESEHATAN
# =============================================================
def show_prediction():
    st.markdown("""
        <div style='background-color: #FAF3E0; padding: 1.5rem; border-radius: 12px;'>
            <h1 style='color: #E2725B;'>Your Health Prediction</h1>
            <p style='color: #4B3F2F;'>Please fill in the details below to get started:</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("We only use this information to provide personalized insights.")
    st.divider()

    #load modelnya
    model = joblib.load("linear_regression.pkl")
    pt = joblib.load("power_transfromer.pkl")
    scaler = joblib.load("scaler.pkl")

    # User Input
    name = st.text_input("**Enter your name**", placeholder="Ex. John Doe", max_chars=50)

    age = st.number_input(
        "**Enter your age**",
        placeholder=25,
        step=1,
        help="*(Age in years)*",
    )
    st.write("You entered", age, "years")
    #clasification age
    if age < 0 or age > 80:
        classification_age = "Invalid age"
    elif age <= 20:
        classification_age = "Less than 20"
    elif age <= 35:
        classification_age = "21 to 35"
    elif age <= 50:
        classification_age = "36 to 50"
    else:  # age between 51 and 80
        classification_age = "51 or more"
    # Mapping age
    age_mapping = {
        "36 to 50": 2,
        "51 or more": 3,
        "21 to 35": 1,
        "Less than 20": 0,
    }
    st.write("Classified age:", classification_age)
    if classification_age in age_mapping:
        st.write("Mapped Age Level:", age_mapping[classification_age])
    else:
        st.write("Invalid age entered.")

    #nanti ubah aja ini nya
    gender_mapping = {
        "Male": "Male",
        "Female": "Female",
        "Other": "Nan",
    }
    gender_numeric = {
        "Male": 0,
        "Female": 1,
        "Other": 2
    }

    gender = st.radio(
        "**Select your gender *(select one)***",
        ["Male", "Female", "Other"]
    )
    st.write("You selected", gender)
    col1, col2 = st.columns(2)
    with col1:
        fruitVeggies_mapping = {
            "never (0 servings)": 0,
            "Almost never (1 servings)": 1,
            "Rarely (2 serving)": 2,
            "Occasionally (3 servings)": 3,
            "Often (4 servings)": 4,
            "Very often (5 or more servings)": 5
            }
        fruitVeggies = st.radio(
            "**1. How Many Fruits Or Vegetables Do You Eat Everyday?**",
            list(fruitVeggies_mapping.keys())
        )
        st.write("You selected", fruitVeggies)

        stress_mapping = {
            "Not at all stressful": 0,
            "Slightly stressful": 1,
            "Somewhat stressful": 2,
            "Moderately stressful": 3,
            "Very stressful": 4,
            "Extremely stressful": 5
        }
        dailyStress = st.radio(
            "**2. How Much Stress Do You Typically Experience Everyday?**",
            list(stress_mapping.keys())
        )
        st.write("You selected:", dailyStress)
        
        placesVisited_mapping = {
            "never" : 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "More than 10": 10
        }
        placesVisited = st.select_slider(
            "**3. How Many New Places Do You Visit In a Month?**",
            options=[
                "never",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "More than 10",
            ]
        )
        st.write("selected", placesVisited)
        st.write("Mapped Places Visited Level:", placesVisited_mapping[placesVisited])

        coreCircle_mapping = {
            "No one": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Large close circle": 10
        }
        coreCircle= st.select_slider(
            "**4. How Many People That Are Very Close To You?**",
            options=[
                "No one",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "Large close circle",
            ]
        )
        st.write("selected", coreCircle)
        st.write("Mapped Core Circle Level:", coreCircle_mapping[coreCircle])

        supportingOthers_mapping = {
            "never" : 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Many people (more than 10)": 10
        }
        supportingOthers = st.select_slider(
            "**5. How Many People Do You Help to Achieve a Better Life??**",
            options=[
                "never",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "Many people (more than 10)",
            ]
        )
        st.write("selected", supportingOthers)
        st.write("Mapped Supporting Others Level:", supportingOthers_mapping[supportingOthers])

        socialNetwork_mapping = {
            "No interactions at all" :0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "A Lot of interactions": 10
        }
        socialNetwork = st.select_slider(
            "**6. With How Many People do You Interact With During the Day?**",
            options=[
                "No interactions at all",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "A Lot of interactions",
            ]
        )
        st.write("selected", socialNetwork)
        st.write("Mapped Supporting Others Level:", socialNetwork_mapping[socialNetwork])
        
        achievements_mapping = {
            "No achievements" :0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Many achievements (more than 10)": 10
        }
        achievements = st.select_slider(
            "**7. How Many Remarkable Achievements Are You Proud of?**",
            options=[
                "No achievements",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "Many achievements (more than 10)",
            ]
        )
        st.write("selected", achievements)
        st.write("Mapped Achievements Level:", achievements_mapping[achievements])

        donations_mapping = {
            "Never" :0,
            "Almost never": 1,
            "Rarely": 2,
            "Often": 3,
            "Very often": 4,
            "Always": 5,
        }
        donation =st.radio(
            "**8. How Many Times do You Donate Your Time or Money for a Good Causes?**",
            [
                "Never",
                "Almost never",
                "Rarely",
                "Often",
                "Very often",
                "Always",
            ]
        )
        st.write("selected", donation)
        st.write("Mapped Donations Level:", donations_mapping[donation])

        bmiRange_mapping = {
            "Underweight to  normal weight ( Less than 18.5 untill 24.9)": 1,
            "Overweight to Obesity (25 until 29.9 or more)": 2,
        }
        bmiRange = st.radio(
            "**9. What  Is Your Body Mass Index (BMI) Range?**",
            [
                "Underweight to  normal weight ( Less than 18.5 untill 24.9)",
                "Overweight to Obesity (25 until 29.9 or more)",
            ]
        )
        st.write("selected", bmiRange)
        st.write("Mapped BMI Range Level:", bmiRange_mapping[bmiRange])

    with col2:
        toDoCompletition_mapping = {
            "never" :0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "Always (10)": 10
        }
        toDoCompletition = st.select_slider(
            "**10. Rate How Well Do You Complete Your Weekly To-Do Lists?**",
            options=[
                "never",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "Always (10)",
            ]
        )
        st.write("selected", toDoCompletition)
        st.write("Mapped To Do Completition Level:", toDoCompletition_mapping[toDoCompletition])

        flow_mapping = {
            "never" :0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "More than 10": 10
        }
        flow = st.select_slider(
            "**11. In a typical day, how many hours do you experience ‘flow’?**",
            help="*(Flow is a state of total immersion in an activity—often called being “in the zone.)*",
            options=[
                "never",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "More than 10",
            ]
        )
        st.write("selected", flow)
        st.write("Mapped Flow Level:", flow_mapping[flow])

        steps_mapping = {
            "None": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "More than 10": 10
        }
        steps = st.select_slider(
            "**12. How Many Steps Do You Walk In a Day?**",
            help="*(measured in units of thousands.)*",
            options=[
                "None",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "More than 10",
            ]
        )
        st.write("selected", steps)
        st.write("Mapped Steps Level:", steps_mapping[steps])

        vision_mapping = {
            "No clarity beyond today": 0,
            "few weeks": 1,
            "1 months": 2,
            "2-3 month": 3,
            "6 months": 4,
            "1 year": 5,
            "2 years": 6,
            "3–5 years": 7,
            "6–9 years": 8,
            "9–10 years": 9,
            "More than 10 years": 10
        }
        vision = st.select_slider(
            "**13. For how many years ahead is your life vision very clear?**",
            help="*(measured in units of hours.)*",
            options=[
                "No clarity beyond today",
                "few weeks",
                "1 months",
                "2-3 month",
                "6 months",
                "1 year",
                "2 years",
                "3–5 years",
                "6–9 years",
                "9–10 years",
                "More than 10 years",
            ]
        )
        st.write("selected", vision)
        st.write("Mapped Vision Level:", vision_mapping[vision])

        sleep_mapping = {
            "Not sleeping at all": 0,
            "1 hours": 1,
            "2 hours": 2,
            "3 hours": 3,
            "4 hours": 4,
            "5 hours": 5,
            "6 hours": 6,
            "7 hours": 7,
            "8 hours": 8,
            "9 hours": 9,
            "More than 9 hours": 10
        }
        sleep = st.select_slider(
            "**14. About how long do you typically sleep each night?**",
            help="*(measured in units of hours.)*",
            options=[
                "Not sleeping at all",
                "1 hours",
                "2 hours",
                "3 hours",
                "4 hours",
                "5 hours",
                "6 hours",
                "7 hours",
                "8 hours",
                "9 hours",
                "More than 9 hours",
            ]
        )
        st.write("selected", sleep)
        st.write("Mapped Sleep Level:", sleep_mapping[sleep])

        lostVacation_mapping = {
            "0 day": 0,
            "1 day": 1,
            "2 days": 2,
            "3 days": 3,
            "4-5 days": 4,
            "6-7 days": 5,
            "8-9 days": 6,
            "10-12 days": 7,
            "13-15 days": 8,
            "14-16 days": 9,
            "more than 16 days": 10
        }
        lostVacation = st.select_slider(
            "**15. How Many Days Do You Typicallly Lose Every Year?**",
            help="*(measured in units of days.)*",
            options=[
                "0 day",
                "1 day",
                "2 days",
                "3 days",
                "4-5 days",
                "6-7 days",
                "8-9 days",
                "10-12 days",
                "13-15 days",
                "14-16 days",
                "more than 16 days"
            ]
        )
        st.write("selected", lostVacation)
        st.write("Mapped Lost Vacation Level:", lostVacation_mapping[lostVacation])

        shout_mapping = {
            "Never": 0,
            "Almost never shout or sulk": 1,
            "Very rarely (a few times a year)": 2,
            "Rarely (once a month or less)": 3,
            "Occasionally (2–3 times a month)": 4,
            "Sometimes (about once a week)": 5,
            "Fairly often (2–3 times a week)": 6,
            "Often (4–5 times a week)": 7,
            "Very often (nearly every day)": 8,
            "Almost always (multiple times daily": 9,
            "Constantly shout or sulk": 10
        }
        shout = st.select_slider(
            "**16. How Many Times Do You Shout or Yell?**",
            help="*(measured in units of times.)*",
            options=[
                "Never",
                "Almost never shout or sulk",
                "Very rarely (a few times a year)",
                "Rarely (once a month or less)",
                "Occasionally (2–3 times a month)",
                "Sometimes (about once a week)",
                "Fairly often (2–3 times a week)",
                "Often (4–5 times a week)",
                "Very often (nearly every day)",
                "Almost always (multiple times daily",
                "Constantly shout or sulk",
            ]
        )
        st.write("selected", shout)
        st.write("Mapped Shout Level:", shout_mapping[shout])

        sufficient_income_mapping = {
            "Sufficient": 1,
            "Not sufficient": 2,
        }
        sufficient_income = st.radio(
            "**17. How sufficient is your income to cover your basic life expenses?**",
            [
                "Sufficient",
                "Not sufficient",
            ]
        )
        st.write("selected", sufficient_income)
        st.write("Mapped Sufficient Income Level:", sufficient_income_mapping[sufficient_income])

        personalAward_mapping = {
            "none": 0,
            "1": 1,
            "2": 2,
            "3-5": 3,
            "6-9": 4,
            "10-14": 5,
            "15-19": 6,
            "20-24": 7,
            "25-29": 8,
            "30-35": 9,
            "more than 35": 10
        }
        personalAward = st.select_slider(
            "**18. How Many Personal Awards Do You Have?**",
            help="*(Here, “recognitions” refers to any formal or informal acknowledgements you’ve received—such as awards, certificates, public praise, or other expressions of appreciation for your achievements or contributions.)*",
            options=[
                "none",
                "1",
                "2",
                "3-5",
                "6-9",
                "10-14",
                "15-19",
                "20-24",
                "25-29",
                "30-35",
                "more than 35",
            ]
        )
        st.write("selected", personalAward)
        st.write("Mapped Personal Award Level:", personalAward_mapping[personalAward])

        timeForPassion_mapping = {
            "never" :0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "More than 10": 10
        }
        timeForPassion = st.select_slider(
            "**19. How Many Hours Do You Spend Everyday On Your Passion?**",
            help="*(measured in units of hours.)*",
            options=[
                "never",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "More than 10",
            ]
        )
        st.write("selected", timeForPassion)
        st.write("Mapped Time For Passion Level:", timeForPassion_mapping[timeForPassion])

        weeklyMeditate_mapping = {
            "never" :0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "More than 10": 10
        }
        weeklyMeditate = st.select_slider(
            "**20. How Many Times Do You Meditate In a Week?**",
            help="*(measured in units of times.)*",
            options=[
                "never",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "More than 10",
            ]
        )
        st.write("selected", weeklyMeditate)
        st.write("Mapped Weekly Meditate Level:", weeklyMeditate_mapping[weeklyMeditate])

    if st.button("Predict Health Status"):
        if not name or age == 0:
            st.warning("⚠️ Silakan isi *nama* dan *usia* terlebih dahulu sebelum melakukan prediksi.")
        else:
            # Grouping data
            input_data = {
                "FRUITS_VEGGIES": fruitVeggies_mapping[fruitVeggies],
                "DAILY_STRESS": stress_mapping[dailyStress],
                "PLACES_VISITED": placesVisited_mapping[placesVisited],
                "CORE_CIRCLE": coreCircle_mapping[coreCircle],
                "SUPPORTING_OTHERS": supportingOthers_mapping[supportingOthers],
                "SOCIAL_NETWORK": socialNetwork_mapping[socialNetwork],
                "ACHIEVEMENT": achievements_mapping[achievements],
                "DONATION": donations_mapping[donation],
                "BMI_RANGE": bmiRange_mapping[bmiRange],
                "TODO_COMPLETED": toDoCompletition_mapping[toDoCompletition],
                "FLOW": flow_mapping[flow],
                "DAILY_STEPS": steps_mapping[steps],
                "LIVE_VISION": vision_mapping[vision],
                "SLEEP_HOURS": sleep_mapping[sleep],
                "LOST_VACATION": lostVacation_mapping[lostVacation],
                "DAILY_SHOUTING": shout_mapping[shout],
                "SUFFICIENT_INCOME": sufficient_income_mapping[sufficient_income],
                "PERSONAL_AWARDS": personalAward_mapping[personalAward],
                "TIME_FOR_PASSION": timeForPassion_mapping[timeForPassion],
                "WEEKLY_MEDITATION": weeklyMeditate_mapping[weeklyMeditate],
                "AGE": age_mapping[classification_age],
                "GENDER": gender_numeric[gender]
            }       

            features_df = pd.DataFrame([input_data])

            # Normalisasi feature tertentu
            col_to_normalize = ['ACHIEVEMENT','FLOW','LIVE_VISION','LOST_VACATION','DAILY_SHOUTING','SUFFICIENT_INCOME','TIME_FOR_PASSION']
            normalized_feature = features_df.copy()
            normalized_feature[col_to_normalize] = pt.transform(normalized_feature[col_to_normalize])
            
            scaled_date = normalized_feature.copy()
            scaled_date = scaler.transform(normalized_feature)
            
            # Prediksi model
            prediction = model.predict(scaled_date)
            
            def scale_value(x, old_min=480, old_max=780, new_min=1, new_max=100):
                scaled = ((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
                return scaled

        
            scaled_values = scale_value(prediction[0])
        
            st.success(f"Hasil Prediksi: {scaled_values:.2f}")
        
            if scaled_values < 50:
                st.markdown(
                    """
                    <div style="background-color:#cb4335;padding:20px;border-radius:12px;text-align:center;">
                        <h2 style="color:#7b241c ;">⚠️ Poor Quality of Life</h2>
                        <p style="font-size:18px;">Your well-being score is low. Consider reviewing the recommendations below to improve your lifestyle.</p>
                    </div>
                    """, unsafe_allow_html=True
                )
            elif 50 <= scaled_values <= 80:
                st.markdown(
                    """
                    <div style="background-color:#f1c40f;padding:20px;border-radius:12px;text-align:center;">
                        <h2 style="color:#cc6600;">✅ Good Quality of Life</h2>
                        <p style="font-size:18px;">You're doing fairly well! But there's still room to grow. Check the suggestions to optimize your well-being.</p>
                    </div>
                """, unsafe_allow_html=True
                )
            else:  # scaled_values > 80
                st.markdown(
                    """
                    <div style="background-color:#1abc9c;padding:20px;border-radius:12px;text-align:center;">
                        <h2 style="color:#006600;">🏆 Excellent Quality of Life</h2>
                        <p style="font-size:18px;">Great job! You're maintaining a very healthy and balanced lifestyle. Keep it up!</p>
                    </div>
                    """, unsafe_allow_html=True
                )

            
            
            # Personalized Recommendations
        recommendations = []


        # 1. Stress
        stress_score = input_data["DAILY_STRESS"]
        if stress_score >= 3 and stress_score <= 4:
            recommendations.append("⚠️ High stress level detected. Consider stress-reducing activities like deep breathing, journaling, or nature walks.")
        if stress_score >= 5:
            recommendations.append("🧠 Your stress level is very high. Seek support from a therapist or mental health professional.")

        # 2. Sleep
        sleep_score = input_data["SLEEP_HOURS"]
        if sleep_score < 4:
            recommendations.append("💤 You're likely sleep-deprived. Aim for at least 7–8 hours of quality sleep.")

        # 3. Fruits & Vegetables
        fruit_score = input_data["FRUITS_VEGGIES"]
        if fruit_score < 2:
            recommendations.append("🍎 Try to increase your intake of fruits and vegetables. They’re vital for energy and mood.")

        # 4. Physical Activity (Steps)
        steps_score = input_data["DAILY_STEPS"]
        if steps_score < 3:
            recommendations.append("🚶‍♂️ You're not walking much. Try to reach 6,000–10,000 steps per day for better health.")

        # 5. Meditation
        meditation_score = input_data["WEEKLY_MEDITATION"]
        if meditation_score < 2:
            recommendations.append("🧘 Consider meditating a few times a week. It can boost focus and emotional well-being.")

        # 6. Time for Passion
        passion_score = input_data["TIME_FOR_PASSION"]
        if passion_score < 3:
            recommendations.append("🎨 Try to spend more time on your hobbies or passions to enhance life satisfaction.")

        # 7. Social Interaction
        social_score = input_data["SOCIAL_NETWORK"]
        if social_score < 3:
            recommendations.append("👥 Low social interaction detected. Connecting with people can improve your happiness and health.")

        # 8. Core Circle (Close friends/family)
        core_circle_score = input_data["CORE_CIRCLE"]
        if core_circle_score < 2:
            recommendations.append("🤝 Building deeper connections with people can increase your emotional support network.")

        # 9. Supporting Others
        support_score = input_data["SUPPORTING_OTHERS"]
        if support_score < 2:
            recommendations.append("❤️ Helping others can give you purpose and boost your self-esteem. Try small acts of kindness.")

        # 10. Life Vision
        vision_score = input_data["LIVE_VISION"]
        if vision_score < 3:
            recommendations.append("🔭 Consider clarifying your life goals. A clear vision can provide direction and motivation.")

        # 11. To-Do Completion
        todo_score = input_data["TODO_COMPLETED"]
        if todo_score < 3:
            recommendations.append("📋 You might benefit from better planning or routine. Try setting smaller, achievable goals.")

        # 12. Achievements
        achievement_score = input_data["ACHIEVEMENT"]
        if achievement_score < 2:
            recommendations.append("🏅 Celebrate small wins and keep setting personal goals to build a sense of accomplishment.")

        # 13. Donation
        donation_score = input_data["DONATION"]
        if donation_score < 2:
            recommendations.append("💰 Donating time or money to causes you care about can give a sense of purpose and fulfillment.")

        # 14. BMI
        bmi_score = input_data["BMI_RANGE"]
        if bmi_score == 2:
            recommendations.append("⚖️ You may be in an overweight category. A balanced diet and regular exercise can help.")

        # 15. Lost Vacation
        vacation_score = input_data["LOST_VACATION"]
        if vacation_score > 5:
            recommendations.append("🌴 You're losing too many vacation days. Taking time off helps restore energy and mental clarity.")

        # 16. Shouting Frequency
        shout_score = input_data["DAILY_SHOUTING"]
        if shout_score > 5:
            recommendations.append("📣 Frequent shouting might indicate unresolved tension. Consider talking to someone or journaling.")

        # 17. Sufficient Income
        income_score = input_data["SUFFICIENT_INCOME"]
        if income_score == 2:
            recommendations.append("💸 Financial stress affects well-being. Look into budgeting or financial planning help.")

        # 18. Personal Awards
        award_score = input_data["PERSONAL_AWARDS"]
        if award_score < 2:
            recommendations.append("🏆 You might benefit from setting goals that lead to recognition or feedback for your efforts.")

        # 19. Flow (Immersed time)
        flow_score = input_data["FLOW"]
        if flow_score < 3:
            recommendations.append("🔄 Try finding activities where you lose track of time. 'Flow' moments are deeply fulfilling.")


        # Display Recommendations
        if recommendations:
            st.markdown("### 📝 Personalized Recommendations:")
            for r in recommendations:
                st.markdown(f"- {r}")
        
        
    # Footer
    st.divider()
    st.caption("© 2025 Good Health & Well-Being Prediction App | Built with ❤️ using Streamlit")

# =============================================================
# 3) WELL-BEING TIPS
# =============================================================
def show_wellbeing():
    st.markdown("""
        <div style='background-color: #FAF3E0; padding: 1.5rem; border-radius: 12px;'>
            <h1 style='color: #E2725B;'>Well-Being Tips Harian</h1>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    now = datetime.datetime.now().strftime("%H:%M • %d %b %Y")
    st.info(f"⏰ Sekarang: {now}")

    tips = [
        "Minum segelas air putih.",
        "Tarik napas dalam 5×.",
        "Jalan kaki 10 menit.",
        "Tulis 3 hal yang kamu syukuri.",
        "Dengarkan musik favorit.",
        "Matikan notifikasi 30 menit.",
        "Tidur cukup malam ini.",
    ]

    if st.button("🎲 Dapatkan Tips"):
        st.success(random.choice(tips))
    else:
        st.write("Klik tombol untuk mendapat tips.")

    st.markdown("---")
    st.subheader("📌 Pengingat Harian")
    team_cards = [
        {
            "number": "💧",
            "name": "Air"
        },
        {
            "number": "🍎",
            "name": "Gizi"
        },
        {
            "number": "💤",
            "name": "Istirahat"
        },
        {
            "number": "🧘",
            "name": "Me-time"
        }
    ]

    cols = st.columns(4)
    for idx, member in enumerate(team_cards):
        with cols[idx]:
            st.markdown(f"""
                <div style='background-color:#FAF3E0; padding:24px; border-radius:16px; box-shadow:0 4px 10px rgba(0,0,0,0.05); text-align:center;'>
                    <div style='background-color:#E2725B; color:white; font-weight:bold; font-size:18px; width:40px; height:40px; line-height:40px; border-radius:50%; margin:auto;'>{member["number"]}</div>
                    <div style='font-size:18px; font-weight:600; color:#4B3F2F; margin-top:10px;'>{member["name"]}</div>
                </div>
            """, unsafe_allow_html=True)

# =============================================================
#                 ROUTER (Pilih Halaman)
# =============================================================
if st.session_state.current_page == "🏠 Home":
    show_home()
elif st.session_state.current_page == "📊 EDA":
    show_eda()
elif st.session_state.current_page == "📈 Health Prediction":
    show_prediction()
elif st.session_state.current_page == "🌿 Well-Being Tips":
    show_wellbeing()