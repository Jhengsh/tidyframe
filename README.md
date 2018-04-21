# tidyframe: Clean data to tidy Dataframe
Overview
--------
+ Clean pandas DataFrame to tidy DataFrame 
+ Inspired by [tidyr](https://github.com/tidyverse/tidyr) in R
+ Goal help you to create **tidy Pandas Dataframe**
+ Wapper window function from DataFrame
+ Implement *tidyr::gather* and *tidyr:spread* using python


Installation
------------
```python
python3 setup.py install
```

Tuturial
--------
```python
from sklearn import datasets
iris = datasets.load_iris()
df = pd.DataFrame(iris['data'], columns=iris.feature_names)
df['target'] = iris.target
df['target2'] = list(map(lambda x: str(x +1), df.target))
df.head()
#  sepal length (cm)	sepal width (cm)	petal length (cm)	petal width (cm)	target	target2
# 0	5.1	3.5	1.4	0.2	0	1
# 1	4.9	3.0	1.4	0.2	0	1
# 2	4.7	3.2	1.3	0.2	0	1
# 3	4.6	3.1	1.5	0.2	0	1
# 4	5.0	3.6	1.4	0.2	0	1

columns = df.columns[:4].tolist()
df_nest= nest(df, columns, key='data_nest', copy=True).head()
df_nest['shape'] = df_nest['data_nest'].apply(lambda x: x.shape)
df_nest
# target	target2	data_nest	shape
# 0	0	1	sepal length (cm) sepal width (cm) petal...	(50, 4)
# 1	1	2	sepal length (cm) sepal width (cm) petal...	(50, 4)
# 2	2	3	sepal length (cm) sepal width (cm) peta...	(50, 4)

nest(df, columns_minus=df.columns[4:6], key='data_nest', copy=True).head()
# 	target	target2	data_nest
# 0	0	1	petal length (cm) petal width (cm) sepal...
# 1	1	2	petal length (cm) petal width (cm) sepal...
# 2	2	3	petal length (cm) petal width (cm) sepa...

nest(df, columns_between=['sepal length (cm)', 'petal width (cm)'])
# target	target2	data
# 0	0	1	sepal length (cm) sepal width (cm) petal...
# 1	1	2	sepal length (cm) sepal width (cm) petal...
# 2	2	3	sepal length (cm) sepal width (cm) peta...

# back to raw DataFrame
unnest(df_nest)[df.columns].head()
# sepal length (cm)	sepal width (cm)	petal length (cm)	petal width (cm)	target	target2
# 0	5.1	3.5	1.4	0.2	0	1
# 1	4.9	3.0	1.4	0.2	0	1
# 2	4.7	3.2	1.3	0.2	0	1
# 3	4.6	3.1	1.5	0.2	0	1
# 4	5.0	3.6	1.4	0.2	0	1

df_string = pd.DataFrame()
df_string['a'] = list('11223')
df_string['b'] = list('22334')
df_string['c'] = ['a', 'bb', 'ccc','dddd','eeeee']
df_string['d'] = df_string['c'].map(lambda x: list(x))
unnest(df_string)
# 	a	b	c	d
# 0	1	2	a	a
# 1	1	2	bb	b
# 2	1	2	bb	b
# 3	2	3	ccc	c
# 4	2	3	ccc	c
# 5	2	3	ccc	c
# 6	2	3	dddd	d
# 7	2	3	dddd	d
# 8	2	3	dddd	d
# 9	2	3	dddd	d
# 10	3	4	eeeee	e
# 11	3	4	eeeee	e
# 12	3	4	eeeee	e
# 13	3	4	eeeee	e
# 14	3	4	eeeee	e

field_apply = {k:v for (k, v) in (zip(df.columns[:2], [np.max, np.mean]))}
field_apply['sepal length (cm)'] = [np.min, np.max]
apply_window(df, field_apply, partition='target').head()
# 	sepal length (cm)_amin	sepal length (cm)_amax	sepal width (cm)_mean
# 0	4.3	5.8	3.418
# 1	4.3	5.8	3.418
# 2	4.3	5.8	3.418
# 3	4.3	5.8	3.418
# 4	4.3	5.8	3.418

col_gather = df.columns[:4]
df_gather = gather(df[col_gather])
df_gather.head()
# 	index	key	value
# 0	0	sepal length (cm)	5.1
# 1	0	sepal width (cm)	3.5
# 2	0	petal length (cm)	1.4
# 3	0	petal width (cm)	0.2
# 4	1	sepal length (cm)	4.9

spread(df_gather, ['index'], 'key')
# 	value
# key	petal length (cm)	petal width (cm)	sepal length (cm)	sepal width (cm)
# index				
# 0	1.4	0.2	5.1	3.5
# 1	1.4	0.2	4.9	3.0
# 2	1.3	0.2	4.7	3.2
# 3	1.5	0.2	4.6	3.1
# 4	1.4	0.2	5.0	3.6
```

