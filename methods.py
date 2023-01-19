import datetime
import glob
import json
import os
import shutil
import urllib

import fitz
import img2pdf
from pdf2image import convert_from_path
from PIL import Image


def delete_files():
    delete_directories=["download","file","images","pdf"]
    for directory in delete_directories:
        shutil.rmtree(directory)
        os.mkdir(directory)

def convert_pdf_to_combined_pdf():
    # pdf_to_image()
    # image_to_pdf()
    pdf_combine()

def pdf_combine():
    pdf_data = glob.glob('./pdf/*.pdf')
    if len(pdf_data) !=0:
        output_pdf = fitz.open(pdf_data[0])
        for i in range(1,len(pdf_data)):
            inserted_pdf = fitz.open(pdf_data[i])
            output_pdf.insert_pdf(inserted_pdf)
        output_pdf.save('./file/result.pdf')

def download_attachment_pdf(attachments:list):
    saved_pdf_num = sum(os.path.isfile(os.path.join("./pdf", name)) for name in os.listdir("./pdf"))
    for index,pdf in enumerate(attachments):
        url =pdf.url
        pdf_download(url, f"./pdf/{saved_pdf_num+index}.pdf")

def pdf_download(url, save_pass):
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, save_pass)

def shape_file_name(message_file_name):
    if message_file_name =="":
        return "result.pdf"
    if ".pdf" == message_file_name[-4:]:
        return message_file_name
    else:
        return message_file_name+".pdf"
def pdf_to_image():
    img_path = "./images"
    pdf_data = glob.glob('./download/*.pdf')
    for index,pdf in enumerate(pdf_data):
        convert_from_path(pdf,output_folder=img_path,fmt='png',output_file=index,single_file=False)

def image_to_pdf():
    png_data = glob.glob("./images/*.png")
    png_data.sort()
    for index,png in enumerate(png_data):
        img = Image.open(png)
        fx = 0.1
        fy = 0.1
        outsize = (img2pdf.mm_to_pt(round(img.width * fx)),img2pdf.mm_to_pt(round(img.height * fy)))
        layout_fun = img2pdf.get_layout_fun(outsize)
        output_path = f"./pdf/{index}.pdf"
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(png,layout_fun=layout_fun))

def save_append_flag(state):
    with open("./append_flag.json","w")as f:
        json.dump({"append":state,"time":str(datetime.datetime.now())},f)

def load_append_flag():
    with open("./append_flag.json","r") as f:
        state = json.load(f)
    return state

def is_time_passed(compare_time):
    now = datetime.datetime.now()
    format_compare_time = datetime.datetime.strptime(compare_time,"%Y-%m-%d %H:%M:%S.%f")
    return (now-format_compare_time).seconds>60

def check_time_passed(compare_time):
    if is_time_passed(compare_time):
        save_append_flag(False)
        delete_files()
        return False
    else:
        return True