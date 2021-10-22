import pandas as pd

dates=['April-10', 'April-11', 'April-12', 'April-13','April-14','April-16']
sales=[200,300,400,200,300,300]
prices=[3, 1, 2, 4,3,2]

df = pd.DataFrame({'Date':dates ,
                   'Sales':sales ,
                   'Price': prices})

df_mask=df['Sales']==300
filtered_df = df[df_mask]
print(filtered_df)