# coding:utf-8
import requests
from time import sleep
from weixin import gettoken, senddata


def get_status():
    url = 'https://enterbj.zhongchebaolian.com/enterbj/platform/enterbj/curtime_03'
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url, verify=False, allow_redirects=False)
    location = r.headers.get("Location", None)
    if location == 'https://enterbj.zhongchebaolian.com/errorpage/enterbj.html':
        status = 0
    else:
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
