#!/usr/bin/python
# _*_coding:utf-8 _*_
import urllib2
import json
import sys
import argparse

reload(sys)
sys.setdefaultencoding('utf-8')


def gettoken(corpid, corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    # print gettoken_url
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except urllib2.HTTPError as e:
        print e.code
        print e.read().decode("utf8")
        sys.exit()
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token


def senddata(access_token, content, party, user, agentid):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": content
        },
        "safe": "0"
    }
    if party:
        send_values["toparty"] = party
    if user:
        send_values["touser"] = user

    send_data = json.dumps(send_values, ensure_ascii=False).encode('utf-8')
    send_request = urllib2.Request(send_url, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print str(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--content", help="微信内容")
    parser.add_argument("-p", "--party", help="指定用户组")
    parser.add_argument("-u", "--user", help="指定用户")
    args = parser.parse_args()
    corpid = '企业CorpID'
    corpsecret = '应用Secret'
	agentid = "应用AgentID"
    accesstoken = gettoken(corpid, corpsecret)
    senddata(accesstoken, args.content, args.party, args.user, agentid)
