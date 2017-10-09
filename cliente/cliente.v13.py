#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Programa responsável por enviar imagens via POST para servidor
Autores: Pablo Souza, Vitor Rezende
Nome do Arquivo: cliente.v13.py
'''
import glob
import requests
import socket

import time
HOST='127.0.0.1'
PORT=5007

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
s.connect((HOST,PORT))
time.sleep(1)
for ar in glob.glob('img/*'): #varre o diretorio pegando todas as imagens
   print ar
   try:
       
      subtipo = ar.split('.')[-1]      
      print ar
      
      if subtipo == "py": #tira o arquivo dos links e o arquivo do cliente do envio, para enviar so as imagens
         print ""
      else:
	 arq=open(ar,'rb')
         print "POST / HTTP/1.1\r\n"+ar
         cabecalho ="""POST / HTTP/1.1\r\nHost:"""+HOST+"""\r\nUser-Agent: cliente.v13\r\nConnection: keep-alive\r\nContent-Type: multipart/form-data; boundary="#_43efr_#\n"
[Full request URI: """+HOST+"""]
MIME Multipart Media Encapsulation, Type: multipart/form-data
[Type: multipart/form-data]      
Encapsulated multipart part:  (imagem/"""+subtipo+""")
Content-Disposition: form-data; name="file"; filename=\""""+ar+"""\"
Content-Type:  imagem/"""+subtipo+"""\r\n\r\n#_43efr_#"""
        
         s.send(cabecalho)
         time.sleep(0.01)
         for i in arq.readlines():        
           s.send(i)
           time.sleep(0.01)
           
         s.send('\r\n\r\n#_43efr_#fin\r\n')
         time.sleep(0.02)
         resposta = s.recv(1024)
         print resposta
         arq.close()
      
   except IOError:
      print "Erro ao abrir o arquivo"
s.close()

