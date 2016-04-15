#! /usr/bin/env python
'''
    Created on 2016-4-15
    
    @author: lingjie
    @name:   git_configuration
'''

import os
import sys

cmds = [
	"git config --global user.name 'owlman'" ,
	"git config --global user.email 'jie.owl2008@gmail.com'",
	"git config --global push.default simple",
	"git config --global color.ui true",
	"git config --global core.quotepath false",
	"git config --global i18n.logOutputEncodiing utf-8",
	"git config --global i18n.commitEncoding utf-8",
	"git config --global color.diff auto",
	"git config --global color.status auto",
	"git config --global color.branch auto",
	"git config --global color.interactive auto"
]

for cmd in cmds:
	os.system(cmd)
