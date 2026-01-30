import streamlit as st
import streamlit_option_menu as option_menu
from streamlit_authenticator import Authenticate
import yaml
import hashlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import requests
import os
from dotenv import load_dotenv
import plotly.figure_factory as ff

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #1E3A8A 100%);
        box-shadow: 0 5px 15px rgba(62, 130, 246, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Load config
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Config authentification
config_file = "config.yaml"
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin AZIIN",
            "password": hashlib.sha256("admin123".encode()).hexdigest()
        },
        "rh": {
            "name": "RH Manager",
            "password": hashlib.sha256("rh123".encode()).hexdigest()
        },
        "manager": {
            "name": "Team Manager",
            "password": hashlib.sha256("manager123".encode()).hexdigest()
        },
        "employee": {
            "name": "John Doe",
            "password": hashlib.sha256("employee123".encode()).hexdigest()
        }
    }
}

# Initialize authenticator
authenticator = Authenticate(
    credentials,
    config_file,
    "hr_dashboard",
    30
)


class HRDashboard:
    def __init__(self):
        self.api_client = APIClient(API_URL)
        self.user_role = None

    def login_page(self):
        """Page de connexion"""
        st.title("🔐 Connexion - AZIIN HR Dashboard")
        st.markdown("---")

        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")

            if submit:
                result = authenticator.login(username, password)
                if result:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = self.get_user_role(username)
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")

    def get_user_role(self, username):
        """Récupère le rôle utilisateur"""
        roles = {
            "admin": "admin",
            "rh": "rh",
            "manager": "manager",
            "employee": "employee"
        }
        return roles.get(username, "employee")

    def sidebar_navigation(self):
        """Navigation latérale professionnelle"""
        with st.sidebar:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h2 style='color: #1E3A8A; margin: 0;'>AZIIN</h2>
                <p style='color: #64748B; margin: 0;'>HR Dashboard</p>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.get("authenticated"):
                selected = option_menu.menu([
                    "🏠 Accueil",
                    "👥 Employés",
                    "💼 Recrutement",
                    "📅 Planning",
                    "📊 Analytics",
                    "⚙️ Administration"
                ],
                    menu_icon="cast",
                    default_index=0,
                    styles={
                        "container": {"padding": "0!important", "background": "#fafafa"},
                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                     "--hover-color": "#1E3A8A"},
                        "nav-link-selected": {"background": "linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)"},
                    })

                st.markdown("---")
                st.info(f"👤 {st.session_state['username']} ({st.session_state['role']})")
                if st.button("🚪 Déconnexion"):
                    authenticator.logout()
                    st.rerun()

    def kpi_cards(self):
        """Cartes KPI principales"""
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h3 style='margin: 0 0 0.5rem 0;'>Employés</h3>
                <h1 style='margin: 0; font-size: 2.5rem;'>247</h1>
                <p style='margin: 0.5rem 0 0 0;'>+12 ce mois</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h3 style='margin: 0 0 0.5rem 0;'>Candidatures</h3>
                <h1 style='margin: 0; font-size: 2.5rem;'>89</h1>
                <p style='margin: 0.5rem 0 0 0;'>+34% vs mois passé</p>
            </div>
            """, unsafe_allow_html=True)

        # Autres KPI...

    def main_dashboard(self):
        """Dashboard principal"""
        st.markdown("<h1 class='main-header'>🚀 Bienvenue dans votre Dashboard RH</h1>", unsafe_allow_html=True)

        self.kpi_cards()

        # Graphiques
        col1, col2 = st.columns(2)
        with col1:
            # Graphique d'évolution
            fig = px.line(pd.DataFrame({
                'date': pd.date_range('2025-01-01', periods=12, freq='M'),
                'candidatures': [23, 34, 45, 56, 67, 78, 89, 92, 87, 95, 102, 110]
            }), x='date', y='candidatures', title="Évolution candidatures")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Répartition départements
            fig = px.pie(values=[45, 32, 28, 25, 20], names=['IT', 'Finance', 'RH', 'Marketing', 'Ops'])
            st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(
        page_title="AZIIN HR Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    dashboard = HRDashboard()

    if not st.session_state.get("authenticated"):
        dashboard.login_page()
    else:
        dashboard.sidebar_navigation()

        # Pages
        if "page" not in st.session_state:
            st.session_state.page = "home"

        pages = {
            "🏠 Accueil": dashboard.main_dashboard,
            "👥 Employés": lambda: st.write("Module Employés - En développement"),
            "💼 Recrutement": lambda: st.write("Module Recrutement - En développement"),
            "📅 Planning": lambda: st.write("Module Planning - En développement"),
            "📊 Analytics": lambda: st.write("Module Analytics - En développement"),
            "⚙️ Administration": lambda: st.write("Module Administration - En développement")
        }

        # Appel de la page sélectionnée
        for page_name, page_func in pages.items():
            if st.session_state.get("selected_page") == page_name:
                page_func()


if __name__ == "__main__":
    main()
