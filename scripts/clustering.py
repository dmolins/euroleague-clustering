from sklearn.cluster import KMeans
import numpy as np
import mysql.connector
from sklearn.preprocessing import StandardScaler
import csv
import pandas as pd
import credentials

mydb = mysql.connector.connect(
  host=credentials.host,
  port=credentials.port,
  user=credentials.user,
  password=credentials.password,
  database=credentials.database
)

mycursor = mydb.cursor()

mycursor.execute("SELECT s.* FROM stats s LEFT JOIN player_info p ON s.player = p.player WHERE Games>5 and minutes>5")

myresult = mycursor.fetchall()


X = np.array(myresult[0][5:])
for ii in range(1,len(myresult)):
    X = np.vstack((X,myresult[ii][5:]))

X = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=10, random_state=0).fit(X)
labels = kmeans.labels_

for jj in range(0,len(myresult)):
    myresult[jj] = myresult[jj] + (labels[jj],)

players = pd.DataFrame(myresult, columns=['id', 'Player', 'Team', 'Season', 'Games', 'minutes', 'PPT2', 'PPT3', 'PPT', '%TO', '%Ass', 'FrTL', '%T2 Abs', '%T3 Abs', '%Poss Abs', '%DReb', '%OReb', 'C3R', 'C3R_A', 'E3R', 'E3R_A', 'Ce3R', 'Ce3R_A', 'Ce3L', 'Ce3L_A', 'E3L', 'E3L_A', 'C3L', 'C3L_A', 'MBR', 'MBR_A', 'MER', 'MER_A', 'MEL', 'MEL_A', 'MBL', 'MBL_A', 'PR', 'PR_A', 'PC', 'PC_A', 'PL', 'PL_A', 'Cluster'])
players.to_csv('/Users/dmolins/Desktop/david/uni/TFG/results/players.csv', sep=',', index = False)

