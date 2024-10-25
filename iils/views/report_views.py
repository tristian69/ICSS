from django.shortcuts import render, get_object_or_404
from openpyxl import Workbook
from io import BytesIO
import pandas as pd

# Create your views here.
wb = Workbook()  # 엑셀 생성
ws = wb.active	# 엑셀 활성화
excelfile = BytesIO() #바이트 배열 생성

ws.title = "제품분류표준" # 엑셀 a1 열 이름 정하기
ws['A1']= '제품명'

wb.save("제품분류표준.xlsx")

wb.close()
