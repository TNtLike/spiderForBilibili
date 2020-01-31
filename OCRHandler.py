import pytesseract
from PIL import Image
import cv2

'''
本地安装tesseract
系统环境变量path添加C:\Program Files (x86)\Tesseract-OCR
pip install pytesseract
pip install opencv-python
调用tesseract的python库pytesseract
下载中文库chi_sim
实现图片中的文字识别
对于复杂图片的处理,例如海报类图片或模糊的图片
需要先对图片进行灰度处理噪点处理等手段后再进行图像文字识别
测试用例说明:
1.jpg-英文图片
2.jpg-数字图片
3.jpg-手写数字
3.png-中文图片
'''

img_path = 'img\\3.png'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
# 使用opencv
img = cv2.imread(img_path)
text1 = pytesseract.image_to_string(Image.fromarray(img))

# 不使用opencv
text2 = pytesseract.image_to_string(Image.open(img_path), lang='chi_sim')

print(text1)
print(text2)
