import MySQLdb

class BD:
    def __init__(self):
        try:
            self.conexion=MySQLdb.connect(
                host='localhost',
                user='usuario',
                passwd='usuario',
                db='bdataxia')
            self._cursor = self.conexion.cursor()
            print("Conexión establecida con éxito")
        except Exception as e:
            print(f'Error de conexión: {e}')    
    
    def cerrar(self):
        self._cursor.close()
      
    def obtenerUsuarios(self):
        try:
            sql= 'SELECT * FROM usuarios'
            self._cursor.execute(sql)
            resultados = self._cursor.fetchall()
            return list(resultados)
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
                
    def login(self, usuario):
        try:
            sql= 'SELECT * FROM usuarios WHERE usuario="{}"'.format(usuario)
            n=self._cursor.execute(sql)
            if n == 0:
                return 0
            else:
                usu = self._cursor.fetchone()
                return usu
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
            
    def registrar(self, usuario, passwd, rol):
        try:
            sql = "INSERT INTO usuarios (usuario, passwd, rol) VALUES ('{}', '{}', '{}')".format(usuario, passwd, rol)
            n = self._cursor.execute(sql)
            self.conexion.commit()
            print("Se ha insertado", n, "usuario")
        except Exception as e:
            print(f'Error al realizar la inserción: {e}')
                        
    def verPublicaciones(self):
        try:
            sql = 'SELECT * FROM publicaciones'
            self._cursor.execute(sql)
            resultados = self._cursor.fetchall()
            return list(resultados)
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
                    
    def publicar(self, idUsuario, idTipoAtaxia, descripcion):
        try:
            sql = "INSERT INTO publicaciones (idUsuario, idTipoAtaxia, descripcion) VALUES ({}, {}, '{}')".format(idUsuario, idTipoAtaxia, descripcion)
            n = self._cursor.execute(sql)
            self.conexion.commit()
            print("Se ha insertado", n, "publicación")
        except Exception as e:
            print(f'Error al realizar la inserción: {e}')
            
    def verTiposAtaxia(self):
        try:
            sql = "SELECT * FROM tiposAtaxia"
            self._cursor.execute(sql)
            resultados = self._cursor.fetchall()
            return list(resultados)
        except Exception as e:
            print(f'Error al realizar la operación: {e}')  
            
    def tipoAtaxia(self):
        tiposAtaxia = list()
        try:
            sql = "SELECT nombre FROM tiposAtaxia"
            self._cursor.execute(sql)
            for ta in self._cursor.fetchall():
                tiposAtaxia.append(ta[0])
            return tiposAtaxia
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
            
    def obtenerIdTipotaxia(self, nombre):
        try:
            sql = 'SELECT * FROM tiposAtaxia WHERE nombre="{}"'.format(nombre)
            self._cursor.execute(sql)
            id = self._cursor.fetchone()
            return id[0]
        except Exception as e:
            print(f'Error al realizar la operación: {e}')       
    def roles(self):
        roles = list()
        try:
            sql = "SELECT nombre FROM roles"
            self._cursor.execute(sql)
            for rol in self._cursor.fetchall():
                roles.append(rol[0])
            return roles
        except Exception as e:
            print(f'Error al realizar la operación: {e}')   
            
    def eliminar(self, idPublicacion):
        try:
            sql = "DELETE FROM publicaciones WHERE id = '{}'".format(idPublicacion)
            n = self._cursor.execute(sql)
            self.conexion.commit()
            print("Se ha eliminado", n, "publicación")
        except Exception as e:
            print(f'Error al realizar la inserción: {e}')
            
    def meGusta(self, idUsuario, idPublicacion):
        try:
            sql = "INSERT INTO likes (idUsuario, idPublicacion) VALUES ({}, {})".format(idUsuario, idPublicacion)
            self._cursor.execute(sql)
            self.conexion.commit()
            
            sql = "UPDATE publicaciones SET likes = likes + 1 WHERE id = {}".format(idPublicacion)
            self._cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
            
    def quitarLike(self, idUsuario, idPublicacion):
        try:
            sql = "DELETE FROM likes WHERE idUsuario = {} AND idPublicacion = {}".format(idUsuario, idPublicacion)
            self._cursor.execute(sql)
            self.conexion.commit()
            
            sql = "UPDATE publicaciones SET likes = likes - 1 WHERE id = {}".format(idPublicacion)
            self._cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            print(f'Error al realizar la operación: {e}')

    def usuarioHaDadoLike(self, idUsuario, idPublicacion):
        try:
            sql = "SELECT * FROM likes WHERE idUsuario = {} AND idPublicacion = {}".format(idUsuario, idPublicacion)
            self._cursor.execute(sql)
            resultado = self._cursor.fetchone()
            return resultado is not None
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
            
    def likes(self, id):
        try:
            sql= 'SELECT likes FROM publicaciones WHERE id="{}"'.format(id)
            self._cursor.execute(sql)
            resultado = self._cursor.fetchone()
            return resultado[0] if resultado else 0
        except Exception as e:
            print(f'Error al realizar la operación: {e}')
