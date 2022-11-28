from cnocr import CnOcr
from pdf2image import convert_from_path
import os
import pandas as pd


def intercept():
    os.system('convert ./temp/page0.jpg -crop 165x44+193+167 ./temp/Machine_id.jpg')
    os.system('convert ./temp/page0.jpg -crop 636x42+290+238 ./temp/Purchaser_name.jpg')
    os.system('convert ./temp/page0.jpg -crop 636x45+290+266 ./temp/Purchaser_id.jpg')
    os.system('convert ./temp/page0.jpg -crop 333x42+1315+18 ./temp/Invoice_code.jpg')
    os.system('convert ./temp/page0.jpg -crop 333x42+1315+75 ./temp/Invoice_id.jpg')
    os.system('convert ./temp/page0.jpg -crop 333x42+1315+128 ./temp/Date.jpg')
    os.system('convert ./temp/page0.jpg -crop 395x256+65+440 ./temp/Commodity.jpg')
    os.system('convert ./temp/page0.jpg -crop 636x42+288+815 ./temp/Seller_name.jpg')
    os.system('convert ./temp/page0.jpg -crop 636x42+288+854 ./temp/Seller_id.jpg')
    os.system('convert ./temp/page0.jpg -crop 245x36+1088+710 ./temp/Amount_before_tax.jpg')
    os.system('convert ./temp/page0.jpg -crop 245x36+1399+710 ./temp/Tax.jpg')
    os.system('convert ./temp/page0.jpg -crop 310x53+1320+750 ./temp/Amount.jpg')


def obtain():
    ocr = CnOcr(det_model_name='naive_det')
    machine_id = ocr.ocr('./temp/Machine_id.jpg')[0]['text'].replace(" ", "")
    purchaser_name = ocr.ocr('./temp/Purchaser_name.jpg')[0]['text'].replace(" ", "")

    purchaser_id = ocr.ocr('./temp/Purchaser_id.jpg')
    if len(purchaser_id) == 0:
        purchaser_id = ''
    else:
        purchaser_id = purchaser_id[0]['text'].replace(" ", "")

    invoice_code = ocr.ocr('./temp/Invoice_code.jpg')[0]['text'].replace(" ", "").replace('O', '0')
    invoice_id = ocr.ocr('./temp/Invoice_id.jpg')[0]['text'].replace(" ", "").replace('O', '0')
    date = ocr.ocr('./temp/Date.jpg')[0]['text'].replace(" ", "").replace('O', '0')

    # Commodity
    out = ocr.ocr('./temp/Commodity.jpg')
    commodity = ''
    for i in range(len(out)):
        if i == 0:
            commodity = commodity + out[i]['text']
        else:
            commodity = commodity + '\n' + out[i]['text']

    seller_name = ocr.ocr('./temp/Seller_name.jpg')[0]['text']
    seller_id = ocr.ocr('./temp/Seller_id.jpg')[0]['text'].replace(" ", "")
    amount_before_tax = ocr.ocr('./temp/Amount_before_tax.jpg')[0]['text'].replace(" ", "")[1:].replace('O', '0')
    tax = ocr.ocr('./temp/Tax.jpg')[0]['text'].replace(" ", "")[1:].replace('O', '0')
    amount = ocr.ocr('./temp/Amount.jpg')[0]['text'].replace(" ", "")[1:].replace('O', '0')

    return [machine_id, purchaser_name, purchaser_id, invoice_code, invoice_id, date, commodity, seller_name, seller_id,
            amount_before_tax, tax, amount]


def convertpdf2img(filepath):
    os.system('mkdir -p temp')
    images = convert_from_path(filepath)
    for i in range(len(images)):
        images[i].save('./temp/page' + str(i) + '.jpg', 'jpeg')


if __name__ == '__main__':
    items = []
    pdffiles = [item for item in os.listdir('.') if 'pdf' in item.lower()]
    for i, pdffile in enumerate(pdffiles, 1):
        print(f'正在处理{i}/{len(pdffiles)}个发票')
        convertpdf2img(pdffile)
        intercept()
        item = obtain()
        print(item)
        items.append(item)

    df = pd.DataFrame(items, columns=['机器编号', '购买方名称', '购买方识别号', '发票代码', '发票号码', '开票日期', '商品名称', '销售方名称', '销售方识别号', '金额', '税额', '价税合计'])
    df.to_csv('发票.csv', encoding="utf_8_sig", index=False)

