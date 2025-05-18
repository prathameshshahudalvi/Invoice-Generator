from fpdf import FPDF
from io import BytesIO
import streamlit as st
import os

class generate_pdf:
    def __init__(self, invoice_data):
        self.invoice_data = invoice_data

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()

        try:
            pdf.add_font("DejaVuSans", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVuSans", "", 12)
        except:
            pdf.set_font("Arial", size=12)

        # Add invoice lines
        for p in self.invoice_data:
            if isinstance(p, tuple):
                p = {"name": p[0], "price": p[1], "amount": p[2]}
            line_total = p["price"] * p["amount"]
            pdf.cell(0, 10, f"{p['name']} - {p['amount']} x ₹{p['price']} = ₹{line_total:.2f}", ln=True)

        # Output to BytesIO directly
        pdf_bytes = pdf.output(dest='S').encode('latin-1') if isinstance(pdf.output(dest='S'), str) else pdf.output(dest='S')
        buffer = BytesIO(pdf_bytes)
        buffer.seek(0)

        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="invoice.pdf",
            mime="application/pdf"
        )
