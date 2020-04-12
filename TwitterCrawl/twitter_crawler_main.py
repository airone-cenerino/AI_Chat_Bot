import datetime, time, sys, os
import errno
from socket import error as SocketError
from requests_oauthlib import OAuth1Session

import check_limit
import get_tweet
import private_key


def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
        oath_key_dict["consumer_key"],
        oath_key_dict["consumer_secret"],
        oath_key_dict["access_token"],
        oath_key_dict["access_token_secret"]
        )
    return oath


def main_loop(search_word, session):
    total= -1
    total_count = 0
    cnt = 0

    url = 'https://api.twitter.com/1.1/search/tweets.json'  # ツイートを検索して取得するためのエンドポイント

    loop_start_time = get_tweet.FIRST_LOOP_START_TIME

    # 1回のループで100ツイートを取得します。
    while True:
        next_reset_time = check_limit.checkLimit(session)  # 回数制限を迎えていたら回復するまで待機。
        tweets_get_time = time.mktime(datetime.datetime.now().timetuple())  #現在時刻取得
        
        unavailableCnt = 0  # ツイートの取得に失敗した回数。

        try :
            res = session.get(url, params = {'q':search_word, 'count':100}) # 検索し、100件のツイートを取得。
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

        if res.status_code != 200:
            raise Exception('Twitter API error %d' % res.status_code)


        loop_start_time ,count ,total_text = get_tweet.getTweet(res, loop_start_time, next_reset_time, session)    # 100件のツイートからリプライのみを抽出してペアで取得する。


        # ファイル書き込み
        date = datetime.date.today()
        fname = 'tweet/' + search_word + 'tweet'+str(date)+'.txt'

        if not os.path.exists("tweet"):
            os.mkdir("tweet")

        f=open(fname,'a', encoding='utf-8')
        for i in range(0, len(total_text)):
            f.write(str(total_text[i]) + "\n")
        f.close()




        total_count += count
        print('total_count=',total_count,'start_time=',loop_start_time)

        current_time = time.mktime(datetime.datetime.now().timetuple()) 
        # 処理時間が2秒未満なら2秒wait
        if current_time - tweets_get_time < 2 :
            check_limit.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 2)

        #デバッグ用
        if total > 0 :
            cnt += 100
        if total > 0 and cnt >= total:
            break


if __name__ == '__main__':
    args = sys.argv     # コマンドライン引数
    session = create_oath_session(private_key.oath_key_dict)  # セッション確立
    main_loop(args[1], session)