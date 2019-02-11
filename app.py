#!/usr/local/bin/python
# coding=utf-8
from flask import Flask, redirect, render_template, request, url_for
# from urllib2 import urlopen
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
global subject_name


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
    subject_form = request.form['subject']
    opt_form = request.form['opt-cat']

    white_space = subject_form.strip(' ')
    if subject_form != "" and white_space != "":
      subject_name = subject_form.lower()
      return redirect(url_for(
        'results', subject=subject_name,
        option = opt_form
        ))
    else:
      return "No se ingresó ningún dato :c"
  # else:
  #   subject_name = request.args.get('subject')
  #   return redirect(url_for('results'))

  return render_template(
    'index.html'
  )

@app.route('/results/<subject>/<option>')
def results(subject, option):
  # El nombre de cada columna
  t_heads = ["Título", "Link", "Lenguaje", "Año", "Autor","Imagen"]
  subject_len = len(subject)
  if " " in subject:
    subject = subject.replace(" ", "+") 
  if subject_len > 1:
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
    princ_link = 'http://libgen.io'
    # Limit number:  YOU CAN EDIT THAT
    limit_number = 9
      
    # Título
    title_find = soup.find_all(colspan=re.compile("2"))
    title_list = []
    quantity = 0
    for title in title_find:
      if quantity <= limit_number:
        title_list.append(title.text)
      quantity += 1
    min_range = len(title_list)  #Identifying the quantity of results

    # For the link
    link_find = soup.find_all(colspan=re.compile("2"))
    link_list = []
    quantity = 0
    for link in link_find:
      if quantity <= limit_number:
        link_finder = link.a['href']
        link_modified = link_finder.replace('..', '')
        union_link = princ_link + link_modified
        link_list.append(union_link)
      quantity += 1

    # For the language
    table_finder = soup.find_all(rules=re.compile("cols"))
    lan_list = []
    quantity = 0
    counter = 0
    for table_lan in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limit_number*2) + limit_number:
        td_lan = table_lan.findAll("tr")
        if counter%2 != 0:
          td_lan = td_lan[6].findAll("td")[1]
          lan_list.append(td_lan.text)
        else:
          del table_lan[counter]

    # For the Age
    table_finder = soup.find_all(rules=re.compile("cols"))
    quantity = 0
    counter = 0
    age_list = []
    for table_age in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limit_number*2) + limit_number:
        trAge = table_age.findAll("tr")
        if counter%2 != 0:
          td_age = trAge[5].findAll("td")[1]
          age_list.append(td_age.text)
        else:
          del table_age[counter]   
    
    # For the Pages
    table_finder = soup.find_all(rules=re.compile("cols"))
    pag_list = []
    quantity = 0
    counter = 0
    for table_pag in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limit_number*2) + limit_number:
        td_pag = table_pag.findAll("tr")
        if counter%2 != 0:
          td_pag = td_pag[6].findAll("td")[3]
          pag_list.append(td_pag.text)
        else:
          del table_pag[counter]

    # For the autor
    autor_find = soup.find_all(colspan=re.compile("3"))
    counter = 0
    quantity = 0
    autor_list = []
    for b_autor in autor_find:
      list_autor = b_autor.find_all("b")
      quantity += 1
      if quantity <= (limit_number * 2) + limit_number:
        if list_autor == []: 
            del autor_find[counter]
        else:
          final_autors = list_autor[0]
          autor_list.append(final_autors.text)
        counter += 1 

    # For the publisher
    table_finder = soup.find_all(rules=re.compile("cols"))
    quantity = 0
    counter = 0
    edit_list = []
    for table_edit in table_finder:
      counter += 1
      quantity += 1
      if quantity <= (limit_number*2) + limit_number:
        tr_edit = table_edit.findAll("tr")
        if counter%2 != 0:
          td_edit = tr_edit[4].findAll("td")[1]
          edit_list.append(td_edit.text)
        else:
          del table_edit[counter]

    # For the img
    img_finder = soup.find_all(rowspan=re.compile("20"))
    quantity = 0
    img_list = []
    for td in img_finder:
      if quantity <= limit_number:
        img_src = td.find("a").find("img")['src']
        union_img = princ_link + img_src
        if union_img == "http://libgen.io/covers/blank.png":
          union_img = "https://s3.amazonaws.com/cdn.laborum.pe/mailer/beautyLib/sad.png"
        img_list.append(union_img)
      quantity += 1

    return render_template (
      'results.html', 
      subject_search = subject, 
      link = page_link, 
      t_heads = t_heads,
      min_ranges = min_range,
      optionSelect = option,
      
      title_lists = title_list,
      link_lists = link_list,
      lan_lists = lan_list,
      pag_lists = pag_list,
      age_lists = age_list,
      autor_lists = autor_list,
      edit_lists = edit_list,
      img_lists = img_list
    ) 

  
