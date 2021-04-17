import psycopg2
from time import time
import texttable
import pandas as pd
import matplotlib
from matplotlib import font_manager as fm, rcParams
import matplotlib.pyplot as plt
import os
import csv
import json
import numpy as np
import matplotlib.dates as mdates
from scipy import interpolate


class Model:
    # connect to the db
    def OpenBD(self, port_):
        self.con = psycopg2.connect(
            host="127.0.0.1",
            database="kursova",
            user="postgres",
            password="password",
            port=port_,
        )
        self.port = port_
        self.cur = self.con.cursor()
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

    def Commit(self):
        self.con.commit()  # commit the transcation

    def RollBack(self):
        self.con.rollback()

    # close connection
    def CloseBD(self):
        self.Commit()  # commit the transcation
        self.cur.close()  # close the self.cursor
        self.con.close()  # close the connection

    def GetPort(self):
        return self.port

    def GetName_of_backup(self):
        f = open("./index/back_up.txt", "r")
        next_id = f.read()
        f.close()
        next_id = int(next_id)
        return next_id

    def UpdateName_of_backup(self):
        next_id = self.GetName_of_backup()
        next_id_str = str(next_id + 1)
        f = open("./index/back_up.txt", "w")
        f.write(next_id_str)
        f.close()

    def backup(self):
        tic = time()
        name_of_backup = self.GetName_of_backup()
        backup_str = (
            'PGPASSWORD="password" /usr/bin/pg_dump --file "./backups/'
            + str(name_of_backup)
            + '.sql" --host "localhost" --port "5432" --username "postgres" --verbose --format=c --blobs "kursova" > /dev/null 2>&1'
        )
        self.UpdateName_of_backup()
        os.system(backup_str)
        toc = time()
        return ["./backups/" + str(name_of_backup) + ".sql", (toc - tic) * 1000]

    def restore(self, backup_id):
        tic = time()
        os.system(
            'PGPASSWORD="password" psql -U postgres -d postgres -h localhost -w -c"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = \'kursova\';" > /dev/null 2>&1'
        )
        os.system(
            'PGPASSWORD="password" psql -U postgres -d postgres -h localhost -w -c"REVOKE CONNECT ON DATABASE kursova FROM PUBLIC, postgres;"> /dev/null 2>&1'
        )
        os.system(
            'PGPASSWORD="password" pg_restore --clean --dbname=kursova --username=postgres "./backups/'
            + str(backup_id)
            + '.sql" '
        )
        self.reconnect(5432)
        toc = time()
        self.Commit()
        return (toc - tic) * 1000

    def reconnect(self, port):
        self.con = psycopg2.connect(
            dbname="kursova",
            user="postgres",
            host="localhost",
            port=port,
            password="password",
        )
        self.cur = self.con.cursor()
        self.port = port

    ####################################
    def AllFilms(self):
        self.cur.execute("SELECT * FROM films order by id")
        rows = self.cur.fetchall()
        return rows

    def FilmById(self, id):
        id = int(id)
        query = f"SELECT * FROM films WHERE id = {id}"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def InsertFilm(self, name, language, overwiev, homepage, adult, budget):
        query = f"INSERT INTO films (name, language, overwiev, homepage, adult, budget) VALUES ('{name}', '{language}', '{overwiev}', '{homepage}', '{adult}', {budget}) RETURNING id"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def UpdateFilm(self, id, name, language, overwiev, homepage, adult, budget):
        id = int(id)
        query = f"UPDATE films SET name = '{name}',language= '{language}', overwiev='{overwiev}', homepage='{homepage}', adult='{adult}',budget={budget} WHERE id = {id}"
        self.cur.execute(query)

    def DeleteFilm(self, id):
        id = int(id)
        query = f"DELETE FROM actors_with_films WHERE film_id = {id}"
        self.cur.execute(query)
        query = f"DELETE FROM films_with_genres WHERE film_id = {id}"
        self.cur.execute(query)
        query = f"DELETE FROM rating WHERE film_id = {id}"
        self.cur.execute(query)
        query = f"DELETE FROM films WHERE id = {id}"
        self.cur.execute(query)

    def InsertFilmsFromData(self, name):
        try:
            movies = pd.read_json(f"{name}.json")
            items = movies
            i = 0
            while i < len(items):
                query = f"INSERT INTO films (name,language,overwiev,homepage,adult,budget) values ('{items.name[i] }', ' {items.language[i]}','{items.overwiev[i]}', '{items.homepage[i]}','{items.adult[i]}',{items.budget[i]})"
                i = i + 1
                self.cur.execute(query)
            return f"{name}.json"
        except Exception as e:
            raise Exception(e)

    #################################################################

    def AllActors(self):
        self.cur.execute("SELECT * FROM actors order by id")
        rows = self.cur.fetchall()
        return rows

    def ActorById(self, id):
        id = int(id)
        query = f"SELECT * FROM actors WHERE id = {id}"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def InsertActor(self, name, image, bio):
        query = f"INSERT INTO actors (name, image,bio) VALUES ('{name}', '{image}', '{bio}') RETURNING id"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def UpdateActor(self, id, name, image, bio):
        id = int(id)
        query = f"UPDATE actors SET name = '{name}',image= '{image}', bio='{bio}' WHERE id = {id}"
        self.cur.execute(query)

    def DeleteActor(self, id):
        id = int(id)
        query = f"DELETE FROM actors_with_films WHERE actor_id = {id}"
        self.cur.execute(query)
        query = f"DELETE FROM actors WHERE id = {id}"
        self.cur.execute(query)

    def InsertActorsFromData(self, name):
        try:
            actors = pd.read_csv(f"{name}.csv", sep=",")
            i = 0
            while i < len(actors.name):
                query = f"INSERT INTO actors (name, image, bio) values ('{actors.name[i]}','{actors.image[i]}','{actors.bio[i]}')"
                i = i + 1
                self.cur.execute(query)
            return f"{name}.csv"
        except Exception as e:
            raise Exception(e)

    ##########################################################################

    def AllUsers(self):
        self.cur.execute("SELECT * FROM users order by id")
        rows = self.cur.fetchall()
        return rows

    def UserById(self, id):
        id = int(id)
        query = f"SELECT * FROM users WHERE id = {id}"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def InsertUser(self, name, surname, login, age, city):
        query = f"INSERT INTO users (name, surname,login,age,city) VALUES ('{name}', '{surname}', '{login}', {age},'{city}') RETURNING id"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def UpdateUser(self, id, name, surname, login, age, city):
        id = int(id)
        query = f"UPDATE users SET name = '{name}',surname= '{surname}', login='{login}',age={age},city='{city}'  WHERE id = {id}"
        self.cur.execute(query)

    def DeleteUser(self, id):
        id = int(id)
        query = f"DELETE FROM rating WHERE user_id = {id}"
        self.cur.execute(query)
        query = f"DELETE FROM users WHERE id = {id}"
        self.cur.execute(query)

    def InsertUsersFromData(self, name):
        try:
            users = pd.read_csv(f"{name}.csv", sep=",")
            i = 0
            while i < len(users.name):
                query = f"INSERT INTO users(name,surname,login,age,city) VALUES ( '{users.name[i]}', '{users.surname[i]}', '{users.name[i]+'_'+users.surname[i]+'###'}'||chr(trunc(65+random()*25)::int)||chr(trunc(65+random()*25)::int)||chr(trunc(65+random()*25)::int),{int(float(users.age[i]))},'{users.city[i]}')"
                self.cur.execute(query)
                i = i + 1
            return f"{name}.csv"
        except Exception as e:
            raise Exception(e)

    ##########################################################################

    def AllRates(self):
        self.cur.execute("SELECT * FROM rating order by id limit 10")
        rows = self.cur.fetchall()
        return rows

    def RateById(self, id):
        id = int(id)
        query = f"SELECT * FROM rating WHERE id = {id}"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def InsertRate(self, user_id, film_id, rate, time):
        query = f"INSERT INTO rating (user_id, film_id, rate, time) VALUES ({user_id}, {film_id}, {rate}, '{time}') RETURNING id"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def UpdateRate(self, id, user_id, film_id, rate, time):
        id = int(id)
        query = f"UPDATE rating SET user_id = {user_id},film_id= {film_id}, rate={rate},time='{time}'  WHERE id = {id}"
        self.cur.execute(query)

    def DeleteRate(self, id):
        id = int(id)
        query = f"DELETE FROM rating WHERE id = {id}"
        self.cur.execute(query)

    def RandomRate(self, amount):
        amount = int(amount)
        query = f"Select * From insert_rating({amount})"
        self.cur.execute(query)

    ##########################################################################

    def AllActorWithFilms(self):
        self.cur.execute("SELECT * FROM actors_with_films order by id limit 10")
        rows = self.cur.fetchall()
        return rows

    def ActorWithFilmsById(self, id):
        id = int(id)
        query = f"SELECT * FROM actors_with_films WHERE id = {id}"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def InsertActorWithFilms(self, film_id, actor_id):
        query = f"INSERT INTO actors_with_films ( film_id, actor_id) VALUES ( {film_id},{actor_id} ) RETURNING id"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def UpdateActorWithFilms(self, id, film_id, actor_id):
        id = int(id)
        query = f"UPDATE actors_with_films SET film_id= {film_id},actor_id={actor_id}  WHERE id = {id}"
        self.cur.execute(query)

    def DeleteActorWithFilms(self, id):
        id = int(id)
        query = f"DELETE FROM actors_with_films WHERE id = {id}"
        self.cur.execute(query)

    def RandomActorWithFilms(self, amount):
        amount = int(amount)
        query = f"Select * From insert_actors_with_films({amount})"
        self.cur.execute(query)

    ##########################################################################

    def AllFilmsWithGenres(self):
        self.cur.execute("SELECT * FROM films_with_genres order by id limit 10")
        rows = self.cur.fetchall()
        return rows

    def FilmsWithGenresById(self, id):
        id = int(id)
        query = f"SELECT * FROM films_with_genres WHERE id = {id}"
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    def InsertFilmsWithGenres(self, film_id, genres):
        query = "INSERT INTO films_with_genres ( film_id,"
        for genre in genres:
            query += genre + ","
        query = query[:-1]
        query += ") Values (" + str(film_id) + ","
        for genre in genres:
            query += "1,"
        query = query[:-1]
        query += ") RETURNING id"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def UpdateFilmsWithGenres(self, id, film_id, genres):
        id = int(id)
        query = "UPDATE films_with_genres SET film_id=" + str(film_id) + ","
        for genre in self.all_genres:
            query += genre + "=0,"

        query = query[:-1]
        query += "WHERE id =" + str(id)
        self.cur.execute(query)
        query = ""
        query = "UPDATE films_with_genres SET film_id=" + str(film_id) + ","
        for genre in genres:
            query += genre + "=1,"

        query = query[:-1]
        query += "WHERE id =" + str(id)
        self.cur.execute(query)

    def DeleteFilmsWithGenres(self, id):
        id = int(id)
        query = f"DELETE FROM films_with_genres WHERE id = {id}"
        self.cur.execute(query)

    ################   Filtr    ###############################################################################################

    def SearchFilmByName(self, name):
        query = f"SELECT * FROM films WHERE name LIKE '%{name}%'"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def SearchFilmByGenres(self, genres):
        query = f"SELECT id, name, language, overwiev, homepage, adult, budget FROM (SELECT film_id FROM films_with_genres WHERE "
        for genre in genres:
            query += genre + "=1 AND "
        query = query[:-4]
        query += ") as b1 INNER JOIN (SELECT * FROM films) as b2 on b1.film_id=b2.id"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def SearchFilmByActor(self, name):
        query = f"""SELECT id, name, language, overwiev, homepage, adult, budget FROM (SELECT film_id FROM (SELECT actor_id, film_id FROM actors_with_films) as b1
        INNER JOIN
        (SELECT * FROM actors WHERE name LIKE '%{name}%') as b2 on b1.actor_id=b2.id) as a1 INNER JOIN 
        (SELECT * FROM films) as a2 on a1.film_id=a2.id"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def SearchAllUsersRate(self, id):
        query = f"Select * from rating WHERE user_id={id}"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def RateOfFilm(self, id):
        query = (
            f"SELECT avg(rate),film_id FROM rating where film_id={id} group by film_id"
        )
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

    #######################   Analiz    #########################################################################################################
    def FilmsName(self, id):
        query = f"select round(CAST(avg as numeric),2),time,name,rate from (Select rate,avg(rate) over (partition by film_id order by time rows between unbounded preceding and current row), film_id, time From rating where film_id={id}) as t1 inner join (select name, id from films) as t2 on t1.film_id=t2.id  order by time"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def FilmsWithAvgRate(self, date_low, date_high):
        query = f"Select name,round(CAST(avg as numeric),2),film_id from (Select avg(rate),film_id From rating where time between '{date_low}' AND '{date_high}' group by film_id order by film_id) as t1 inner join (select id,name from films) as t2 on t1.film_id=t2.id order by round limit 10"
        self.cur.execute(query)
        rows1 = self.cur.fetchall()
        query = f"Select name,round(CAST(avg as numeric),2),film_id from (Select avg(rate),film_id From rating where time between '{date_low}' AND '{date_high}' group by film_id order by film_id) as t1 inner join (select id,name from films) as t2 on t1.film_id=t2.id order by round desc limit 10"
        self.cur.execute(query)
        rows2 = self.cur.fetchall()
        return [rows1, rows2]

    def RatingTime(self, date_low, date_high):
        query = f"Select time,round(CAST(avg as numeric),2) from (Select avg(rate),time From rating where time between '{date_low}' AND '{date_high}' group by time ) as k order by time"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def FilmsWithGenresRate(self, date_low, date_high):
        date_low = str(date_low)
        date_high = str(date_high)
        query = f"Select sum(documentary) as documentary,sum(romance) as romance,sum(fantasy) as fantasy,sum(drama) as drama,sum(vision_view_entertainment) as vision_view_entertainment,sum(telescene_film_group_productions) as telescene_film_group_productions,sum(action) as action,sum(music) as music,sum(science_fiction) as science_fiction,sum(carousel_productions) as carousel_productions,sum(thriller) as thriller,sum(the_cartel) as the_cartel,sum(adventure) as adventure,sum(family) as family,sum(rogue_state) as rogue_state,sum(pulser_productions) as pulser_productions,sum(odyssey_media) as odyssey_media,sum(war) as war,sum(horror) as horror,sum(history) as history,sum(animation) as animation,sum(western) as western,sum(foreign_) as foreign_,sum(comedy) as comedy,sum(crime) as crime,sum(tv_movie) as tv_movie,sum(mystery) as mystery from (Select film_id From rating where time between '{date_low}' AND '{date_high}' group by film_id order by film_id) as t1 inner join (select documentary,romance,fantasy,drama,vision_view_entertainment,telescene_film_group_productions,action,music,science_fiction,carousel_productions,thriller,the_cartel,adventure,family,rogue_state,pulser_productions,odyssey_media,war,horror,history,animation,western,foreign_,comedy,crime,tv_movie,mystery,film_id from films_with_genres ) as t2 on t1.film_id=t2.film_id"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def GetName_of_graph(self):
        f = open("./index/graph.txt", "r")
        next_id = f.read()
        f.close()
        next_id = int(next_id)
        return next_id

    def UpdateName_of_file(self):
        next_id = self.GetName_of_graph()
        next_id_str = str(next_id + 1)
        f = open("./index/graph.txt", "w")
        f.write(next_id_str)
        f.close()

    def RatingTimeDiagram(self, date_low, date_high):
        rows = self.RatingTime(date_low, date_high)
        rate_avg_rows = []
        date_avg_rows = []
        i = 0
        aver = rows
        while i < len(aver):
            rate_avg_rows.append(float(aver[i][1]))
            date_avg_rows.append(aver[i][0])
            i = i + 1
        x = mdates.date2num(date_avg_rows)
        z4 = np.polyfit(x, rate_avg_rows, 3)
        p4 = np.poly1d(z4)
        fig, cx = plt.subplots()
        xx = np.linspace(x.min(), x.max(), 100)
        dd = mdates.num2date(xx)
        plt.title(f"Average rating films from {date_low} to {date_high}")
        plt.ylabel("Average rate")
        plt.xticks(rotation="vertical")
        plt.plot(date_avg_rows, rate_avg_rows, c="black")
        plt.plot(dd, p4(xx), "-r")
        plt.legend(["average rate line", "trend line"])
        name_of_graph = self.GetName_of_graph()
        name = f"./Analiz/film{name_of_graph}.pdf"
        figure = plt.gcf()
        figure.set_size_inches(20, 10)
        plt.savefig(name, dpi=100)
        plt.show()
        self.UpdateName_of_file()
        return name

    def RateGenresDiagram(self, date_low, date_high):
        rows = self.FilmsWithGenresRate(date_low, date_high)
        rows = list(rows[0])
        rate_rows = []
        max_rate = []
        max_index = []
        min_rate = []
        min_index = []
        genres = []
        if rows[0] is not None:
            i = 0
            without_zero = []
            while i < len(rows):
                if not rows[i] == 0:
                    without_zero.append(rows[i])
                i = i + 1
            i = 0
            while i < len(rows):
                if not rows[i] == 0:
                    rate_rows.append(rows[i])
                    genres.append(self.all_genres[i])
                    if rows[i] == max(rows, key=lambda x: x):
                        max_rate.append(rows[i])
                        max_index.append(i)

                    if rows[i] == min(without_zero, key=lambda x: x):
                        min_rate.append(rows[i])
                        min_index.append(i)
                i = i + 1
            plt.bar(genres, rate_rows)

            i = 0
            genres_with_max = "The most popular genre "
            genres_with_min = "The most unpopular genre "
            min_genres = []
            while i < len(min_rate):
                min_genres.append(self.all_genres[min_index[i]])
                genres_with_min += (
                    ' "' + str(self.all_genres[min_index[i]]) + '" ' + "AND"
                )
                i = i + 1

            plt.bar(min_genres, min_rate, color="g")
            genres_with_min = genres_with_min[:-3]
            genres_with_min += " with rate " + str(min_rate[0])

            i = 0
            max_genres = []
            while i < len(max_rate):
                max_genres.append(self.all_genres[max_index[i]])
                genres_with_max += (
                    ' "' + str(self.all_genres[max_index[i]]) + '" ' + "AND"
                )
                i = i + 1

            plt.bar(max_genres, max_rate, color="r")
            genres_with_max = genres_with_max[:-3]
            genres_with_max += " with rate " + str(max_rate[0])
            plt.title(f"Rating genres from {date_low} to {date_high}")
            plt.ylabel("Quantity of rating genre")
            csfont = {"fontsize": "6"}
            plt.xticks(rotation="vertical", **csfont)
            csfont = {"fontsize": "8"}
            plt.legend(["rate bar", genres_with_min, genres_with_max], **csfont)
            name_of_graph = self.GetName_of_graph()
            name = f"./Analiz/filmsGenres{name_of_graph}.pdf"
            figure = plt.gcf()
            figure.set_size_inches(20, 10)
            plt.savefig(name, dpi=100)
            plt.show()
            self.UpdateName_of_file()
            return name
        else:
            raise Exception("No rating for this period genres")

    def RateFilmsDiagram(self, date_low, date_high):
        rows = self.FilmsWithAvgRate(date_low, date_high)
        rate_max_rows = []
        films_max_rows = []
        rate_min_rows = []
        films_min_rows = []
        i = 0
        if not len(rows[0]) == 0:
            while i < len(rows[0]):
                rate_max_rows.append(rows[0][i][1])
                films_max_rows.append(rows[0][i][0])
                i = i + 1

            i = 0
            while i < len(rows[1]):
                rate_min_rows.append(rows[1][i][1])
                films_min_rows.append(rows[1][i][0])
                i = i + 1

            csfont = {"fontsize": "6"}

            f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

            ax1.set_title(f"The most unpopular 10 films from {date_low} to {date_high}")
            ax2.set_title(f"The most popular 10 films from {date_low} to {date_high}")
            plt.sca(ax2)
            plt.xticks(rotation="vertical", **csfont)
            plt.ylabel("Rate")

            ax2.bar(films_min_rows, rate_min_rows, color="red")
            y0, y1 = ax2.get_ybound()  # размер графика по оси Y
            y_shift = 0.1 * (y1 - y0)  # дополнительное место под надписи

            for i, rect in enumerate(
                ax2.patches
            ):  # по всем нарисованным прямоугольникам
                height = rect.get_height()
                label = str(rate_min_rows[i])
                x = rect.get_x() + rect.get_width() / 2  # посередине прямоугольника
                y = (
                    y0 + height + y_shift / 4
                )  # над прямоугольником в середине доп. места
                ax2.text(x, y, label, ha="center", va="center")  # выводим текст
            plt.sca(ax1)
            plt.xticks(rotation="vertical", **csfont)
            plt.ylabel("Rate")
            ax1.bar(films_max_rows, rate_max_rows, color="green")

            y0, y1 = ax1.get_ybound()  # размер графика по оси Y
            y_shift = 0.1 * (y1 - y0)  # дополнительное место под надписи

            for i, rect in enumerate(
                ax1.patches
            ):  # по всем нарисованным прямоугольникам
                height = rect.get_height()
                label = str(rate_max_rows[i])
                x = rect.get_x() + rect.get_width() / 2  # посередине прямоугольника
                y = (
                    y0 + height + y_shift / 4
                )  # над прямоугольником в середине доп. места
                ax1.text(x, y, label, ha="center", va="center")  # выводим текст

            name_of_graph = self.GetName_of_graph()
            name = f"./Analiz/films{name_of_graph}.pdf"
            figure = plt.gcf()
            figure.set_size_inches(20, 10)
            plt.savefig(name, dpi=100)
            plt.show()
            self.UpdateName_of_file()
            return name
        else:
            raise Exception("No rating for this period films")

    def RateFilmDiagram(self, id):
        rows = self.FilmsName(id)
        rate_rows = []
        date_rows = []
        max_rate = []
        min_rate = []
        rate_avg_rows = []
        max_avg_rate = []
        min_avg_rate = []
        i = 0
        if not len(rows) == 0:
            while i < len(rows):
                rate_avg_rows.append(float(rows[i][0]))
                rate_rows.append(float(rows[i][3]))
                date_rows.append(pd.to_datetime(rows[i][1]))
                if rows[i][0] == max(rows, key=lambda x: x[0])[0]:
                    max_avg_rate.append(rows[i])
                if rows[i][0] == min(rows, key=lambda x: x[0])[0]:
                    min_avg_rate.append(rows[i])
                if rows[i][3] == max(rows, key=lambda x: x[3])[3]:
                    max_rate.append(rows[i])
                if rows[i][3] == min(rows, key=lambda x: x[3])[3]:
                    min_rate.append(rows[i])
                i = i + 1
            i = 0
            min_avg_date = []
            min_avg_rates = []
            while i < len(min_avg_rate):
                min_avg_date.append(pd.to_datetime(min_avg_rate[i][1]))
                min_avg_rates.append(min_avg_rate[i][0])
                i = i + 1
            i = 0
            max_avg_date = []
            max_avg_rates = []
            while i < len(max_avg_rate):
                max_avg_date.append(pd.to_datetime(max_avg_rate[i][1]))
                max_avg_rates.append(max_avg_rate[i][0])
                i = i + 1
            i = 0
            min_date = []
            min_rates = []
            while i < len(min_rate):
                min_date.append(pd.to_datetime(min_rate[i][1]))
                min_rates.append(min_rate[i][3])
                i = i + 1
            i = 0
            max_date = []
            max_rates = []
            while i < len(max_rate):
                max_date.append(pd.to_datetime(max_rate[i][1]))
                max_rates.append(max_rate[i][3])
                i = i + 1

            x = mdates.date2num(date_rows)
            z4 = np.polyfit(x, rate_avg_rows, 3)
            p4 = np.poly1d(z4)
            xx = np.linspace(x.min(), x.max(), 100)
            dd = mdates.num2date(xx)

            plt.plot(date_rows, rate_avg_rows, c="g")
            plt.plot(dd, p4(xx), "-r")
            plt.scatter(date_rows, rate_rows, c="black")
            plt.scatter(min_avg_date, min_avg_rates, c="violet")
            plt.scatter(max_avg_date, max_avg_rates, color="orange")
            plt.scatter(min_date, min_rates, c="b")
            plt.scatter(max_date, max_rates, c="r")
            plt.title(f"Rating film with name {rows[0][2]}")
            plt.ylabel("Rate")
            plt.xticks(rotation="vertical")
            plt.legend(
                [
                    "rate line of average rate",
                    "trend line",
                    "all rates",
                    "min average rate " + str(min_avg_rate[0][0]),
                    "max average rate " + str(max_avg_rate[0][0]),
                    "min rate " + str(min_rate[0][3]),
                    "max rate " + str(max_rate[0][3]),
                ]
            )

            name_of_graph = self.GetName_of_graph()
            name = f"./Analiz/film{name_of_graph}.pdf"
            figure = plt.gcf()
            figure.set_size_inches(20, 10)
            plt.savefig(name, dpi=100)
            plt.show()
            self.UpdateName_of_file()
            return name
        else:
            raise Exception("No rating for this period film")

    #####################################################################

    def UsersToCsv(self, name):
        with open(f"./export_files_csv/{name}.csv", mode="w") as users_file:
            users_writer = csv.writer(
                users_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            users_writer.writerow(["id", "name", "surname", "login", "age", "city"])
            users = self.AllUsers()
            i = 0
            while i < len(users):
                users_writer.writerow(list(users[i]))
                i = i + 1
        return f"./export_files_csv/{name}.csv"

    def UsersToJson(self, name):
        with open(f"./export_files_json/{name}.json", mode="w") as users_file:
            i = 0
            users = self.AllUsers()
            users_list = []
            while i < len(users):
                user_dict = {
                    "id": users[i][0],
                    "name": users[i][1],
                    "surname": users[i][2],
                    "login": users[i][3],
                    "age": users[i][4],
                    "city": users[i][5],
                }
                users_list.append(user_dict)
                i = i + 1
            json.dump(users_list, users_file, indent=4, sort_keys=True)
        return f"./export_files_json/{name}.json"

    def FilmsToCsv(self, name):
        with open(f"./export_files_csv/{name}.csv", mode="w") as films_file:
            films_writer = csv.writer(
                films_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            films_writer.writerow(
                ["id", "name", "language", "overwiev", "homepage", "adult", "budget"]
            )
            films = self.AllFilms()
            i = 0
            while i < len(films):
                films_writer.writerow(list(films[i]))
                i = i + 1
        return f"./export_files_csv/{name}.csv"

    def FilmsToJson(self, name):
        with open(f"./export_files_json/{name}.json", mode="w") as films_file:
            i = 0
            films = self.AllFilms()
            films_list = []
            while i < len(films):
                film_dict = {
                    "id": films[i][0],
                    "name": films[i][1],
                    "language": films[i][2],
                    "overwiev": films[i][3],
                    "homepage": films[i][4],
                    "adult": films[i][5],
                    "budget": films[i][6],
                }
                films_list.append(film_dict)
                i = i + 1
            json.dump(films_list, films_file, indent=4, sort_keys=True)
        return f"./export_files_json/{name}.json"

    def ActorsToCsv(self, name):
        with open(f"./export_files_csv/{name}.csv", mode="w") as actors_file:
            actors_writer = csv.writer(
                actors_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            actors_writer.writerow(["id", "name", "image", "bio"])
            actors = self.AllActors()
            i = 0
            while i < len(actors):
                actors_writer.writerow(list(actors[i]))
                i = i + 1
        return f"./export_files_csv/{name}.csv"

    def ActorsToJson(self, name):
        with open(f"./export_files_json/{name}.json", mode="w") as actors_file:
            i = 0
            actors = self.AllActors()
            actors_list = []
            while i < len(actors):
                actor_dict = {
                    "id": actors[i][0],
                    "name": actors[i][1],
                    "image": actors[i][2],
                    "bio": actors[i][3],
                }
                actors_list.append(actor_dict)
                i = i + 1
            json.dump(actors_list, actors_file, indent=4, sort_keys=True)
        return f"./export_files_json/{name}.json"

    def RatesToCsv(self, name):
        with open(f"./export_files_csv/{name}.csv", mode="w") as rates_file:
            rates_writer = csv.writer(
                rates_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            rates_writer.writerow(["id", "name", "image", "bio"])
            rates = self.AllRates()
            i = 0
            while i < len(rates):
                rates_writer.writerow(list(rates[i]))
                i = i + 1
        return f"./export_files_csv/{name}.csv"

    def RatesToJson(self, name):
        with open(f"./export_files_json/{name}.json", mode="w") as rates_file:
            i = 0
            rates = self.AllRates()
            rates_list = []
            while i < len(rates):
                rate_dict = {
                    "id": rates[i][0],
                    "user_id": rates[i][1],
                    "film_id": rates[i][2],
                    "rate": rates[i][3],
                    "time": str(rates[i][4]),
                }
                rates_list.append(rate_dict)
                i = i + 1
            json.dump(rates_list, rates_file, indent=4, sort_keys=True)
        return f"./export_files_json/{name}.json"


# x1 = [1, 2, 3, 4]
# x2 = [1, 2, 3, 4]
# y1 = [53.30, 143.59, 63.38, 71.34]
# y2 = [64.07, 97.32, 63.2, 66.8]
# x1 = np.arange(1, 5) - 0.2
# x2 = np.arange(1, 5) + 0.2
## y1 = np.random.randint(1, 10, size=7)
## y2 = np.random.randint(1, 10, size=7)
#
# fig, ax = plt.subplots()
#
# ax.bar(x1, y1, width=0.4, color="violet")
# ax.bar(x2, y2, width=0.4, color="red")
#
# plt.sca(ax)
# plt.title("Brin indexing")
# plt.ylabel("Time of query execution (ms)")
# plt.xlabel("Number of test")
# plt.legend(["without indexing", "with indexing"])
