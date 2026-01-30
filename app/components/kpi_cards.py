import streamlit as st
import plotly.graph_objects as go

def kpi_card(title: str, value: str, trend: str, icon: str = "📈"):
    """Carte KPI professionnelle"""
    col = st.container()
    with col:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        ">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{icon}</div>
            <h3 style="margin: 0 0 1rem 0; font-size: 1.1rem; opacity: 0.9;">{title}</h3>
            <h1 style="margin: 0 0 0.5rem 0; font-size: 2.5rem; font-weight: 700;">{value}</h1>
            <p style="margin: 0; font-size: 0.95rem; opacity: 0.8;">{trend}</p>
        </div>
        """, unsafe_allow_html=True)
