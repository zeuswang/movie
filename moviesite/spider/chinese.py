#!/usr/bin/env python
# -*- coding:utf-8 -*- 

__author__="internetsweeper <zhengbin0713@gmail.com>"
__date__="2007-08-04"

def is_chinese(uchar):
	if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
		return True
	else:
		return False

def is_number(uchar):
	if uchar >= u'\u0030' and uchar<=u'\u0039':
		return True
	else:
		return False

def is_alphabet(uchar):
	if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
		return True
	else:
		return False

def is_other(uchar):
	if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
		return True
	else:
		return False

def B2Q(uchar):
#"""ban jiao to quanjiao"""
	inside_code=ord(uchar)
	if inside_code<0x0020 or inside_code>0x7e:      
		return uchar
	if inside_code==0x0020:
		inside_code=0x3000
	else:
		inside_code+=0xfee0
	return unichr(inside_code)

def Q2B(uchar):
	"""quanjiao to banjiao"""
	inside_code=ord(uchar)
	if inside_code==0x3000:
		inside_code=0x0020
	else:
		inside_code-=0xfee0
	if inside_code<0x0020 or inside_code>0x7e:   
		return uchar

	return unichr(inside_code)

def stringQ2B(ustring):
	return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
	return stringQ2B(ustring).lower()

def string2List(ustring):
	retList=[]
	utmp=[]
	for uchar in ustring:
		if is_other(uchar):
			if len(utmp)==0:
				continue
			else:
				retList.append("".join(utmp))
				utmp=[]
		else:
			utmp.append(uchar)
	if len(utmp)!=0:
		retList.append("".join(utmp))
	return retList

if __name__=="__main__":
#test Q2B and B2Q
#	for i in range(0x0020,0x007F):
#		print Q2B(B2Q(unichr(i))),B2Q(unichr(i))

#test uniform
	ustring=u'【急速飞车】【2014美国大片】abc.cccc'
	for uchar in ustring:
		if not is_other(uchar):
			if not is_chinese(uchar):
				print uchar	
	ustring=uniform(ustring)
	ret=string2List(ustring)
	print ret
