from media.sub_media import *
from setting.directory import *
from tracker import *

media_data = media_preprocess()
ga_data = ga.ga_preprocess()
registration = conversion.registration()
issue = conversion.issue()

report_data = pd.concat([media_data, ga_data, registration, issue], sort = False)
fill_values(report_data, columns=['비용'], fill_type=0)
report_data['비용'] = report_data['비용'].astype('float')
report_data = media_cost(report_data)

sns_list = ['페이스북', '인스타그램', '트위터']
nw_list = ['모먼트', '비즈보드', '네이버GFA', '모비엠', '블라인드']
partner_list = ['나이스지키미', '올크레딧']
cpa_list = ['아이렉스', '핀다', '밸류체인', '뱅큐']

report_data.loc[report_data['매체'].isin(sns_list), '카테고리'] = 'SNS'
report_data.loc[report_data['매체'].isin(nw_list), '카테고리'] = 'NW'
report_data.loc[report_data['매체'].isin(partner_list), '카테고리'] = '제휴'
report_data.loc[report_data['매체'].isin(cpa_list), '카테고리'] = 'CPA'

report_data.to_csv(merge_raw_dir + f'/report_concat_data_{day_1_yearmonth}.csv', index = False, encoding='utf-8-sig')