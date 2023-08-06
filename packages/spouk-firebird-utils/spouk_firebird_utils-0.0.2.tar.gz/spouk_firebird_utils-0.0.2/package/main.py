import fdb
class Stocker:
    """ version 0.0.2 update"""

    def convertdbpath(self, dbpath):
        " convert string from 172.30.32.199:t053 -> 172.30.32.199/3050:t053"
        res = dbpath.split(':')
        return f'{res[0]}/3050:{res[1]}'

    def makeconnect(self, dbpath, dbuser, dbpassword):
        "make connect to database with user and password save global namespace for future uses"
        dsn = dict(dsn=self.convertdbpath(dbpath), user=dbuser, password=dbpassword, charset='utf8')
        try:
            self.currentconnect = fdb.connect(**dsn)
        except Exception as err:
            print(f'[error] establish connect to {dsn}, return `None` in result')
            self.currentconnect = None
            return None
        return

    def makeconnectExt(self, dbpath, dbuser, dbpassword):
        "make connect to database with user and password save global namespace for future uses"
        dsn = dict(dsn=self.convertdbpath(dbpath), user=dbuser, password=dbpassword, charset='utf8')
        try:
            con = fdb.connect(**dsn)
        except Exception as err:
            print(f'[error] establish connect to {dsn}, return `None` in result')
            return None
        return con

    def rundbrequest(self, request, many=True, single=False, nothing=False):
        "make request use self.currentconnection and return raw result"
        if self.currentconnect is not None:
            result = None
            cursor = self.currentconnect.cursor()
            try:
                cursor.execute(request)
            except Exception as err:
                print(f'[error] error in execute sql request in cursor  = {err}')
                return result
            if many:
                try:
                    result = cursor.fetchall()
                except Exception as err:
                    print(f'[error] error fetchall {err}')
                return result
            if single:
                try:
                    result = cursor.fetchone()
                except Exception as err:
                    print(f'[error] error fetchall {err}')
                return result
            if nothing:
                pass

            cursor.close()
            self.currentconnect.commit()
            return 0

    def rundbrequestExt(self, connector, request, many=True, single=False, nothing=False):
        "make request use self.currentconnection and return raw result"
        if connector is not None:
            cursor = connector.cursor()
            result = None
            try:
                cursor.execute(request)
            except Exception as err:
                print(f'[error] error in execute sql request in cursor  = {err}')
                return result
            if many:
                try:
                    result = cursor.fetchall()
                except Exception as err:
                    print(f'[error] error fetchall {err}')
                return result
            if single:
                try:
                    result = cursor.fetchone()
                except Exception as err:
                    print(f'[error] error fetchall {err}')
                return result

            if nothing:
                pass

            cursor.close()
            connector.commit()
            return 0
