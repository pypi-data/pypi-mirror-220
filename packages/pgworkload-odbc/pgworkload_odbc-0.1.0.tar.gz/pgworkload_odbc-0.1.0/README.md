# pgworkload-odbc

**pgworkload-odbc** is [pgworkload](https://github.com/fabiog1901/pgworkload)'s little brother using [pyodbc](https://github.com/mkleehammer/pyodbc) and [psqlODBC](https://odbc.postgresql.org/).

## Setup

### MacOS

Steps taken from <https://www.boriel.com/postgresql-odbc-connection-from-mac-os-x.html>.

First, install [unixODBC](https://www.unixodbc.org/)

```bash
brew install unixodbc
```

Then, download latest **psqlODBC** source code from <https://www.postgresql.org/ftp/odbc/versions/src/>.

Unzip, cd to that directory and

```bash
./configure
make
make install
```

You will see these files have been built:

```bash
ll /usr/local/lib/ps*
-rwxr-xr-x  1 fabio  admin   992B Jul 18 09:25 /usr/local/lib/psqlodbca.la*
-rwxr-xr-x  1 fabio  admin   557K Jul 18 09:25 /usr/local/lib/psqlodbca.so*
-rwxr-xr-x  1 fabio  admin   992B Jul 18 09:25 /usr/local/lib/psqlodbcw.la*
-rwxr-xr-x  1 fabio  admin   580K Jul 18 09:25 /usr/local/lib/psqlodbcw.so*
```

Create file `/usr/local/etc/odbcinst.ini` :

```ini
[PostgreSQL Unicode]
Description     = PostgreSQL ODBC driver (Unicode version)
Driver          = psqlodbcw.so
Debug           = 0
CommLog         = 1
UsageCount      = 1
```

Optionally, if you want to use the DSN, create file `~/.odbc.ini`

```ini
[fabio]
Driver      = PostgreSQL Unicode
ServerName  = localhost
Port        = 5432
Database    = fabio
Username    = fabio
Password    = 
Protocol    = 13.1.6
Debug       = 1

[fabiocrl]
Driver      = PostgreSQL Unicode
ServerName  = localhost
Port        = 26257
Database    = fabio
Username    = fabio
Password    = 
Protocol    = 13.1.6
Debug       = 1
```

Now you can install [pyodbc](https://github.com/mkleehammer/pyodbc)

```bash
pip install pyodbc
```

Here below some sample code, just for reference, as we use `pgworkload-odbc` to run transactions.

```python
import pyodbc

APP_NAME='fab2'

# with pyodbc.connect('DSN=fabiocrl') as conn:
with pyodbc.connect('Driver={PostgreSQL UNICODE};Server=localhost;Port=26257;Database=fabio;Uid=fabio;Pwd=fabio;sslmode=require', autocommit=True,) as conn:
    with conn.cursor() as cur:
        cur.execute(f"SET application_name = '{APP_NAME}'")
        # cur.execute("select * from fabio;")

        # while True:
        #     row = cur.fetchone()
        #     if not row:
        #         break
        #     print(row)
    
    
        for x in range(500):
            cur.execute("insert into fabio (id) values (?)", (x, ))
```

## Running

```bash
# install pgworkload_odbc
pip install pgworkload_odbc

# run it
pgworkload-odbc run -w workloads/bank.py --url 'Driver={PostgreSQL UNICODE};Server=localhost;Port=26257;Database=bank;Uid=fabio;Pwd=fabio;sslmode=require' -c 1
```
