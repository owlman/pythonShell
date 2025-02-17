#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
"""
Created on 2018-06-11 
    
@author: lingjie 
@name:   open_ssh_proxy
"""

import pexpect
import os

if __name__ == "__main__":
    # 从环境变量中获取用户名、主机名和密码
    user = os.getenv("SSH_USER")
    host = os.getenv("SSH_HOST")
    pword = os.getenv("SSH_PASSWORD")

    # 检查是否设置了用户名、主机名和密码
    if not user or not host or not pword:
        print("Please set SSH_USER, SSH_HOST, and SSH_PASSWORD environment variables.")
        exit(1)

    print(f"Connecting to {user}@{host}...")

    try:
        # 启动 SSH 连接并设置动态端口转发
        child = pexpect.spawn("ssh -D 7070 %s@%s" % (user, host))
        
        # 等待密码提示并发送密码
        child.expect("password:")
        child.sendline(pword)
        
        # 将控制权交给用户
        child.interact()
    except pexpect.ExceptionPexpect as e:
        print(f"An error occurred: {e}")
        exit(1)
