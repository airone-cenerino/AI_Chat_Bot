from requests_oauthlib import OAuth1Session
import json
import datetime, time, sys
import datetime
import sys
import pickle
import os
from socket import error as SocketError
import errno

import seq2seq_manager
import make_reply
import private_key
import setting
import get_tweet
import check_limit
import post_tweet


def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
        oath_key_dict["consumer_key"],
        oath_key_dict["consumer_secret"],
        oath_key_dict["access_token"],
        oath_key_dict["access_token_secret"]
        )
    return oath


def load_since_id():
    if os.path.isfile('since_id.pickle') :
        with open('since_id.pickle', 'rb') as f :
            return pickle.load(f) 
    else : 
        return 1092760343191871493


if __name__ == '__main__':
    url = 'https://api.twitter.com/1.1/search/tweets.json'  # ツイート検索用エンドポイント

    encoder, decoder, searcher, word_index_dict = seq2seq_manager.get_trained_data()    # 作成済みのモデル・辞書をロード。
    session = create_oath_session(private_key.oath_key_dict)  # セッション確立

    since_id = load_since_id()   #since_idロード


    while True:
        unavailableCnt = 0
        reset  = check_limit.checkLimit(session)    # 回数制限確認
        get_time = time.mktime(datetime.datetime.now().timetuple())  #getの時刻取得
        
        try :
            res = session.get(url, params = {'q':setting.BOT_SCREEN_NAME, 'since_id':since_id, 'count':100})    # Botへのメンションツイートの確認
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


        # tweet本文と発信者取得
        since_id, tweet_list = get_tweet.getTweet(res, since_id, reset, setting.BOT_USER_NAME)


        # 応答送信
        for i in range(len(tweet_list)):
            res_text = make_reply.evaluateInput(encoder, decoder, searcher, word_index_dict, tweet_list[i][2])
            print("「" + res_text + "」と返信しました。")
            print()

            res_text = '@'+tweet_list[i][1] + ' '+ res_text  # 返信文作成
            post_tweet.postTweet(session, res_text, tweet_list[i][0])


        #since_id 保存
        with open('since_id.pickle', 'wb') as f :    
            pickle.dump(since_id , f)


        current_time = time.mktime(datetime.datetime.now().timetuple())
        # 処理時間が2秒未満なら2+10秒wait
        if current_time - get_time < 2 :
            check_limit.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 2)