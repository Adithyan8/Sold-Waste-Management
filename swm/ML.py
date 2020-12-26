import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')
df=pd.read_csv('ml.csv')
df.sort_values(by=['Date'],axis=0,inplace=True)
last=df.tail(1)['Date']

df=df.dropna()
import datetime as dt
def convert_date_to_ordinal(date):
    t=dt.datetime.strptime(str(date),'%Y-%M-%d').date()
    return t.toordinal()

# df['Date'] = pd.to_datetime(df['Date'])
df['Date']=df['Date'].apply(convert_date_to_ordinal)
X=df[['Date']]

y=df[['Waste']]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=101)

from sklearn.linear_model import LinearRegression
lm= LinearRegression()
lm.fit(X_train,y_train)
from sklearn import metrics
import datetime
r=str(last).split('\n')
r1=r[0].split(' ')
r2=r1[4].split('-')
dt = datetime.datetime(int(r2[0]), int(r2[1]), int(r2[2]))
end = datetime.datetime(int(r2[0])+2, int(r2[1]), int(r2[2]), 23, 59, 59)
step = datetime.timedelta(days=1)
result = []
while dt < end:
    result.append(dt.strftime('%Y-%m-%d'))
    dt += step
import datetime as dt
def convert_date_to_ordinal(date):
    t=dt.datetime.strptime(date,'%Y-%M-%d').date()
    return t.toordinal()

for z in range(len(result)):
    result[z]=convert_date_to_ordinal(result[z])
df2=pd.DataFrame(result)
pre=lm.predict(df2)
orignal2=df2[0].map(dt.datetime.fromordinal)
import matplotlib.pyplot as plt
# line 1 points
x1 =orignal2
y1 =pre
# plotting the line 1 points 
plt.plot(x1, y1, label = "Prediction")
plt.xlabel('Timeframe')
# Set the y axis label of the current axis.
plt.ylabel('Waste')
# Set a title of the current axes.
plt.title('Waste vs Date')

# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
