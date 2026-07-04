from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "main_data.csv"

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#6C5CE7"
ACCENT = "#00CEC9"
WARNING = "#FF6B6B"
MUTED = "#A0A7B4"
BG_CARD = "#FFFFFF"
PLOTLY_TEMPLATE = "plotly_white"
CATEGORICAL_PALETTE = ["#6C5CE7", "#00CEC9", "#FDCB6E", "#FF6B6B", "#74B9FF", "#55EFC4"]

st.markdown(
    f"""
    <style>
    .main {{
        background-color: #F4F6FB;
    }}
    #MainMenu, footer {{visibility: hidden;}}
    h1, h2, h3 {{
        font-family: 'Segoe UI', sans-serif;
        color: #2D3436;
    }}
    div[data-testid="stMetric"] {{
        background-color: {BG_CARD};
        border-radius: 16px;
        padding: 18px 20px 12px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #EEF0F6;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {MUTED};
        font-weight: 600;
    }}
    div[data-testid="stMetricValue"] {{
        color: {PRIMARY};
    }}
    .section-card {{
        background-color: {BG_CARD};
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #EEF0F6;
    }}
    .section-title {{
        font-size: 20px;
        font-weight: 700;
        color: #2D3436;
        margin-bottom: 2px;
    }}
    .section-subtitle {{
        color: {MUTED};
        font-size: 14px;
        margin-bottom: 14px;
    }}
    .hero {{
        background: linear-gradient(120deg, {PRIMARY} 0%, #8E7CFF 100%);
        border-radius: 20px;
        padding: 30px 34px;
        color: white;
        margin-bottom: 24px;
    }}
    .hero h1 {{
        color: white;
        margin-bottom: 6px;
    }}
    .hero p {{
        color: rgba(255,255,255,0.9);
        font-size: 15px;
        margin-bottom: 0;
    }}
    .badge {{
        display: inline-block;
        background-color: rgba(255,255,255,0.18);
        border-radius: 999px;
        padding: 4px 14px;
        font-size: 12px;
        margin-top: 10px;
    }}
    section[data-testid="stSidebar"] {{
        background-color: #1E1B3A;
    }}
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] .stCaption {{
        color: #F4F6FB !important;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] *,
    section[data-testid="stSidebar"] div[data-baseweb="input"] *,
    section[data-testid="stSidebar"] div[data-baseweb="datepicker"] *,
    section[data-testid="stSidebar"] div[data-baseweb="popover"] * {{
        color: #2D3436 !important;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] input {{
        background-color: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    return df


main_data = load_data()

with st.sidebar:
    st.markdown("### 🛍️ E-Commerce Analytics")
    st.caption("Filter data untuk eksplorasi lebih lanjut")

    min_date = main_data["order_purchase_timestamp"].min().date()
    max_date = main_data["order_purchase_timestamp"].max().date()
    date_range = st.date_input(
        "Rentang Tanggal Pemesanan",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    state_options = ["Semua"] + sorted(main_data["customer_state"].dropna().unique().tolist())
    selected_state = st.selectbox("Negara Bagian (State) Pelanggan", state_options)

    category_options = ["Semua"] + sorted(main_data["product_category"].dropna().unique().tolist())
    selected_category = st.selectbox("Kategori Produk", category_options)

    st.markdown("---")
    st.caption("Dibuat dengan Streamlit + Plotly")

filtered_data = main_data[
    (main_data["order_purchase_timestamp"].dt.date >= start_date)
    & (main_data["order_purchase_timestamp"].dt.date <= end_date)
]
if selected_state != "Semua":
    filtered_data = filtered_data[filtered_data["customer_state"] == selected_state]
if selected_category != "Semua":
    filtered_data = filtered_data[filtered_data["product_category"] == selected_category]

st.markdown(
    """
    <div class="hero">
        <h1>Dashboard Analisis E-Commerce Public Dataset</h1>
        <p>Rangkuman tren pesanan, segmentasi pelanggan (RFM), dan performa pengiriman periode Januari 2017 - Agustus 2018.</p>
        <span class="badge">Data terupdate otomatis mengikuti filter di sidebar</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pesanan", f"{filtered_data['order_id'].nunique():,}")
col2.metric("Total Revenue (BRL)", f"{filtered_data['price'].sum():,.0f}")
col3.metric("Rata-Rata Pengiriman", f"{filtered_data['delivery_days'].mean():.1f} hari")
col4.metric("Rata-Rata Skor Ulasan", f"{filtered_data['review_score'].mean():.2f} / 5")

st.write("")

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">📈 Pertanyaan 1: Tren Pesanan & Kategori Produk Terlaris</div>
        <div class="section-subtitle">Bagaimana tren jumlah pesanan bulanan dan kategori mana yang menyumbang revenue terbesar?</div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["📊 Tren Pesanan Bulanan", "🏆 Top 10 Kategori Produk"])

with tab1:
    monthly_summary = filtered_data.groupby("order_month").agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("price", "sum"),
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly_summary["order_month"],
            y=monthly_summary["total_orders"],
            mode="lines+markers",
            line=dict(color=PRIMARY, width=3, shape="spline"),
            marker=dict(size=7, color=PRIMARY),
            fill="tozeroy",
            fillcolor="rgba(108,92,231,0.10)",
            hovertemplate="Bulan: %{x}<br>Pesanan: %{y:,}<extra></extra>",
        )
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title="Tren Jumlah Pesanan Bulanan",
        xaxis_title="Bulan",
        yaxis_title="Jumlah Pesanan",
        height=430,
        margin=dict(t=60, l=10, r=10, b=10),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    category_revenue = (
        filtered_data.groupby("product_category")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .rename(columns={"price": "total_revenue"})
        .sort_values("total_revenue")
    )
    colors = [ACCENT] * (len(category_revenue) - 1) + [PRIMARY]
    fig = go.Figure(
        go.Bar(
            x=category_revenue["total_revenue"],
            y=category_revenue["product_category"],
            orientation="h",
            marker_color=colors,
            hovertemplate="%{y}<br>Revenue: BRL %{x:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title="10 Kategori Produk dengan Revenue Tertinggi",
        xaxis_title="Total Revenue (BRL)",
        yaxis_title="",
        height=430,
        margin=dict(t=60, l=10, r=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">🎯 Pertanyaan 2: Segmentasi Pelanggan (RFM Analysis)</div>
        <div class="section-subtitle">Segmen pelanggan mana yang paling perlu diprioritaskan untuk kampanye retensi?</div>
    """,
    unsafe_allow_html=True,
)

snapshot_date = filtered_data["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm = filtered_data.groupby("customer_unique_id").agg(
    last_purchase_date=("order_purchase_timestamp", "max"),
    frequency=("order_id", "nunique"),
    monetary=("payment_value", "sum"),
).reset_index()
rfm["recency"] = (snapshot_date - rfm["last_purchase_date"]).dt.days

if len(rfm) >= 4:
    r_labels = range(4, 0, -1)
    score_labels = range(1, 5)
    rfm["r_score"] = pd.qcut(rfm["recency"], q=4, labels=r_labels, duplicates="drop").astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=4, labels=score_labels).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"], q=4, labels=score_labels, duplicates="drop").astype(int)

    def assign_segment(row):
        if row["r_score"] >= 3 and row["f_score"] >= 3 and row["m_score"] >= 3:
            return "Champions"
        elif row["r_score"] >= 3 and row["f_score"] <= 2:
            return "New / Promising"
        elif row["r_score"] <= 2 and row["f_score"] >= 3:
            return "At Risk"
        elif row["r_score"] <= 2 and row["f_score"] <= 2 and row["m_score"] <= 2:
            return "Hibernating / Lost"
        else:
            return "Need Attention"

    rfm["segment"] = rfm.apply(assign_segment, axis=1)
    segment_summary = rfm.groupby("segment").agg(
        jumlah_pelanggan=("customer_unique_id", "count"),
        total_monetary=("monetary", "sum"),
    ).reset_index()
    priority_segments = ["At Risk", "Need Attention"]

    col_a, col_b = st.columns(2)
    with col_a:
        order = segment_summary.sort_values("jumlah_pelanggan", ascending=False)
        colors = [WARNING if s in priority_segments else PRIMARY for s in order["segment"]]
        fig = go.Figure(
            go.Bar(
                x=order["segment"],
                y=order["jumlah_pelanggan"],
                marker_color=colors,
                hovertemplate="%{x}<br>Pelanggan: %{y:,}<extra></extra>",
            )
        )
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            title="Jumlah Pelanggan per Segmen",
            yaxis_title="Jumlah Pelanggan",
            height=380,
            margin=dict(t=60, l=10, r=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        order2 = segment_summary.sort_values("total_monetary", ascending=False)
        colors2 = [WARNING if s in priority_segments else PRIMARY for s in order2["segment"]]
        fig = go.Figure(
            go.Bar(
                x=order2["segment"],
                y=order2["total_monetary"],
                marker_color=colors2,
                hovertemplate="%{x}<br>Monetary: BRL %{y:,.0f}<extra></extra>",
            )
        )
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            title="Total Monetary per Segmen",
            yaxis_title="Total Monetary (BRL)",
            height=380,
            margin=dict(t=60, l=10, r=10, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info("🔴 Segmen **At Risk** dan **Need Attention** merupakan prioritas utama untuk kampanye retensi pelanggan.")
else:
    st.warning("Data terlalu sedikit pada filter ini untuk membentuk segmentasi RFM.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">🚚 Pertanyaan 3: Waktu Pengiriman vs Skor Ulasan per Negara Bagian</div>
        <div class="section-subtitle">Wilayah mana yang butuh perhatian logistik lebih, dan bagaimana dampaknya ke kepuasan pelanggan?</div>
    """,
    unsafe_allow_html=True,
)

state_summary = filtered_data.dropna(subset=["delivery_days"]).groupby("customer_state").agg(
    avg_delivery_days=("delivery_days", "mean"),
    avg_review_score=("review_score", "mean"),
    jumlah_pesanan=("order_id", "nunique"),
).reset_index()
state_summary = state_summary[state_summary["jumlah_pesanan"] >= 10].sort_values(
    "avg_delivery_days", ascending=False
)

col_c, col_d = st.columns(2)
with col_c:
    top_states = state_summary.head(10).sort_values("avg_delivery_days")
    colors3 = [WARNING] * 3 + [PRIMARY] * max(len(top_states) - 3, 0)
    colors3 = colors3[-len(top_states):]
    fig = go.Figure(
        go.Bar(
            x=top_states["avg_delivery_days"],
            y=top_states["customer_state"],
            orientation="h",
            marker_color=colors3,
            hovertemplate="%{y}<br>Rata-rata: %{x:.1f} hari<extra></extra>",
        )
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title="Rata-Rata Waktu Pengiriman Terlama per State",
        xaxis_title="Rata-Rata Waktu Pengiriman (hari)",
        height=420,
        margin=dict(t=60, l=10, r=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
with col_d:
    fig = px.scatter(
        state_summary,
        x="avg_delivery_days",
        y="avg_review_score",
        size="jumlah_pesanan",
        text="customer_state",
        color_discrete_sequence=[ACCENT],
        template=PLOTLY_TEMPLATE,
        labels={
            "avg_delivery_days": "Rata-Rata Waktu Pengiriman (hari)",
            "avg_review_score": "Rata-Rata Skor Ulasan",
        },
    )
    fig.update_traces(textposition="top center", marker=dict(opacity=0.75, line=dict(width=1, color="white")))
    fig.update_layout(
        title="Waktu Pengiriman vs Skor Ulasan per State",
        height=420,
        margin=dict(t=60, l=10, r=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.caption("Dashboard dibuat menggunakan Streamlit dan Plotly sebagai bagian dari Proyek Analisis Data E-Commerce Public Dataset.")