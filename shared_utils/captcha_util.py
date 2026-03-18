# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2024/7/4 11:13
desc:
'''

def get_captcha(captcha_img_ele):
    #captcha_img_ele.screenshot('capcha.png')
    img_bytes = captcha_img_ele.screenshot_as_png # 把图片转成字节流数据

    import ddddocr
    ocr = ddddocr.DdddOcr()
    # 调用classification方法，传一个字节流的图片信息，解析里面的文字
    text = ocr.classification(img_bytes)
    print(text)
    return text

import pytesseract
import cv2

# def get_captcha(img):
#     #img = cv2.imread('test.jpg')
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     retval, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
#     blur = cv2.GaussianBlur(threshold, (5,5), 0)
#     contours, hierarchy = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     count = 0
#     for contour in contours:
#         (x,y,w,h) = cv2.boundingRect(contour)
#         if w > 10 and h > 10:
#             roi = blur[y:y+h, x:x+w]
#             cv2.imwrite(str(count)+'.jpg', roi)
#             text = pytesseract.image_to_string(roi, lang='eng')
#             print("*************text: %s************************"%text)
#             count += 1
#     # cv2.imshow('Image', img)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
