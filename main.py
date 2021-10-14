from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import inch
from tkinter import *
from tkinter import filedialog

#white (opaque) rectangle, covers the text on existing PDF file
def drawRect():
    buffer = BytesIO()

    p = canvas.Canvas(buffer, pagesize=A6)
    p.setStrokeColorRGB(255, 255, 255)
    p.setFillColorRGB(255, 255, 255, 1)
    p.rect(.1*inch, 3.7*inch, 3.7*inch, .25*inch, fill=1)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

newPdf = PdfFileReader(drawRect())

rectOverlay = drawRect().getvalue()
open('pdf1.pdf','wb').write(rectOverlay)


def openFile():
    filePath = filedialog.askopenfilename(initialdir="", title="Select a file", filetypes=[("PDF files", "*.pdf")])
    # theFile = Label(window, text=filePath).grid(row=8, column=0)

    existingPdf = PdfFileReader(open(filePath, 'rb'))
    return existingPdf


def stampExistingFile():
    theFile = openFile()
    numPages = theFile.getNumPages()
    output = PdfFileWriter()

    for page in range(numPages):
        pdf_page = theFile.getPage(page)
        pdf_page.mergePage(newPdf.getPage(0))
        output.addPage(pdf_page)
    return output

def run():
    outputStream = open('output.pdf', 'wb')
    stampExistingFile().write(outputStream)
    outputStream.close()


window = Tk()
window.title("Welcome to PDF Stamper")

selectFile = Button(window, text="Select a File to Stamp", command=run).grid(row=2, column=0)



window.mainloop()


#pyinstaller --onefile stamp.py
#run to make executable
