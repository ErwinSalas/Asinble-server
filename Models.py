class Usuario:
    def _init_(self, nombreUsuario, contrasenna, rol):
        self.nombreUsuario = nombreUsuario
        self.contrasenna = contrasenna
        self.rol = rol




class Session:
    __instance = None
    usuario= None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if Session.__instance == None:
            Session()
        return Session.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Session.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Session.__instance = self

    def getlogedUser(self):
        return  self.usuario


    def logUser(self,usuario):
        self.usuario=usuario