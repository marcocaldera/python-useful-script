import pandas as pd
from PyPDF4 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pgeocode
import time
import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
nomi = pgeocode.Nominatim('IT')

if not os.path.exists('assets/other'):
    os.makedirs('assets/other')
if not os.path.exists('assets/cfto'):
    os.makedirs('assets/cfto')

username_list = pd.read_csv('info.csv', dtype={'Numero civico': object, 'CAP': object})
username_list.drop_duplicates(subset="Email", keep=False, inplace=True)
for index, user in username_list.iterrows():
    box = ''.join(c.lower() for c in user["Box di provenienza"] if not c.isspace())
    print(user["Cognome"].lower() + user["Nome"], box)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Vera', 11)

    # Io sottoscritto
    can.drawString(95, 770, "{} {}".format(
        user["Nome"].title(),
        user["Cognome"].title()))

    # Nato a
    if len(user["Nato a"]) > 15:
        can.setFont('Vera', 8)
    can.drawString(312, 770, user["Nato a"].capitalize())
    can.setFont('Vera', 11)

    # il
    date = pd.to_datetime(user["Data di nascita"]).strftime("%d/%m/%Y")
    can.drawString(438, 770, date)

    # residente in

    can.drawString(80, 752, user["Residente a"].capitalize())

    # # address
    # address = nomi.query_postal_code(user["CAP"])
    # can.drawString(435, 683, address["county_code"])
    #
    # cap
    can.drawString(44, 734, user["CAP"])

    # via
    can.drawString(260, 752, user["Indirizzo"].capitalize())

    # n°
    can.drawString(509, 752, user["Numero civico"])

    # e-mail
    can.drawString(280, 734, user["Email"].lower())

    # codice fiscale
    can.drawString(85, 716, user["Codice Fiscale"].upper())

    can.drawString(50, 295, "01/02/2020")
    can.drawString(50, 571, "01/02/2020")
    can.drawString(50, 59, "01/02/2020")

    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf_1 = PdfFileReader(packet)

    ## FINE PAGINA 1

    # packet_2 = io.BytesIO()
    # can_2 = canvas.Canvas(packet_2, pagesize=letter)
    # can_2.setFont('Vera', 11)
    # can_2.drawString(180, 141, "01/02/2020")
    # can_2.drawString(85, 141, "Torino")
    #
    # can_2.drawString(180, 209, user["Cognome"].capitalize())
    # can_2.drawString(350, 209, user["Nome"].capitalize())
    #
    # can_2.save()
    #
    # packet_2.seek(0)
    # new_pdf_2 = PdfFileReader(packet_2)

    # read your existing PDF
    existing_pdf = PdfFileReader(open("./assets/partecip.pdf", "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page_1
    page_1 = existing_pdf.getPage(0)
    page_1.mergePage(new_pdf_1.getPage(0))
    output.addPage(page_1)

    # page_2 = existing_pdf.getPage(1)
    # page_2.mergePage(new_pdf_2.getPage(0))
    # output.addPage(page_2)

    # output.addPage(existing_pdf.getPage(1))

    # finally, write "output" to a real file

    right_folder = "other/" if box != "crossfittorino" else "cfto/"
    outputStream = open(
        "assets/" + right_folder +
        user["Cognome"].replace(" ", "").lower() +
        user["Nome"].replace(" ", "") + ".pdf",
        "wb")
    output.write(outputStream)
    outputStream.close()

    # break
