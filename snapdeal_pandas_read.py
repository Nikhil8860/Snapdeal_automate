import datetime
import pymysql.cursors
import pandas as pd
import os
import glob


class DB:
    user_id = None
    conn = None

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


def read_details():
    conn = pymysql.connect(host="13.233.239.105", user="root",
                           password='evanik@2019', database="evanik_erp_cronjobs")
    cursor = conn.cursor()
    query = """SELECT UserId,UserName,PASSWORD,channel_id,TYPE,sellerId,updatetime FROM
                    inv_userlist WHERE TYPE IN ('snapdeal') AND exp_date  > NOW() 
                    AND active ='1' ORDER BY priority DESC,UserId DESC"""
    cursor.execute(query)
    all_data = cursor.fetchall()
    conn.close()
    cursor.close()
    channel_id = []
    seller_id = []
    user_id = []
    for i in all_data:
        if str(i[0]) in os.listdir(r'F:\\SnapdealAutomate\\snapdeal'):
            user_id.append(i[0])
            channel_id.append(i[3])
            seller_id.append(i[5])
    return user_id, channel_id, seller_id


info = read_details()

for u, c, s in zip(info[0], info[1], info[2]):
    for name in glob.glob(f"F:\\SnapdealAutomate\\snapdeal\\{u}\\{c}" + "\\*.xlsx"):
        DB.user_id = u
        db.connect()
        df = pd.read_excel(r"C:\Users\nikhils3\Downloads\CompOrderReport_13_01_2021_12_00_04_070-440563970.xlsx",
                           sheet_name='ConsolidateReportOrders')
        df1 = df[df.index % 2 == 0]
        for i, v in df1.head().iterrows():
            order_date = v['ORDER DATE']
            invoice_date = v['INVOICE DATE']
            manifest_by_date = v['MANIFEST BY DATE']
            cancelled_on = v['CANCELLED ON']
            if not order_date:
                if manifest_by_date:
                    date = manifest_by_date
                elif cancelled_on:
                    order_date = cancelled_on
            reference_no = v['REFERENCE CODE']
            customer_name = v['BUYER NAME']
            total = v['SELLER INVOICE AMOUNT']
            grand_total = v['SELLER INVOICE AMOUNT']
            sale_status = v['CURRENT ORDER STATE']
            if v['RETURN INITIATED ON'] and str(v['RETURN INITIATED ON']) != 'NaT':
                return_initated_on = v['RETURN INITIATED ON']
                return_created_on = v['RETURN INITIATED ON']
            else:
                return_initated_on = ''
                return_created_on = ''

            dispute_created = ''

            staff_note = 'auto_' + str(datetime.datetime.now())
            invoice_number = v['INVOICE NUMBER']
            total_items = v['QTY']
            fsn = v['SUPC']
            product = v['PRODUCT NAME']
            order_type = v['FULLFILMENT MODE']
            order_id = v['SUBORDER CODE']
            order_item_id = v['SUBORDER CODE']
            sku_code = v['SKU CODE']
            buyer_name = v['BUYER NAME']
            address1 = v['DELIVERY ADDRESS']
            city = v['SHIPPING CITY']
            state = v['CUSTOMER STATE']
            pincode = v['CUSTOMER PINCODE']
            tracking_id = v['AWB NO']
            sgst_rate = v['SGST']
            igst_rate = v['IGST']
            cgst_rate = v['CGST']
            sellerId = s
            created_by = u
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
            val = (order_date, invoice_date, reference_no, customer_name, total, grand_total, sale_status,
                   return_initated_on, dispute_created, staff_note, invoice_number, total_items, fsn, product,
                   order_type, order_id, order_item_id, sku_code, buyer_name, address1, city, state, pincode,
                   tracking_id, sgst_rate, igst_rate, cgst_rate, sellerId, created_by,
                   order_date, invoice_date, reference_no, customer_name, total, grand_total, sale_status,
                   return_initated_on, dispute_created, staff_note, invoice_number, total_items, fsn, product,
                   order_type, order_id, order_item_id, sku_code, buyer_name, address1, city, state, pincode,
                   tracking_id, sgst_rate, igst_rate, cgst_rate, sellerId, created_by,)
            db.query(query, val)
