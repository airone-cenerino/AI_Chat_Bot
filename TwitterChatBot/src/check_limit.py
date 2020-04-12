import datetime, time, json, sys
from socket import error as SocketError


def waitUntilReset(reset):
    seconds = reset - time.mktime(datetime.datetime.now().timetuple())
    seconds = max(seconds, 0)
    sys.stdout.flush()
    time.sleep(seconds + 10)  # 念のため + 10 秒


def getLimitContext(res_text):
    # searchの制限情報
    remaining_search = res_text['resources']['search']['/search/tweets']['remaining']
    reset1     = res_text['resources']['search']['/search/tweets']['reset']
    # 制限情報取得の制限情報
    remaining_limit = res_text['resources']['application']['/application/rate_limit_status']['remaining']
    reset3     = res_text['resources']['application']['/application/rate_limit_status']['reset']

    return int(remaining_search), int(remaining_limit), max(int(reset1), int(reset3))


def checkLimit(session):
    unavailableCnt = 0
    url = "https://api.twitter.com/1.1/application/rate_limit_status.json"

    while True :
        try:
            res = session.get(url)
        except SocketError as e:
            print('erron=',e.errno)
            print('ソケットエラー')
            if unavailableCnt > 10:
                raise

            waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            unavailableCnt += 1
            continue

        if res.status_code == 503:
            # 503 : Service Unavailable
            if unavailableCnt > 10:
                raise Exception('Twitter API error %d' % res.status_code)

            unavailableCnt += 1
            print ('Service Unavailable 503')
            waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            continue

        unavailableCnt = 0

        if res.status_code != 200:
            raise Exception('Twitter API error %d' % res.status_code)

        remaining_search, remaining_limit ,reset = getLimitContext(json.loads(res.text))
        if remaining_search <= 1 or  remaining_limit <= 1:
            waitUntilReset(reset+30)
        else :
            break

    return reset
