from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import utils
import db
import numpy as np

class ContentFiltering(object):
    '''Methods for performing Content Filtering.
    Input: data - a pandas dataframe of items and features.
        similarity_metric = str definining the similarity metrics to use.'''

    def __init__(self, products,user_style,user_occasion, user_category,storeId):
        self.ids = products.product_id.tolist() 
        if storeId==7:
            products['info']=products[['description', 'category']].apply(lambda x: x[0]+' '+x[1], axis=1)
        if storeId==6:
            products['info']=products[ 'category']
            
        self.data=products
        self.user_style=user_style
        self.user_occasion=user_occasion
        self.user_category=user_category

    def tfidf_tokenizer(self, min_df,max_df, ngram_rang, documents_column_name):
        '''Performes TF-IDF tokenization. Use documents_column_name to specify the
        column containing the text data to be tokenized.
        Returns a dataframe of TF-IDF features indexed by item id.'''
        sty_occ_df=pd.DataFrame(self.styles_occasions_categories_vector(), index=self.ids)
        tfidf = TfidfVectorizer(ngram_range =ngram_rang,min_df=min_df,max_df=max_df,
            stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.data[documents_column_name])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=self.ids)
        df=pd.concat([ tfidf_df, sty_occ_df], axis=1)
        return df
    
    def styles_occasions_categories_vector(self):
        styles_matrix=pd.read_excel("Pondération similarité - Occasions styles catégories.xlsx",skiprows=1,sheet_name="Styles",usecols=np.arange(1,6),index_col=0)
        values=styles_matrix.unstack().values.reshape(4,4)
        values=np.triu(values) + np.triu(values,1).T
        values[np.isnan(values)]=1
        styles=pd.DataFrame(values,index=styles_matrix.index,columns=styles_matrix.columns)
        occasions_matrix=pd.read_excel("Pondération similarité - Occasions styles catégories.xlsx",skiprows=1,sheet_name="Occasions",usecols=np.arange(1,11),index_col=0)
        values=occasions_matrix.unstack().values.reshape(9,9)
        values=np.triu(values) + np.triu(values,1).T
        values[np.isnan(values)]=1
        occasions=pd.DataFrame(values,index=occasions_matrix.index,columns=occasions_matrix.columns)
        categories_matrix=pd.read_excel("Pondération similarité - Occasions styles catégories.xlsx",skiprows=1,sheet_name="Catégories",usecols=np.arange(1,28),index_col=0)
        values=categories_matrix.unstack().values.reshape(26,26)
        values=np.triu(values) + np.triu(values,1).T
        values[np.isnan(values)]=1
        categories=pd.DataFrame(values,index=categories_matrix.index,columns=categories_matrix.columns)
        sty_occ_vec=[[0,0,0] for i in range(len(self.ids))]
        occasion=self.user_occasion
        style=self.user_occasion
        category=self.user_category
        if style in styles.index or occasion in occasions.index or category in categories.index:
            for i,p in enumerate(self.data):
                try:
                    sty_occ_vec[i][0]= styles.loc[p['style']][style]
                except:
                    pass
                try:
                    sty_occ_vec[i][1]= occasions.loc[p['occasion']][occasion]
                except:
                    pass
                try:
                    sty_occ_vec[i][2]= categories.loc[p['normalized_category']][category]
                except:
                    pass

        return  sty_occ_vec
        
                    
    def get_svd_embeddings(self, feature_matrix, n):
        '''Compress the original feature matrix into n latent features using matrix factorization.
        Returns a dataframe with n latent features.'''
        svd = TruncatedSVD(n_components=n)
        latent_matrix = svd.fit_transform(feature_matrix)
        latent_df = pd.DataFrame(latent_matrix, index=self.ids)
        return latent_df

    def save_embeddings(self, tfidf_df, path, file_format='csv'):
        '''Save embeddings locally'''
        assert file_format in ['csv', 'pickle'], "unsupported format"
        if file_format == 'csv':
            tfidf_df.to_csv(path, header=True, index=True)
        elif file_format == 'pickle':
            tfidf_df.to_pickle(path)
