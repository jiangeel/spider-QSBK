__author__='Eel'
#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
class QSBK:

	def __init__(self):
		self.pageIndex=1
		self.user_agent='Mozilla/4.0(compatible;MSIE 55.;Windows NT)'
		self.headers={'User-Agent':self.user_agent}
		self.stories=[]
		self.enable=False
	def getPage(self,pageIndex):
		try:
			url='http://www.qiushibaike.com/hot/page/'+str(pageIndex)
			request=urllib2.Request(url,headers=self.headers)
			response=urllib2.urlopen(request)
			page=response.read().decode('utf-8')
			#print response.read()
			return page
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print "fail to connect qiushibaike! reason:" + e.reason	

	def getPageItems(self,pageIndex):
		page=self.getPage(pageIndex)
		if not page:
			print "fail to load page..."
			return None

		regAUTHOR=r'<div.*?author clearfix.*?<a.*?<img.*?title="(.*?)">.*?'
		#regCONTENT=r'content">.*?<span>(.*?)</span.*?'#have photo
		regCONTENT=r'content">.*?<span>(.*?)</span.*?/a>(.*?)stats.*?'#no photo
		regLIKENUM=r'number">(.*?)</i.*?'
		regCOMMENT=r'cmtMain.*?main-text">\s(.*?)<div.*?'
		pattern=re.compile(regAUTHOR+regCONTENT+regLIKENUM+regCOMMENT,re.S)
		items=re.findall(pattern,page)
		pageStories=[]
		for item in items:
			havingImg=re.search("img",item[2])
			if not havingImg:
				replaceBR=re.compile('<br/>')
				content=re.sub(replaceBR,'\n',item[1])
				#item[0]=>author,item[1]=>content,item[2]=>photoInContent
				#item[3]=>numberOfLike,item[4]=>hotComment
				pageStories.append([item[0],content,item[3],item[4]])
				#print item[0]+":\n"+item[1]+"\n"+"Like:"+item[3]+"\n"+"comment"+item[4]		
		print 'stories remaining this page:',len(pageStories)
		return pageStories

	def loadPage(self):
		if self.enable==True:
			if len(self.stories)<2:
				pageStories=self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex +=1
				else:
					print "flag 3"

	def getOneStory(self,pageStories,page):
		for story in pageStories:
			input = raw_input()
			print "stories len:",len(pageStories)
			self.loadPage()
			if input=="Q":
				self.enable=False
				return
			print u"page%d\tauthor:%s\tlike:%s \n %s \ncomment%s" %(page,story[0],story[2],story[1],story[3])


	def start(self):
		print u"Loading Qiushibaike,press Enter to get one,Q to quit"
		self.enable=True
		self.loadPage()
		nowPage=0
		while self.enable:
			if len(self.stories)>0:
				pageStories=self.stories[0]
				nowPage+=1
				del self.stories[0]
				self.getOneStory(pageStories,nowPage)

spider=QSBK()
spider.start()