#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Programa responsável por ler log wireshark  e coletar links
para baixar as imagens dos links
Autores: Pablo Souza , Vitor Rezende
Nome do Arquivo: gera_links.py
'''



import urllib2 
def baixaImagens():
   links  = open('img/links.txt','rb')
   for l in links: 
     
     try:
       page = urllib2.urlopen(l)
       nfile = l.split("/")[-1]
       print l
       nomefile =nfile[:nfile.index('.')+4]
    
       saida = open("img/"+nomefile, "wb")
       saida.write(page.read())
     
       saida.close()
       page.close()
     except urllib2.HTTPError, e:
       print e.code
       print e.msg
  
     
     
     


def geralinks():
   a =  open('captura_wireshark.txt','rb')
   
   lslinks = []
   for b in a.readlines():
      
      if '[Full request URI: ' in b:
         if '.jpg' in b:
            lslinks.append(b[b.index('Full request URI:')+18:b.index(']')])
         elif '.gif' in b:
            lslinks.append(b[b.index('Full request URI:')+18:b.index(']')])
         elif '.png' in b:
            lslinks.append(b[b.index('Full request URI:')+18:b.index(']')])
       
   links = list(set(lslinks)) # remove url de imagens repetidas
   
   arq = open('img/links.txt','w+b')
   
   listalinkSrepetir = []
   for  l in arq.readlines():
      lslinks.append(l)   
   
   #print lslinks
   listalinkSrepetir = list(set(lslinks))
   for v in links:
      arq.write(v+"\t\n")
   arq.close()
   a.close()
   
   
geralinks()

#baixaImagens()

    
