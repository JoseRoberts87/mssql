a useful library to facilitate interfacing with MsSql databases and enabling or simplifying functionality that otherwise does not exist or is difficult to compose

basic usage

pip install mssql


From MsSql import MsSql

# initialize the class
ms = MsSql(host='', db_name='', user='', pw='', driver='')

# Start the session
ms.session_conn() #this returns a sql alchemy engine session