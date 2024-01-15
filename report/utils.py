from datetime import datetime
from re import sub
import decimal
import pytz

# from django.utils import timezone, dateformat
from io import BytesIO, StringIO
from datetime import date, time
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

local_timezone = pytz.timezone("America/Sao_Paulo")


class GeneratePDF:
    def __init__(self, title, headers, values):
        self.max_width = 750
        self.min_col_table = 50
        self.cols_width = []

        # resources
        self.title = title
        self.headers = headers
        self.values = values

        self.pdf_elements = None
        self.list_keys = []
        self.list_data = []
        self.output = BytesIO()
        self.filename = None
        # styles

        self.defaultFontSize = 7

        styles = getSampleStyleSheet()
        self.styleN = styles["BodyText"]
        self.styleN.alignment = TA_LEFT
        self.styleN.fontSize = self.defaultFontSize

        self.styleBH = styles["Normal"]
        self.styleBH.alignment = TA_CENTER
        self.styleBH.fontSize = self.defaultFontSize + 1
        self.horizontal = True 

    def generate_template(self):
        file_date = datetime.now().astimezone(local_timezone).date().strftime("%d%m%Y")
        file_time = datetime.now().astimezone(local_timezone).time().strftime("%H%M%S")
        self.filename = (
            "relatorios_entradas_{}_{}.pdf".format(file_date, file_time)
        )
        pattern = 0.1 * cm
        page_size = (A4[1], A4[0]) if self.horizontal else (A4[0], A4[0])
        # Cria documento
        doc = SimpleDocTemplate(
            self.output,
            rightMargin=pattern,
            leftMargin=pattern,
            topMargin=pattern,
            bottomMargin=pattern,
            pagesize=page_size,
        )
        doc.build(self.pdf_elements)
        self.output.seek(0)
        return self.output

    def header_report(self):
        # Titulo do PDF
        title_style = ParagraphStyle(
            "Normal",
            fontSize=self.defaultFontSize + 2,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=12,
            leading=10,
        )

        #logo = Image("images/logo_abastece.png", height=25, width=60)
        infos = Paragraph(
            "Relatório de {} exportado pelo sistema.<br />Relatório emitido em {} às {}".format(
                self.title,
                datetime.now().astimezone(local_timezone).strftime("%d/%m/%Y"),
                datetime.now().astimezone(local_timezone).strftime("%H:%M"),
            ),
            title_style,
        )

        table_style = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.white),
            ]
        )

        table_grid_style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (100, 0), "#FFFFFF"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )

        table = Table([[]], colWidths=[45, self.max_width - 85])

        table.setStyle(table_grid_style)
        table.setStyle(table_style)

        return table

    def generate_header(self):
        # header da tabela do relatorio
        try:
            for key in self.headers:
                item = (Paragraph(key.upper(), self.styleBH),)
                self.list_keys.append(item)
        except Exception as e:
            print("error header - {}".format(e))

    def get_format(self, value, value_format):
        if value_format != "":
            return str(value_format).format(value).replace(".", ",")

        if isinstance(value, (decimal.Decimal)):
            return "{:>-.16n}".format(value).replace(".", ",")

        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M")

        if isinstance(value, date):
            return value.strftime("%d/%m/%Y")

        if isinstance(value, time):
            return value.strftime("%H:%M")

        if isinstance(value, bool):
            return "sim" if value else "não"

        return value

    def generate_paragraph(self, v):
        prefix = "" if "prefix" not in v else v["prefix"]
        suffix = "" if "suffix" not in v else v["suffix"]

        try:
            custom_format = v["custom_format"]["pdf"]
        except Exception:
            custom_format = ""

        if v['value']:
            value = self.get_format(v["value"], custom_format)

        return (
            Paragraph(
                "{} {} {}".format(str(prefix), str(value), str(suffix)), self.styleBH
            )
            if v["value"] or isinstance(v["value"], bool)
            else None
        )

    def generate_columns(self):
        try:
            self.list_data.append(self.list_keys)
            for value in self.values:
                data = []
                for v in value:
                    field = self.generate_paragraph(v)
                    data.append(field)
                self.list_data.append(data)
        except Exception as e:
            print("error data - {}".format(e))

    def define_table_col_widths(self):
        col_tmp = self.cols_width

        # calcula as colunas com base nos caracteres
        for value in self.values:
            for idx, v in enumerate(value):
                size = len(str(v["value"]))
                try:
                    old_value = col_tmp[idx]
                    new_value = size
                    if old_value < new_value:
                        col_tmp[idx] = size
                except:
                    col_tmp.append(size)

        # define o coeficiente com base na largura maxima definida
        total = 0
        for v in col_tmp:
            total += v
        k = total * 100 / self.max_width

        diff = 0
        cols_discount = 0
        cols_resize = 0

        # aplica o coeficiente na largura das colunas e define o minimo que deve ter
        for idx, item in enumerate(col_tmp):
            col_width = int(item * 100 / k)
            if col_width >= self.min_col_table:
                col_tmp[idx] = col_width
                cols_discount += col_width
            else:
                col_tmp[idx] = self.min_col_table
                diff += self.min_col_table - col_width
                cols_resize += 1

        # recalcula descontando a diferença da operação anterior
        if diff:
            diff = int(diff * 100 / cols_discount)
            for idx, item in enumerate(col_tmp):
                if item > self.min_col_table:
                    col_tmp[idx] = int(item * (1 - diff / 100))

        self.cols_width = col_tmp

    def prepare_report_pdf(self):
        elements = []
        elements.append(self.header_report())

        self.generate_header()
        self.generate_columns()

        try:
            # TABLE
            self.define_table_col_widths()
            table = Table(self.list_data, colWidths=self.cols_width)

            # TABLE STYLE
            table_style = TableStyle(
                [
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, "#CCCCCC"),
                    ("BOX", (0, 0), (-1, -1), 0.25, "#CCCCCC"),
                ]
            )

            table_grid_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (100, 0), "#CCCCCC"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                ]
            )

            table.setStyle(table_grid_style)
            table.setStyle(table_style)

            elements.append(table)

        except Exception as e:
            print("error table style - {}".format(e))

        self.pdf_elements = elements

        return self.pdf_elements
