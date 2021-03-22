from tika import parser
import re

parsed_pdf = parser.from_file(
    r"C:\Users\nikhils3\Downloads\All_LabelPlusInvoice.pdf")

data = parsed_pdf['content']
tracking_id = re.findall('Tracking ID:(\s+\w+)', data)
print(tracking_id)
