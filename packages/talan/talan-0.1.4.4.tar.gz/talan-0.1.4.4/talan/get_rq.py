#!/usr/bin/env python3
'''Fetch REQUEST INFO
'''
import sys,os

def evv(va):
	try:
		return eval(va)
	except:
		return va

def qsparse(qs='',**opts):
	import urllib.parse
	if not qs:
		qs=os.getenv('QUERY_STRING')
	if not qs:
		return opts
	qs=urllib.parse.unquote_plus(qs)
	for xs in qs.strip().split('&'):
		vs=xs.strip().split('=')
		if len(vs)==2:
			opts.update({vs[0]:evv(vs[1])})
		elif len(vs)>2:
			opts.update({vs[0]:evv("=".join(vs[1:]))})
	return opts

def rqparse(xreq='POST', debugTF=False):
	if xreq=='POST':
		pst=sys.stdin.read().strip()
	else:
		pst=''
	opts=qsparse() #DEPRECATED, opts=get_cgi(xreq)
	if pst:
		opts.update(eval(pst))
	if not debugTF:
		return opts
	remoteAddr=os.getenv('REMOTE_ADDR')
	if remoteAddr:
		opts.update(remoteAddr=remoteAddr)
	realAddr=os.getenv('HTTP_X_REAL_IP')
	if realAddr:
		opts.update(remoteAddr=realAddr)
	envLst=",".join(["({}:{})".format(x,y) for x,y in os.environ.items()])
	opts.update(envLst=envLst)
	return opts

def get_rq(**optx):
	xreq=os.getenv('REQUEST_METHOD')
	if xreq not in ('GET','POST'):
		return optx
	try:
		optx=rqparse(xreq)
	except Exception as e:
		optx={"err":str(e)}
	ctype=optx.get('ctype','plain')
	if ctype=='html':
		print("Content-type:text/html;charset=utf-8\r\n\r\n")
	elif ctype=='json':
		print("Content-type:application/json;charset=utf-8\r\n\r\n")
	else:
		print("Content-type:text/plain;charset=utf-8\r\n\r\n")
	return optx

def prn_df(df,**optx):
	ctype=optx.get('ctype','plain')
	indexTF=optx.get('indexTF',False)
	# use commas to separate thousands in floats, complex numbers, and integers
	clx=df.columns
	cfm={s:'{:,}'.format for s in clx if df[s].values.dtype in ['int64']}
	cfx={s:'{:,.2f}'.format for s in clx if df[s].values.dtype in ['float64']}
	cfm.update(cfx)
	_ = cfm.pop('pbdate',None)
	cfx=optx.get('cfm',{})
	if cfx:
		cfm.update(cfx)
	if ctype=='html':
		print(df.to_html(index=indexTF,justify='right',formatters=cfm))
	elif ctype=='json':
		print(df.to_json(orient='records'))
	elif ctype=='dictionary': # special debugging format for `dict` type
		from pprint import pprint
		pprint(df.to_dict(orient='records'))
	else:
		print(df.to_string(index=indexTF,formatters=cfm))
