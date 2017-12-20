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
    elif location == 'https://enterbj.zhongchebaolian.com/errorpage/powermaintenance.html':
	status = 2
    elif 'errorpage' in location:
	status = 3
    else:
        status = 1
    return status


if __name__ == "__main__":
    corpid = '企业CorpID'
    corpsecret = '应用Secret'
    agentid = "应用AgentID"
    laststatus = 0
    while True:
	try:
	    status = get_status()
	    if status != laststatus:
	        # 状态发生改变时告警
		if status == 0 or status == 3:
		    message = "进京证办理通道关闭"
	        elif status == 2:
		    message = "机房设备断电维护中"
	        else:
	            message = "进京证办理通道开启"
			#以下是企业微信告警推送
	        accesstoken = gettoken(corpid, corpsecret)
	        senddata(accesstoken, message, 4, None, agentid)
		laststatus = status
	except Exception,e:
            print Exception,e
        sleep(60)
