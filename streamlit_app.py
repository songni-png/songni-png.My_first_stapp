import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import os
import glob

# 전국 시군구 출생률 데이터 불러오기
df_korea_birthrate = pd.read_csv('C:/Users/soyoe/OneDrive/jupyter/data/전국_시군구_출생아수__합계출산율_20241119114124.csv', header=3, encoding='utf-8')

df_korea_birthrate.head()  # 데이터 출력하기

# 필요한 열만 선택하기
df_korea_birthrate = df_korea_birthrate[['11 서울특별시', '0.552']]

# 열 이름 변경하기
df_korea_birthrate.columns = ['행정구', '출생률']

# 숫자를 제외하고 행정구 열의 값만 출력하기
df_korea_birthrate['행정구'] = df_korea_birthrate['행정구'].str.replace('\d+', '', regex=True)

# '행정구' 열의 공백 제거 및 데이터 타입 변환
df_korea_birthrate['행정구'] = df_korea_birthrate['행정구'].str.strip().astype(str)

# NaN 값 확인 및 처리
df_korea_birthrate['출생률'] = df_korea_birthrate['출생률'].fillna(0)

# 파일 경로 설정
folder_path = r"data/"
file_pattern = os.path.join(folder_path, "LARD_ADM_SECT_SGG_*.json")

# 모든 파일을 불러와 GeoDataFrame으로 합치기
file_list = glob.glob(file_pattern)
gdfs = [gpd.read_file(file) for file in file_list]
gdf_korea_sido = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

gdf_korea_sido

# 'SGG_NM' 열의 앞부분 단어 제거
gdf_korea_sido['행정구'] = gdf_korea_sido['SGG_NM'].str.split().str[1:].str.join(' ')

# 결과 확인
gdf_korea_sido.head()

# 좌표계 변경하기
korea_5179 = gdf_korea_sido.to_crs(epsg=5179, inplace=False)

korea_5179.plot(figsize=(10, 6))  # 데이터 plot하기

# 기본 지도 생성하기
korea_map = folium.Map(
    location=[37, 126],
    zoom_start=7,
    tiles='cartodbpositron'  # 타일 레이어
)

# 제목 추가하기
title = '전국 시군구 출생률'  # 타이틀
title_html = f'<h3 align="center" style="font-size:20px"><b>{title}</b></h3>'
korea_map.get_root().html.add_child(folium.Element(title_html))

# Choropleth map 그리기
folium.Choropleth(
    geo_data=gdf_korea_sido,  # GeoJSON 파일
    data=df_korea_birthrate,  # 데이터프레임
    columns=['행정구', '출생률'],  # 열
    key_on='feature.properties.행정구',  # key
    fill_color='BuPu',  # 색상 Blue-Purple
    fill_opacity=0.7,  # 투명도 조정
    line_opacity=0.3
).add_to(korea_map)

# Streamlit 앱 설정
st.title('전국 시군구 출생률')
st.markdown(title_html, unsafe_allow_html=True)

# Folium 지도 출력
folium_static(korea_map)

# 사이드바
st.header('🤖 사이드바')
st.sidebar.write('## 사이드바 텍스트')
st.sidebar.checkbox('체크박스 1')
st.sidebar.checkbox('체크박스 2')
st.sidebar.radio('라디오 버튼', ['radio 1', 'radio 2', 'radio 3'])
st.sidebar.selectbox('셀렉트박스', ['select 1', 'select 2', 'select 3'])

# 레이아웃: 컬럼
st.header('🤖 컬럼 레이아웃')
col_1, col_2, col_3 = st.columns([1,2,1]) # 컬럼 인스턴스 생성. 1:2:1 비율로 컬럼을 나눔

with col_1:
    st.write('## 1번 컬럼')
    st.checkbox('이것은 1번 컬럼에 속한 체크박스 1')
    st.checkbox('이것은 1번 컬럼에 속한 체크박스 2')

with col_2:
    st.write('## 2번 컬럼')
    st.radio('2번 컬럼의 라디오 버튼', ['radio 1', 'radio 2', 'radio 3'])  # 동일한 라디오 버튼을 생성할 수 없음
    # 사이드바에 이미 라디오 버튼이 생성되어 있기 때문에, 여기서는 라디오 버튼의 내용을 변경해야 오류가 발생하지 않음

col_3.write('## 3번 컬럼')
col_3.selectbox('3번 컬럼의 셀렉트박스', ['select 1', 'select 2', 'select 3'])
# 사이드바에 이미 셀렉트박스가 생성되어 있기 때문에, 여기서는 셀렉트박스의 내용을 변경해야 오류가 발생하지 않음

# 레이아웃: 탭
st.header('🤖 탭 레이아웃')
tab_1, tab_2, tab_3 = st.tabs(['탭A', '탭B', '탭C'])  # 탭 인스턴스 생성. 3개의 탭을 생성

with tab_1:
    st.write('## 탭A')
    st.write('이것은 탭A의 내용입니다.')

with tab_2:
    st.write('## 탭B')
    st.write('이것은 탭B의 내용입니다.')

tab_3.write('## 탭C')
tab_3.write('이것은 탭C의 내용입니다.')

# 사용자 입력
st.header('🤖 사용자 입력')

text = st.text_input('여기에 텍스트를 입력하세요') # 텍스트 입력은 입력된 값을 반환
st.write(f'입력된 텍스트: {text}')

number = st.number_input('여기에 숫자를 입력하세요') # 숫자 입력은 입력된 값을 반환
st.write(f'입력된 숫자: {number}')

check = st.checkbox('여기를 체크하세요') # 체크박스는 True/False 값을 반환
if check:
    st.write('체크되었습니다.')

radio = st.radio('여기에서 선택하세요', ['선택 1', '선택 2', '선택 3']) # 라디오 버튼은 선택된 값을 반환
st.write(radio+'가 선택되었습니다.')

select = st.selectbox('여기에서 선택하세요', ['선택 1', '선택 2', '선택 3']) # 셀렉트박스는 선택된 값을 반환
st.write(select+'가 선택되었습니다.')

slider = st.slider('여기에서 값을 선택하세요', 0, 100, 50) # 슬라이더는 선택된 값을 반환
st.write(f'현재의 값은 {slider} 입니다.')

multi = st.multiselect('여기에서 여러 값을 선택하세요', ['선택 1', '선택 2', '선택 3']) # 멀티셀렉트박스는 선택된 값을 리스트로 반환
st.write(f'{type(multi) = }, {multi}가 선택되었습니다.')

button = st.button('여기를 클릭하세요') # 버튼은 클릭 여부를 반환
if button:
    st.write('버튼이 클릭되었습니다.(일반 텍스트: st.write()')
    st.success('버튼이 클릭되었습니다.(메시지: st.success())')  # 성공 메시지 출력
    st.balloons() # 풍선 애니메이션 출력

# 캐싱
st.header('🤖 캐싱 적용')

import time

@st.cache_data
def long_running_function(param1):
    time.sleep(5)
    return param1*param1

start = time.time()
num_1 = st.number_input('입력한 숫자의 제곱을 계산합니다.') # 숫자 입력은 입력된 값을 반환
st.write(f'{num_1}의 제곱은 {long_running_function(num_1)} 입니다. 계산시간은 {time.time()-start:.2f}초 소요')


# 세션 상태
st.header('🤖 세션 상태')

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("session_state를 사용하지 않은 경우")
color1 = st.color_picker("Color1", "#FF0000")
st.divider() # 구분선
st.scatter_chart(df, x="x", y="y", color=color1)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("session_state를 사용한 경우")
color2 = st.color_picker("Color2", "#FF0000")
st.divider() # 구분선
st.scatter_chart(st.session_state.df, x="x", y="y", color=color2)
