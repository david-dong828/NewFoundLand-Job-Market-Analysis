# Name: Dong Han
# Student ID: 202111878
# Mail: dongh@mun.ca

import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.manifold import TSNE

#############################################    DATA MINNING    #############################################
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Function to calculate Euclidean distance
def euclidean_dist (a,b):
    return np.sqrt(np.sum((a-b)**2 , axis=1))

def create_clusters(k,points, centroids):
    clusters = {}
    for i in range(k):
        clusters[i] = []
    for p in points:
        dis = euclidean_dist(p,centroids)
        print('dis: ',dis)
        cluster_index = np.argmin(dis)
        clusters[cluster_index].append(p)

    return clusters

def set_new_centroids(k,clusters):
    new_centroids = np.zeros((k, 2)) # [[0 0] [0 0] [0 0]]
    for i in range(k):
        new_centroids[i] = np.mean(clusters[i],axis=0)

    return new_centroids

def kMeans():
    k=3
    a1,a2,a3 = [2,10],[2,5],[8,4]
    b1,b2,b3 = [5,8],[7,5],[6,4]
    c1,c2 = [1,2],[4,9]

    init_centroids = np.array([a1,b1,c1])
    points = np.array([a1,a2,a3,b1,b2,b3,c1,c2])

    centroids = init_centroids
    for _ in range(10):
        clusters = create_clusters(k, points, centroids)
        new_centroids = set_new_centroids(k,clusters)

        # if np.all(new_centroids == centroids):
        #     print('break')
        #     break
        centroids = new_centroids

        print(_+1)
        print(clusters)
        print(new_centroids)

def dbscan(dataPath):
    df = pd.read_csv(dataPath)
    # Example: Using only Latitude and Longitude for clustering
    X = StandardScaler().fit_transform(df[['Latitude', 'Longitude']])
    clustering = DBSCAN(eps=0.3, min_samples=10).fit(X)
    df['Cluster'] = clustering.labels_
    print(df['Cluster'])

    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",
                            color="Cluster",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            size_max=15, zoom=10,
                            mapbox_style="open-street-map")
    fig.show()

def hdbscan(dataPath):
    import hdbscan
    df = pd.read_csv(dataPath)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[['Latitude', 'Longitude']])

    clusterer = hdbscan.HDBSCAN(min_cluster_size=5)
    cluster_labels = clusterer.fit_predict(scaled_data)
    df['Cluster'] = cluster_labels
    df.to_csv("jobs_with_hdbscan_geo.csv",index=False)

    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                            color='Cluster',
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            mapbox_style="open-street-map")
    fig.show()

def hdbscan_title(dataPath):
    from sklearn.feature_extraction.text import TfidfVectorizer
    import hdbscan
    import seaborn as sns

    df = pd.read_csv(dataPath)

    # Combine Title and Description for clustering
    df['Title'] = df['Title'].fillna('').astype(str)
    df['Description'] = df['Description'].fillna('').astype(str)
    text_data = df['Title'] + ' ' + df['Description']

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(text_data)

    # Apply HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5,min_samples=2)
    clusters = clusterer.fit_predict(X.toarray())
    df['Cluster'] = clusters

    # Count the number of titles in each cluster
    cluster_counts = df['Cluster'].value_counts()
    # Get the top 5 clusters with the most titles
    top_clusters = cluster_counts.head(5).index
    # Mark the top clusters
    df['TopCluster'] = df['Cluster'].apply(lambda x: 'Top5' if x in top_clusters else 'Others')

    for cluster_id in top_clusters:
        print(f"\nCluster {cluster_id} example titles:")
        print(df[df['Cluster'] == cluster_id]['Title'].head(5))


        # Use tSNE to reduce dimensionality
    tsne = TSNE(n_components=2, perplexity=30, n_iter=300)
    X_tsne = tsne.fit_transform(X.toarray())
    # print("X_tsne: ",X_tsne[:5])

    # Convert to DataFrame for easier plotting
    tsne_df = pd.DataFrame(
        {'X': X_tsne[:, 0], 'Y': X_tsne[:, 1], 'Cluster': df['Cluster'], 'TopCluster': df['TopCluster']})

    # Plotting
    plt.figure(figsize=(15, 12))

    # Plot other clusters
    sns.scatterplot(data=tsne_df[tsne_df['TopCluster'] == 'Others'], x='X', y='Y', hue='Cluster', style='TopCluster',
                    alpha=0.5)
    # Highlight top 5 clusters
    sns.scatterplot(data=tsne_df[tsne_df['TopCluster'] == 'Top5'], x='X', y='Y', hue='Cluster', style='TopCluster',
                    palette='Set1', s=100, legend='full')
    plt.title('t-SNE HDBSCAN Clusters with Top 5 Highlighted')
    plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc="upper right",prop={'size': 10})
    plt.show()

    # or use plotly to show
    # fig = px.scatter(tsne_df, x='X', y='Y', color='Cluster', symbol='TopCluster')
    # fig.update_layout(legend_title='Cluster', legend=dict(x=1, y=1))  # Adjust legend position
    # fig.show()

def topicModeling(dataPath):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    from sklearn.feature_extraction.text import CountVectorizer
    from nltk.corpus import stopwords
    import nltk

    import pyLDAvis

    # Download NLTK French stopwords
    nltk.download('stopwords')

    df = pd.read_csv(dataPath)

    df['Title'] = df['Title'].fillna('').astype(str)
    df['Description'] = df['Description'].fillna('').astype(str)

    # Combine English and French stopwords
    french_stop_words = set(stopwords.words('french'))
    combined_stop_words = list(ENGLISH_STOP_WORDS.union(french_stop_words))

    vectorizer = CountVectorizer(stop_words=combined_stop_words)
    X = vectorizer.fit_transform(df['Title'] + ' ' + df['Description'])

    # Extract vocabulary and term frequency
    vocab = vectorizer.get_feature_names_out()
    term_frequency = np.asarray(X.sum(axis=0)).ravel().tolist()

    # Choose the number of topics, apply LDA
    num_topics = 5
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda.fit(X)

    topic_term_dists = lda.components_

    # View topics
    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic #{topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))

    # Assign the highest probability topic to each document
    doc_topics = lda.transform(X)
    df['Dominant_Topic'] = doc_topics.argmax(axis=1)

    # Prepare the LDA visualization
    panel = pyLDAvis.prepare(topic_term_dists=topic_term_dists,
                         doc_topic_dists=lda.transform(X),
                         doc_lengths=np.sum(X, axis=1).getA1(),
                         vocab=vocab,
                         term_frequency=term_frequency,
                         mds='tsne')
    # Save the visualization as an HTML file
    pyLDAvis.save_html(panel, 'lda_visualization.html')



#############################################    MAIN    #############################################
def main():

    # # Data Minning
    dataPath = "jobs_with_coordinates.csv"
    # dbscan(dataPath)
    # hdbscan(dataPath)
    # hdbscan_title(dataPath)
    topicModeling(dataPath)
if __name__ == '__main__':
    main()