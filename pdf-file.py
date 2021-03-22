from tika import parser
import re


def get_list_id():
    quantity = []
    parsed_pdf = parser.from_file(
        r"C:\Users\nikhils3\Downloads\Flipkart-PickList-P111120-1E4FFA74E42B-11-Nov-2020-07-13.pdf")

    data = parsed_pdf['content'].split('LID / WID')[1]

    pick_list_id = parsed_pdf['content'].split('LID / WID')[0].split('Pick List')[0].strip()

    for i in parsed_pdf['content'].split('Content')[0].strip().splitlines():
        if re.match(r'^\d{1,2}$', i):
            quantity.append(i)

    info = re.findall(r"[A-Z]{7,}\d+\w+", data)
    print(pick_list_id)
    for i, v in enumerate(quantity):
        for _ in range(int(v)):
            print(info[i])
        print("--------------------------")


def get_courier_no():
    parsed_pdf_courier = parser.from_file(
        r"C:\Users\nikhils3\Downloads\All_LabelPlusInvoice.pdf")
    courier_data = parsed_pdf_courier['content']
    courier_no = [i.strip() for i in re.findall(r'Courier AWB No:(\s+\w+)', courier_data)]
    print(courier_no)


if __name__ == '__main__':
    get_list_id()
    get_courier_no()
