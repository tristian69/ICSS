from django.shortcuts import render
#f=open("static/한국전력공사_지역별 전기차 충전소 현황정보_20231231.csv", 'r', encoding='UTF-8')
f=open("static/경상남도_전기차 충전소 설치현황_20240314.csv", 'r', encoding='cp949')
l=[]
lines = f.readlines()
for line in lines:
    l.append(line.split(','))
    print(line)
    f.close()

    data = l[1:100]

# Create your views here.
def index(request):
    context={'data':data}
    return render(request, 'mapping/mapping_list.html', context)

def detail(request):
    context = {'data': data}
    return render(request, 'mapping/mapping_detail.html', context)