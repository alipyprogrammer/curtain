import requests
from math import ceil


token = "sa3098276450:sIy0DUeyIlZlxNM0QSEoAYnGYT2hyMhIDCkB"
def send_sms_2(list_phone, list_message):
    url = f"https://api.sabanovin.com/v1/{token}/sms/send_array.json"
    if (len(list_phone)) > 100:
        n=ceil(len(list_phone)/100)
        for i in range(n):
            if i!=n-1:
                ali = ""
                send_sms = requests.post(url,json={
                    "gateway" : 10007737486526 ,
                    "to"      : list_phone[i*100:100*(i+1)],
                    "text"    : list_message[i*100:100*(i+1)]
                })
                print("send_sms")
                print(send_sms.status_code)
            elif i==n-1:
                send_sms = requests.post(url,json={
                    "gateway" : 10007737486526 ,
                    "to"      : list_phone[i*100:],
                    "text"    : list_message[i*100:]
                })
                print("send_sms")
                print(send_sms.status_code)
    else :
            send_sms = requests.post(url,json={
                    "gateway" : 10007737486526 ,
                    "to"      : list_phone,
                    "text"    : list_message
            })
            print("send_sms")
            print(send_sms.status_code)
