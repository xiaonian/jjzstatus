# coding:utf-8
import requests
from time import sleep
from weixin import gettoken, senddata


def get_status():
    url = "https://api.jinjingzheng.zhongchebaolian.com/errorpage/enterbj.html"
    r = requests.get(url)
    r.encoding = "utf-8"
    # print r.text
    if u"由于办理电子进京证申请排队人数过多" in r.text:
        # print "当前不可用"
        status = 0
    else:
        # print "进京证可以正常办理了"
        status = 1
    return status


if __name__ == "__main__":
    corpid = '企业CorpID'
    corpsecret = '应用Secret'
	agentid = "应用AgentID"
    laststatus = 1
    while True:
        status = get_status()
        if status != laststatus:
            # 状态发生改变时告警
            laststatus = status
            message = "进京证办理通道开启" if status == 1 else "进京证办理通道关闭"
			#以下是企业微信告警推送
            accesstoken = gettoken(corpid, corpsecret)
            senddata(accesstoken, message, 4, None, agentid)
        sleep(60)
