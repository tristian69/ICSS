from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'iils/question_list.html', context)
    #return HttpResponse("통합정보연계시스템 Test Site #1")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'iils/question_detail.html', context)


@api_view(('POST',))
def uploadExcelDataToTargetTag(request):
    try:
        # 포스트요청으로 들어온 엑셀파일을 받아온다.
        excel_file = request.FILES['excelFile']

        filename, fileExtension = os.path.splitext(str(excel_file))
        # 파일확장자를 통해 엑셀파일이 맞는지 체크해준다
        if fileExtension != ".xlsx":
            return Response("Unavailable file extension")

        else:
            df = pd.read_excel(excel_file, usecols='C:CU')
            time_array = pd.read_excel(excel_file, usecols='D:CU').columns.to_numpy()

            bulk_list = []

            for row in df.itertuples():
                date = row[1].replace('.', '-')  # timestamp 포멧 변경
                values = row[2:]  # 00:15 ~ 24:00 까지의 values
                timestamp = ""
                for i, d in enumerate(list(values)):
                    if isinstance(d, (int, float)):
                        timestamp = f"{date} {time_array[i]}"

                        bulk_list.append(Data(
                            timestamp=timestamp,
                            value=d
                        ))

            Data.objects.bulk_create(bulk_list, batch_size=250)
            return Response("Data Uploaded")

    except Exception as e:
        print(e)
        return Response('Data Upload Failed')


@api_view(('POST',))
def downloadExcelData(request):
    start_date = request.data['start_date']  # 시작날짜
    end_date = request.data['end_date']  # 끝난 날짜

    datas = Data.objects.filter(timestamp__range=[start_date, end_date])
    columns = ['고객번호', '계기번호', '날짜', '00:00', '00:15', '00:30', '00:45', '01:00', '01:15', '01:30', '01:45', '02:00',
               '02:15', '02:30', '02:45', '03:00', '03:15', '03:30', '03:45', '04:00', '04:15', '04:30', '04:45',
               '05:00', '05:15', '05:30', '05:45', '06:00', '06:15', '06:30', '06:45', '07:00', '07:15', '07:30',
               '07:45', '08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15',
               '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', '11:00', '12:00', '12:15', '12:30', '12:45',
               '13:00', '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30',
               '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45', '18:00', '18:15',
               '18:30', '18:45', '19:00', '19:15', '19:30', '19:45', '20:00', '20:15', '20:30', '20:45', '21:00',
               '21:15', '21:30', '21:45', '22:00', '22:15', '22:30', '22:45', '23:00', '23:15', '23:30', '23:45',
               '합계(kWh)']  # 칼럼 우선 생성해주기,,,노가다,,,ㅎㅎ,,,
    dates = []  # 인스턴스에서 날짜만 저장해주기
    for r in raw_datas:
        date, hour = str(r.timestamp).split(' ')  # 타임스탬프에 날짜와 시간이 모두 있기 때문에 나눠주기
        if date in dates:  # 중복이면 패스
            pass
        else:
            dates.append(date)

    excel_data = [[" " for j in range(len(columns))] for i in range(len(dates))]

    for i in len(dates):
        excel_data[i][2] = dates[i]  # 날짜만 우선 넣어주기

    for data in datas:
        date, hour = str(raw_data.timestamp).split(' ')
        hour = hour[:5]  # 시간만 추출해주기
        for j, column in enumerate(columns): 해당
        시간에
        데이터
        저장해주기
        if hour == column:
            excel_data[dates.index(date)][j] = data.value


result = 0
for x in range(len(excel_data)):
    for y in range(3, len(excel_data[x])):
        if excel_data[x][y] != ' ':
            result += excel_data[x][y]
    excel_data[x][100] = result  # 00:00~23:45분까지 데이터들의 합 저장해주기
df = pd.DataFrame(data, columns=columns)
df.to_excel('sample.xlsx', index=False)
return Response("Data Download")

