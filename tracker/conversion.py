from setting.spread_sheet import *



def registration():
    reg_data = reg_sheet()
    reg_data['날짜'] = pd.to_datetime(reg_data['접수일자'], format = '%Y/%m/%d').dt.date
    reg_data = reg_data.loc[(reg_data['대행사']=='매드잇')&(reg_data['발급구분']=='신규')]
    reg_data = reg_data.loc[reg_data['매체']!='Kbpay_내부사용']

    name_dict = {
        'kakao AD_MO_모먼트' : '모먼트_',
        'kakao AD_MO_비즈보드' : '비즈보드_',
        'SKT_T전화/빌레터' : '모비엠_',
        '네이버M 메일DA' : 'OCB_'
    }

    reg_data['매체'] = reg_data['매체'].apply(lambda x : name_dict.get(x) if x in name_dict.keys() else x)
    reg_data['매체'] = reg_data['매체'].apply(lambda x : x.split('_')[0])
    reg_data['매체'] = reg_data['매체'].apply(lambda x : '올크레딧' if x=='올크래딧' else x)

    reg_columns = ['날짜', '상품코드', '권유자번호', '매체', '상품', '카테고리']

    reg_reg= reg_data[reg_columns]
    reg_reg['cnt'] = 1

    reg_reg = reg_reg.pivot_table(index = reg_columns, values = 'cnt', aggfunc='sum')
    reg_reg = reg_reg.reset_index()
    reg_reg = reg_reg.rename(columns = {'cnt' : '신청-신청'})

    reg_iss = reg_data.loc[reg_data['처리상태']=='발급']
    reg_iss = reg_iss[reg_columns]
    reg_iss['cnt'] = 1

    reg_iss = reg_iss.pivot_table(index = reg_columns, values = 'cnt', aggfunc='sum')
    reg_iss = reg_iss.reset_index()
    reg_iss = reg_iss.rename(columns = {'cnt' : '신청-발급'})

    raw_data = reg_reg.merge(reg_iss, on = reg_columns, how = 'outer')
    raw_data['신청-발급'] = raw_data['신청-발급'].fillna(0)



    return raw_data

def issue():
    issue_data = iss_sheet()
    issue_data = issue_data.melt(id_vars= ['매체','카테고리', '상품'])
    issue_data = issue_data.rename(columns = {'variable' : '날짜', 'value' : '발급완료'})

    name_dict = {
        'Kakao AD_MO' : '모먼트_',
        'kakao AD_MO_비즈보드' : '비즈보드_',
        'Kakao AD_PC': '모먼트_',
        'SKT_T전화/빌레터' : '모비엠_',
        '네이버M 메일DA' : 'OCB_'
    }

    issue_data['매체'] = issue_data['매체'].apply(lambda x : name_dict.get(x) if x in name_dict.keys() else x)
    issue_data['매체'] = issue_data['매체'].apply(lambda x : x.split('_')[0] if '_' in str(x) else x)
    issue_data['발급완료'] = issue_data['발급완료'].astype('int')
    issue_data = issue_data.loc[issue_data['발급완료']!=0]

    return issue_data

