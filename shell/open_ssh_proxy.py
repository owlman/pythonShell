#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
'''
Created on 2018-06-11 
    
@author: lingjie 
@name:   open_ssh_proxy
'''
import pexpect  
    
if __name__ == "__main__":  
    user = "username"  
    host = "hostname"  
    pword = "password"  

    if(user=="username" or host=="hostname" or pword=="password"):
       print("Please setting username,hostname and password...")
       exit(1)
        
    print user  
    child = pexpect.spawn("ssh -D 7070 %s@%s" % (user,host))  
    child.expect("password:")  
    child.sendline(pword)  
        
    child.interact()     # Give control of the child to the user.  
