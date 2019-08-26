# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:21:17 2019

@author: afafe
"""
###A USER HAS TO RECIEVE AS A PROPS :AND SIZES FRENCH SIZES!!!!!!

#open categories sheet
import pandas as pd
sizes_sheet= {'men': pd.read_excel("C:\\Users\\afafe\\Desktop\\stage\\taille.xlsx", sheet_name='H', header=1, dtype={'Vestes FR':str, 'Vestes US':str, 'Vestes IT':str, 'Vestes UK':str, 'Vestes Jap':str, 'Chemises FR':str, 'Chemises US':str, 'Pantalons FR':str, 'Pantalons US':str, 'Pantalons IT':str}),\
             'women': pd.read_excel("C:\\Users\\afafe\\Desktop\\stage\\taille.xlsx", sheet_name='F', header=1, dtype={'Tops FR':str, 'Tops US':str, 'Tops IT':str, 'Tops UK':str, 'Tops JAP':str, 'Pantalons FR':str, 'Pantalons US':str}),\
             'shoes': pd.read_excel("C:\\Users\\afafe\\Desktop\\stage\\taille.xlsx", sheet_name='Chaussures', header=1, dtype={'FR':str, 'US':str, 'UK':str, 'IT':str, 'Tops JAP':str})}
sheet_size={}
sheet_size['women']={}
sheet_size['women']['Tops']=sizes_sheet['women']['Tops FR']
sheet_size['women']['Bottoms']=sizes_sheet['women']['Pantalons FR']
sheet_size['women']['Tailles universelles']=sizes_sheet['women']['Tailles universelles']


dict_corr={}
dict_corr['Accessoires']=['Accessoires','handle','bag','tote','wallet', 'pocket','bracelet','cuff','scarf','bangle','besace','bags','wallet', 'sunglasses', 'ring','glasses','earrings']
dict_corr['Robes']=['dress','frill','Robes']
dict_corr['Chaussures']=['knife','sandal','sandals','boots','pumps','loafers','pump','mule','heels','booties','mules','print','bootie', 'sneakers','ballerinas']
dict_corr['Jupes']=['skirt','Jupes et shorts','Jupes']
dict_corr['Pantalons']=['Pantalons','Chino','pant','denim','leggings','pants', 'jeans','legging', 'jean','culottes','suit']
dict_corr['Vestes & Manteaux']=['Vestes & Manteaux','Poncho','cardigans','blazer','jacket','coat','trench','overcoat', 'blouse','trousers','Bombers']
dict_corr['Chemises']=['shirt','suit','Chemise','Chemises']
dict_corr['Shorts']=['bermuda','Bermuda','Shorts']
dict_corr['Pulls & Sweats']=['Sweat','hooded','pull','sweater','sweatshirt', 'hoodie','knitwear','Pulls & Sweat']
dict_corr['Tshirts']=['tshirt','Tshirt',]
dict_corr['Tops']=['tunic','top','body','Polo']
dict_corr['Sous-Vêtements']=['Boxer','boxer','Boite']
dict_corr['Costumees']=['Costumes','suit']
dict_corr['Pyjamas']=['Pyjama']
dict_corr['Maillots de bain']=['Maillots de bain']
import db

wishes = {
            'wishes.Tshirt': ["T-shirts","Tops"],
            'wishes.Shirts': ["Chemises","Tops"],
            'wishes.Knitwear':[ "Pulls & Sweats","Tops"],
            'wishes.Dresses': ["Robes","Tops"],
            'wishes.Skirts': ["Jupes","Bottoms"],
            'wishes.Shorts':["Shorts","Bottoms"],
            'wishes.Pants': ["Pantalons","Bottoms"],
            'wishes.Swimwear':["Maillots de bain","Maillot de bain" ],
            'wishes.Jackets': ["Vestes & Manteaux","Tops"],
            'wishes.Accessories' : ["Accessoires","Accessoires" ],
            'wishes.Bombers': ["Bombers","Tops"],
            'wishes.Shoes': ["Chaussures","Shoes"]
        }
style= {
            'classic': "Plutôt classique",
            'working': "Working girl",
            'sporty': "Sporty",
            'fashion': "Ultra fashion"}
occasion={
            'dailyLife': "Quotidien (« FRAICHE à tout moment… »)",
            'Nightout': "Sortie (« FRAICHE entre amis »)",
            'Date': "Date (« FRAICHE in love »)",
            'Wedding': "Mariage (« La plus FRAICHE pour ce grand jour »)",
            'Work': "Travail (« FRAICHE at work »)",
            'Festival': "Festival (« FRAICHE en musique »)",
            'weekEnd': "Week-end / Vacances (« FRAICHE loin de Paris »)",
            'Beach': "Plage (« FRAICHE on the beach »)",
            'Sport': "Sport (« FRAICHE at the gym »"}

Categories={'Tops':['Pulls & Sweat','Vestes & Manteaux','Chemises','Tops','T-shirts','Robes','Tshirts','Bombers'],
            'Combinaisons':['Combinaisons'],
            'Costumes':['Costumes'],
            'Bottoms':['Jupes','Pantalons','Shorts','Jupes et shorts'],
            'Shoes':['Chaussures'],
            'Sous-vetements':['Sous-vetements'],
            'Vetements de nuit':['pyjamas'],
            'Maillots de Bain':['Maillots de bain'],
            'Accessoires':['Accessoires']   
            }

user_prod_sizes={'sizes_top':'Tops','sizes_bottom':'Bottoms','sizes_shoes':'Shoes'}

Style=[s for s in style.keys()]
Occasion=[s for s in occasion.keys()]


fr_occasions={ 'dailyLife':'Quotidien',
              'Nightout' :'Sortie',
              'Festival':'Festival',
              'Date':'Date',
              'Work':'Travail',
              'Wedding':'Mariage',
              'weekEnd':'Week-end',
              'Beach':'Plage',
              'Sport':'Sport'}

fr_styles={ 'classic':'Classic',
              'working':'WORK',
               'sporty':'Sportswear',
               'fashion':'Creative'}
    

user_prod_sizes={'sizes_top':'Tops','sizes_bottom':'Bottoms','sizes_shoes':'Shoes'}
def get_key(uni_size,cat):
    df=pd.DataFrame(sheet_size['women'])
    size=df[df['Tailles universelles']==uni_size.upper()][cat].iloc[0]
    return size
    
def getKeybyValue(dicto,value_to_search):
    for key,value in dicto.items():
        if isinstance(value,list):
            if value_to_search in value:
                return key 
        else:
            if value== value_to_search:
                return key


def concat_dict(dict1,dict2):
    d=dict2.copy()
    liste=[]
    for k in dict2.keys():
        for c in dict2[k].keys():
            try:
                if isinstance(dict1[k][c],list):
                    liste=dict1[k][c]
                    try:
                        liste+=[d[k][c]]
                        d[k][c]=liste
                    except:
                        d[k][c]=list(dict.fromkeys(liste))
                else:
                    liste=[dict1[k][c]]
                    try:
                        
                        liste.append(d[k][c])
                        d[k][c]=liste
                    except:
                        d[k][c]=list(dict.fromkeys(liste))
            except :
                pass
        
    return d


def verify(user_cat,user_size,prod_cat_size,store_Id):
    if store_Id==7:
        if getKeybyValue(Categories,prod_cat_size[0])==user_cat :
            return user_size in prod_cat_size[1] 
        else:
            return True
    if store_Id==6:
        prod_cat=getKeybyValue(Categories,prod_cat_size[0])
        if getKeybyValue(Categories,prod_cat_size[0])==user_cat :
            return user_size in normalize(prod_cat_size[1] ,user_size,prod_cat)
        else:
            return True
        
        
    

def normalize(size,user_size,prod_cat):
    if size!='{}' and size!='{TU}':
        if size[1].isalpha():
            if prod_cat in ['Tops','Bottoms']:
                size=size[1:-1].split(',')
                size=[get_key(t,prod_cat) for t in size]
                return size
                
            else: 
                return user_size
        else:
              return user_size   
    else:
        return user_size

def products_interactions(userId, storeId):
    user = db.get_user(userId, storeId)[0]
    for k in user.keys():
        if user[k] == None:
            user[k] = []
    products_seen = user['products_liked'] + user['products_bookmarked'] + user['products_ignored'] + [p for p in user['products_disliked'].keys()] + user['products_seen']
    products_seen = list(set(products_seen))
    products_liked = user['products_liked']
    products_disliked=[p for p in user['products_disliked'].keys()]
    return products_seen, products_liked, products_disliked
