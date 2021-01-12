import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def recommend():
    recommendations={}
    items_df = pd.read_csv('./data/itemdata.csv',usecols=['itemId','item'],dtype={'itemId': 'int32', 'item': 'str'})
    rating_df=pd.read_csv('./data/ratings.csv',usecols=['userId', 'item', 'rating'],dtype={'userId': 'str', 'item': 'str', 'rating':'float32'})

    df = pd.merge(rating_df,items_df,on='item')
    combine_item_rating = df.dropna(axis = 0, subset = ['item'])
    item_ratingCount = (combine_item_rating.
        groupby(by = ['item'])['rating'].
        count().
        reset_index().
        rename(columns = {'rating': 'totalRatingCount'})
        [['item', 'totalRatingCount']]
        )
    rating_with_totalRatingCount = combine_item_rating.merge(item_ratingCount, left_on = 'item', right_on = 'item', how = 'left')
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    popularity_threshold = 2
    rating_popular_item= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
    rating_popular_item.shape
    item_features_df=rating_popular_item.pivot_table(index='item',columns='userId',values='rating').fillna(0)

    item_features_df_matrix = csr_matrix(item_features_df.values)

    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(item_features_df_matrix)


    item_features_df.shape
    query_index = np.random.choice(item_features_df.shape[0])
    print(query_index)
    distances, indices = model_knn.kneighbors(item_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 3)

    for i in range(0, len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:\n'.format(item_features_df.index[query_index]))
            recommendations[i]=item_features_df.index[query_index]
        else:
            print('{0}: {1}, with distance of {2}:'.format(i, item_features_df.index[indices.flatten()[i]], distances.flatten()[i]))
            recommendations[i]=item_features_df.index[indices.flatten()[i]]
    return recommendations