from jinja2 import Template
from apistar import http

from mihawk.common import dbapi
from mihawk.common.config import project_config
from mihawk.common.alert import send_wechat
from mihawk.common.alert import send_mail
from mihawk.common.alert import send_sms


def alert(params: http.QueryParams):

    try:
        assert "endpoint" in params.keys()
        assert "exp_id" in params.keys()
        assert "metric" in params.keys()
        assert "tpl_id" in params.keys()
    except AssertionError as e:
        return {"error": "endpoint and metric must in params"}

    title = f'{params["endpoint"]} {params["metric"]}报警'

    tpl_id = int(params["tpl_id"])
    exp_id = int(params["exp_id"])
    user_infos = dbapi.get_user_contact_by_tpl_id(tpl_id, exp_id)

    endpoint = params["endpoint"]

    metric = params["metric"]
    tags = params["tags"]

    # 目前的415错误先过滤掉，等下一个版本发布后再恢复
    if tags == "api=__serv__,errcode=415" or tags == "api=/dangdang/api/config,errcode=415":
        return {"mail": "misstatement", "sms": "misstatement", "im": "misstatement"}

    metric = (params["metric"] + "/" + params["tags"].replace(":", "=")).strip()

    # 仅当10分钟内相同报警出现3次或3次以上才会触发短信报警
    event_infos = dbapi.get_infos_by_endpoint_metric_time(endpoint, metric, interval=10)

    if len(event_infos) == 0:
        return {"mail": "misstatement", "sms": "misstatement", "im": "misstatement"}

    event_info = event_infos[0]

    emails = [user[1] for user in user_infos]
    emails = ",".join(emails)

    phones = [user[2] for user in user_infos]
    phones = ",".join(phones)

    ims = [user[3] for user in user_infos]
    ims = ",".join(ims)

    path = project_config["path"]
    with open(f"{path}/templates/alert.tmpl", "r") as f:

        t = "".join(f.readlines())
        t = Template(t)

        html_message = t.render(params=event_info)

        # 仅当10分钟内相同报警出现3次或3次以上才会触发短信报警
        if event_info[4] >= 3:
            response = {
                "mail": send_mail(title, html_message, emails),
                "sms": send_sms(event_info, phones),
                "im": send_wechat(event_info, ims)
            }
        else:
            response = {
                "mail": send_mail(title, html_message, emails),
                "sms": "misstatement",
                "im": send_wechat(event_info, ims)
            }

    return response


def notify_email(params: http.RequestData):
    email_config = params["email"]

    path = project_config["path"]
    with open(f"{path}/templates/notify.tmpl", "r") as f:
        t = "".join(f.readlines())
        t = Template(t)
        message = t.render(params=params)
        status = send_mail(email_config["subject"], message, email_config["to"])
    return {"status": status}


def notify_sms(params: http.RequestData):
    # TODO 短信接口
    pass
