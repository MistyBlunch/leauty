#!/usr/local/bin/python
# coding=utf-8
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
# from urllib2 import urlopen
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os, sys
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')

app = Flask(__name__)
global subjectName


#Error page
@app.errorhandler(404)
def page_not_found(error):
  return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def error_ocurred(error):
  return render_template('page_not_found.html'), 500

# Pagina principal
@app.route('/', methods = ['POST', 'GET'] )
def search():
  if request.method == 'POST':
    subjectForm = request.form['subject']
    optForm = request.form['opt-cat']

    whiteSpace = subjectForm.strip(' ')
    if subjectForm != "" and whiteSpace != "":
      subjectName = subjectForm.lower()
      return redirect(url_for(
        'results', subject=subjectName,
        option = optForm
        ))
    else:
      return "No se ingresó ningún dato :c"
  # else:
  #   subjectName = request.args.get('subject')
  #   return redirect(url_for('results'))

  return render_template(
    'index.html'
  )

@app.route('/results/<subject>/<option>')
def results(subject, option):
  # El nombre de cada columna
  tHeads = ["Título", "Link", "Lenguaje", "Año", "Autor","Imagen"]
  subjectLen = len(subject)
  if " " in subject:
    subject = subject.replace(" ", "+") 
  if subjectLen > 1:
    if option == 'anno':
      page_link ='http://libgen.io/search.php?&req=' + subject + '&phrase=1&view=detailed&column=def&sort=year&sortmode=DESC'
    elif option == 'defecto':
      page_link = 'http://libgen.io/search.php?req=' + subject + '&open=0&res=25&view=detailed&phrase=1&column=def'
    elif option == 'editorial':
      page_link = 'http://libgen.io/search.php?&req=' + subject + '&phrase=1&view=detailed&column=def&sort=publisher&sortmode=ASC'
    elif option == 'paginas':
      page_link = 'http://libgen.io/search.php?&req=' + subject + '&phrase=1&view=detailed&column=def&sort=pages&sortmode=DESC'
    else:
       page_link = 'page_not_found.html'
    
    page = urlopen(page_link)
    soup = BeautifulSoup(page, 'html.parser')

    # Find the table
    table_finder = soup.find_all(rules=re.compile("cols"))
    # For the link:
    princLink = 'http://libgen.io'
    # Limit number:  YOU CAN EDIT THAT
    limitNumber = 9
      
    # Título
    titleFind = soup.find_all(colspan=re.compile("2"))
    titleList = []
    quantity = 0
    for title in titleFind:
      if quantity <= limitNumber:
        titleList.append(title.text)
      quantity += 1
    minRange = len(titleList)  #Identifying the quantity of results

    # For the link
    linkFind = soup.find_all(colspan=re.compile("2"))
    linkList = []
    quantity = 0
    for link in linkFind:
      if quantity <= limitNumber:
        linkFinder = link.a['href']
        linkModified = linkFinder.replace('..', '')
        unionLink = princLink + linkModified
        linkList.append(unionLink)
      quantity += 1

    # For the language
    table_finder = soup.find_all(rules=re.compile("cols"))
    lanList = []
    quantity = 0
    counter = 0
    for tableLan in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limitNumber*2) + limitNumber:
        tdLan = tableLan.findAll("tr")
        if counter%2 != 0:
          tdLan = tdLan[6].findAll("td")[1]
          lanList.append(tdLan.text)
        else:
          del tableLan[counter]

    # For the Age
    table_finder = soup.find_all(rules=re.compile("cols"))
    quantity = 0
    counter = 0
    ageList = []
    for tableAge in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limitNumber*2) + limitNumber:
        trAge = tableAge.findAll("tr")
        if counter%2 != 0:
          tdAge = trAge[5].findAll("td")[1]
          ageList.append(tdAge.text)
        else:
          del tableAge[counter]   
    
    # For the Pages
    table_finder = soup.find_all(rules=re.compile("cols"))
    pagList = []
    quantity = 0
    counter = 0
    for tablePag in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limitNumber*2) + limitNumber:
        tdPag = tablePag.findAll("tr")
        if counter%2 != 0:
          tdPag = tdPag[6].findAll("td")[3]
          pagList.append(tdPag.text)
        else:
          del tablePag[counter]

    # For the autor
    autorFind = soup.find_all(colspan=re.compile("3"))
    counter = 0
    quantity = 0
    autorList = []
    for bAutor in autorFind:
      listAutor = bAutor.find_all("b")
      quantity += 1
      if quantity <= (limitNumber * 2) + limitNumber:
        if listAutor == []: 
            del autorFind[counter]
        else:
          finalAutors = listAutor[0]
          autorList.append(finalAutors.text)
        counter += 1 

    # For the publisher
    table_finder = soup.find_all(rules=re.compile("cols"))
    quantity = 0
    counter = 0
    editList = []
    for tableEdit in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limitNumber*2) + limitNumber:
        trEdit = tableEdit.findAll("tr")
        if counter%2 != 0:
          tdEdit = trEdit[4].findAll("td")[1]
          editList.append(tdEdit.text)
        else:
          del tableEdit[counter]

    # For the img
    imgFinder = soup.find_all(rowspan=re.compile("20"))
    quantity = 0
    imgList = []
    for td in imgFinder:
      if quantity <= limitNumber:
        imgSRC = td.find("a").find("img")['src']
        unionImg = princLink + imgSRC
        if unionImg == "http://libgen.io/covers/blank.png":
          unionImg = "https://s3.amazonaws.com/cdn.laborum.pe/mailer/beautyLib/sad.png"
        imgList.append(unionImg)
      quantity += 1

    return render_template (
      'results.html', 
      subjectSearch = subject, 
      link = page_link, 
      tHeads = tHeads,
      minRanges = minRange,
      optionSelect = option,
      
      titleLists = titleList,
      linkLists = linkList,
      lanLists = lanList,
      pagLists = pagList,
      ageLists = ageList,
      autorLists = autorList,
      editLists = editList,
      imgLists = imgList
    ) 

  # @app.route('/aboutUs')
  # def aboutUs():
  #     return 'About us :3'
  
  # #  is not necesary
  # @app.route('/aboutUs/<string:name>/')
  # def getMember(name):
  #     return name

  # @app.route('/<btn>')  #tipo de variable en < >
  # def backToHome(btn):
  #    if btn =='backHome':
  #       return redirect(url_for('index'))
  # #    else:
  # #    return redirect(url_for('hello_guest',guest = name))
