# input
import psycopg2
import model
import view


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.view = view.View()

    def RandomFilm(self):
        items = self.view.GetFromTo()
        self.model.RandomFilm(self.view.Amount(), items[0], items[1])

    def OpenBD(self, port):
        try:
            self.model.OpenBD(port)
        except Exception as e:
            items = self.view.Errors(e)
            if items[0] == 1:
                try:
                    self.model.OpenBD(5433)
                    self.view.YourPort(5433)
                except psycopg2.OperationalError:
                    self.view.BothClosed()
                    return -1
            if items[0] == 2:
                return -1

    def CloseBD(self):
        self.model.CloseBD()

    def start(self):
        ch = -1
        while ch != 0:
            try:
                ch = int(self.view.Ask())
                while ch == 1:
                    cho = int(self.view.AskFilm())
                    try:
                        if cho == 1:
                            self.AllFilms()
                        elif cho == 2:
                            id = int(self.view.GetId())
                            self.FilmById(id)
                        elif cho == 3:
                            items = self.view.GetItemsFilm()
                            self.InsertFilm(
                                items[0],
                                items[1],
                                items[2],
                                items[3],
                                items[4],
                                items[5],
                            )
                            self.model.Commit()
                        elif cho == 4:
                            id = int(self.view.GetId())
                            self.FilmById(id)
                            items = self.view.GetItemsFilm()
                            self.UpdateFilm(
                                id,
                                items[0],
                                items[1],
                                items[2],
                                items[3],
                                items[4],
                                items[5],
                            )
                            self.model.Commit()
                        elif cho == 5:
                            id = int(self.view.GetId())
                            self.FilmById(id)
                            self.DeleteFilm(id)
                            self.model.Commit()
                        elif cho == 6:
                            self.InsertFilmsFromData()
                            self.model.Commit()
                        elif cho == 7:
                            name = self.view.AskNameOfFile()
                            name = self.model.FilmsToCsv(name)
                            self.view.ExportFile(name)
                        elif cho == 8:
                            name = self.view.AskNameOfFile()
                            name = self.model.FilmsToJson(name)
                            self.view.ExportFile(name)
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 2:
                    cho = int(self.view.AskActor())
                    try:
                        if cho == 1:
                            self.AllActors()
                        elif cho == 2:
                            id = int(self.view.GetId())
                            self.ActorById(id)
                        elif cho == 3:
                            items = self.view.GetItemsActor()
                            self.InsertActor(items[0], items[1], items[2])
                            self.model.Commit()
                        elif cho == 4:
                            id = int(self.view.GetId())
                            self.ActorById(id)
                            items = self.view.GetItemsActor()
                            self.UpdateActor(id, items[0], items[1], items[2])
                            self.model.Commit()
                        elif cho == 5:
                            id = int(self.view.GetId())
                            self.ActorById(id)
                            self.DeleteActor(id)
                            self.model.Commit()
                        elif cho == 6:
                            self.InsertActorsFromData()
                            self.model.Commit()
                        elif cho == 7:
                            name = self.view.AskNameOfFile()
                            name = self.model.ActorsToCsv(name)
                            self.view.ExportFile(name)
                        elif cho == 8:
                            name = self.view.AskNameOfFile()
                            name = self.model.ActorsToJson(name)
                            self.view.ExportFile(name)
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 3:
                    cho = int(self.view.AskUser())
                    try:
                        if cho == 1:
                            self.AllUsers()
                        elif cho == 2:
                            id = int(self.view.GetId())
                            self.UserById(id)
                        elif cho == 3:
                            items = self.view.GetItemsUser()
                            self.InsertUser(
                                items[0], items[1], items[2], items[3], items[4]
                            )
                            self.model.Commit()
                        elif cho == 4:
                            id = int(self.view.GetId())
                            self.UserById(id)
                            items = self.view.GetItemsUser()
                            self.UpdateUser(
                                id, items[0], items[1], items[2], items[3], items[4]
                            )
                            self.model.Commit()
                        elif cho == 5:
                            id = int(self.view.GetId())
                            self.UserById(id)
                            self.DeleteUser(id)
                            self.model.Commit()
                        elif cho == 6:
                            self.InsertUsersFromData()
                            self.model.Commit()
                        elif cho == 7:
                            name = self.view.AskNameOfFile()
                            name = self.model.UsersToCsv(name)
                            self.view.ExportFile(name)
                        elif cho == 8:
                            name = self.view.AskNameOfFile()
                            name = self.model.UsersToJson(name)
                            self.view.ExportFile(name)
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 4:
                    cho = int(self.view.AskRate())
                    try:
                        if cho == 1:
                            self.AllRates()
                        elif cho == 2:
                            id = int(self.view.GetId())
                            self.RateById(id)
                        elif cho == 3:
                            items = self.view.GetItemsRate()
                            self.InsertRate(items[0], items[1], items[2], items[3])
                            self.model.Commit()
                        elif cho == 4:
                            id = int(self.view.GetId())
                            self.RateById(id)
                            items = self.view.GetItemsRate()
                            self.UpdateRate(id, items[0], items[1], items[2], items[3])
                            self.model.Commit()
                        elif cho == 5:
                            id = int(self.view.GetId())
                            self.RateById(id)
                            self.DeleteRate(id)
                            self.model.Commit()
                        elif cho == 6:
                            amount = int(self.view.Amount())
                            self.RandomRate(amount)
                            self.model.Commit()
                        elif cho == 7:
                            name = self.view.AskNameOfFile()
                            name = self.model.RatesToCsv(name)
                            self.view.ExportFile(name)
                        elif cho == 8:
                            name = self.view.AskNameOfFile()
                            name = self.model.RatesToJson(name)
                            self.view.ExportFile(name)
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 5:
                    cho = int(self.view.AskActorWithFilms())
                    try:
                        if cho == 1:
                            self.AllActorWithFilms()
                        elif cho == 2:
                            id = int(self.view.GetId())
                            self.ActorWithFilmsById(id)
                        elif cho == 3:
                            items = self.view.GetItemsActorWithFilms()
                            self.InsertActorWithFilms(items[0], items[1])
                            self.model.Commit()
                        elif cho == 4:
                            id = int(self.view.GetId())
                            self.ActorWithFilmsById(id)
                            items = self.view.GetItemsActorWithFilms()
                            self.UpdateActorWithFilms(id, items[0], items[1])
                            self.model.Commit()
                        elif cho == 5:
                            id = int(self.view.GetId())
                            self.ActorWithFilmsById(id)
                            self.DeleteActorWithFilms(id)
                            self.model.Commit()
                        elif cho == 6:
                            amount = int(self.view.Amount())
                            self.RandomActorWithFilms(amount)
                            self.model.Commit()
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 6:
                    cho = int(self.view.AskFilmsWithGenres())
                    try:
                        if cho == 1:
                            self.AllFilmsWithGenres()
                        elif cho == 2:
                            id = int(self.view.GetId())
                            self.FilmsWithGenresById(id)
                        elif cho == 3:
                            items = self.view.GetItemsFilmsWithGenres()
                            print(items)
                            self.InsertFilmsWithGenres(items[0], items[1])
                            self.model.Commit()
                        elif cho == 4:
                            id = int(self.view.GetId())
                            self.FilmsWithGenresById(id)
                            items = self.view.GetItemsFilmsWithGenres()
                            self.UpdateFilmsWithGenres(id, items[0], items[1])
                            self.model.Commit()
                        elif cho == 5:
                            id = int(self.view.GetId())
                            self.FilmsWithGenresById(id)
                            self.DeleteFilmsWithGenres(id)
                            self.model.Commit()
                        elif cho == 6:
                            amount = int(self.view.Amount())
                            self.RandomFilmsWithGenres(amount)
                            self.model.Commit()
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 7:
                    try:
                        name = str(self.view.GetName())
                        self.FilmByName(name)
                        self.model.Commit()
                        break
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 8:
                    try:
                        genres = self.view.GetGenres()
                        self.FilmByGenres(genres)
                        self.model.Commit()
                        break
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 9:
                    try:
                        name = str(self.view.GetName())
                        self.FilmByActor(name)
                        self.model.Commit()
                        break
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 10:
                    try:
                        id = int(self.view.GetId())
                        self.RateByUser(id)
                        self.model.Commit()
                        break
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 11:
                    try:
                        id = int(self.view.GetId())
                        self.RateOfFilm(id)
                        self.model.Commit()
                        break
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 12:
                    cho = int(self.view.AskDiagram())
                    try:
                        if cho == 1:
                            items = self.view.GetDates()
                            self.RateGenresDiagram(items[0], items[1])
                            self.model.Commit()
                        elif cho == 2:
                            items = self.view.GetDates()
                            self.RateFilmsDiagram(items[0], items[1])
                            self.model.Commit()
                        elif cho == 3:
                            id = int(self.view.GetId())
                            self.RateFilmDiagram(id)
                            self.model.Commit()
                        elif cho == 4:
                            items = self.view.GetDates()
                            name_of_file = self.model.RatingTimeDiagram(
                                items[0], items[1]
                            )
                            self.view.PathToGraph(name_of_file)
                            self.model.Commit()
                        elif cho == 0:
                            break
                        else:
                            self.view.NoCom()
                    except ValueError:
                        self.view.VError()
                    except AttributeError as e:
                        print(e)
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        print(e)
                        self.view.Errors(e)
                        self.model.Commit()
                while ch == 13:
                    if self.model.GetPort() == 5432:
                        try:
                            self.model.reconnect(5433)
                            self.view.YourPort(self.model.GetPort())
                            break
                        except psycopg2.OperationalError:
                            self.view.PortClosed(5433)
                            break
                    if self.model.GetPort() == 5433:
                        try:
                            self.model.reconnect(5432)
                            self.view.YourPort(self.model.GetPort())
                            break
                        except psycopg2.OperationalError:
                            self.view.PortClosed(5432)
                            break
                while ch == 14:
                    items = self.model.backup()
                    self.view.BackUp(items)
                    break
                while ch == 15:
                    try:
                        id_max = self.model.GetName_of_backup()
                        name_of_back = self.view.GetBackUpName(int(id_max))
                        items = self.model.restore(name_of_back)
                        self.view.Restore(items)
                        self.model.Commit()
                        break
                    except ValueError:
                        self.view.VError()
                    except AttributeError:
                        self.view.AError()
                    except psycopg2.OperationalError as e:
                        items = self.view.Errors(e)
                        if items[0] == 1:
                            try:
                                if self.model.GetPort() == 5432:
                                    self.model.reconnect(5433)
                                if self.model.GetPort() == 5433:
                                    self.model.reconnect(5432)
                                self.view.YourPort(self.model.GetPort())
                            except psycopg2.OperationalError:
                                self.view.BothClosed()
                                ch = 0
                        if items[0] == 2:
                            ch = 0
                        try:
                            self.model.Commit()
                        except psycopg2.InterfaceError:
                            do_nothing = 0
                    except psycopg2.errors.ReadOnlySqlTransaction as e:
                        self.view.YouCanOnlyRead()
                        self.model.Commit()
                    except Exception as e:
                        self.view.Errors(e)
                        self.model.Commit()
                if ch > 15 or ch < 0:
                    self.view.NoCom()
            except ValueError:
                self.view.VErrorMenu()

    ####################################################################

    def RateGenresDiagram(self, date_low, date_high):
        name_of_file = self.model.RateGenresDiagram(date_low, date_high)
        self.view.PathToGraph(name_of_file)

    def RateFilmsDiagram(self, date_low, date_high):
        name_of_file = self.model.RateFilmsDiagram(date_low, date_high)
        self.view.PathToGraph(name_of_file)

    def RateFilmDiagram(self, id):
        name_of_file = self.model.RateFilmDiagram(id)
        self.view.PathToGraph(name_of_file)

    ##############################################################

    def AllFilms(self):
        rows = self.model.AllFilms()
        self.view.showAllFilms(rows)

    def FilmById(self, id):
        row = self.model.FilmById(id)
        self.view.FilmById(row)

    def FilmByName(self, name):
        rows = self.model.SearchFilmByName(name)
        self.view.showAllFilms(rows)

    def FilmByActor(self, name):
        rows = self.model.SearchFilmByActor(name)
        self.view.showAllFilms(rows)

    def FilmByGenres(self, genres):
        rows = self.model.SearchFilmByGenres(genres)
        self.view.showAllFilms(rows)

    def InsertFilm(self, name, language, overwiev, homepage, adult, budget):
        id = self.model.InsertFilm(name, language, overwiev, homepage, adult, budget)
        row = self.model.FilmById(id)
        self.view.InsertFilm(row)

    def UpdateFilm(self, id, name, language, overwiev, homepage, adult, budget):
        self.model.UpdateFilm(id, name, language, overwiev, homepage, adult, budget)
        self.view.UpdateFilm(id)

    def DeleteFilm(self, id):
        self.model.DeleteFilm(id)
        self.view.DeleteFilm(id)

    def InsertFilmsFromData(self):
        name = self.view.AskNameOfFile()
        name = self.model.InsertFilmsFromData(name)
        self.view.ImportFile(name)
        self.view.InsertFilmsFromData()

    ##############################################################
    def AllActors(self):
        rows = self.model.AllActors()
        self.view.showAllActors(rows)

    def ActorById(self, id):
        row = self.model.ActorById(id)
        self.view.ActorById(row)

    def InsertActor(self, name, image, bio):
        id = self.model.InsertActor(name, image, bio)
        row = self.model.ActorById(id)
        self.view.InsertActor(row)

    def UpdateActor(self, id, name, image, bio):
        self.model.UpdateActor(id, name, image, bio)
        self.view.UpdateActor(id)

    def DeleteActor(self, id):
        self.model.DeleteActor(id)
        self.view.DeleteActor(id)

    def InsertActorsFromData(self):
        name = self.view.AskNameOfFile()
        name = self.model.InsertActorsFromData(name)
        self.view.ImportFile(name)
        self.view.InsertActorsFromData()

    #######################################################################
    def AllUsers(self):
        rows = self.model.AllUsers()
        self.view.showAllUsers(rows)

    def UserById(self, id):
        row = self.model.UserById(id)
        self.view.UserById(row)

    def InsertUser(self, name, surname, login, age, city):
        id = self.model.InsertUser(name, surname, login, age, city)
        row = self.model.UserById(id)
        self.view.InsertUser(row)

    def UpdateUser(self, id, name, surname, login, age, city):
        self.model.UpdateUser(id, name, surname, login, age, city)
        self.view.UpdateUser(id)

    def DeleteUser(self, id):
        self.model.DeleteUser(id)
        self.view.DeleteUser(id)

    def InsertUsersFromData(self):
        name = self.view.AskNameOfFile()
        name = self.model.InsertUsersFromData(name)
        self.view.ImportFile(name)
        self.view.InsertUsersFromData()

    #######################################################################
    def AllRates(self):
        rows = self.model.AllRates()
        self.view.showAllRates(rows)

    def RateById(self, id):
        row = self.model.RateById(id)
        self.view.RateById(row)

    def InsertRate(self, user_id, film_id, rate, time):
        id = self.model.InsertRate(user_id, film_id, rate, time)
        row = self.model.RateById(id)
        self.view.InsertRate(row)

    def UpdateRate(self, id, user_id, film_id, rate, time):
        self.model.UpdateRate(id, user_id, film_id, rate, time)
        self.view.UpdateRate(id)

    def DeleteRate(self, id):
        self.model.DeleteRate(id)
        self.view.DeleteRate(id)

    def RandomRate(self, amount):
        self.model.RandomRate(amount)
        self.view.RandomRate(amount)

    #######################################################################
    def AllActorWithFilms(self):
        rows = self.model.AllActorWithFilms()
        self.view.showAllActorWithFilms(rows)

    def ActorWithFilmsById(self, id):
        row = self.model.ActorWithFilmsById(id)
        self.view.ActorWithFilmsById(row)

    def InsertActorWithFilms(self, film_id, actor_id):
        id = self.model.InsertActorWithFilms(film_id, actor_id)
        row = self.model.ActorWithFilmsById(id)
        self.view.InsertActorWithFilms(row)

    def UpdateActorWithFilms(self, id, film_id, actor_id):
        self.model.UpdateActorWithFilms(id, film_id, actor_id)
        self.view.UpdateActorWithFilms(id)

    def DeleteActorWithFilms(self, id):
        self.model.DeleteActorWithFilms(id)
        self.view.DeleteActorWithFilms(id)

    def RandomActorWithFilms(self, amount):
        self.model.RandomActorWithFilms(amount)
        self.view.RandomActorWithFilms(amount)

    #######################################################################
    def AllFilmsWithGenres(self):
        rows = self.model.AllFilmsWithGenres()
        self.view.showAllFilmsWithGenres(rows)

    def FilmsWithGenresById(self, id):
        row = self.model.FilmsWithGenresById(id)
        self.view.FilmsWithGenresById(row)

    def InsertFilmsWithGenres(self, film_id, genres):
        id = self.model.InsertFilmsWithGenres(film_id, genres)
        row = self.model.FilmsWithGenresById(id)
        self.view.InsertFilmsWithGenres(row)

    def UpdateFilmsWithGenres(self, id, film_id, genres):
        self.model.UpdateFilmsWithGenres(id, film_id, genres)
        self.view.UpdateFilmsWithGenres(id)

    def DeleteFilmsWithGenres(self, id):
        self.model.DeleteFilmsWithGenres(id)
        self.view.DeleteFilmsWithGenres(id)

    def RandomFilmsWithGenres(self, amount):
        self.model.RandomFilmsWithGenres(amount)
        self.view.RandomFilmsWithGenres(amount)

    #############################################################
    def RateByUser(self, id):
        rows = self.model.SearchAllUsersRate(id)
        self.view.showAllRates(rows)

    def RateOfFilm(self, id):
        row = self.model.RateOfFilm(id)
        self.view.RateOfFilm(row)
