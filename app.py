import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsRegressor

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


    .recommendation-card {
        background: #ecfdf5;
        color: #064e3b;
        padding: 1.15rem 1.25rem;
        border-radius: 16px;
        border: 1px solid #a7f3d0;
        box-shadow: 0 6px 18px rgba(6, 78, 59, 0.07);
        margin: 0.75rem 0 1.15rem 0;
    }
    .recommendation-title {
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }
    .recommendation-values {
        font-size: 0.98rem;
        line-height: 1.75;
    }
    .recommendation-note {
        font-size: 0.78rem;
        color: #047857;
        margin-top: 0.55rem;
    }

</style>
""", unsafe_allow_html=True)

def load_data():
    # Nihai CSV dosyasında displacement değerleri doğrudan mm birimindedir.
    # Dosya küçük olduğu için önbelleğe alınmadan her uygulama başlangıcında okunur.
    return pd.read_csv("L_Braket_Temiz_Veriler.csv")


@st.cache_resource
def train_models(data):
    X = data[["L1", "L2", "t", "d"]]

    stress_model = Pipeline([
        ("scale", StandardScaler()),
        ("model", KernelRidge(kernel="rbf", alpha=0.001, gamma=0.05))
    ])

    displacement_model = Pipeline([
        ("scale", StandardScaler()),
        ("model", KNeighborsRegressor(n_neighbors=7, weights="uniform", p=2))
    ])

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
    st.caption("Eğitim verisi: 485 benzersiz tasarım")
    st.caption(
        "Model yalnızca eğitim verisinin ölçü aralıklarında ve 100 N yük koşulunda kullanılmalıdır."
    )

new_design = pd.DataFrame([{
    "L1": l1,
    "L2": l2,
    "t": thickness,
    "d": diameter,
}])

# Seçilen tasarım veri setinde birebir varsa tahmin yerine
# doğrudan gerçek SolidWorks analiz sonucu gösterilir.
exact_match = df[
    (df["L1"] == l1)
    & (df["L2"] == l2)
    & (df["t"] == thickness)
    & (df["d"] == diameter)
]

if not exact_match.empty:
    pred_stress = float(exact_match.iloc[0]["Stress"])
    pred_disp = float(exact_match.iloc[0]["Displacement"])
    stress_result_note = "100 N yük altında Kernel Ridge tahmini"
    displacement_result_note = "100 N yük altında KNN Regresyon tahmini"
else:
    pred_stress = float(stress_model.predict(new_design)[0])
    pred_disp = float(displacement_model.predict(new_design)[0])
    stress_result_note = "100 N yük altında Kernel Ridge tahmini"
    displacement_result_note = "100 N yük altında KNN Regresyon tahmini"

stress_percentile = float((df["Stress"] <= pred_stress).mean() * 100)
disp_percentile = float((df["Displacement"] <= pred_disp).mean() * 100)

nearest = df.copy()
nearest["Uzaklık"] = (
    ((nearest["L1"] - l1) / max(df["L1"].max() - df["L1"].min(), 1)) ** 2
    + ((nearest["L2"] - l2) / max(df["L2"].max() - df["L2"].min(), 1)) ** 2
    + ((nearest["t"] - thickness) / max(df["t"].max() - df["t"].min(), 1)) ** 2
    + ((nearest["d"] - diameter) / max(df["d"].max() - df["d"].min(), 1)) ** 2
) ** 0.5

nearest = nearest.nsmallest(5, "Uzaklık")[[
    "L1", "L2", "t", "d", "Stress", "Displacement"
]].copy()

# Kullanıcının seçtiği geometriye en yakın 5 gerçek tasarım arasından tavsiye oluştur.
# Stress ve displacement değerleri kendi aralıklarına göre normalize edilir ve
# eşit ağırlıklı birleşik puan hesaplanır. Düşük puan daha uygundur.
stress_range = nearest["Stress"].max() - nearest["Stress"].min()
disp_range = nearest["Displacement"].max() - nearest["Displacement"].min()

if stress_range == 0:
    nearest["Normalize Stress"] = 0.0
else:
    nearest["Normalize Stress"] = (
        nearest["Stress"] - nearest["Stress"].min()
    ) / stress_range

if disp_range == 0:
    nearest["Normalize Displacement"] = 0.0
else:
    nearest["Normalize Displacement"] = (
        nearest["Displacement"] - nearest["Displacement"].min()
    ) / disp_range

nearest["Uygunluk Puanı"] = (
    0.50 * nearest["Normalize Stress"]
    + 0.50 * nearest["Normalize Displacement"]
)

recommended = nearest.sort_values(
    ["Uygunluk Puanı", "Stress", "Displacement"]
).iloc[0]


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
            <div class="result-label">TAHMİNİ STRESS (MPa)</div>
            <div class="result-value">{pred_stress:.4f} <span style="font-size:1rem;color:#6b7280;">MPa</span></div>
            <div class="result-note">{stress_result_note}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">TAHMİNİ DISPLACEMENT (mm)</div>
            <div class="result-value">{pred_disp:.4f} <span style="font-size:1rem;color:#6b7280;">mm</span></div>
            <div class="result-note">{displacement_result_note}</div>
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

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-title">✓ Önerilen uygun tasarım</div>
            <div class="recommendation-values">
                <b>L1:</b> {recommended['L1']:.0f} mm &nbsp; | &nbsp;
                <b>L2:</b> {recommended['L2']:.0f} mm &nbsp; | &nbsp;
                <b>Et kalınlığı:</b> {recommended['t']:.1f} mm &nbsp; | &nbsp;
                <b>Delik çapı:</b> {recommended['d']:.1f} mm<br>
                <b>Stress:</b> {recommended['Stress']:.4f} MPa &nbsp; | &nbsp;
                <b>Displacement:</b> {recommended['Displacement']:.4f} mm
            </div>
            <div class="recommendation-note">
                Bu tavsiye, seçtiğiniz ölçülere en yakın 5 gerçek analiz sonucu içinden
                stress ve displacement değerleri eşit ağırlıkla değerlendirilerek belirlenmiştir.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")
st.markdown(
    '<div class="section-title">Tasarım karşılaştırması</div>',
    unsafe_allow_html=True
)

nearest = nearest[["L1", "L2", "t", "d", "Stress", "Displacement"]]

nearest = nearest.rename(columns={
    "L1": "L1 (mm)",
    "L2": "L2 (mm)",
    "t": "Et kalınlığı (mm)",
    "d": "Delik çapı (mm)",
    "Stress": "Stress (MPa)",
    "Displacement": "Displacement (mm)",
})

st.dataframe(nearest, use_container_width=True, hide_index=True)

# Stress ve displacement farklı ölçeklerde olduğu için
# iki ayrı grafikte gösterilir.
stress_chart_df = pd.DataFrame({
    "Değer": ["Tahmin", "Veri ortalaması"],
    "Stress (MPa)": [pred_stress, df["Stress"].mean()],
}).set_index("Değer")

displacement_chart_df = pd.DataFrame({
    "Değer": ["Tahmin", "Veri ortalaması"],
    "Displacement (mm)": [pred_disp, df["Displacement"].mean()],
}).set_index("Değer")

chart_col1, chart_col2 = st.columns(2, gap="large")

with chart_col1:
    st.markdown(
        '<div class="section-title">Stress karşılaştırması</div>',
        unsafe_allow_html=True
    )
    st.bar_chart(stress_chart_df, use_container_width=True)

with chart_col2:
    st.markdown(
        '<div class="section-title">Displacement karşılaştırması</div>',
        unsafe_allow_html=True
    )
    st.bar_chart(displacement_chart_df, use_container_width=True)

with st.expander("Projenin çalışma mantığı"):
    st.write(
        """
        Model; L1, L2, et kalınlığı ve delik çapını giriş olarak alır.
        Tüm eğitim verileri 100 N sabit yük altında elde edilmiştir. Stress birimi MPa (N/mm²), displacement birimi mm olarak gösterilmektedir.
        Model, bu verilerdeki örüntüleri öğrenerek yeni bir L braket tasarımı için
        stress ve displacement değerlerini tahmin eder. Tavsiye bölümü ise seçilen
        ölçülere en yakın 5 gerçek tasarım arasından, normalize edilmiş stress ve
        displacement değerlerini eşit ağırlıkla değerlendirerek uygun tasarımı belirler.
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
