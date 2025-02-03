import pysftp as sftp

class Connection:
    user = ""
    password = ""
    host = ""
    cnopts = ""

    def Connect(self,user,password,host,cnopts):
        conn = sftp.Connection(
        host=host, username=user, password=password,
        cnopts=cnopts)
        return conn

