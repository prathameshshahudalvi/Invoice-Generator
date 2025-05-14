from fpdf import FPDF
from io import BytesIO
import streamlit as st

class generate_pdf:
    def __init__(self, invoice_data):
        self.invoice_data = invoice_data
    
    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        pdf.add_font("DejaVuSans", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVuSans", size=12)

        for _, p in enumerate(st.session_state.products):
            if isinstance(p, tuple):
                p = {"name": p[0], "price": p[1], "amount": p[2]}
            line_total = p['price'] * p['amount']
            pdf.cell(0, 10, f"{p['name']} - {p['amount']} x ₹{p['price']} = ₹{line_total:.2f}", ln=True)


        # Convert to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        buffer = BytesIO(pdf_bytes)

        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="invoice.pdf",
            mime="application/pdf"
        )