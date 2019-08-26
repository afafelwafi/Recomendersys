import db
import pandas as pd
from content_filtering  import ContentFiltering
from similarity import SimilarityPredictions
from  product_filter import ProductFilter

"""
in order to test this recommender out we need as inputs userId storeId user_data(containing only s)
"""
def recommend(userId, storeId, user_data,cat,products_seen,products_liked,products_disliked): 
#    user_category=user_data['user_category']
#    user_style=user_data['user_style']
#    user_occasion=user_data['occasion']
    products=db.get_products(storeId)

    produ_filter=ProductFilter(products,user_data,userId,storeId,products_seen,products_liked,products_disliked) #create an instance of products filter

    produ_filter.filter_size_products()# filter products which don't fit the user
    produ_filter.filter_disliked_seeen_products() #filter the seen and disliked products
   #create an instance of content filter :
    products=db.get_products_from_ids(produ_filter.products,storeId)
    products_df=pd.DataFrame.from_dict(products)
    CF= ContentFiltering(products_df,'','',cat,storeId)# instead of '' we should add the user's style and user's occasion 
    tfidif_df=CF.tfidf_tokenizer(0,0.5, (1,2), 'info')
    CF.save_embeddings(tfidif_df, "C:\\Users\\afafe\\Styles\\tf.pkl", file_format='pickle')
   ###similarity calculation
   
    features = []
    features_out =db.get_features(produ_filter.products,storeId)
    c = 0
    for i,feature in enumerate(features_out):
        if 'tensor' not in feature:
            del produ_filter.products[i-c]
            c+=1
        else:
           features.append(feature['tensor'])
    features_df=pd.DataFrame(features,index=produ_filter.products)
    SM=SimilarityPredictions(tfidif_df,'cosine',features_df) ## well euclidian distance is also an option just the order is reversed 
    similarity_matrix=SM.predict_similar_items(produ_filter.products_liked.split(),cat,4,products_df,6)
    return similarity_matrix
    
    
   
   
