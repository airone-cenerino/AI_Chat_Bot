import time, datetime
from socket import error as SocketError
import check_limit

def postTweet(session, res_text, src_tweet_id) :

    unavailableCnt = 0

    url = "https://api.twitter.com/1.1/statuses/update.json" #ツイートポストエンドポイント

    while True :
        reset  = check_limit.checkLimit(session) 

        try :
            res = session.post(url, params = {'status':res_text, 'in_reply_to_status_id':src_tweet_id})
        except SocketError as e:
            print('ソケットエラー errno=',e.errno)
            if unavailableCnt > 10:
                raise

            check_limit.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            unavailableCnt += 1
            continue

        if res.status_code == 503:
            # 503 : Service Unavailable
            if unavailableCnt > 10:
                raise Exception('Twitter API error %d' % res.status_code)

            unavailableCnt += 1
            print ('Service Unavailable 503')
            check_limit.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            continue

        if res.status_code == 403:     #post文重複対策
            res_text = res_text + '_'
            unavailableCnt += 1
            continue

        unavailableCnt = 0

        if res.status_code != 200:
            raise Exception('Twitter API error %d' % res.status_code)
        else :
            break