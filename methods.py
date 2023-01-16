import glob
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
    pdf_to_image()
    image_to_pdf()
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
    for index,pdf in enumerate(attachments):
        url =pdf.url
        pdf_download(url, f"./pdf/{index}.pdf")

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

convert_pdf_to_combined_pdf()
