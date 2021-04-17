# output
import texttable
from termcolor import colored
from datetime import datetime


class View:
    def __init__(self):
        self.table = texttable.Texttable()
        self.all_genres = [
            "documentary",
            "romance",
            "fantasy",
            "drama",
            "vision_view_entertainment",
            "telescene_film_group_productions",
            "action",
            "music",
            "science_fiction",
            "carousel_productions",
            "thriller",
            "the_cartel",
            "adventure",
            "family",
            "rogue_state",
            "pulser_productions",
            "odyssey_media",
            "war",
            "horror",
            "history",
            "animation",
            "western",
            "foreign_",
            "comedy",
            "crime",
            "tv_movie",
            "mystery",
        ]

    def SqlTime(self, time):
        print(colored(f"Time of query: {time} seconds", "green"))

    def AskReconnection(self):
        ch = input(
            "Do you want to reconnect to another port?\n1.Yes\n2.No\nEnter your chose: "
        )
        return ch

    def GetBackUpName(self, id_max):
        name_of_back = input(
            "Enter version of backup from 1 to " + str(int(id_max) - 1) + ": "
        )
        errors = ""
        if not name_of_back.isdigit():
            errors += "Name must contain only numbers. "
        if name_of_back.isdigit():
            if int(name_of_back) >= int(id_max) or int(name_of_back) < 0:
                errors += "Name must be higher than 0 and lower than " + str(id_max)
        if not errors == "":
            print(colored(errors, "red"))
            raise Exception
        return name_of_back

    def YourPort(self, port):
        print(f"You are on server with port: " + colored(port, "green"))

    def PortClosed(self, port):
        print(colored(f"Service with port {port} is closed", "red"))

    def BothClosed(self):
        print(colored("Both sevices are closed. Try to connect later", "red"))

    def YouCanOnlyRead(self):
        print("This service is " + colored("readonly", "red"))

    def Restore(self, items):
        print("Time of doing backup: " + colored(items, "green") + " ms")

    def BackUp(self, items):
        print("Time of doing backup: " + colored(items[1], "green") + " ms")
        print("Name backup: " + colored(items[0], "green"))

    def Errors(self, error):
        err = str(error)
        errors = ""
        if (
            err.find("Error tokenizing data") != -1
            or err.find("'DataFrame' object has no attribute") != -1
        ):
            errors += "Incorrect file content."
        if (
            err.find("[Errno 2] No such file or directory") != -1
            or err.find("Expected object or value") != -1
        ):
            errors += "No such file or directory."
        if (
            err.find("could not connect to server: Connection refused") != -1
            and err.find("TCP/IP connections on port 5432") != -1
        ):
            print(colored("Could not connect to server", "red"))
            ch = self.AskReconnection()
            return [int(ch), 5433]
        if (
            err.find("could not connect to server: Connection refused") != -1
            and err.find("TCP/IP connections on port 5433") != -1
        ):
            print(colored("Could not connect to server", "red"))
            ch = self.AskReconnection()
            return [int(ch), 5432]
        if err.find("server closed the connection unexpectedly") != -1:
            print(colored("Could not connect to server", "red"))
            ch = self.AskReconnection()
            return [int(ch), -1]
        if err.find("No file with such name") != -1:
            errors += "No file with such name."
        if err.find("Incorrect file content") != -1:
            errors += "Incorrect file content."
        if err.find("неприпустимий синтаксис для типу date") != -1:
            errors += "Incorrect date."
        if err.find("значення поля типу дата/час поза діапазоном") != -1:
            errors += "Incorrect date."
        if err.find('не присутній в таблиці "users"') != -1:
            errors += "No user with such id."
        if err.find('не присутній в таблиці "films"') != -1:
            errors += "No film with such id."
        if err.find('не присутній в таблиці "actors"') != -1:
            errors += "No actor with such id."
        if err.find("No rating for this period genres") != -1:
            errors += "No rating of genres for this period."
        if err.find("No rating for this period films") != -1:
            errors += "No rating of films for this period."
        if err.find("No rating for this period film") != -1:
            errors += "No rating of film."
        if err.find("Точка файл") != -1:
            errors += "You cannot create file with name which contains dot."
        print(colored(errors, "red"))
        return [-1, -1]

    def NoCom(self):
        print(colored("No such command", "red"))

    def VErrorMenu(self):
        print(colored("Incorrect command", "red"))

    def FKey(self):
        print(colored("Foreign Key error", "red"))

    def VError(self):
        print(colored("Incorrect id", "red"))

    def AError(self):
        print(colored("No entity with such id", "red"))
        print(
            "*****************************************************************************************************************"
        )

    ###############################################################################

    def Ask(self):
        print(
            """Choose table or sort which you want : \n1.Films\n2.Actor\n3.Users\n4.Rate\n5.Actor with films\n6.Films with genres\n7.Search film by name\n8.Search film by genres\n9.Search film by actor\n10.Get all user's rates\n11.Get rate of film\n12.Get diagrams of analize\n13.Reconnect to another service\n14.Do backup\n15.Back to save version\n0.Exit"""
        )
        return input("Your choise: ")

    def AskFilm(self):
        print(
            "Choose what you want : \n1.Show all films\n2.Show film by id\n3.Add film\n4.Update film\n5.Delete film\n6.Add films from json file\n7.Make csv file\n8.Make json file\n0.Exit"
        )
        return input("Your choise: ")

    def AskActor(self):
        print(
            "Choose what you want : \n1.Show all actors\n2.Show actor by id\n3.Add actor\n4.Update actor\n5.Delete actor\n6.Add actors from csv file\n7.Make csv file\n8.Make json file\n0.Exit"
        )
        return input("Your choise: ")

    def AskUser(self):
        print(
            "Choose what you want : \n1.Show all users\n2.Show user by id\n3.Add user\n4.Update user\n5.Delete user\n6.Add users from csv file\n7.Make csv file\n8.Make json file\n0.Exit"
        )
        return input("Your choise: ")

    def AskRate(self):
        print(
            "Choose what you want : \n1.Show all rates\n2.Show rate by id\n3.Add rate\n4.Update rate\n5.Delete rate\n6.Add random rates\n7.Make csv file\n8.Make json file\n0.Exit"
        )
        return input("Your choise: ")

    def AskActorWithFilms(self):
        print(
            "Choose what you want : \n1.Show all links between actor and film\n2.Show link between actor and film by id\n3.Add link between actor and film\n4.Update link between actor and film\n5.Delete link between actor and film\n6.Add random links between actor and film\n0.Exit"
        )
        return input("Your choise: ")

    def AskFilmsWithGenres(self):
        print(
            "Choose what you want : \n1.Show all links between film and genres\n2.Show link between film and genres by id\n3.Add link between film and genres\n4.Update link between film and genres\n5.Delete link between film and genres\n6.Add random links between film and genres\n0.Exit"
        )
        return input("Your choise: ")

    def AskDiagram(self):
        print(
            "Choose what you want : \n1.Rating of genres\n2.Rating of films\n3.Rating of speacial film\n4.Average rating on special dates\n0.Exit"
        )
        return input("Your choise: ")

    def GetId(self):
        return input("Enter id: ")

    def Amount(self):
        return input("Enter amount of random entities: ")

    def GetDates(self):
        date_low = input("Enter from which date: ")
        date_high = input("Enter to which date: ")
        return [str(date_low), str(date_high)]

    def AskNameOfFile(self):
        name = input("Enter name of file: ")
        # if name.find(".") != -1:
        #    raise Exception("Точка файл")
        return name

    def ExportFile(self, name):
        print(f"File was successfully exported with name" + colored(name, "green"))

    def ImportFile(self, name):
        print(colored(f"Import file from file with {name}", "green"))

    def PathToGraph(self, name_of_file):
        print(colored(f"This graph was added by path {name_of_file}", "green"))

    def RandomActorWithFilms(self, amount):
        print(
            colored(
                f"Random {amount} links beetwen actors and films was added", "green"
            )
        )

    def RandomRate(self, amount):
        print(colored(f"Random {amount} Rates was added", "green"))

    def RandomFilm(self, amount):
        print(colored(f"Random {amount} Films was added", "green"))

    def InsertActorsFromData(self):
        print(colored("Actors from file was added", "green"))

    def InsertFilmsFromData(self):
        print(colored("Films from file was added", "green"))

    def InsertUsersFromData(self):
        print(colored("Users from file was added", "green"))

    #################################################################
    def GetName(self):
        return input("Enter name: ")

    def GetItemsFilm(self):
        errors = ""
        name = input("Enter name: ")
        language = input("Enter language: ")
        overwiev = input("Enter overwiev: ")
        homepage = input("Enter homepage: ")
        adult = input("Enter adult: ")
        budget = input("Enter budget: ")
        if not budget.isdigit():
            errors += "Budget must contain only numbers. "

        if (
            not adult.lower() == "true"
            and not adult.lower() == "false"
            and not adult.lower() == "1"
            and not adult.lower() == "0"
        ):
            errors += "Adult must be true or false or 1 or 2."

        if not errors == "":
            print(colored(errors, "red"))
            raise Exception
        return [name, language, overwiev, homepage, adult, budget]

    def GetGenres(self):
        errors = ""
        i = 0
        while i < len(self.all_genres):
            print(str(i + 1) + ". " + self.all_genres[i])
            i = i + 1
        numders_of_genres = (
            input("Enter numders of genres: ").replace(" ", "").split(",")
        )
        genres = []
        for num in numders_of_genres:
            if not num.isdigit():
                errors += "You need enter only number of genres"
                print(colored(errors, "red"))
                raise Exception
            genres.append(self.all_genres[int(num) - 1])
        return genres

    def showAllFilms(self, rows):
        print(
            "*****************************************************************************************************************\nFilms"
        )
        rows = [
            ("Id", "Name", "Language", "Overwiev", "Homepage", "Adult", "Budget")
        ] + rows
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def FilmById(self, row):
        print(
            "*****************************************************************************************************************\nFilm"
        )
        rows = [
            ("Id", "Name", "Language", "Overwiev", "Homepage", "Adult", "Budget")
        ] + [row]
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def InsertFilm(self, row):
        print("/////////////////////////////////////////////////")
        rows = [
            ("Id", "Name", "Language", "Overwiev", "Homepage", "Adult", "Budget")
        ] + [row]
        self.table.add_rows(rows)
        print("Film was added")
        print(self.table.draw())
        self.table = texttable.Texttable()
        print("/////////////////////////////////////////////////")

    def UpdateFilm(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Film with id: {id} was updated")
        print("/////////////////////////////////////////////////")

    def DeleteFilm(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Film with id: {id} was deleted")
        print("/////////////////////////////////////////////////")

    ###################################################################################################
    def GetItemsActor(self):
        name = input("Enter name: ")
        image = input("Enter image: ")
        bio = input("Enter bio: ")
        return [name, image, bio]

    def showAllActors(self, rows):
        print(
            "*****************************************************************************************************************\nActors"
        )
        rows = [("Id", "Name", "Image", "Bio")] + rows
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def ActorById(self, row):
        print(
            "*****************************************************************************************************************\nActor"
        )
        rows = [("Id", "Name", "Image", "Bio")] + [row]
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def InsertActor(self, row):
        print("/////////////////////////////////////////////////")
        rows = [("Id", "Name", "Image", "Bio")] + [row]
        self.table.add_rows(rows)
        print("Actor was added")
        print(self.table.draw())
        self.table = texttable.Texttable()
        print("/////////////////////////////////////////////////")

    def UpdateActor(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Actor with id: {id} was updated")
        print("/////////////////////////////////////////////////")

    def DeleteActor(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Actor with id: {id} was deleted")
        print("/////////////////////////////////////////////////")

    ###################################################################################################
    def GetItemsUser(self):
        errors = ""
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        login = input("Enter login: ")
        age = input("Enter age: ")
        city = input("Enter city: ")
        if not age.isdigit():
            print("Age must be a number.")
            raise Exception
        age = int(age)
        if age > 170 or age < 0:
            print("Age cannot be bigger than 170 or lower than 0.")
            raise Exception
        return [name, surname, login, age, city]

    def showAllUsers(self, rows):
        print(
            "*****************************************************************************************************************\nUsers"
        )
        rows = [("Id", "Name", "Surname", "Login", "Age", "City")] + rows
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def UserById(self, row):
        print(
            "*****************************************************************************************************************\nUser"
        )
        rows = [("Id", "Name", "Surname", "Login", "Age", "City")] + [row]
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def InsertUser(self, row):
        print("/////////////////////////////////////////////////")
        rows = [("Id", "Name", "Surname", "Login", "Age", "City")] + [row]
        self.table.add_rows(rows)
        print("User was added")
        print(self.table.draw())
        self.table = texttable.Texttable()
        print("/////////////////////////////////////////////////")

    def UpdateUser(self, id):
        print("/////////////////////////////////////////////////")
        print(f"User with id: {id} was updated")
        print("/////////////////////////////////////////////////")

    def DeleteUser(self, id):
        print("/////////////////////////////////////////////////")
        print(f"User with id: {id} was deleted")
        print("/////////////////////////////////////////////////")

    ###################################################################################################

    def GetItemsRate(self):
        errors = ""
        user_id = input("Enter user_id: ")
        film_id = input("Enter film_id: ")
        rate = input("Enter rate: ")
        time = input("Enter time: ")
        if not user_id.isdigit():
            errors += "User_id must be a number."
        if not film_id.isdigit():
            errors += "Film_id must be a number."
        if not rate.replace(".", "", 1).replace(",", "", 1).isdigit():
            print(colored(errors + "Rate can be only number. ", "red"))
            raise Exception
        rate = float(rate)
        if rate > 10 or rate < 0:
            print(colored(errors + "Rate can be between 10 and 0. ", "red"))
            raise Exception
        if not errors == "":
            print(colored(errors, "red"))
            raise Exception
        user_id = int(user_id)
        film_id = int(film_id)
        return [user_id, film_id, rate, time]

    def showAllRates(self, rows):
        print(
            "*****************************************************************************************************************\nRates"
        )
        rows = [("Id", "User_id", "Film_id", "Rate", "Time")] + rows
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def RateById(self, row):
        print(
            "*****************************************************************************************************************\nRate"
        )
        rows = [("Id", "User_id", "Film_id", "Rate", "Time")] + [row]
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def InsertRate(self, row):
        print("/////////////////////////////////////////////////")
        rows = [("Id", "User_id", "Film_id", "Rate", "Time")] + [row]
        self.table.add_rows(rows)
        print("Rate was added")
        print(self.table.draw())
        self.table = texttable.Texttable()
        print("/////////////////////////////////////////////////")

    def UpdateRate(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Rate with id: {id} was updated")
        print("/////////////////////////////////////////////////")

    def DeleteRate(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Rate with id: {id} was deleted")
        print("/////////////////////////////////////////////////")

    ###################################################################################################

    def GetItemsActorWithFilms(self):
        errors = ""
        film_id = input("Enter film_id: ")
        actor_id = input("Enter actor_id: ")
        if not film_id.isdigit():
            errors += "Film_id must be a number."
        if not actor_id.isdigit():
            errors += "Actor_id must be a number."
        if not errors == "":
            print(colored(errors, "red"))
            raise Exception
        film_id = int(film_id)
        actor_id = int(actor_id)
        return [film_id, actor_id]

    def showAllActorWithFilms(self, rows):
        print(
            "*****************************************************************************************************************\nLinks between actor and film"
        )
        rows = [("Id", "Film_id", "Actor_id")] + rows
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def ActorWithFilmsById(self, row):
        print(
            "*****************************************************************************************************************\nLink between actor and film"
        )
        rows = [("Id", "Film_id", "Actor_id")] + [row]
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def InsertActorWithFilms(self, row):
        print("/////////////////////////////////////////////////")
        rows = [("Id", "Film_id", "Actor_id")] + [row]
        self.table.add_rows(rows)
        print("Link between actor and film was added")
        print(self.table.draw())
        self.table = texttable.Texttable()
        print("/////////////////////////////////////////////////")

    def UpdateActorWithFilms(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Link between actor and film with id: {id} was updated")
        print("/////////////////////////////////////////////////")

    def DeleteActorWithFilms(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Link between actor and film with id: {id} was deleted")
        print("/////////////////////////////////////////////////")

    ###################################################################################################

    def GetItemsFilmsWithGenres(self):
        errors = ""
        film_id = input("Enter film_id: ")
        if not film_id.isdigit():
            errors += "Film_id must be a number."
        i = 0
        while i < len(self.all_genres):
            print(str(i + 1) + ". " + self.all_genres[i])
            i = i + 1
        numders_of_genres = (
            input("Enter numders of genres: ").replace(" ", "").split(",")
        )
        genres = []
        for num in numders_of_genres:
            if not num.isdigit():
                errors += "You need enter only number of genres"
                print(colored(errors, "red"))
                raise Exception
            genres.append(self.all_genres[int(num) - 1])
        return [film_id, genres]

    def showAllFilmsWithGenres(self, rows):
        end_rows = []
        for row in rows:
            row_tuple = []
            genres = ""
            row_tuple.append(row[0])
            row_tuple.append(row[1])
            i = 2
            while i < len(row):
                if row[i] == 1:
                    genres += self.all_genres[i - 2] + ","
                i = i + 1
            genres = genres[:-1]
            row_tuple.append(genres)
            end_rows.append(tuple(row_tuple))

        print(
            "*****************************************************************************************************************\nFilms with genres"
        )
        end_rows = [("Id", "Film_id", "Genres")] + end_rows
        self.table.add_rows(end_rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def FilmsWithGenresById(self, row):
        row_tuple = []
        end_rows = []
        genres = ""
        if row:
            row_tuple.append(row[0])
            row_tuple.append(row[1])
            i = 2
            while i < len(row):
                if row[i] == 1:
                    genres += self.all_genres[i - 2] + ","
                i = i + 1
            genres = genres[:-1]
            row_tuple.append(genres)
            end_rows.append(tuple(row_tuple))
        print(
            "*****************************************************************************************************************\nFilms with genres"
        )
        if not row:
            raise AttributeError
        end_rows = [("Id", "Film_id", "Genres")] + end_rows
        self.table.add_rows(end_rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )

    def InsertFilmsWithGenres(self, row):
        print("/////////////////////////////////////////////////")
        row_tuple = []
        end_rows = []
        genres = ""
        row_tuple.append(row[0])
        row_tuple.append(row[1])
        i = 2
        while i < len(row):
            if row[i] == 1:
                genres += self.all_genres[i - 2] + ","
            i = i + 1
        genres = genres[:-1]
        row_tuple.append(genres)
        end_rows.append(tuple(row_tuple))
        end_rows = [("Id", "Film_id", "Genres")] + end_rows
        self.table.add_rows(end_rows)
        print("Link between film and genres was added")
        print(self.table.draw())
        self.table = texttable.Texttable()
        print("/////////////////////////////////////////////////")

    def UpdateFilmsWithGenres(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Link between film and genres with id: {id} was updated")
        print("/////////////////////////////////////////////////")

    def DeleteFilmsWithGenres(self, id):
        print("/////////////////////////////////////////////////")
        print(f"Link between film and genres with id: {id} was deleted")
        print("/////////////////////////////////////////////////")

    ######################################################################################
    def RateOfFilm(self, row):
        print(
            "*****************************************************************************************************************\nRate of film"
        )
        rows = [("Avg rate", "Film_id")] + [row]
        self.table.add_rows(rows)
        print(self.table.draw())
        self.table = texttable.Texttable()
        print(
            "*****************************************************************************************************************"
        )
