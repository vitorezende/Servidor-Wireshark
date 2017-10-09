#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Programa responsável por criar servidor e tratar requisições get e post
Autores: Pablo Souza , Vitor Rezende
Nome do Arquivo: servidor.py
'''

import socket
import thread
import time
import os
HOST = '127.0.0.1'              # Endereco IP do Servidor
PORT = 5007        # Porta que o Servidor esta


def extrai_nome_doc(req):
        
	return req.split()[1][1:]				#Quebro a requisicao escolho a parte que contem o nome do arquivo e tiro o primeiro elemento que eh o barra
	
def constroi_resposta(doc):
	res = "HTTP/1.1 200 OK\r\n\r\n"
	#print doc
	try:
		if doc == "":
			gera_html()
			narq = "index.html"
			f = open(narq)
			dados = f.read()
			f.close()
		else:
			narq = doc
			f = open(narq)
			dados = f.read()
			f.close()
	except:
		f = open("notfound.html")
		dados = f.read()
		res = "HTTP/1.1 404 Not Found\r\n\r\n"
		f.close()
	res = res + dados
	return res
      

def gera_html():
  
  
   file_links = open('img/links.txt')
   aux = ''
   linkim=''
   
   for l in file_links.readlines():
    if '\r\n' in l:
      continue
    else:
      nfile = l.split("/")[-1]
      aux =nfile[:nfile.index('.')+4]
      linkim=linkim+ """\n<div class='box'><a href="""+l+"""><img src=\"img/"""+aux+"""\" height=\"100px\" width=\"150px\"></a> </div>\n"""
     
    
   page = "<html>\n<head>\n<title>\nImagens\n</title>\n<link rel='stylesheet'   href='img/style.css' type='text/css'  />\n</head>\n"
   
   page = page+ "\n<body>\n<div id='container'>\n<h1>TRABALHO DE REDES : SERVIDOR HTTP</h1>\n<h2>GRUPO: PABLO SOUZA , VITOR REZENDE</h2><br><br><br>\n"+linkim+"\n</div>\n</body>\n</html>"
   arquivo = open('index.html', 'w')
   arquivo.write(page)
   arquivo.close()   
      
      
      
def conectado(con, cliente):
   print 'inicio conexao com o cliente ', cliente
   arq = ''   
   iBoundary = ''
   i=1
   while i:
        try:
	      req_http = con.recv(1024)     
	      if not req_http:
                print 'sucesso'
                con.send("HTTP/1.1 200 OK\r\n\r\n")
                
		break
		
            
	      #verifica que tipo de requisicao e http POST ou http GET
	      if "POST" in req_http:
		  #print req_http
		  if "boundary=" in req_http:
		     iBoundary = req_http[req_http.index('boundary=\"')+10:req_http.index('boundary=\"')+19]
                     
                     
                     
                     if 'filename' in req_http:
		      
		      b = req_http[req_http.index('filename=\"')+10:]		    
		      ext = b.split("\"")[0]
		      
		      arq = open(ext,'wb')
		     
		      valor =req_http.split(iBoundary)[2]		      
		     
		      arq.write(valor)
              #se iBoundary tiver no req_http, significa que o segmento contem o inicio do arquivo
              
		  
		    
	      elif iBoundary+"fin" in req_http: #VERIFICA SE EH O FIM DE ARQUIVO
		
		a = req_http.split(iBoundary)[0]
		
		arq.write(a)
		con.send("HTTP/1.1 200 OK\r\n\r\n")
		#time.sleep(0.01)
		 #ENVIA UMA RESPOSTA DE SUCESSO PARA O CLIENTE
	      elif "GET" in req_http:
		 #print req_http
		 #gera_html()
		 if "HTTP/1.1" in req_http:
	            doc = extrai_nome_doc(req_http)
	            #print "Nome do arquivo:", doc
	            resposta = constroi_resposta(doc)
	            con.send(resposta)
	            #arq.close()	
                    i=0
                 #thread.exit()
	      else:
		 
		 arq.write(req_http)
		 
	         
	        
        except IOError: 
	   print "erro no arquivo"
   print 'Finalizando conexao do cliente', cliente
   if arq != '':
      arq.close()
   
   con.close()
   thread.exit()
   
   
#gera_html()
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(4)



while 1:
    con, cliente = tcp.accept()   
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()