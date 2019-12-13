from gevent import monkey;monkey.patch_all()
import socket
import gevent
import random
import re
import json
from functools import wraps

class Server_Gevent():
    def __init__(self,Host,Port):
        self.Host = Host
        self.Port = Port
        self.response = "HTTP/1.1 200 OK\r\nAuthion:\r\n"
        self.response += "\r\n"
        #1. 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #2. 绑定
        #设置当前服务器先close 即服务器4次挥手后资源能够立即释放，
        #下次运行程序时，立即执行
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.tcp_server_socket.bind((Host, Port))
        #3. 变为监听套接字
        self.tcp_server_socket.listen(128)
    #service client服务创建
    def service_client(self,new_socket):
        try:
            request = new_socket.recv(1024).decode("utf-8")
            #请求方式
            Request_way = request.splitlines()[0].split(" ")[0]
        except:
            pass
        else:
            if Request_way == "GET": 
                self.do_GET(new_socket,request)
            elif Request_way == "POST":
                    self.do_POST(new_socket,request)
    #POST请求处理
    def do_POST(self,new_socket,request):
        try:        
            self.PostWay_Out(new_socket,request)
        except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                new_socket.send(response.encode("utf-8"))
                new_socket.send(b"------Data parsing error-----")
        finally:
            new_socket.close()
    #请求路由处理
    def routing(self,request):
        return request.splitlines()[0].split(" ")[1]
     #GET请求处理
    def do_GET(self,new_socket,request):
        try:
            self.GetWay_Out(new_socket,request)
        
        except:
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            response += "\r\n"
            response += "------file not found-----"
            new_socket.send(response.encode("utf-8"))
        finally:
            new_socket.close()
    #POST请求获取参数，处理
    def PostWay_Out(self,new_socket,request):
        Post_url = self.routing(request)
        if Post_url == '/abc/def':
            p1 = re.compile(r'[{](.*?)[}]', re.S)
            re_dic = '{'+re.findall(p1, request.replace("\n","").replace("\t",""))[0]+'}'
            ser_dict = eval(re_dic)
            date = json.dumps({'abc':1,"qwe":2})
            response = "HTTP/1.1 200 OK\r\nContent-Type:{}\r\n".format('application/json')
            response += "\r\n"
            new_socket.send(response.encode("utf-8"))
            new_socket.send(date.encode("utf-8"))
        #此间可以添加更多的elif  对不同路由不同的处理
        '''elif: .....'''
    #GET请求获取参数，处理
    def GetWay_Out(self,new_socket,request):
        Get_url = self.routing(request)
        #如果路由为 / 
        if Get_url == "/":
            file_name = 'index.html'
            f = open("temp/" + file_name,"rb")
            html_content = f.read()
            f.close()
            response = "HTTP/1.1 200 OK\r\n"
            response += "\r\n"
            new_socket.send(response.format("23123123213").encode("utf-8"))
            new_socket.send(html_content)
        #此间可以添加更多的elif  对不同路由不同的处理
        else:
            response = "HTTP/1.1 404 NOT FOUND\r\n"
            response += "\r\n"
            response += "------file not found-----"
            new_socket.send(response.encode("utf-8"))
    def main(self):
            while True:
                #4. 等待新用户端的连接
                new_socket,client_addr = self.tcp_server_socket.accept()
                #5.为这个客户服务
                gevent.spawn(self.service_client, new_socket)
            
            self.tcp_server_socket.close()

if __name__ == '__main__':
    run=Server_Gevent(Host='0.0.0.0',Port=7890)
    run.main()