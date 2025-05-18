import streamlit as st
from src.invoicegenerator.ui.uiconfigfile import Config
from src.invoicegenerator.generatepdf.generate_pdf import generate_pdf
from src.invoicegenerator.googlesheet.add_in_googlesheet import AddInGoogleSheet
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")  # <-- Move this to the top

        # Sidebar for credentials and spreadsheet key
        st.sidebar.header("Google Sheets Credentials")
        credentials_file = st.sidebar.file_uploader("Upload credentials.json", type=["json"])
        spreadsheet_key = st.sidebar.text_input("Spreadsheet Key")

        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False

        # Company and client information
        company_name = st.text_input("Company Name", "Your Company")
        company_slogan = st.text_input("Slogan", "Your slogan here")
        company_info = st.text_area("Company Address and Contact", "123 Street\nCity, ZIP\nPhone | Fax\nEmail | Website")

        client_name = st.text_input("Client Name", "Client Co.")
        client_info = st.text_area("Client Address and Contact", "Client Street\nCity, ZIP\nPhone | Email")

        invoice_no = st.text_input("Invoice #", "INV-001")
        invoice_date = st.date_input("Date", datetime.today())
        project_desc = st.text_input("Project Description", "Project XYZ")
        po_number = st.text_input("P.O. #", "PO123")

        # Editable table
        st.subheader("Invoice Items")
        items = []
        for i in range(1, 8):  # 7 rows
            col1, col2 = st.columns([3, 1])
            with col1:
                desc = st.text_input(f"Description {i}", f"Item {i}")
            with col2:
                try:
                    amount = float(st.text_input(f"Amount {i}", "0.00"))
                except:
                    amount = 0.0
            items.append((desc, amount))

        total = sum(amount for _, amount in items)

        # Generate PDF function
        def create_invoice():
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=LETTER)
            width, height = LETTER

            y = height - 50
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, company_name)

            c.setFont("Helvetica-Oblique", 10)
            c.drawString(50, y - 20, company_slogan)

            c.setFont("Helvetica", 10)
            for i, line in enumerate(company_info.split("\n")):
                c.drawString(50, y - 40 - i*12, line)

            # Invoice details
            c.setFont("Helvetica-Bold", 10)
            c.drawString(400, y - 10, "INVOICE")
            c.setFont("Helvetica", 10)
            c.drawString(400, y - 30, f"INVOICE #: {invoice_no}")
            c.drawString(400, y - 45, f"DATE: {invoice_date.strftime('%Y-%m-%d')}")
            c.drawString(400, y - 60, f"FOR: {project_desc}")
            c.drawString(400, y - 75, f"P.O. #: {po_number}")

            # Client info
            c.setFont("Helvetica", 10)
            c.drawString(50, y - 100, "TO:")
            for i, line in enumerate(client_info.split("\n")):
                c.drawString(70, y - 115 - i*12, line)

            # Table
            table_y = y - 200
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, table_y, "Description")
            c.drawString(450, table_y, "Amount")
            c.line(50, table_y - 2, 550, table_y - 2)

            c.setFont("Helvetica", 10)
            for i, (desc, amount) in enumerate(items):
                if amount == 0:
                    continue
                c.drawString(50, table_y - 20 * (i+1), desc)
                c.drawRightString(540, table_y - 20 * (i+1), f"Rs {amount:.2f}")

            # Total
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, table_y - 20 * (len(items)+1), "Total")
            c.drawRightString(540, table_y - 20 * (len(items)+1), f"Rs {total:.2f}")
            c.line(50, table_y - 20 * (len(items)+1) - 2, 550, table_y - 20 * (len(items)+1) - 2)

            # Footer
            c.setFont("Helvetica", 9)
            c.drawString(50, 100, f"Make all checks payable to {company_name}")
            c.drawString(50, 85, "Payment is due within 30 days.")
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(50, 65, "If you have any questions concerning this invoice, contact [Name] | [Phone] | [Email]")
            c.setFont("Helvetica-Bold", 9)
            c.drawString(200, 45, "Thank you for your business!")

            c.showPage()
            c.save()
            buffer.seek(0)
            return buffer

        # Download button
        if st.button("Generate PDF Invoice"):
            pdf = create_invoice()
            st.download_button("📥 Download Invoice PDF", data=pdf, file_name="invoice.pdf", mime="application/pdf")

            # Google Sheets integration
            if credentials_file and spreadsheet_key:
                google_sheet = AddInGoogleSheet(credentials_file, spreadsheet_key)
                metadata = [invoice_no, invoice_date.strftime('%Y-%m-%d')]
                google_sheet.add_invoice_row(items, total, metadata)