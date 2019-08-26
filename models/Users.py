from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import db as ddb
db = SQLAlchemy()

# define what our database user looks like.
class User(db.Model):

    __tablename__ = "users"

   
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(255))
    categories=db.Column('categories',db.String(500))
    sizes=db.Column('sizes',db.String(500))
    budget=db.Column('budget',db.String(255))
    style=db.Column('style',db.String(255))
    occasion=db.Column('occasion',db.String(255))  
    gender=db.Column('gender',db.String(255))  
    products_seen=db.Column('products_seen',db.String(1000))  
    products_liked=db.Column('products_liked',db.String(1000)) 
    products_disliked=db.Column('products_disliked',db.String(1000)) 
    nm_reco=db.Column('nm_reco', db.Integer)
    reco=db.Column('reco',db.String(1000)) 
    email = db.Column('email', db.String(60), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password,products_seen,products_liked,products_disliked,reco,nm_reco,email,sizes,categories,budget,occasion,style,gender):
        self.username = username
        self.products_seen=products_seen
        self.products_disliked=products_disliked
        self.products_liked=products_liked
        self.reco=reco
        self.nm_reco=nm_reco
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.sizes=sizes
        self.categories=categories
        self.budget=budget
        self.style=style
        self.occasion=occasion
        self.gender=gender
    def is_authenticated(self):
        return True
    def get_sizes(self):
        return self.sizes
    
    def features(self,products):
        features = []
        features_out =ddb.get_features(products,7)
        c = 0
        for i,feature in enumerate(features_out):
            if 'tensor' not in feature:
                del products[i-c]
                c+=1
            else:
               features.append(feature['tensor'])
        features
    
    def popular_products(self,storeId):
        Liste=ddb.popular_products(storeId)
        if len(Liste)>3:
            self.reco=Liste
            self.nm_reco=1
            return self.reco
        else:
            Lis_te=ddb.get_products(storeId)
            Liste2=[{'picture_url':p['picture_url']} for p in Lis_te if p['category']!='Frais']
            Liste2=Liste+Liste2[:1]+Liste2[3:]
            Liste2=Liste2[:4]
            self.reco=Liste2
            self.nm_reco=1
            return self.reco
            
            
            
            
            
        
        

    def set_sizes(self,sizes):
       self.sizes=sizes
    
    def get_category(self):
        return self.categories
    
    def set_category(self,cat):
        self.categories=cat
        
    def set_gender(self,gend):
        self.gender=gend
    
    def get_gender(self):
        return self.gender   
      
    def set_budget(self,bud):
        self.budget=bud 
    
    def get_budget(self):
        return self.budget

    def get_style(self):
        return self.style
    
    def set_style(self,st):
        self.style=st
    
    def get_occasion(self):
        return self.occasion
    
    def set_occasion(self,occ):
        self.occasion=occ
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    # don't judge me...
    def unique(self):

        e_e = email_e = db.session.query(User.email).filter_by(email=self.email).scalar() is None
        u_e = username_e = db.session.query(User.username).filter_by(username=self.username).scalar() is None

        # none exist
        if e_e and u_e:
            return 0

        # email already exists
        elif e_e == False and u_e == True:
            return -1

        # username already exists
        elif e_e == True and u_e == False:
            return -2

        # both already exists
        else:
            return -3