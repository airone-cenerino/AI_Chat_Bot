import json, re, sys, emoji


def screening(text) :
    s = " ".join(text.splitlines()) # 改行を空白に変更。

    #RTを外す
    if s[0:3] == "RT ":
        s = s.replace(s[0:3], "")
        
    #@screen_nameを外す
    while s.find("@") != -1:
        index_at = s.find("@")
        if s.find(" ") != -1  :
            index_sp = s.find(" ",index_at) # @後の空白の場所を探す。
            if index_sp != -1 :
                s = s.replace(s[index_at:index_sp+1],"")
            else :
                s = s.replace(s[index_at:],"")
        else :
            s = s.replace(s[index_at:], "")

    #改行を外す
    while s.find("\n") != -1 :
        index_ret = s.find("\n")
        s = s.replace(s[index_ret], "")

    #URLを外す
    s = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", s)
    #絵文字を「。」に置き換え その１
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '。')
    s = s.translate(non_bmp_map)
    #絵文字を「。」に置き換え　その２
    s=''.join(c if c not in emoji.UNICODE_EMOJI else '。' for c in s  )

    #置き換えた「。」が連続していたら１つにまとめる
    while s.find('。。') != -1 :
        index_period = s.find('。。')
        s = s.replace(s[index_period:index_period+2],'。')

    #ハッシュタグを外す
    while s.find('#') != -1 :
        index_hash = s.find('#') 
        s = s[0:index_hash]

    return s


def getTweet(res,since_id ,reset, BOT_user_name):
    res_text = json.loads(res.text)
    url1 = 'https://api.twitter.com/1.1/statuses/user_timeline.json'    #今回こちらは使わない
    url2 = 'https://api.twitter.com/1.1/statuses/lookup.json'

    cnt_req = 0
    max_tweet = since_id

    tweet_list = []                           # n_reply_to_status_idと応答tweetの対のリスト
    for tweet in res_text['statuses']:
        tweet_id=tweet['id']                  # tweetのid

        if max_tweet < tweet_id :
            max_tweet = tweet_id

        user = tweet['user']
        screen_name = user['screen_name']
        if screen_name == BOT_user_name :
            continue

        res_sentence = tweet['text']

        #RTを対象外にする
        if res_sentence[0:3] == "RT " :
            continue

        res_sentence = screening(res_sentence)

        if res_sentence == '' :
            continue

        tweet_list.append([tweet_id, screen_name, res_sentence])
        print(screen_name + "さんから「" + res_sentence + "」とリプが来ました。") 

    if len(tweet_list) == 0 :
        return max_tweet,tweet_list

    return max_tweet,tweet_list