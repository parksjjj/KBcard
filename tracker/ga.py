import pandas as pd
from setting.directory import *
from setting.report_date import *
from setting.spread_sheet import *
import datetime

def ga_raw():
    day = start_day

    pc_data = pd.DataFrame()
    mo_data = pd.DataFrame()
    while day < today :
        ymd = day.strftime('%Y%m%d')
        pc_dir = tracker_raw_dir + f'/PC/Analytics 02.1 PC WEB Daily_PC {ymd}-{ymd}.csv'
        mo_dir = tracker_raw_dir + f'/MO/Analytics 02.2 MOBILE WEB Daily_Mobile {ymd}-{ymd}.csv'

        pc_temp = pd.read_csv(pc_dir, encoding = 'utf-8-sig', header = 5)
        mo_temp = pd.read_csv(mo_dir, encoding='utf-8-sig', header=5)


        pc_data = pd.concat([pc_data, pc_temp], sort = False)
        mo_data = pd.concat([mo_data, mo_temp], sort=False)

        day = day+datetime.timedelta(1)

    pc_data = pc_data.rename(columns = {'[중요]  PC 카드신청 완료 (목표 1 완료 수)' : 'GA신청'})
    mo_data = mo_data.rename(columns = {'[중요] 모바일 카드신청 최종(2018/03/19~) (목표 19 완료 수)' : 'GA신청'})

    ga_raw = pd.concat([pc_data, mo_data], sort= False)
    ga_raw['source'] = ga_raw['소스/매체'].apply(lambda x : x.split(' / ')[0])
    ga_raw['medium'] = ga_raw['소스/매체'].apply(lambda x : x.split(' / ')[-1])

    ga_raw['날짜'] = pd.to_datetime(ga_raw['날짜'], format = '%Y%m%d').dt.date

    return ga_raw

def ga_preprocess():
    source_name_dict = {
        'mkakao': '모먼트',
        'kakao': '모먼트',
        'mnaver_gfa': '네이버GFA',
        'facebook': '페이스북',
        'instagram': '인스타그램',
        'twitter': '트위터',
        'nice': '나이스지키미',
        'mnice': '나이스지키미',
        'allcredit': '올크레딧',
        'mallcredit': '올크레딧',
        'irex': '아이렉스',
        'mirex': '아이렉스',
        'bankQ': '뱅큐',
        'finda': '핀다',
        'mfinda': '핀다',
        'valuechampion': '벨류체인',
        'mvaluechampion': '벨류체인',
        'blind': '블라인드',
        'naver_platform': '네이버통합DA',
        'mnaver_platform': '네이버통합DA',
        'TargetingGates': '타겟팅게이츠',
        'mTargetingGates': '타겟팅게이츠',
        'criteo': '크리테오',
        'navermmail': '네이버메일'

    }

    raw_data = ga_raw()
    raw_data = raw_data.rename(columns = {'광고 콘텐츠' : 'adcontent', '캠페인' : 'campaign', '키워드' : '소재'})
    del raw_data['소스/매체']

    ga_index = index_sheet()
    ga_index = ga_index.drop_duplicates(subset = ['source','campaign','medium','adcontent', '소재'], keep = 'last')


    ga_index_merge = raw_data.merge(ga_index, on= ['source','campaign','medium','adcontent', '소재'], how = 'left')
    ga_index_merge['매체'] = ga_index_merge['source'].apply(lambda x : source_name_dict.get(x) if x in source_name_dict.keys() else x)

    return ga_index_merge







