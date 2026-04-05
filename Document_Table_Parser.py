import pdfplumber
import pandas as pd


class PDFTableExtractor:
    @staticmethod
    def extract(file_path):
        all_tables = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        df_page = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df_page)
            return (
                pd.concat(all_tables, ignore_index=True)
                if all_tables
                else pd.DataFrame()
            )
        except Exception as e:
            print(f"❌ Error en PDF: {e}")
            return pd.DataFrame()
