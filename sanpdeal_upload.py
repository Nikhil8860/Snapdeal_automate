import pymysql.cursors
import xlrd
import pandas as pd
import os
import glob
import shutil


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
    info = cursor.fetchall()
    conn.close()
    cursor.close()
    channel_id = []
    sellerId = []
    UserId = []
    for i in info:
        if str(i[0]) in os.listdir(r'F:\\SnapdealAutomate\\snapdeal'):
            UserId.append(i[0])
            channel_id.append(i[3])
            sellerId.append(i[5])
    return UserId, channel_id, sellerId


info = read_details()

for u, c, s in zip(info[0], info[1], info[2]):
    try:
        for name in glob.glob(f"F:\\SnapdealAutomate\\snapdeal\\{u}\\{c}" + "\\*.xlsx"):
            DB.user_id = u
            db.connect()
            book = xlrd.open_workbook(name)
            sheet_names = book.sheet_names()
            sheet = book.sheet_by_name("ConsolidateReportOrders")
            for r in range(1, sheet.nrows, 2):
                if (sheet.cell(r, 0).value):
                    try:
                        dat = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 0).value, 'D')
                    except ValueError:
                        dat = ''
                    try:
                        invoicedate = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 11).value, 'D')
                    except ValueError:
                        invoicedate = ''
                    try:
                        ManifestByDate = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 29).value,
                                                                                        'D')  # 2329
                    except ValueError:
                        ManifestByDate = ''
                    try:
                        cancelledon = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 33).value,
                                                                                     'D')  # 27 33
                    except ValueError:
                        cancelledon = ''
                    if dat == None:
                        if ManifestByDate != None:
                            date = ManifestByDate
                        elif cancelledon != None:
                            date = cancelledon
                    referenceno = sheet.cell(r, 2).value
                    customername = sheet.cell(r, 43).value
                    total = sheet.cell(r, 12).value
                    grand_total = sheet.cell(r, 12).value
                    sale_status = sheet.cell(r, 7).value
                    try:
                        ReturnInitatedOn = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 34).value,
                                                                                          'D')  # 2834
                    except ValueError:
                        ReturnInitatedOn = ''
                    if sheet.cell(r, 34).value:
                        try:
                            ReturnCreatedOn = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 34).value,
                                                                                             'D')  # 2834
                            DisputeCreated = pd.to_datetime('1899-12-30') + pd.to_timedelta(sheet.cell(r, 34).value,
                                                                                            'D')  # 28#34
                        except ValueError:
                            ReturnCreatedOn = ''
                            DisputeCreated = ''
                    else:
                        ReturnInitatedOn = 'NULL'
                        DisputeCreated = 'NULL'

                    staff_note = sheet.cell(r, 7).value
                    invoice_number = sheet.cell(r, 10).value
                    print("INVOICE NUMBER", invoice_number)
                    try:
                        total_items = sheet.cell(r, 60).value
                    except IndexError:
                        try:
                            pass
                            os.remove(f"F:\\snapdeal\\{u}")
                        except shutil.Error:
                            pass
                    FSN = sheet.cell(r, 6).value
                    Product = sheet.cell(r, 4).value
                    OrderType = sheet.cell(r, 28).value  # 22#28
                    OrderId = sheet.cell(r, 2).value
                    print(OrderId)
                    OrderItemID = sheet.cell(r, 2).value
                    SKUCode = sheet.cell(r, 5).value
                    BuyerName = sheet.cell(r, 43).value  # 37
                    Address1 = sheet.cell(r, 44).value  # 38
                    print(Address1, BuyerName, sep='---')
                    City = sheet.cell(r, 45).value  # 39
                    State = sheet.cell(r, 46).value  # 40
                    PinCode = sheet.cell(r, 47).value  # 41
                    TrackingID = sheet.cell(r, 1).value
                    sgst_rate = sheet.cell(r, 15).value
                    igst_rate = sheet.cell(r, 17).value
                    cgst_rate = sheet.cell(r, 16).value
                    sellerId = s
                    created_by = u
                    print(sellerId, created_by, sep='----')
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
                    val = (dat, invoicedate, referenceno, customername, total, grand_total, sale_status,
                           ReturnInitatedOn, DisputeCreated, staff_note, invoice_number, total_items, FSN, Product,
                           OrderType, OrderId, OrderItemID, SKUCode, BuyerName, Address1, City, State, PinCode,
                           TrackingID, sgst_rate, igst_rate, cgst_rate, sellerId, created_by,

                           dat, invoicedate, referenceno, customername, total, grand_total, sale_status,
                           ReturnInitatedOn, DisputeCreated, staff_note, invoice_number, total_items, FSN, Product,
                           OrderType, OrderId, OrderItemID, SKUCode, BuyerName, Address1, City, State, PinCode,
                           TrackingID, sgst_rate, igst_rate, cgst_rate, sellerId, created_by)

                    db.query(query, val)
            try:
                shutil.move(name, "F:\\completed")
            except shutil.Error:
                pass
    except FileNotFoundError as e:
        print(e)
    try:
        pass
    except shutil.Error:
        pass
print("bye bye byebye")

