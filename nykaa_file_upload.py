import pymysql.cursors
from datetime import datetime
import csv


class DB:
    user_id = 77492

    def connect(self):
        self.conn = pymysql.connect('13.233.239.105', 'root', 'evanik@2019', f'invento_{DB.user_id}')

    def query(self, sql, val):
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql, val)
            except Exception as e:
                print(e)
            self.conn.commit()
            print(cursor.rowcount, "record(s) affected")
        except (AttributeError, pymysql.err.InterfaceError, pymysql.OperationalError, pymysql.err.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            try:
                cursor.execute(sql, val)
            except Exception as e:
                print(e)
            self.conn.commit()
            print(cursor.rowcount, "record(s) affected Success")
        return cursor


db = DB()


def processing_file():
    db.connect()
    name = r'C:\Users\nikhils3\Downloads\sample_order_sheet.csv'
    with open(name) as f:
        csv_reader = csv.reader(f, delimiter=',')
        csv_reader.__next__()
        for row in csv_reader:
            order_id = row[0]
            order_date = datetime.strptime(row[1], '%d-%b-%y')
            channel = row[2]
            status = row[3]
            payment = row[4]
            on_hold = row[5]
            product = row[6]
            channel_created_at = row[7]
            display_order = row[8]
            customer_name = row[9]
            customer_email = row[10]
            customer_mobile = row[11]
            address_line_1 = row[12]
            address_line_2 = row[13]
            address_city = row[14]
            address_state = row[15]
            address_pincode = row[16]
            pymt = row[17]
            currency_code = row[18]
            order_price = row[19]
            seller_skus = row[20]
            fulfillment_type = row[21]
            order_priority = row[22]
            payment_status = row[23]
            qty = row[24]
            invoice_no = row[25]
            invoice_date = datetime.strptime(row[26], '%d-%b-%y')
            gst_no = row[27]
            query = """
                INSERT INTO sales (date, invoice_date, reference_no, customer, total, grand_total, 
                sale_status, ReturnCreatedOn, DisputeCreated, staff_note, invoice_number, total_items,
                FSN, Product, OrderType, OrderId, OrderItemID, SKUCode, BuyerName, Address1, City, 
                State, PinCode, TrackingID, sgst_rate, igst_rate, cgst_rate, sellerId, created_by) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                date=%s, invoice_date=%s, reference_no=%s, customer=%s, total=%s, grand_total=%s, 
                sale_status=%s, ReturnCreatedOn=%s, DisputeCreated=%s, staff_note=%s, invoice_number=%s, 
                total_items=%s, FSN=%s, Product=%s, OrderType=%s, OrderId=%s, OrderItemID=%s, SKUCode=%s, 
                BuyerName=%s, Address1=%s, City=%s, State=%s, PinCode=%s, TrackingID=%s, sgst_rate=%s, 
                igst_rate=%s, cgst_rate=%s, sellerId=%s, created_by=%s
            """
            val = (order_date, invoice_date, order_id, customer_name, order_price, '', payment_status,
                   '', '', '', invoice_no, qty, '', product, '', order_id, display_order, seller_skus,
                   customer_name, address_line_1, address_city, address_state, address_pincode, '', gst_no,
                   '', '', 'Nykaa', order_id,
                   order_date, invoice_date, order_id, customer_name, order_price, '', payment_status,
                   '', '', '', invoice_no, qty, '', product, '', order_id, display_order, seller_skus,
                   customer_name, address_line_1, address_city, address_state, address_pincode, '', gst_no,
                   '', '', 'Nykaa', order_id)
            print(val)
            db.query(query, val)


if __name__ == '__main__':
    processing_file()
