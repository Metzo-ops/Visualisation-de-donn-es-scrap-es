from cProfile import label
import os,psycopg2,requests,csv,re,flask
from flask import Flask, render_template
from bs4 import BeautifulSoup


app = Flask(__name__)

conn = psycopg2.connect(
        host="localhost",
        database="SCRAP_JUMIA",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])
cur = conn.cursor()  

url_jumia_maroc = "https://www.jumia.ma/ensembles-costumes-hommes/"
url_jumia = "https://www.jumia.sn/catalog/?q=ensemble+costume+homme"
url_jumia_ci = "https://www.jumia.ci/catalog/?q=costume+complet+homme"

page_jumia_maroc = requests.get(url_jumia_maroc)
page_jumia_ci = requests.get(url_jumia_ci)
page_jumia = requests.get(url_jumia)

soup_jumia_maroc = BeautifulSoup(page_jumia_maroc.text, "html.parser")
soup_jumia_ci = BeautifulSoup(page_jumia_ci.text, "html.parser")
soup_jumia = BeautifulSoup(page_jumia.text, "html.parser")


liste_photo_jum_sn = []
liste_detai_jum_sn = []
liste_prix_jum_sn = []

images_jumia = soup_jumia.find_all(class_="img")
for image in images_jumia:
    photos_jumia = image["data-src"]
    liste_photo_jum_sn.append(photos_jumia)

details_jumia = soup_jumia.find_all(class_="name") 
for detail in details_jumia:
    description = detail.contents[0]
    liste_detai_jum_sn.append(description)
prix_jumia = soup_jumia.find_all(class_="prc")
for pri in prix_jumia:
    prices = pri.contents[0]
    price = re.sub(r"\s","",prices)
    price = price.replace("FCFA","")
    liste_prix_jum_sn.append(price)    

liste_photo_mar =[]

jum_mar = soup_jumia_maroc.find_all(class_="img")
for img in jum_mar:
    if img["data-src"]!="":
        photo_mar_jum = img["data-src"]
        liste_photo_mar.append(photo_mar_jum)

liste_desc_mar = []

desc_mar = soup_jumia_maroc.find_all(class_="name")
for desc in desc_mar:
    try:
        if desc.contents != "":
            description = desc.contents[0]
            liste_desc_mar.append(description)
    except:
        pass        

liste_prix_mar = []

prix_mar = soup_jumia_maroc.find_all(class_="prc")
for pri in prix_mar:
    try:
        prices = pri.contents[0]
        liste_prix_mar.append(prices)
    except:
        pass    

liste_photo_ci = []
img_ci = soup_jumia_ci.find_all(class_="img")
for img in img_ci:
    photos_ci = img["data-src"]
    liste_photo_ci.append(photos_ci)
liste_detail_ci = []
desc_ci = soup_jumia_ci.find_all(class_="name")    
for det in desc_ci:
    descr_ci = det.contents[0]
    liste_detail_ci.append(descr_ci)
liste_prix_ci = []   
pri_ci = soup_jumia_ci.find_all(class_="prc") 
for pr in pri_ci:
    price_ci = pr.contents[0]
    liste_prix_ci.append(price_ci)

liste_prix_mar_valide = []
for m in liste_prix_mar:
    a = m.split(" ")
    try:
        cfa = float(a[0])*62.66
        cfa = round(cfa)
        liste_prix_mar_valide.append(cfa)
    except:
        pass 
liste_prix_jum_sn_valide = []    
for n in liste_prix_jum_sn:
    n = n.replace("FCFA","") 
    liste_prix_jum_sn_valide.append(n)
liste_prix_ci_valide = []    
for e in liste_prix_ci:
    e = e.replace("FCFA","").replace(",","")
    liste_prix_ci_valide.append(e)
  


# for j in range(10):
#     photos_maroc = liste_photo_mar[j]
#     detail_maroc = liste_desc_mar[j]
#     prix_maroc = liste_prix_mar_valide[j]
#     photo_sn = liste_photo_jum_sn[j]
#     detail_sn = liste_detai_jum_sn[j]
#     prix_sn = liste_prix_jum_sn_valide[j]
#     toff_ci = liste_photo_ci[j]
#     descrb_ci = liste_detail_ci[j]
#     prix_ci = liste_prix_ci_valide[j]

# PULLING DATAS IN THE DB
    # try:
    #     cur.execute("INSERT INTO jumia_maroc(images_jum_mar,details_jum_mar,prices_jum_mar) VALUES(%s,%s,%s)",(photos_maroc,detail_maroc,prix_maroc))
    #     cur.execute("INSERT INTO jumia(images_jumia,details_jumia,prices_in_CFA_jumia) VALUES(%s,%s,%s)",(photo_sn,detail_sn,prix_sn))
    
    #     cur.execute("INSERT INTO jumia_ci(images_jum_ci,details_jum_ci,prices_jum_ci) VALUES(%s,%s,%s)",(toff_ci,descrb_ci, prix_ci))
    # except:
    #     pass
    

# PULLING UP DATAS FROM THE DB
liste_visual_desc_sn = []
liste_visual_prix_sn = []
liste_visual_desc_maroc = []
liste_visual_prix_maroc = []
liste_visual_desc_ci = []
liste_visual_prix_ci = []
mpo = "select details_jumia from jumia"
cur.execute(mpo)
desc_prod_jum_sn = cur.fetchall()


for i in desc_prod_jum_sn:
    liste_visual_desc_sn.append(i[0])

sprix = "select prices_in_cfa_jumia from jumia"
cur.execute(sprix)
prix_prod_jum_sn = cur.fetchall()

for j in prix_prod_jum_sn:
    liste_visual_prix_sn.append(j[0])

kol = "select details_jum_mar from jumia_maroc"
cur.execute(kol)
desc_prod_jum_maroc = cur.fetchall()
for k in desc_prod_jum_maroc:
    liste_visual_desc_maroc.append(k[0])

lok = "select prices_jum_mar from jumia_maroc"
cur.execute(lok)
prices_prod_jum_mar = cur.fetchall()
for l in prices_prod_jum_mar:
    liste_visual_prix_maroc.append(l[0])

cod = "select details_jum_ci from jumia_ci"
cur.execute(cod)
desc_prod_jum_ci = cur.fetchall()
for m in desc_prod_jum_ci:
    liste_visual_desc_ci.append(m[0])
doc = "select prices_jum_ci from jumia_ci"
cur.execute(doc)
prices_prod_jum_ci = cur.fetchall()
for n in prices_prod_jum_ci:
    liste_visual_prix_ci.append(n[0])

# DATAS VIZUALISATION
@app.route("/visualization")
def visual_sn():
    return render_template("jumia_sn.html", x_values = liste_visual_desc_sn, y_values = liste_visual_prix_sn,x_x_values = liste_visual_desc_maroc, y_y_values = liste_visual_prix_maroc,x_x_x_values = liste_visual_desc_ci, y_y_y_values =liste_visual_prix_ci)


if __name__ == '__main__':
    app.run(debug =True,port = 5000)



       
# conn.commit()

cur.close()
conn.close() 
