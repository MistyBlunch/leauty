from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
app = Flask(__name__)
global subjectName

# Pagina principal
@app.route('/')
def index():
  return render_template(
    'index.html'
  )

# Pagina de busqueda
@app.route('/search', methods = ['POST', 'GET'])
def search():
  if request.method == 'POST':
    if request.form['subject'] != "":
      subjectName = request.form['subject'].lower()
      return redirect(url_for('results', subject=subjectName))
    else:
      return "No se ingresó ningún dato :c"
  # else:
  #   subjectName = request.args.get('subject')
  #   return redirect(url_for('results'))

  return render_template(
    'search.html'
  )

@app.route('/results/<subject>')
def results(subject):
  # El nombre de cada columna
  tHeads = ["Título", "Link", "Lenguaje", "Año", "Autor","Imagen"]
  subjectLen = len(subject)
  if " " in subject:
    subject = subject.replace(" ", "+") 
  if subjectLen > 1:
    page_link = 'http://libgen.io/search.php?&req=' + subject + '&phrase=1&view=detailed&column=def&sort=year&sortmode=DESC'

  page = urlopen(page_link)
  soup = BeautifulSoup(page, 'html.parser')

  # Find the table
  table_finder = soup.find_all(rules=re.compile("cols"))
  # For the link:
  princLink = 'http://libgen.io'
  # Limit number:  YOU CAN EDIT THAT
  limitNumber = 4
    
  # Título
  titleFind = soup.find_all(colspan=re.compile("2"))
  titleList = []
  quantity = 0
  for title in titleFind:
    if quantity <= limitNumber:
      titleList.append(title.text)
    quantity += 1

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

  # For the img
  imgFinder = soup.find_all(rowspan=re.compile("20"))
  quantity = 0
  imgList = []
  for td in imgFinder:
    quantity += 1
    if quantity <= limitNumber:
      imgSRC = td.find("a").find("img")['src']
      unionImg = princLink + imgSRC
      imgList.append(unionImg)

  return render_template (
    'results.html', 
    subjectSearch = subject, 
    link = page_link, 
    tHeads = tHeads,
    titleLists = titleList,
    linkLists = linkList,
    lanLists = lanList,
    ageLists = ageList,
    autorLists = autorList,
    imgLists = imgList
  ) 

# @app.route('/aboutUs')
# def aboutUs():
#     return 'About us :3'
 
# #  is not necesary
# @app.route('/aboutUs/<string:name>/')
# def getMember(name):
#     return name

@app.route('/<btn>')  #tipo de variable en < >
def backToHome(btn):
   if btn =='backHome':
      return redirect(url_for('index'))
#    else:
#    return redirect(url_for('hello_guest',guest = name))