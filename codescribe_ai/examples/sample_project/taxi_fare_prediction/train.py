import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

df=pd.read_csv('/data/ride_data_large.csv')

df['datetime'] = pd.to_datetime(df['datetime'])
# df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour
df['day_of_week']= df['datetime'].dt.dayofweek

df=df.drop(columns=['datetime','location'])

x=df.drop(columns=['demand'])
y=df['demand']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model=RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

with open("model.pkl","wb") as f:
    pickle.dump((model,list(x.columns)),f)