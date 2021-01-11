from setting.spread_sheet import *
from setting.function import *
from report import column_rule


def sub_media_dataset() :
    raw_data = sub_media_raw_data_read()


    raw_data = raw_data[column_rule.media_columns]
    fill_values(raw_data, column_rule.media_index_columns, '-')
    fill_values(raw_data, column_rule.media_value_columns, 0)

    return raw_data

def media_preprocess():
    sub_media_data = sub_media_dataset()

    media_data = pd.concat([sub_media_data],sort =False)

    media_index = index_sheet()
    media_index = media_index.drop_duplicates(subset = ['캠페인', '광고그룹','소재'], keep = 'last')

    media_index_merge = media_data.merge(media_index, on = ['캠페인', '광고그룹', '소재'], how = 'left')
    return media_index_merge