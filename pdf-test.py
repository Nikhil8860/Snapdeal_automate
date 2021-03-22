import PyPDF2
pdf_file = open(r"C:\Users\nikhils3\Downloads\Flipkart-PickList-P100820-8D2B2ADE7FD9-09-Nov-2020-05-28.pdf", 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
print(page_content.encode('utf-8'))
