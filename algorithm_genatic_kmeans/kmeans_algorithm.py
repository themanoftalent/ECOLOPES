import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


class KMeansService:
    def __init__(self, n_clusters=3, random_state=42, n_init=10):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.n_init = n_init

    def fit_predict(self, df):
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init=self.n_init)
        df['cluster'] = kmeans.fit_predict(df.drop(columns='cluster', errors='ignore'))
        self.centers = kmeans.cluster_centers_
        return df
    
    def get_score(self, df, score_function):
        features = df.drop(columns='cluster', errors='ignore')
        labels = df['cluster']
        score = score_function(features, labels)
        return score

    def get_silhouette_score(self, df):
        return self.get_score(df, silhouette_score)

    def get_davies_bouldin_score(self, df):
        return self.get_score(df, davies_bouldin_score)

    def get_calinski_harabasz_score(self, df):
        return self.get_score(df, calinski_harabasz_score)

    def plot_clusters(self, df):
        cluster_colors = {0: 'red', 1: 'green', 2: 'blue'}
                
        plt.figure(figsize=(15, 10))
        
        sns.scatterplot(data=df, x=df.columns[0], y=df.columns[1], hue='cluster',
                        palette=cluster_colors, alpha=0.7, style='cluster', markers=['o', '^', 's'], s=50)
        
        plt.scatter(self.centers[:, 0], self.centers[:, 1], c='black', marker='X', s=200, label='Centroids')
        
        for i in range(self.n_clusters):
            points = df[df['cluster'] == i][df.columns[:2]].values
            if len(points) > 2:
                hull = ConvexHull(points)
                x_hull = np.append(points[hull.vertices,0], points[hull.vertices,0][0])
                y_hull = np.append(points[hull.vertices,1], points[hull.vertices,1][0])
                plt.fill(x_hull, y_hull, alpha=0.3, c=cluster_colors[i])

        plt.legend(title='Cluster', loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.title("Cluster plot with Convex Hull")
        plt.xticks(rotation=90)

        if not os.path.exists('output'):
            os.makedirs('output')
        filename = f'output/cluster_plot.png'
        plt.savefig(filename, bbox_inches='tight')
        plt.show()


class MainApplication:
    def __init__(self, file_path):
        self.file_path = file_path
        self.service = KMeansService()

    def upload_file(self):
        df = pd.read_csv(self.file_path)
        return df

    def process_file(self):
        df = self.upload_file()
        df_numerical = df[['Species', 'PFG']]
        df_clustered = self.service.fit_predict(df_numerical)
        self.service.plot_clusters(df_clustered)

        silhouette_score = self.service.get_silhouette_score(df_clustered)
        davies_bouldin_score = self.service.get_davies_bouldin_score(df_clustered)
        calinski_harabasz_score = self.service.get_calinski_harabasz_score(df_clustered)

        self.save_scores_to_csv('KMeans', silhouette_score, davies_bouldin_score, calinski_harabasz_score)

    def save_scores_to_csv(self, model_name, silhouette_score, davies_bouldin_score, calinski_harabasz_score):
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = f'{output_dir}/{model_name}_performance.csv'
        
        scores_df = pd.DataFrame({
            'Model': [model_name],
            'Silhouette Score': [silhouette_score],
            'Davies-Bouldin Score': [davies_bouldin_score],
            'Calinski-Harabasz Score': [calinski_harabasz_score]
        })

        scores_df.to_csv(filename, index=False)
        print(f"Scores have been saved to {filename}")


def run_kmeans_algorithm():
    file_path = 'output/selected_species_data.csv'
    app = MainApplication(file_path)
    app.process_file()