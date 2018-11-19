# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def myFunc():
  # Write a subject
  subject = "discretas"
  subjectLen = len(subject)

  if " " in subject:
    subject = subject.replace(" ", "+")

  #-----------------------------------Conditions---------------------------------------------
  if subjectLen > 1:
    # Principal configuration
    # page_link ='http://libgen.io/search.php?req=' + subject + '&open=0&res=25&view=detailed&phrase=1&column=def'
    page_link = 'http://libgen.io/search.php?&req=' + subject + '&phrase=1&view=detailed&column=def&sort=year&sortmode=DESC'

    page = urlopen(page_link)
    soup = BeautifulSoup(page, 'html.parser')

    # Principal Variables
    # For the table
    table_finder = soup.find_all(rules=re.compile("cols"))
    # For the link:
    princLink = 'http://libgen.io'
    # Limit number:  YOU CAN EDIT THAT
    limitNumber = 4
    # ----------------------------------------------------------------------------------------

    # For the title
    titleFind = soup.find_all(colspan=re.compile("2"))
    titleList = []
    quantity = 0
    for title in titleFind:
      if quantity <= limitNumber:
        titleList.append(title.text)
      quantity += 1
    # -----------------------------------------------------------------

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

    # -----------------------------------------------------------------

    # For the language
    table_finder = soup.find_all(rules=re.compile("cols"))
    quantity = 0
    counter = 0
    lanList = []
    for tableLan in table_finder:
      counter += 1
      quantity += 1
      if quantity <= limitNumber*2:
        tdLan = tableLan.findAll("tr")
        if counter%2 != 0:
          tdLan = tdLan[6].findAll("td")[1]
          lanList.append(tdLan.text)
        else:
          del tableLan[counter]
    # -----------------------------------------------------------------


    # For the Age
    table_finder = soup.find_all(rules=re.compile("cols"))
    quantity = 0
    counter = 0
    ageList = []
    for tableAge in table_finder:
      counter += 1
      quantity += 1
      if quantity <= limitNumber*2 :
        trAge = tableAge.findAll("tr")
        if counter%2 != 0:
            tdAge = trAge[5].findAll("td")[1]
            ageList.append(tdAge.text)
        else:
            del tableAge[counter]
    # -----------------------------------------------------------------

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
    # -----------------------------------------------------------------

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
    # -----------------------------------------------------------------
  else:
    print("Ingrese un texto que contenga más de un caracter")
