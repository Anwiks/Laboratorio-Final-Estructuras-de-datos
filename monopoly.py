from random import randint

class Dye(object):

    def __init__(self):
        pass

    def roll(self):
        return randint(0,6)

class Cuadro(object):
    """
    Data Attributes:
        name
    """

    def __init__(self, nombre):
        self.nombre = nombre

    def hacer_evento(self):
        print("Evento de cuadro activado")

class Propiedad(Cuadro):
    """
    Data Attributes:
        name
        price
        base_rent
        is_utility
        is_rr
        owner
    """

    def __init__(self, nombre, precio, renta_base, es_utilidad=False, 
                 is_rr=False):
        self.nombre = nombre
        self.precio = precio
        self.renta_base = renta_base
        self.dueño=None

        if es_utilidad:
            self.es_utilidad = True
        if(is_rr):
            self.is_rr = True

    def hacer_evento(self):
        if self.dueño is None:
            print("Caiste en una propiedad sin dueño")

            while True:
                print("\n", "Menu de propiedad sin dueño")    
                Juego.mostrar_menu(Juego.menu_de_propiedad_sin_dueño)
                seleccion = input("Selecciona una opcion: ")
                if seleccion == '1':
                    # Buy Property
                    if Juego.jugador_actual.balance >= self.precio:
                        Juego.jugador_actual.propiedades_con_dueño.append(self)
                        Juego.jugador_actual.balance -= self.precio 
                        print("Felicitaciones!", Juego.jugador_actual.nombre, 
                              "se compro exitosamente", self.nombre, 
                              "por el precio de", self.precio)
                        Juego.jugador_actual.mostrar_balance()
                    else:
                        print("Tu balance es de", Juego.jugador_actual.balance,
                              "Es insuficiente", self.nombre, "para el precio de",
                              self.price)

                    break    
                elif seleccion == '2':
                    # Do Not Buy Property
                    print("Elegiste no comprar {}.".format(self.nombre))
                    break
                else:
                   print("Opcion desconocida elegida!")

    def ver_propiedad(self):
        print(self.nombre)    

class Jugador(object):
    """
    Class Attributes:
        player_list
        max_num_players
    Data Attributes:
       name
       current_tile_index
       current_tile
       is_in_jail
       properties_owned       
       amount_of_money
    """
    lista_de_jugadores = []
    max_de_jugadores = 4

    def __init__(self, nombre):
        if len(Jugador.lista_de_jugadores) == Jugador.max_de_jugadores:
            print("Error: No puede haber mas de", Jugador.max_de_jugadores, "jugadores!") #DEBUG
        else:    
            self.nombre = nombre
            self.index_de_cuadro_actual = 0
            self.cuadro_actual = None # sets current tile to "GO" 
            self.esta_en_carcel = False
            self.rondas_en_carcel = 0
            self.propiedades_con_dueño = []
            self.balance = 1500

            Jugador.lista_de_jugadores.append(self)
            print(self.nombre, "fue perfectamente añadido!") #DEBUG            

    def roll_y_moverse(self): # should a method from one class depend on a data attribute from another class?
        roll_1 = Juego.DYE.roll()
        roll_2 = Juego.DYE.roll()
        total_roll = roll_1 + roll_2
        print("Tiraste un", roll_1) #DEBUG
        print("Tiraste un", roll_2) #DEBUG

        # move player to new tile
        if total_roll + self.index_de_cuadro_actual >= len(Juego.tablero):
            final_index = (self.index_de_cuadro_actual + total_roll) - len(Juego.tablero) 
            self.index_de_cuadro_actual = final_index
            self.cuadro_actual = Juego.tablero[self.index_de_cuadro_actual]
            self.balance += 200 # Pass GO
            print("Tu pasaste!") #DEBUG
        else:
            self.index_de_cuadro_actual = self.index_de_cuadro_actual + total_roll
            self.cuadro_actual = Juego.tablero[self.index_de_cuadro_actual]

        print("Tu actual cuadro es",self.cuadro_actual.nombre)    #DEBUG

        # trigger_event
        self.cuadro_actual.hacer_evento()

    def propiedades_con_dueño(self):
        print("{} Propiedades: ".format(self.nombre))
        for propiedad in self.propiedades_con_dueño:
            print(propiedad.nombre)

    def mostrar_balance(self):
        print("{} su balance es de {}".format(self.nombre, self.balance))

    def salir_de_carcel(self):
        pass

    """
    will put this in option function:

    def add_player():
        if len(Player.player_list) == Player.max_num_players:
            print("Error, cannot have more than",Player.max_num_players, "players")
            return
        else:
            print("You are adding a player")
            name = input('Please type the name of the player: ') # TODO: error check
            Player.player_list.append(Player(name))
            for player in Player.player_list: #DEBUG
                print(player.name, "successfully added!") 
    """


class Juego(object):
    """ Instantiate once"""

    jugador_actual = None
    contador_de_turno = 0
    DYE = Dye()
    tablero = None   
    setup_de_menu = None
    menu_de_jugador = None
    menu_de_propiedad_sin_dueño = None


    def __init__(self):

        Juego.tablero = [
            Cuadro("GO"),
            Propiedad("Mediterranean Avenue", 60, 2),
            Cuadro("Community Chest"),
            Propiedad("Baltic Avenue",60, 8),
            Cuadro("Income Tax"),
            Propiedad("Reading Railroad", 200, 50),
            Propiedad("Oriental Avenue", 100, 6),
            Cuadro("Chance"),
            Propiedad("Vermont Avenue", 100, 6),
            Propiedad("Connecticut Avenue", 120, 8),
            Cuadro("Jail"),
            Propiedad("St. Charles Place", 140, 10),
            Propiedad("Electric Company", 150, 0, es_utilidad=True),
            Propiedad("States Avenue", 140, 10),
            Propiedad("Virginia Avenue", 160, 12),
            Propiedad("Pennsylvania Railroad", 200, 50),
            Propiedad("St. James Place", 180, 14),
            Cuadro("Community Chest"),
            Propiedad("Tennessee Avenue", 180, 14),
            Propiedad("New York Avenue", 200, 16),
            Cuadro("Free Parking"),
            Propiedad("Kentucky Avenue", 220, 18),
            Cuadro("Chance"),
            Propiedad("Indiana Avenue", 220, 18),
            Propiedad("Illinois Avenue", 240, 20),
            Propiedad("B. & O. Railroad", 200, 50),
            Propiedad("Atlantic Avenue", 260, 22),
            Propiedad("Ventnor Avenue", 260, 22),
            Propiedad("Water Works", 150, 0, es_utilidad=True),
            Propiedad("Marvin Gardens", 280, 24),
            Cuadro("Go To Jail"),
            Propiedad("Pacific Avenue", 300, 26),
            Propiedad("North Caroliina Avenue", 300, 26),
            Cuadro("Community Chest"),
            Propiedad("Pennsylvania Avenue", 320, 28),
            Propiedad("Short Line", 200, 50),
            Cuadro("Chance"),
            Propiedad("Park Place", 350, 35),
            Cuadro("Luxury Tax"),
            Propiedad("Boardwalk", 400, 50)]

        Juego.setup_de_menu = {}
        Juego.setup_de_menu = {'1': "Añadir jugador." , '2': "Empezar juego."}
        Juego.menu_de_jugador = {}
        Juego.menu_de_jugador = {'1': "Tirar el dado.", '2': "Mostrar propiedades."}
        Juego.menu_de_propiedad_sin_dueño = {}
        Juego.menu_de_propiedad_sin_dueño = {'1': "Comprar propiedad", '2': "No comprar propiedad"}

        print("Bienvenido a Monopoly!")
        while True:
            print("\n")
            Juego.mostrar_menu(Juego.setup_de_menu)
            seleccion = input("Selecciona una opcion: ")
            if seleccion == '1':
                nombre_de_jugador = input("Porfavor poner el nombre de jugador: ")
                Jugador(nombre_de_jugador)
            elif seleccion == '2':
                if len(Jugador.lista_de_jugadores) == 0:
                    print("Error: No se puede empezar sin jugadores")
                else:
                    break
            else:
               print("Opcion desconocida seleccionada!")

        Juego.jugador_actual = Jugador.lista_de_jugadores[0]
        self.main() # Starts Main Game

    @staticmethod
    def mostrar_menu(menu: dict):
        for opcion in menu:
            print("{}. {}".format(opcion, menu[opcion]))


    def empezar_turno_de_jugador(self):
        if Juego.jugador_actual.esta_en_carcel:
            hizo_su_tiempo = Juego.jugador_actual.rondas_en_carcel == 3
            if hizo_su_tiempo:
                Juego.jugador_actual.salir_de_carcel()
            else:
                print("Todavia tiene que estar en carcel!")
                #TODO:
                #increment current_player.num_turns_in_jail
                #display in_jail_menu
                #code logic for menu selections
        elif True==False: #if player is bankrupt/ has lost
            pass
        else:
            while True:
                print("\n", "Menu de jugador:")
                Juego.mostrar_menu(Juego.menu_de_jugador)
                selection = input("Selecciona una opcion: ")
                if selection == '1':
                    # Player Rolls Dice and Moves
                    Juego.jugador_actual.roll_y_moverse()
                elif selection == '2':
                    # TODO:
                    print("")
                else:
                   print("Opcion seleccionada desconocida!")

    def terminar_turno_de_jugador(self):
        pass

    def main(self):
        while True:
            if Juego.jugador_actual.esta_en_carcel:
                self.terminar_turno_de_jugador()
            elif True == False: #TODO:make function that checks if there is a winner
                pass # all other players bankrupt, end game 
            else:
                self.empezar_turno_de_jugador()



if __name__ == "__main__":    
    Juego()