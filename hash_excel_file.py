from xlrd import open_workbook
import pandas as pd
import hashlib
import hmac
import binascii
import os
import json
pd.options.mode.chained_assignment = None



# SHA-256 hashing method using siteID as hashing key
def hash_acc(num, length, sideID):
    try:
        siteID = str.encode(sideID)
        #md5 hash
        m = hmac.new(siteID, num, hashlib.sha256).digest()
        #convert to dec
        m = str(int(binascii.hexlify(m),16))
        #split till length
        m=m[:length]
        return m
    except Exception as e:
        print("Something went wrong hashing a value :(")
        return

# Reading config.json
def read_json(path):
    print("Reading:"+path)
    try:
        if os.path.exists(path):
            with open(path) as data_file:
                data= json.loads(data_file.read())
            return data
        else:
            print(path + " not found.")
            return
    except Exception as e:
        print("Something went wrong reading config.json :(")
        return

if __name__ == '__main__':
    # Getting data from config.json
    master_dict=read_json("./config.json")
    siteID = master_dict['siteID']
    hashing_length = master_dict['hashing_length']
    path_file = master_dict['input_path']
    columns_to_hash = master_dict['column_to_hash']

    # Reading excel file
    df = pd.read_excel(path_file)

    # Hashing for each column specified in config.json
    try:
        for column in columns_to_hash:
            print("Hashing column " + column + "...")
            rows_value = df.get(column)
            for row in range(len(rows_value)):
                print("Hashind row number " + str(row))
                rows_value[row] = hash_acc(rows_value[row].encode('utf-8'), hashing_length, siteID)

        df.to_excel("output.xlsx")
        print("Hashing completed successfully")
    except Exception as e:
        print("Something went wrong hashing :(")
        print(e)
