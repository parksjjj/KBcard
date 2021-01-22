# 개인 로컬 환경에 맞추어 조정
dropbox_dir = 'C:/Users/user/Dropbox (주식회사매드업)'
download_dir = 'C:/Users/user/Downloads'
# ========================

report_dir = dropbox_dir + '/광고사업부/4. 광고주/KB국민카드/리포트 자동화'
env_dir = dropbox_dir + '/광고사업부/4. 광고주/KB국민카드/report_env/KBcard'

media_raw_dir = report_dir + '/1. 매체 데이터'
da_raw_dir = media_raw_dir + '/1. DA'
sa_raw_dir = media_raw_dir + '/2. SA'
bs_raw_dir = media_raw_dir + '/3. BS'

tracker_raw_dir = report_dir + '/2. 트래커 데이터'


merge_raw_dir = report_dir + '/3. 머지 데이터'
token_dir = env_dir + '/token'

#셀레니움용 크롬드라이버
chrome_driver = token_dir + '/chromedriver'