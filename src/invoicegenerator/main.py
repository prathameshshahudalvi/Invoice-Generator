import streamlit as st
from src.invoicegenerator.ui.streamlitui.loadui import LoadStreamlitUI

def load_invoice_generator_app():
    print("Loading Invoice Generator App...")
    ui = LoadStreamlitUI()
    ui.load_streamlit_ui()