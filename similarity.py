from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
import numpy as np
import random
import utils
class SimilarityPredictions(object):
    '''This class calculates a similarity matrix from latent embeddings.
    There is a method to save this similarity model locally, and a method for
    predicting similar items from the matrix.
    Input: embeddings - a pandas dataframe of items and latent dimensions.
            similarity_metric = str definining the similarity metrics to use
    output: top n most similar products to the input product'''

    def __init__(self, embeddings, similarity_metric,features):
        assert similarity_metric in ['cosine', 'euclidean'], "unsupported similarity metric."
        self.embeddings = embeddings
        self.ids_embeddings = embeddings.index.tolist()
        self.features=features
        self.ids_features=features.index.tolist()
        self.similarity_metric = similarity_metric
        if self.similarity_metric == 'cosine':
            self.similarity_matrix = self.calculate_cosine_similarity_matrix()
        if self.similarity_metric == 'euclidean':
            self.similarity_matrix = self.calculate_euclidean_distances_matrix()

    def calculate_cosine_similarity_matrix(self):
        '''Calculates a cosine similarity matrix from the embeddings'''
        #X=pd.concat((self.features,self.embeddings),axis=1)
        similar_features=pd.DataFrame(cosine_similarity(self.features),index=self.ids_features)
        similar_embeddings=pd.DataFrame(cosine_similarity(self.embeddings),index=self.ids_embeddings)
        similarity_matrix=pd.concat([similar_features,similar_embeddings]).groupby(level=0).mean()
        #similarity_matrix = pd.DataFrame(cosine_similarity(X),index=self.ids_embeddings)
        similarity_matrix.columns = self.ids_embeddings
        return similarity_matrix

    def calculate_euclidean_distances_matrix(self):
        '''Calculates a cosine similarity matrix from the embeddings'''
        #X=pd.concat((self.features,self.embeddings),axis=1)
        #similarity_matrix= pd.DataFrame(euclidean_distances(X),index=self.ids_embeddings)
        similar_features=pd.DataFrame(cosine_similarity(self.features),index=self.ids_features)
        similar_embeddings=pd.DataFrame(cosine_similarity(self.embeddings),index=self.ids_embeddings)
        similarity_matrix=pd.concat([similar_features,similar_embeddings]).groupby(level=0).mean()
        similarity_matrix.columns = self.ids_embeddings
        return similarity_matrix

    def predict_similar_items(self, seed_items,user_cat, n,products,storeId):
        '''Use the similarity_matrix to return n most similar items.'''
        # the maximum number of items with the same category
        ids=self.ids_embeddings
        dict_similar={"item_id":{},"similarity_score":{}} # the dictionary that will be having all similar products to liked products
        if storeId==7:
            prod_similar_userCat=[products['product_id'].iloc[s] for s in range(products.shape[0]) if products['product_id'].iloc[s] in ids and products['normalized_category'].iloc[s]==user_cat]## products which have the samecategory as the user
            prod_different_userCat=[t for t in ids if t not in prod_similar_userCat] # products which have different categories 
        if storeId==6:
            prod_similar_userCat=[products['product_id'].iloc[s] for s in range(products.shape[0]) if products['product_id'].iloc[s] in ids and utils.getKeybyValue(utils.dict_corr,products['category'].iloc[s])==user_cat]## products which have the samecategory as the user
            prod_different_userCat=[t for t in ids if t not in prod_similar_userCat] # products which have different categories 
        if seed_items!=[]: ## seed_item=product_liked
            for seed_item in seed_items:
                if storeId==7:
                    prod_similar_cat=[products['product_id'].iloc[s] for s in range(products.shape[0]) if products['product_id'].iloc[s] in ids and products['normalized_category'].iloc[s]==products[products['product_id']==seed_item].category.iloc[0] ]
                    prod_diff_cat=[t  for t in ids if t not in prod_similar_cat]  
                if storeId==6:
                    prod_similar_cat=[products['product_id'].iloc[s] for s in range(products.shape[0]) if products['product_id'].iloc[s] in ids and utils.getKeybyValue(utils.dict_corr,products['category'].iloc[s])==products[products['product_id']==seed_item].category.iloc[0] ]
                    prod_diff_cat=[t  for t in ids if t not in prod_similar_cat]  
                similar_items = pd.DataFrame(self.similarity_matrix.loc[seed_item])
                similar_items.columns = ["similarity_score"]
                #if self.similarity_metric == 'cosine':
                    #similar_items = similar_items.sort_values('similarity_score', ascending=False)
                #if self.similarity_metric == 'euclidean':
                    #similar_items = similar_items.sort_values('similarity_score', ascending=True)
                #similar_items = similar_items.head(n)
                similar_items.reset_index(inplace=True)
                similar_items = similar_items.rename(index=str, columns={"index": "item_id"})
                dict_similarity=similar_items.to_dict()
                dict_similar=utils.concat_dict(dict_similar,dict_similarity)
            d1={k: v[0] for k, v in dict_similar['item_id'].items()}
            d2 = {k: np.mean(v) for k, v in dict_similar['similarity_score'].items()}
            dict_similar["similarity_score"].update(d2)
            dict_similar["item_id"].update(d1)
            similar_items=pd.DataFrame.from_dict(dict_similar)
            similar_items = similar_items.sort_values('similarity_score', ascending=False)
            dict_similarity=similar_items.to_dict()
            intersection=list(set([dict_similarity["item_id"][x] for x in [str(s) for s in np.arange(1,n+1)] ]) & set( prod_similar_userCat))
            if len(intersection)>n//2: #if what we recommend has more than 50% of the searched category
                keep_fhalf=intersection[:n//2] # we keeep the first half 
                keep_shalf=[dict_similarity["item_id"][x] for x in [str(s) for s in np.arange(1,len(ids))] if dict_similarity["item_id"][x] not in  prod_similar_userCat][n//2:] # we add other similar products but with different category 
                
                L=keep_fhalf+ keep_shalf
#                similar_items[similar_items["item_id"].isin(L[:n])].to_dict()
#                dict_similar['similarity_score']+=similar_items[similar_items["item_id"].isin(L[:n])].to_dict()['similarity_score']
                return  similar_items[similar_items["item_id"].isin(L[:n])].to_dict()
            else: #if it's not the case we keep the similarity recommendation
#                dict_similar['item_id']+=similar_items[similar_items.index.isin([str(s) for s in np.arange(1,n)])].to_dict()['item_id']
#                dict_similar['similarity_score']+=similar_items[similar_items.index.isin([str(s) for s in np.arange(1,n)])].to_dict()['similarity_score']
      
                return similar_items[similar_items.index.isin([str(s) for s in np.arange(1,n)])].to_dict()
            
        else:
            random.shuffle( prod_similar_userCat)
            return prod_similar_userCat[:n//2]+ prod_different_userCat[min(n//2,len( prod_similar_userCat[:n//2])):n]
              
            
            
            
        

            
            