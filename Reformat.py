#!/usr/bin/env python
# coding: utf-8

# In[1]:
from tkinter import filedialog, Tk #pip install tkinter
import pandas as pd #pip install pandas
import numpy as np #pip install numpy
import random
import time
import zipfile #pip install zipfile
import pycountry #pip install pycountry
import pycountry_convert #pip install pycountry_convert
from langdetect import detect #pip install langdetect
from geopy.geocoders import Nominatim #pip install geopy
geolocator = Nominatim(user_agent="geoapiExercises")

# In[2]:
#Seleccion de archivo de FB/IG a ser procesado
root = Tk()
root.wm_attributes('-topmost',1)
root.withdraw()
accepted_filetypes = (("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"))
file_path = filedialog.askopenfilename(parent=root, filetypes=accepted_filetypes)
dataframe_to_transform = pd.read_csv(file_path, encoding="utf8")

# In[3]:
#Creacion de dataframe para realizar escritura de archivo formateado
columns = pd.DataFrame(['Query Id', 'Query Name', 'Date', 'Title', 'Url', 'Domain', 'Sentiment','Page Type', 'Language', 'Country Code', 'Continent Code', 'Continent','Country', 'City Code', 'Account Type', 'Added', 'Assignment', 'Author','Avatar', 'Category Details', 'Checked', 'City', 'Display URLs','Expanded URLs', 'Facebook Author ID', 'Facebook Comments','Facebook Likes', 'Facebook Role', 'Facebook Shares','Facebook Subtype', 'Full Name', 'Full Text', 'Gender', 'Hashtags','Impact', 'Impressions', 'Instagram Comments', 'Instagram Followers','Instagram Following', 'Instagram Interactions Count','Instagram Likes', 'Instagram Posts', 'Interest','Last Assignment Date', 'Latitude', 'Location Name', 'Longitude','Media Filter', 'Media URLs', 'Mentioned Authors', 'Original Url','Priority', 'Professions', 'Resource Id', 'Short URLs', 'Starred','Status', 'Subtype', 'Thread Author', 'Thread Created Date','Thread Entry Type', 'Thread Id', 'Thread URL','Total Monthly Visitors', 'Twitter Author ID', 'Twitter Channel Role','Twitter Followers', 'Twitter Following', 'Twitter Reply Count','Twitter Reply to', 'Twitter Retweet of', 'Twitter Retweets','Twitter Likes', 'Twitter Tweets', 'Twitter Verified', 'Updated','Reach (new)', 'Air Type', 'Blog Name', 'Broadcast Media Url','Broadcast Type', 'Content Source', 'Content Source Name', 'Copyright','Engagement Type', 'Is Syndicated', 'Item Review', 'Linkedin Comments','Linkedin Engagement', 'Linkedin Impressions', 'Linkedin Likes','Linkedin Shares', 'Linkedin Sponsored', 'Linkedin Video Views','Media Type', 'Page Type Name', 'Parent Blog Name', 'Parent Post Id','Pub Type', 'Publisher Sub Type'
'Rating', 'Reddit Author Awardee Karma','Reddit Author Awarder Karma', 'Reddit Author Karma', 'Reddit Comments','Reddit Score', 'Reddit Score Upvote Ratio', 'Region', 'Region Code','Root Blog Name', 'Root Post Id', 'Subreddit', 'Subreddit Subscribers','Weblog Title'])
columns = columns.transpose()
column_dict, column_list = dict(), list()

dataframe_rows = [[None] * len(columns.columns) for _ in range(len(dataframe_to_transform[1:]))]
for column in columns.iloc[0]:
    column_list.append(column)
    column_dict[column] = column
formatted_file = pd.DataFrame(dataframe_rows, columns=column_list)














# In[4]:
def createID():
    """
    Creacion de ID -aleatorio- para llenar columna de queryID. Cada ejecucion arroja un valor distinto
    """
    numbers = list(range(10))
    id = ""
    for n in range(10):
        id += str(numbers[random.randint(0,9)])
    return id

def convertDate(datee, added_date):
    """
    Transformacion de fecha de creacion de pieza de conversacion a formato BW-GEA
    El valor por default es la fecha de creacion del archivo de IG. Dentro de la funcion se formatea la fecha
    """
    try:
        if datee != "":
            date = time.strftime('%Y-%m-%d %H:%M:%S.0', time.localtime(int(datee[0:-5])))
        else:
            date = added_date[0:10]+  " " +added_date[11:-7]
        return date
    except: return added_date[0:10]+ " " +added_date[11:-7]

def generateTitle(post_text):
  """
  Obtencion de los primeros 200 caracteres dentro de la pieza de conversacion, para la columna -Title-
  """
  try:
    post_text = post_text.replace("\n", " ")
    post_text = post_text.replace("\t", " ")
    post_text = post_text.replace("\v", " ")
    post_text = post_text.replace("\f", " ")
    post_text = post_text.replace("\r\n", " ")  
    words = post_text.split(" ")
    characters_count = 0
    title = ""
    for word in words:
      if characters_count + len(word) < 280:
        title += word + " "
        characters_count += len(word) + 1
      else: break
  except: title = ""
  return title

global current_code
current_code = ""
def generateIGUrl(post_id):
    """
    Generacion de link para la publicacion de Instagram
    """   
    global current_code
    if type(post_id) != float:
        link = f"http://www.instagram.com/p/{post_id}"
        current_code = post_id
    else:
        link = f"http://www.instagram.com/p/{current_code}"
    return link

global current_thread_author
current_thread_author = ""
def getThreadAuthor(post_type, post_author):
    """
    Definicion de creador/autor de hilo; en el caso de IG, es la publicacion original con imagen
    """
    global current_thread_author
    if post_type == "post":
        current_thread_author = post_author
        thread_author = ""
    elif post_type == "comment":
        thread_author = current_thread_author
    else: thread_author = current_thread_author
    return thread_author

global current_thread_date
current_thread_date = ""
def getThreadDate(post_type, post_date, default):
    """
    Definicion de fecha de creacion de hilo; en el caso de IG, es la publicacion original con imagen.
    El valor por default es la fecha de creacion del archivo de IG.
    """
    global current_thread_date
    if post_date == "": date = default 
    else:
        try:
            if post_type == "post":
                current_thread_date = time.strftime('%Y-%m-%dT%H:%M:%S.000+0000', time.localtime(int(post_date[0:-5])))
                date = ""
            elif post_type == "comment":    
                date = current_thread_date
        except: date = default
    return date

def getUpdateDateFormatted(post_date, default):
    """
    Definicion de fecha de actualizacion de publicacion/pieza de conversacion.
    El valor por default es la fecha de creacion del archivo de IG.
    """
    try:
        date = time.strftime('%Y-%m-%dT%H:%M:%S.000+0000', time.localtime(int(post_date[0:-5])))
    except: date = default
    return date

global current_thread_id
current_thread_id = ""
def getThreadID(post_type, post_id):
    """
    Definicion de ID de hilo; en el caso de IG, es la publicacion original con imagen.
    """
    global current_thread_id
    if post_type == "post":
        current_thread_id = post_id
        id = 0
    elif post_type == "comment":
        id = current_thread_id
    else: id = current_thread_id
    return id

def generateDomain(domain):
    """
    Generacion de dominio para columna de archivo; para IG es instagram.com
    """
    return domain+".com"

def generatePageType(type):
    return type

def identifyTextLanguage(post_text):
    """
    Identificacion de idioma de la pieza de conversacion. 
    En caso de no ser poisble, se declara como "Indetectable"
    """
    try:
        language = detect(post_text)
    except:
        language = "Undetectable"
    return language

def identifyHashtags(post_text):
  """
  Identificacion de hashtags/tendencias dentro de las piezas de conversacion
  """
  try:
    words_in_text = post_text.split(" ")
    words_in_text = [x for x in words_in_text if len(x) > 1]
    if len(words_in_text) == 0: return ""
    hashtags = [x for x in words_in_text if x[0] == "#"]
    if len(hashtags) == 0: return ""
    hashtag_list = ""
    for h in hashtags:
        if h is hashtags[-1]:
          hashtag_list += h.lower()
        else:
            hashtag_list += h.lower() + ", "
  except: hashtag_list = ""
  return hashtag_list

def getFullName(profile_handle, user_name):
    """
    Creacion de valor para columna -Full Name-, conformada por handle y nombre completo del perfil
    """
    if type(user_name) == float: return f"{profile_handle} ({profile_handle})"
    return f"{profile_handle} ({user_name})"

def identifyExpandedURLs(post_text): 
  """
  Obtencion de URLs -normales-, excluyendo aquellos categorizados como cortos.
  """
  try:
    post_text = post_text.replace("\n", " ")
    post_text = post_text.replace("  ", " ")
    words = post_text.split(" ")
    expandend_urls = [x for x in words if "http" == x[0:4] or "www" == x[0:3] and not "bit.ly" in x]
    urls_list = ""
    for h in expandend_urls:
        if h is expandend_urls[-1]:
          urls_list += h
        else:
            urls_list += h + ", "
  except: urls_list = ""
  return urls_list

def identifyShortURLs(post_text):
  """
  Obtencion de URLs de tipo -corto-, como lo son bit.ly, goo.gl, ow.ly, youtu.be
  """
  try:
    post_text = post_text.replace("\n", " ")
    post_text = post_text.replace("  ", " ")
    words = post_text.split(" ")
    expandend_urls = [x for x in words if "bit.ly" in x or "goo.gl" in x or "g.co" in x or "ow.ly" in x or "t.co" in x or "w.wiki" in x or "youtu.be" in x or "tinyurl" in x ]
    urls_list = ""
    for h in expandend_urls:
        if h is expandend_urls[-1]:
          urls_list += h
        else:
            urls_list += h + ", "
  except:  urls_list = ""
  return urls_list

def generateGeoInfo(longitude, latitude):
    """
    Obtencion de toda la informacion geografica referente a la pieza de conversacion.
    Se utiliza API de Nominatim para la obtencion de la informacion
    """
    continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'}
    try:
        location = geolocator.reverse(str(latitude)+","+str(longitude)).raw["address"]
        country = location.get("country")
        try: city = location.get("city")
        except: city = ""
        country_code = pycountry.countries.get(alpha_2=location.get("country_code"))
        country_code_3 = country_code.alpha_3
        country_code_2 = country_code.alpha_2
        try:
            city_code = country_code_3+"."+location.get("state")+"."+location.get("region")
        except:
            city_code = country_code_3+"."+country_code_3+"."+country_code_3
        continent_name = pycountry_convert.country_alpha2_to_continent_code(country_code_2)
        continent_name = continents[continent_name]
        continent_code = continent_name.upper()
        try: region = location.get("region")
        except: region = ""
        try: region_code = country_code_3+"."+region
        except: region_code = ""
        return [country_code_3, continent_code, continent_name, country, city_code, city, region, region_code]
    except: return ["", "", "", "", "", "", "", ""]

def getMentionedAuthors(post_text):
  """
  Identificacion de handles de IG mencionados en publicaciones/comentarios scrapeados
  """
  try:
    words = post_text.split(" ")
    words = [x for x in words if len(x) > 1]
    mentioned_authors_list = [w for w in words if w[0] == "@"]
    mentioned_authors = ""
    for author in mentioned_authors_list:
        if author is mentioned_authors_list[-1]:
              mentioned_authors += author
        else:
            mentioned_authors += author + ", "
  except: mentioned_authors = ""
  return mentioned_authors

def engagementType(post_type):
    """
    Definicion de tipo de publicacionde
    """
    if post_type == "post": return ""
    elif post_type == "comment": return "COMMENT"
    else: return ""

# In[5]:


#Celda de ejecucion de la transformacion 
answer = ""
while answer != "y" and answer != "n":
    answer = input("Desea implementar obtencion de info Geografica? (y/n)")


query_name = dataframe_to_transform.head(1)["hashtag"].values[0] #Hashtag/Tema scrapeado
added_date = dataframe_to_transform.head(1)["scraped_datetime"].values[0]
added_date = added_date.split(" ")[0] + "T" + added_date.split(" ")[1] + ".000+0000" #Fecha de scrapeo
query_id = createID() #DFefinicion del ID de la query
info = dataframe_to_transform[1:]
for index, row in (formatted_file.iterrows()):
    formatted_file._set_value(index, "Query Id", query_id)
    formatted_file._set_value(index, "Query Name", query_name)
    formatted_file._set_value(index, "Date", convertDate(str(info.iloc[index]["created_at_utc"]),added_date))
    formatted_file._set_value(index, "Title", generateTitle(info.iloc[index]["text"]))
    #formatted_file._set_value(index, ["Url", "Original Url"], generateIGUrl(info.iloc[index]["code"]))
    formatted_file._set_value(index, "Domain", generateDomain("instagram"))
    formatted_file._set_value(index, "Sentiment Brandwatch", "neutral")
    formatted_file._set_value(index, "Page Type", generatePageType("instagram"))
    formatted_file._set_value(index, "Language", identifyTextLanguage(info.iloc[index]["text"]))
    if answer == "y":
        if not np.isnan(info.iloc[index]["loc_lat"]) or not np.isnan(info.iloc[index]["loc_lng"]):
            geo_information = generateGeoInfo(info.iloc[index]["loc_lng"], info.iloc[index]["loc_lat"])
            formatted_file._set_value(index, "Country Code", geo_information[0])
            formatted_file._set_value(index, "Continent Code", geo_information[1])
            formatted_file._set_value(index, "Continent", geo_information[2])
            formatted_file._set_value(index, "Country", geo_information[3])
            formatted_file._set_value(index, "City Code", geo_information[4])
            formatted_file._set_value(index, "City", geo_information[5])
            formatted_file._set_value(index, "Region", geo_information[6])
            formatted_file._set_value(index, "Region Code", geo_information[7])
            formatted_file._set_value(index, "Location Name", geo_information[4])
    formatted_file._set_value(index, "Account Type", "individual")
    formatted_file._set_value(index, "Added", added_date)
    formatted_file._set_value(index, "Author", info.iloc[index]["us_username"])
    formatted_file._set_value(index, "Avatar", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9dsmG0mf7G_IbvdSFt7UkWhDwnOsBjtbEmQ&usqp=CAU")
    formatted_file._set_value(index, "Checked", "false")
    formatted_file._set_value(index, "Expanded URLs", identifyExpandedURLs(info.iloc[index]["text"]))
    #formatted_file._set_value(index, ["Facebook Comments", "Facebook Likes", "Facebook Shares", "Twitter Followers", "Twitter Following", "Twitter Reply Count", "Twitter Retweets", "Twitter Likes", "Twitter Tweets", "Linkedin Comments", "Linkedin Engagement", "Linkedin Impressions", "Linkedin Likes", "Linkedin Shares", "Linkedin Video Views"], 0)
    #formatted_file._set_value(index, ["Full Name", "Weblog Title"], getFullName(info.iloc[index]["us_username"], info.iloc[index]["us_full_name"]))
    formatted_file._set_value(index, "Full Text", info.iloc[index]["text"])
    formatted_file._set_value(index, "Hashtags", identifyHashtags(info.iloc[index]["text"]))
    formatted_file._set_value(index, "Short URLs", identifyShortURLs(info.iloc[index]["text"]))
    formatted_file._set_value(index, "Thread Author", getThreadAuthor(info.iloc[index]["type"],info.iloc[index]["us_username"]))
    formatted_file._set_value(index, "Thread Created Date", getThreadDate(info.iloc[index]["type"],str(info.iloc[index]["created_at_utc"]), added_date))
    formatted_file._set_value(index, "Thread Id", getThreadID(info.iloc[index]["type"],info.iloc[index]["pk"]))
    formatted_file._set_value(index, "Gender", "unknown")
    formatted_file._set_value(index, "Impact", 0.0)
    formatted_file._set_value(index, "Impressions", 0) #Impressions OWN Implementation
    formatted_file._set_value(index, "Instagram Comments", info.iloc[index]["comment_count"])
    formatted_file._set_value(index, "Instagram Followers", 0)
    formatted_file._set_value(index, "Instagram Following", 0)
    formatted_file._set_value(index, "Instagram Interactions Count", 0)
    formatted_file._set_value(index, "Instagram Likes", info.iloc[index]["like_count"]) 
    formatted_file._set_value(index, "Instagram Posts", 0)
    formatted_file._set_value(index, "Latitude", info.iloc[index]["loc_lat"])
    formatted_file._set_value(index, "Longitude", info.iloc[index]["loc_lng"])
    formatted_file._set_value(index, "Mentioned Authors", getMentionedAuthors(info.iloc[index]["text"]))
    formatted_file._set_value(index, "Resource Id", info.iloc[index]["pk"])
    formatted_file._set_value(index, "Starred", "false")
    formatted_file._set_value(index, "Thread Entry Type", info.iloc[index]["type"])
    formatted_file._set_value(index, "Total Monthly Visitors", 6000000000)
    formatted_file._set_value(index, "Twitter Verified", "false")
    formatted_file._set_value(index, "Updated", getUpdateDateFormatted(str(info.iloc[index]["created_at_utc"]), added_date))
    formatted_file._set_value(index, "Reach (new)", 0) #Faltaria sacar numero de seguidores
    formatted_file._set_value(index, "Content Source", "instagram")
    formatted_file._set_value(index, "Content Source Name", "Instagram")
    formatted_file._set_value(index, "Engagement Type", engagementType(str(info.iloc[index]["type"])))
    #formatted_file._set_value(index, ["Is Syndicated", "Item Review", "Linkedin Sponsored"], "false")
    formatted_file._set_value(index, "Linkedin Video Views", 0)
    formatted_file._set_value(index, "Page Type Name", "Instagram")
    formatted_file._set_value(index, "Pub Type", "Instagramstream")
    if int(index%100)==0:
        print("Procesando " + str(index)+ " filas de "+ str(len(formatted_file))+"...")

    
# %%Guadar en un archivo
query_name = query_name+'_'+str(time.strftime("%d%m%y"))
encabezado = pd.DataFrame(['"Report:","Bulk Mentions Download"','"Brand:","Encabezado_Por_Default"','"From:","Sat Jan 01 00:00:00 UTC 2020"','"To:","Wed Dec 31 00:00:00 UTC 2031"','"Label:","Nombre_Por_Default"','"Linea6:","Se pone solamente para cumplir las primeras 6 lineas"'])
encabezado.to_csv(f"./{query_name}.csv",header=False, index=False, mode="a")
pd.DataFrame.to_csv(formatted_file, f"{query_name}.csv", index=False, mode="a")

#Crear Zip
zip = zipfile.ZipFile(f"./{query_name}.zip",'w')
zip.write(f"./{query_name}.csv")
zip.close()
