import pandas as pd
import datetime
import re

from setting.report_date import *
from setting.directory import *

# columns에 있는 nan값들을 fill_type으로 채움
def fill_values(df, columns, fill_type):
    for col in columns:
        if col not in df.columns:
            df[col] = fill_type
        df[col] = df[col].fillna(fill_type)
        df[col] = df[col].apply(lambda x : fill_type if x=='' else x)

def media_cost(df):
    df.index = range(0, len(df))
    vat_media = ['Naver_GFA', '모먼트', '비즈보드']
    df.loc[df['매체'].isin(vat_media), '비용'] = df['비용']

    markup_10_media = ['페이스북', '인스타그램', '트위터']
    df.loc[df['매체'].isin(markup_10_media), '비용'] = df['비용'] * 1.1 * 1.1

    return df