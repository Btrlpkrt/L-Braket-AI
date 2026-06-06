import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(
    page_title="L Braket AI Tasarım Aracı",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f7f8fb 0%, #eef1f6 100%);
    }
    .main-title {
        font-size: 2.15rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: .25rem;
    }
    .sub-title {
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .section-title {
        color: #0B1F3A;
        font-size: 1.55rem;
        font-weight: 800;
        margin: 0.35rem 0 0.9rem 0;
    }
    .result-card {
        background: white;
        padding: 1.35rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 24px rgba(17, 24, 39, .07);
        min-height: 145px;
    }
    .result-label {
        color: #6b7280;
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: .05em;
    }
    .result-value {
        color: #111827;
        font-size: 2rem;
        font-weight: 800;
        margin-top: .55rem;
    }
    .result-note {
        color: #9ca3af;
        font-size: .78rem;
        margin-top: .35rem;
    }
    .info-box {
        background: #eff6ff;
        color: #1e3a8a;
        padding: 1rem 1.1rem;
        border-radius: 14px;
        border: 1px solid #bfdbfe;
    }
    div[data-testid="stSidebar"] {
        background: #111827;
    }
    div[data-testid="stSidebar"] * {
        color: white;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary * {
        color: #000000 !important;
    }

    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"],
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] * {
        color: #000000 !important;
    }

    .footer-text {
        color: #000000;
        font-size: 0.85rem;
        margin-top: 1rem;
    }


    .author-name {
        width: 100%;
        text-align: right;
        color: #0B1F3A;
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        padding-right: 0.2rem;
    }

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("L_Braket_Temiz_Veriler.csv")


@st.cache_resource
def train_models(data):
    X = data[["L1", "L2", "t", "d"]]

    stress_model = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        min_samples_leaf=1
    )

    displacement_model = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        min_samples_leaf=1
    )

    stress_model.fit(X, data["Stress"])
    displacement_model.fit(X, data["Displacement"])

    return stress_model, displacement_model


df = load_data()
stress_model, displacement_model = train_models(df)

with st.sidebar:
    st.markdown("## Tasarım Parametreleri")
    st.caption("Değerleri değiştirerek yeni bir L braket tasarımı oluşturun.")

    l1 = st.slider(
        "L1 uzunluğu (mm)",
        float(df["L1"].min()),
        float(df["L1"].max()),
        80.0,
        1.0
    )

    l2 = st.slider(
        "L2 uzunluğu (mm)",
        float(df["L2"].min()),
        float(df["L2"].max()),
        60.0,
        1.0
    )

    thickness = st.slider(
        "Et kalınlığı t (mm)",
        float(df["t"].min()),
        float(df["t"].max()),
        8.0,
        0.5
    )

    diameter = st.slider(
        "Delik çapı d (mm)",
        float(df["d"].min()),
        float(df["d"].max()),
        18.0,
        0.5
    )

    st.markdown("---")
    st.info("Uygulanan yük: 100 N (sabit)")
    st.caption(
        "Model yalnızca eğitim verisinin ölçü aralıklarında ve 100 N yük koşulunda kullanılmalıdır."
    )

new_design = pd.DataFrame([{
    "L1": l1,
    "L2": l2,
    "t": thickness,
    "d": diameter,
}])

pred_stress = float(stress_model.predict(new_design)[0])
pred_disp = float(displacement_model.predict(new_design)[0])

stress_percentile = float((df["Stress"] <= pred_stress).mean() * 100)
disp_percentile = float((df["Displacement"] <= pred_disp).mean() * 100)

st.markdown(
    '<div class="author-name">BİLGİSAYAR DESTEKLİ TASARIMDA PROGRAMLAMA TEKNİKLERİ FİNAL PROJESİ - BATURALP</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🔩 L Braket AI Tasarım Aracı</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">100 N sabit yük altında geometrik ölçülerden stress ve displacement tahmini yapan etkileşimli makine öğrenmesi uygulaması</div>',
    unsafe_allow_html=True
)

top_left, top_right = st.columns([1.05, 1.45], gap="large")

with top_left:
    st.markdown(
        '<div class="section-title">Seçilen tasarım</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(0, 130)
    ax.set_ylim(0, 110)
    ax.axis("off")

    x0, y0 = 25, 20
    horizontal = min(90, 35 + l1 * 0.45)
    vertical = min(80, 25 + l2 * 0.50)
    visual_t = max(7, thickness * 1.4)

    ax.plot(
        [x0, x0 + horizontal],
        [y0, y0],
        linewidth=visual_t,
        solid_capstyle="round",
        color="#1f77b4",
        zorder=1
    )

    ax.plot(
        [x0, x0],
        [y0, y0 + vertical],
        linewidth=visual_t,
        solid_capstyle="round",
        color="#ff7f0e",
        zorder=1
    )

    hole_x = x0 + horizontal * 0.72
    hole_y = y0

    # Delik çapı arttıkça iki siyah çizgi arasındaki mesafe orantılı büyür.
    d_min = float(df["d"].min())
    d_max = float(df["d"].max())

    if d_max > d_min:
        diameter_ratio = (diameter - d_min) / (d_max - d_min)
    else:
        diameter_ratio = 0.5

    min_hole_gap = 1.8
    max_hole_gap = 6.0
    hole_gap = min_hole_gap + diameter_ratio * (max_hole_gap - min_hole_gap)

    hole_half = max(6, diameter * 0.22)

    # Siyah çizgiler mavi çizginin dışına taşmaz.
    max_half = visual_t * 0.42
    hole_half = min(hole_half, max_half)

    white_rect = Rectangle(
        (hole_x - hole_gap, hole_y - hole_half),
        2 * hole_gap,
        2 * hole_half,
        facecolor="white",
        edgecolor="none",
        zorder=5
    )
    ax.add_patch(white_rect)

    ax.plot(
        [hole_x - hole_gap, hole_x - hole_gap],
        [hole_y - hole_half, hole_y + hole_half],
        color="black",
        linewidth=1.8,
        zorder=6
    )

    ax.plot(
        [hole_x + hole_gap, hole_x + hole_gap],
        [hole_y - hole_half, hole_y + hole_half],
        color="black",
        linewidth=1.8,
        zorder=6
    )

    ax.annotate(
        f"L1 = {l1:.0f} mm",
        xy=(x0 + horizontal / 2, y0 - 13),
        ha="center",
        fontsize=11
    )

    ax.annotate(
        f"L2 = {l2:.0f} mm",
        xy=(x0 - 13, y0 + vertical / 2),
        va="center",
        ha="center",
        rotation=90,
        fontsize=11
    )

    ax.text(
        hole_x,
        hole_y + hole_half + 9,
        f"Ø {diameter:.1f} mm",
        va="bottom",
        ha="center",
        fontsize=10
    )

    ax.set_title(f"Et kalınlığı: {thickness:.1f} mm", fontsize=12, pad=12)

    st.pyplot(fig, use_container_width=True)

with top_right:
    st.markdown(
        '<div class="section-title">Yapay zekâ tahmini</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">TAHMİNİ STRESS</div>
            <div class="result-value">{pred_stress:.4f}</div>
            <div class="result-note">100 N yük altında Random Forest tahmini</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">TAHMİNİ DISPLACEMENT</div>
            <div class="result-value">{pred_disp:.4f}</div>
            <div class="result-note">100 N yük altında Random Forest tahmini</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
        Bu tasarımın tahmini stress değeri veri setindeki örneklerin yaklaşık
        <b>%{stress_percentile:.0f}</b>'inden; displacement değeri ise yaklaşık
        <b>%{disp_percentile:.0f}</b>'inden daha yüksektir.
        Bu karşılaştırma yalnızca mevcut veri setine ve 100 N yük koşuluna göredir.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    '<div class="section-title">Tasarım karşılaştırması</div>',
    unsafe_allow_html=True
)

nearest = df.copy()
nearest["Uzaklık"] = (
    ((nearest["L1"] - l1) / max(df["L1"].max() - df["L1"].min(), 1)) ** 2
    + ((nearest["L2"] - l2) / max(df["L2"].max() - df["L2"].min(), 1)) ** 2
    + ((nearest["t"] - thickness) / max(df["t"].max() - df["t"].min(), 1)) ** 2
    + ((nearest["d"] - diameter) / max(df["d"].max() - df["d"].min(), 1)) ** 2
) ** 0.5

nearest = nearest.nsmallest(5, "Uzaklık")[
    ["L1", "L2", "t", "d", "Stress", "Displacement"]
]

st.dataframe(nearest, use_container_width=True, hide_index=True)

chart_df = pd.DataFrame({
    "Sonuç": ["Stress", "Displacement"],
    "Tahmin": [pred_stress, pred_disp],
    "Veri ortalaması": [df["Stress"].mean(), df["Displacement"].mean()],
}).set_index("Sonuç")

st.bar_chart(chart_df)

with st.expander("Projenin çalışma mantığı"):
    st.write(
        """
        Model; L1, L2, et kalınlığı ve delik çapını giriş olarak alır.
        Tüm eğitim verileri 100 N sabit yük altında elde edilmiştir.
        Model, bu verilerdeki örüntüleri öğrenerek yeni bir L braket tasarımı için
        stress ve displacement değerlerini tahmin eder.
        Bu uygulama yalnızca 100 N yük altındaki hızlı ön değerlendirme içindir;
        nihai mühendislik doğrulaması için sonlu elemanlar analizi kullanılmalıdır.
        """
    )

st.markdown(
    """
    <div class="footer-text">
        Yüksek lisans final projesi — 100 N Yük Altında Makine Öğrenmesi ile
        L Braket Performans Tahmini
    </div>
    """,
    unsafe_allow_html=True
)
