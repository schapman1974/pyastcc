#!/usr/bin/python

from urllib import urlencode
from urllib2 import urlopen
import datetime
import sha

class Upay:
  def __init__(self, server):
    self.server = server
    self.pincode="somepincode"
    self.sourcekey= "somesourcekey"

  def __encode(self, name, value):
    if len(value) != 0:
      return urlencode({name: value})+"&"
    else:
      return ""

  def hexascii(self,theline):
    asciidict={'20':' ','21':'!','22':'"','23':'#','24':'$','25':'%','26':'&','27':"'",'28':'(','29':')',
    '2A':'*','2B':'+','2C':',','2D':'-','2E':'.','2F':'/','30':'0','31':'1','32':'2','33':'3',
    '34':'4','35':'5','36':'6','37':'7','38':'8','39':'9','3A':':','3B':';','3C':'<','3D':'=',
    '3E':'>','3F':'?','40':'@','41':'A','42':'B','43':'C','44':'D','45':'E','46':'F','47':'G',
    '48':'H','49':'I','4A':'J','4B':'K','4C':'L','4D':'M','4E':'N','4F':'O','50':'P','51':'Q',
    '52':'R','53':'S','54':'T','55':'U','56':'V','57':'W','58':'X','59':'Y','5A':'Z','5B':'[',
    '5C':'\\','5D':']','5E':'^','5F':'_','60':'`','61':'a','62':'b','63':'c','64':'d','65':'e',
    '66':'f','67':'g','68':'h','69':'i','6A':'j','6B':'k','6C':'l','6D':'m','6E':'n','6F':'o',
    '70':'p','71':'q','72':'r','73':'s','74':'t','75':'u','76':'v','77':'w','78':'x','79':'y',
    '7A':'z','7B':'{','7C':'|','7D':'}','7E':'~'}
    thekeys=asciidict.keys()
    for x in range(0,95):
     theline=theline.replace('%'+thekeys[x],asciidict[thekeys[x]])
    return theline

  def ahash(self,pin,command,amount,invoice):
    today = datetime.date.today()
    hashseed=today.strftime("%Y%m%d%M%s")
    hashdata=command+':'+str(pin)+':'+amount+':'+invoice+':'+str(hashseed)
    thehash=sha.new(hashdata)
    hash= thehash.hexdigest()
    return 's/'+str(hashseed)+'/'+str(hash)+'/'+'n'

  def process (self,TLF):
    data=""
    getstat={}
    try:
      if TLF.has_key("UMmagstripe"):
        getstat['SWIPED']='YES'
        tear=TLF['UMmagstripe'].split("^")
        tear2=tear[0][2:len(tear[0])-1].replace(" ","")
        getstat['CC']=tear2[len(tear2)-4:len(tear2)]
      else:
        getstat['SWIPED']='NO'
        getstat['CC']=TLF['UMcard'][len(TLF['UMcard'])-4:len(TLF['UMcard'])]
      getstat['DOLLARS']=TLF['UMamount']
      getstat['TICKET']=TLF['UMinvoice']
    except:
      pass

    TLF['UMhash']=self.ahash(self.pincode,TLF['UMcommand'],TLF['UMamount'],TLF['UMinvoice'])
    TLF['UMkey']=self.sourcekey
    for key,info in TLF.items():
      #print key + "=" + info
      data += self.__encode(key,info)
    content = urlopen(self.server, data).read()
    content = self.hexascii(content).replace(":","=")
    content = content.split('&')
    ctnt={}
    for cont in content:
      theval=cont.split('=')
      ctnt[theval[0]]=theval[1]
    response = {}
    tac=[]
    return ctnt,getstat

  def printResults(self, response):
    tac=response[0].split("&")
    self.authcode=tac[3].split("=")[1]
    return self.authcode