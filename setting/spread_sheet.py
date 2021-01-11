from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from setting.directory import *
from setting.auth import *
from setting.report_date import *

def spread_document_read(spread_url):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    json_file = token_dir + '/' + json_file_name
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    gc = gspread.authorize(credentials)
    read = gc.open_by_url(spread_url)
    print('스프레드시트 읽기 완료')
    return read

doc = spread_document_read('https://docs.google.com/spreadsheets/d/1dQHlLxEtVu5qWKdvVGI88P0bgH2reyx-i9AMhaPOr3M/edit#gid=1436562944')
media_doc = spread_document_read('https://docs.google.com/spreadsheets/d/1T15PoahyLEUBljsJESGZyZa1XNqaWKdVsonkaSgdo7o/edit#gid=1238296719')

def spread_sheet(doc, sheet_name, col_num, row_num=0):
    data_sheet = doc.worksheet(sheet_name)
    data_sheet_read = data_sheet.get_all_values()
    result = pd.DataFrame(data_sheet_read, columns=data_sheet_read[row_num]).iloc[row_num + 1:, col_num:]
    return result

def index_sheet():
    index = spread_sheet(doc, sheet_name = 'UTM Builder', row_num = 1, col_num=0)

    def group_name(row):
        head = row['광고그룹']
        tail = row['타겟팅']
        return head + '-' + tail

    index = index.rename(columns={'&utm_source=': 'source',
                                  '&utm_medium=': 'medium',
                                  '&utm_campaign=': 'campaign',
                                  '&utm_content=': 'adcontent',
                                  '&utm_term=': '소재',
                                  '권유자코드': '권유자번호',
                                  '소재': '필요없엉'})

    index['광고그룹'] = index.apply(group_name, axis=1)

    index_columns = ['캠페인', '광고그룹', 'source', 'medium', 'campaign', 'adcontent', '소재', '상품','카테고리','권유자번호']

    return index[index_columns]

def sub_media_raw_data_read():
    dashboard = spread_sheet(media_doc,sheet_name='매체별 RD', col_num = 0)
    operating_media = dashboard.loc[dashboard[day_1_yearmonth]=='TRUE', '매체'].tolist()

    result = pd.DataFrame()
    for media in operating_media :
        data = spread_sheet(media_doc, media, 0)
        data = data.loc[pd.notnull(data['날짜'])]
        data = data.loc[pd.to_datetime(data['날짜']).dt.month==day_1.month]
        result = pd.concat([result, data], sort= False)

    return result

def reg_sheet():
    sheet = spread_sheet(media_doc, sheet_name = '신청', col_num = 0)
    return sheet

def iss_sheet():
    sheet = spread_sheet(media_doc, sheet_name = '발급', col_num = 0)
    return sheet
