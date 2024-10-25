from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.template import loader

from IPython.display import display

from . import views
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'

# Create your views here.

# 전기차 현황정보 파일 불러오기
    # file_path2 = '한국전력공사_지역별 전기차 현황정보_20231231.csv'
    # file_path3 = '한국전력공사_지역별 전기차 충전소 현황정보_20230718.csv'

    with open('한국전력공사_지역별 전기차 현황정보.csv', 'r', encoding='cp949') as file1:
        df1 = pd.read_csv(file1)  # csv.reader 객체 생성
        for row in df1:
            print(row)
    with open('한국전력공사_지역별 전기차 현황정보_20240731.csv', 'r', encoding='UTF-8') as file2:
        df2 = pd.read_csv(file2)  # csv.reader 객체 생성
        for row in df2:
            print(row)
    with open('한국전력공사_지역별 전기차 충전소 현황정보_20231231.csv', 'r', encoding='UTF-8') as file3:
        station = pd.read_csv(file3)  # csv.reader 객체 생성
        for row in station:
            print(row)

    # 상위 2개행씩 출력하기
    print("df1:", df1.head(2))
    print("----------" * 10)
    print("df2:", df2.head(2))
    print("----------" * 10)
    print("station:", station.head(2))

    # df1과 df2의 2022년 1월부터 3월까지의 데이터 출력하기
    print(df1.loc[[2, 1, 0], '기준일':'경기'])
    print(df2.loc[0:2, '기준일':'경기'])

    # df1에서 중복된 데이터 제거하기
    df1.drop([0, 1, 2], axis=0, inplace=True)
    print(df1.loc[0:5, '기준일':'경기'])

    # df1과 df2 병합하기
    ev = pd.concat([df1, df2])

    # option_context()로 처음과 끝 행/열을 각각 4개씩 출력하여 병합 결과를 확인
    with pd.option_context('display.max_rows', 8, 'display.max_columns', 8):
        pd.set_option("show_dimensions", False)
        display(ev)

    # ev의 '기준일'열을 기준으로 오름차순 정렬하고 인덱스 재설정하기
    ev = ev.sort_values(by='기준일', ascending=True, ignore_index=True)

    with pd.option_context('display.max_rows', 8, 'display.max_columns', 8):
        pd.set_option("show_dimensions", False)
        display(ev)

    # info() 메서드로 '기준일' 열의 데이터 타입 확인하기
    ev.info()

    # '기준일' 열의 데이터 타입을 datetime 객체로 로 변환하고 월 단위로 포맷 변경
    ev['기준일'] = pd.to_datetime(ev['기준일']).dt.to_period('M')
    ev.head()

    # 데이터프레임 station의 행과 열 방향 전환
    station = station.set_index('지역').T

    # 열 이름 그룹의 레이블(columns.name) 제거
    station.columns.name = None
    # 행 인덱스(연도 데이터)에 '연도'로 인덱스 레이블 부여
    station.index.name = '연도'

    # 정수 인덱스 재설정
    station.reset_index(inplace=True)

    # 데이터프레임 ev와 station의 열 이름을 출력하여 지역명 확인하기
    print("ev:", ev.columns)
    print("station:", station.columns)

    # ev의 '합계' 열을 삭제
    ev.drop('합계', axis=1, inplace=True)

    # '기준일' 열의 이름을 '연도'로 변경
    ev.rename(columns={'기준일': '연도'}, inplace=True)

    # 원래의 열 순서 저장
    original_columns = ev.columns.tolist()

    # 열 이름을 오름차순으로 정렬
    sorted_columns = sorted(ev.columns)
    # 정렬된 열 이름으로 데이터프레임의 열 순서 변경
    ev = ev[sorted_columns]

    ev.head()

    # station의 열 이름을 오름차순으로 정렬
    sorted_columns2 = sorted(station.columns)
    # 정렬된 열 이름으로 데이터프레임의 열 순서 변경
    station = station[sorted_columns2]

    station.head()

    # ev 의 열 이름으로 station의 열 이름에 덮어쓰기
    station.columns = ev.columns
    station.head()

    # station도 동일한 순서로 재정렬
    station = station[original_columns]
    station.head(2)

    # iloc[]를 이용해 두 데이터프레임의 '연도'열의 처음과 마지막 데이터 출력하기
    print("ev 시작: ", ev.iloc[0, 0], "/ ev 마지막: ", ev.iloc[-1, 0])
    print("station 시작: ", station.iloc[0, 0], "/ station 마지막: ", station.iloc[-1, 0])

    # station의 2016~2018 데이터 삭제 후 인덱스 재설정
    station = station.drop([0, 1, 2]).reset_index(drop=True)

    # 연도별로 그룹화한 후 각 그룹의 마지막 행 추출
    ev_final = ev.groupby(ev['연도'].dt.year).tail(1)
    ev_final.reset_index(drop=True, inplace=True)  # 인덱스 재설정

    # '연도'열의 형식을 '연-월'에서 '연도'로 변환
    ev_final['연도'] = ev_final['연도'].dt.year

    # ev_final 데이터 타입 확인
    ev_final.info()

    # station의 데이터 타입 확인
    station.info()

    # station의 '연도'열의 데이터 타입을 int64로 변환
    station['연도'] = station['연도'].astype('int64')
    station.info()

    # ev_final에서 2022년 데이터 행 삭제
    ev_final = ev_final[ev_final['연도'] != 2022]
    ev_final.reset_index(drop=True, inplace=True)

    # 가장 최근 연도 선택 (2023년)
    recent_year = 2023
    recent_ev = ev_final[ev_final['연도'] == recent_year].drop('연도', axis=1)
    recent_station = station[station['연도'] == recent_year].drop('연도', axis=1)

    # 전기차 수 대비 충전소 수 비율 계산
    ratio_2023 = recent_ev.iloc[0] / recent_station.iloc[0]

    # 전기차 수 대비 충전소 수 비율  시각화
    plt.figure(figsize=(10, 6))
    ratio_2023.plot(kind='bar', color='teal')
    plt.title(f'{recent_year}년 지역별 전기차 수 대비 충전소 수 비율')
    plt.xlabel('지역')
    plt.ylabel('전기차 1대 당 충전소 수')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig("ev_st_ratio.png")
    plt.show()
    #plt.savefig(f'/static/images/{recent_year}년 지역별 전기차 수 대비 충전소 수 비율.png')
    plt.cla()  # clear the current axes
    plt.clf()  # clear the current figure
    plt.close() # closes the current figure

    # '연도'를 데이터프레임 인덱스로 설정
    ev_final.set_index('연도', inplace=True)
    station.set_index('연도', inplace=True)

    # 서울 지역 데이터 선택
    seoul_ev = ev_final['서울']
    seoul_stations = station['서울']

    # 연도별 증가율 계산
    seoul_ev_growth = seoul_ev.pct_change() * 100  # 전기차 성장률 (백분율)
    seoul_station_growth = seoul_stations.pct_change() * 100  # 충전소 성장률 (백분율)

    print("서울의 연도별 전기차 성장률")
    print(seoul_ev_growth)
    print("----------------------------------")
    print("서울의 연도별 전기차 충전소 성장률")
    print(seoul_station_growth)

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.plot(seoul_ev_growth.index, seoul_ev_growth, label='전기차 성장률', marker='o', linestyle='-')
    plt.plot(seoul_station_growth.index, seoul_station_growth, label='충전소 확장 속도', marker='o', linestyle='--')
    plt.title('서울 지역 연도별 전기차 및 충전소 성장률 비교')
    plt.xlabel('연도')
    plt.ylabel('성장률 (%)')
    plt.legend()
    plt.xticks(seoul_ev_growth.index)  # 연도를 x축 레이블로 표시
    plt.grid(True)
    plt.savefig("sst_compare.png")
    plt.show()
    #plt.savefig('/static/images/서울 지역 연도별 전기차 및 충전소 성장률 비교.png', dpi=300)
    plt.cla()  # clear the current axes
    plt.clf()  # clear the current figure
    plt.close()  # closes the current figure
