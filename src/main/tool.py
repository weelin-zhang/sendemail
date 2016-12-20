#coding=utf8
'''
Created on 2016年12月19日

@author: ZWJ
'''

def user_pwd():
    
    with open('config') as f:
        return f.readline().strip().split('=')[1],f.readline().strip().split('=')[1]
    