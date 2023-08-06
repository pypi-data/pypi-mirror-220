
# <b>Python Query Language PQL</b>

<b>PQL</b> is a python wrapper of the sql sintax based in SQLalchemy and pandas, this code introduces a new syntax to use 
in your code when calling a database table.

## Requirements

You only need a distribution of python3 installed.

## ⚙️Installation:

You can install the requirements (preferably in an environment) using:

> pip install PythonQueryLanguage

## Basic Usage:

PQL is managed by a class called SQLManager, to instanciated you will need to pass your connection strings in a dictionary
and the enviroment you are willoing to use

`
connection_dict = {'test_env': 'connection string from engine',
                   'prod_env': 'mssql+pyodbc://ur@prod.com/url2?driver=ODBC+Driver+17+for+SQL+Server'
                  }
env = 'test_env'
pql = SQLManager(connection_dict,env)
`

Once you have instanciated the class you can use it with his convenient functions that will wrap SQL expresions.

> pql.select_all('tableA','id','myid')  =  SELECT * FROM tableA WHERE id = 'myid

PQL supports searchs in arrays:

> pql.select_all('tableA','id',['myid','myid2'])  =  SELECT * FROM tableA WHERE id IN ('myid','myid2')

PQL cast the data in a inteligent manner:

> pql.select_all('tableA',['id','name'],['myid','myName'])  =  SELECT * FROM tableA WHERE id = 'myid' AND myName = 'myid2'

PQL accepts adiotional arguments:

> pql.select('column','tableA',['id','name'],['myid','myName'],'OR')  =  SELECT column FROM tableA WHERE id = 'myid' OR myName = 'myid2'

PQL accepts direct evaluation or raw sql expressions (thougt only recommended in edge cases)

> pql.query("SELECT * FROM tableA WHERE id = 'myid")  =  SELECT * FROM tableA WHERE id = 'myid'

PQL accepst function and Store procedure evaluations.

## Multy enviroment usage.

PQL is built to support working with different db environments at the same time, this multi enviroment work can be done in different ways:

- 1. Instanciate the PQLmanager with different enviroments and run them.
- 2. Changing the enviroment of the class with the change_enviroment method.
- 3. Using scoped functions.

Example of scoped functions:

You are working in a database test enviroment but you need to extract some data from the production enviroment without changing the enviroment of the PQLmanager
Then you can query the table at producion using a scope:

> pql.select_all('TableA',env='prod')

This function will run in the production environment and retrieve the information from it without changing your global environment.

## IUD

PQL supports Insert Update Delete Operations, all these operations are based in pandas dataframes.

## Interactive.

PQL is thought to be used in a jupyter notebook as well as used in real code. PQL contains different functionalities that allows the user
to know what query will be executed in the database and confirmation security.

