import pandas as pd
import utils 


#self : a user's id /products is a DataFrame 

class ProductFilter(object):

    def __init__(self, Products,user_data,user_id,store_id,products_seen,products_liked,products_disliked):
        self.products_seen=products_seen
        self.products_disliked=products_disliked
        self.products_liked=products_liked
        self.products = Products
        self.user_col=user_data#user's data caracteristics aka style occasion sizes ....
        self.user_id=user_id# user's id
        self.store_id=store_id# store's id 
    def filter_size_products(self):
        if self.user_col!=None:
            user_sizes={s:t for s,t in self.user_col.items() if t!='undefined' and  s in ['sizes_top','sizes_bottom','sizes_shoes']}
#            user_style={s:t for s,t in self.user_col.items() if t!='undefined' and s=='style'}
#            user_occasion={s:t for s,t in self.user_col.items() if t!='undefined' and s=='occasion'}
#            user_category={s:t for s,t in self.user_col.items() if t!='undefined' and s=='wishes'}
#            ##removing products which don't fit the user :
        products_df=pd.DataFrame.from_dict(self.products)
        if user_sizes!={} and user_sizes!=None:
            for size_key in user_sizes.keys():
                size=user_sizes[size_key]
                cat_key=utils.user_prod_sizes[size_key]
                if size:
                    if self.store_id==7:
                        products_df['test']=products_df[['normalized_category','sizes']].apply(lambda x: utils.verify(cat_key,size,x,7),axis=1)
                        products_df=products_df[products_df['test']==True]   
                        self.products=products_df['product_id'].tolist()
                   
                    if self.store_id==6:
                        products_df['test']=products_df[['category','sizes']].apply(lambda x: utils.verify(cat_key,size,x,6),axis=1)
                        products_df=products_df[products_df['test']==True]   
                        products_df=products_df[products_df.category!='Frais']  
                        self.products=products_df['product_id'].tolist()
        self.products=products_df['product_id'].tolist()
            

    def filter_disliked_seeen_products(self):
        #products_seen,products_liked,products_disliked=utils.products_interactions(self.user_id, self.store_id)
        products_seen,products_liked,products_disliked=self.products_seen.split(),self.products_disliked.split(),self.products_disliked.split()
        len0=len(self.products)
        self.products=[t for t in self.products if t not in products_disliked and t not in products_seen]
        len1=len(self.products)
        self.liked_products=products_liked
        #self.print_filter_results("filter_disliked_seeen_products", len0, len1)


    def print_filter_results(self,filter_name, len0, len1):
        print('{} filtered out {} products. Num before: {}. Num after: {}'.format(filter_name, len0 - len1, len0, len1))

    def reduce_ratings_dataset(self, ratings, product_col='productId'):
        mask = ratings[product_col].isin(self.products['product_id'])
        len0 = len(ratings)
        ratings = ratings[mask]
        len1 = len(ratings)
        print('Filtered out {} ratings. Num before: {}. Num after: {}'.format(len0 - len1, len0, len1))