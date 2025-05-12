import streamlit as st
from src.invoicegenerator.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        print("LoadStreamlitUI initialized with config file.")

    def load_streamlit_ui(self):
        st.set_page_config(page_title= self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False

        with st.form("invoice_form"):
            product_name = st.text_input("Product Name")
            product_price = st.number_input("Price", min_value=0.0)
            product_amount = st.number_input("Amount", min_value=1)
            submitted = st.form_submit_button("Add Product")

            if submitted:
                if "products" not in st.session_state:
                    st.session_state.products = []
                st.session_state.products.append({
                    "name": product_name,
                    "price": product_price,
                    "amount": product_amount
                })
                st.success("Product added.")

        if "products" in st.session_state and st.session_state.products:
            st.subheader("🛒 Product List")
            total = 0
            for i, p in enumerate(st.session_state.products):
                line_total = p['price'] * p['amount']
                total += line_total
                st.write(f"{i+1}. {p['name']} - {p['amount']} x ₹{p['price']} = ₹{line_total:.2f}")

            st.markdown(f"### 🧮 Total: ₹{total:.2f}")

            if st.button("📄 Generate Invoice"):
                print("Generating invoice...")