""" Módulo que incluye la clase de reproductor de música """


class Player:
    """ Clase que crea un reproductor de música """

    def play(self, song):
        """ 
        Reproduce la canción que recibe como parámetro

        Parameters:
        song (str): string con el path de la canción

        Returns:
        int: 1 si reproduce con éxito, en caso de fracaso devuelve 0
        """
        print("reproduciendo canción", song)

    def stop(self, song):
        """ 
        Deja de reproducir la canción que recibe como parámetro

        Parameters:
        song (str): string con el path de la canción

        Returns:
        int: 1 si reproduce con éxito, en caso de fracaso devuelve 0
        """
        print("stopping", song)
