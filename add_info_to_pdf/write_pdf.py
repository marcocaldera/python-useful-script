from PyPDF4 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
# can.drawString(10, 100, "Hello world a")
can.drawString(135, 707, "Marco Caldera")  # nome e cognome
can.drawString(361, 707, "Torino")  # nato a
can.drawString(455, 707, "11/12/1993")  # il

can.drawString(80, 672, "10138")  # cap
can.drawString(316, 637, "CLDMRC93T11L219S")  # codice fiscale
can.save()

# move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)

# read your existing PDF
existing_pdf = PdfFileReader(open("ISCRIZIONE.pdf", "rb"))
output = PdfFileWriter()

# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)

# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()
