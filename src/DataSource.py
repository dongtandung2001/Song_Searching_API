import sqlite3
from datetime import datetime


class DataSource:
    def __init__(self):
        # create connection and cursor
        self._db = sqlite3.connect('src/Music.db')
        self._cursor = None

    def open(self):
        try:
            self._cursor = self._db.cursor()
            print('Successfully connect to the database')
        except sqlite3.Error as e:
            print('Cannot connect to the database' + e)

    def close(self):
        try:
            self._cursor.close()
        except sqlite3.Error as e:
            print('Cannot close the database ' + e)
        try:
            self._db.close()
        except sqlite3.Error as e1:
            print('Cannot clos the cursor ' + e1)

    def query_song_by_lyrics(self, lyrics, searching_type):
        results = set()  # info result
        result_dict = dict()  # result on each keyword
        json_result = []  # for api use
        # query all keywords
        for lyric in lyrics:
            # Keyword at the beginning of the paragraph or sentence
            # Keyword at the middle of the sentence
            a = "%" + lyric.lower().capitalize() + " %"
            b = "% " + lyric.lower() + " %"

            self._cursor.execute("PRAGMA CASE_SENSITIVE_LIKE = 1;")
            query_command = """
            SELECT 
                *
            FROM lyrics 
            WHERE Lyric LIKE ? OR Lyric LIKE ?"""

            par_ = (a, b)
            self._cursor.execute(query_command, par_)
            # handle duplicate in the database
            results = set(self._cursor.fetchall())
            # store result to dict { keyword : result_set() }
            result_dict[lyric] = results.copy()
            # reset temp storage
            results.clear()

        # result_dict = {'kw': (tuple of info from lyrics table) }
        # i = inclusive searching = all keywords should be in the result
        if searching_type.lower() == 'i':
            count = 0
            for x in result_dict.values():
                if count == 0:
                    results = x
                    count += 1
                else:
                    results = results.intersection(x)
        elif searching_type.lower() == 'e':  # e = exclusive searching, result can contain one of the keywords
            count = 0
            for x in result_dict.values():
                if count == 0:
                    results = x
                    count += 1
                else:
                    results = results ^ x  # values that are in either A or B, but not both
        else:
            print('Invalid choice')

        # numbers of result of searching
        print("Total:", len(results), "results")

        # query the Artists info of the result through link and make it become json type
        index = 1
        for x in results:
            # get the artist info of the song
            a = self.query_artist_by_link(x[0])
            if a != "No reference found":
                x = x + a  # concentrate 2 tuples
                # push to dict
                temp_result = {'id': index, 'Alink': x[0], 'SName': x[1],
                               'SLink': x[2], 'Lyric': x[3], 'Idiom': x[4],
                               'Artist': x[5], 'Songs': x[6], 'Popularity': x[7],
                               'Link': x[8], 'Genre': x[9], 'Genres': x[10]}
                json_result.append(temp_result)

                print(index, ": ", x[1], " By ", x[5])  # print results
                index += 1
            else:
                temp_result = {'id': index, 'Alink': x[0], 'SName': x[1],
                               'SLink': x[2], 'Lyric': x[3], 'Idiom': x[4],
                               'Artist': None, 'Songs': None, 'Popularity': None,
                               'Link': None, 'Genre': None, 'Genres': None}
                json_result.append(temp_result)
                pass
        return json_result

    def query_artist_by_link(self, link):
        query_command = """
        SELECT 
            *
        FROM 
            artists 
        WHERE artists.Link = (?)
        """
        par_ = (link,)
        self._cursor.execute(query_command, par_)
        results = tuple(self._cursor.fetchall())
        if len(results) != 0:
            return results[0]
        else:
            return "No reference found"

    def query_artist_by_name(self, names, searching_type):
        results = set()  # info result
        result_dict = dict()  # result on each keyword
        json_result = []
        for name in names:
            a = "%" + name.lower() + "%"
            query_command = """
                            SELECT 
                                *
                            FROM 
                                artists 
                            WHERE Artist LIKE (?)
                            """
            par_ = (a,)
            self._cursor.execute(query_command, par_)
            # handle duplicate in the database
            results = set(self._cursor.fetchall())
            # store result to dict { keyword : result_set() }
            result_dict[name] = results.copy()
            # reset temp storage
            results.clear()

        if searching_type.lower() == 'i':
            count = 0
            for x in result_dict.values():
                if count == 0:
                    results = x
                    count += 1
                else:
                    results = results.intersection(x)
        elif searching_type.lower() == 'e':
            count = 0
            for x in result_dict.values():
                if count == 0:
                    results = x
                    count += 1
                else:
                    results = results ^ x  # values that are in either A or B, but not both
        else:
            print('Invalid choice')

        index = 1
        print("Total:", len(results), "results")
        for x in results:
            # get the all songs of searching artist
            songs = self.query_song_by_link(x[3])
            if songs != "No reference found":
                # Make a json object of an artist
                temp_result = {'id': index, 'Artist': x[0], 'Songs': x[1], 'Popularity': x[2],
                               'Link': x[3], 'Genre': x[4], 'Genres': x[5]}
                json_result.append(temp_result)
                index += 1
            else:
                # Make json object
                temp_result = {'id': index, 'Artist': x[0], 'Songs': x[1], 'Popularity': x[2],
                               'Link': x[3], 'Genre': x[4], 'Genres': x[5]}
                json_result.append(temp_result)
                index += 1
                pass
        return json_result

    def query_song_by_link(self, link):
        query_command = """
                SELECT 
                    *
                FROM 
                    lyrics 
                WHERE ALink = (?)
                """
        par_ = (link,)
        self._cursor.execute(query_command, par_)
        results = tuple(self._cursor.fetchall())
        if len(results) != 0:
            return results
        else:
            return "No reference found"

    def query_song_by_title(self, title, searching_type):
        results = set()  # info result
        result_dict = dict()  # result on each keyword
        json_result = []  # for api use
        # query all keywords
        for title in title:
            # Keyword at the beginning of the paragraph or sentence
            # Keyword at the middle of the sentence
            a = "%" + title.lower().capitalize() + " %"
            b = "% " + title.lower().capitalize() + " %"

            self._cursor.execute("PRAGMA CASE_SENSITIVE_LIKE = 1;")
            query_command = """
                    SELECT 
                        *
                    FROM lyrics 
                    WHERE SName LIKE ? OR Sname LIKE ?"""

            par_ = (a, b)
            self._cursor.execute(query_command, par_)
            # handle duplicate in the database
            results = set(self._cursor.fetchall())
            # store result to dict { keyword : result_set() }
            result_dict[title] = results.copy()
            # reset temp storage
            results.clear()

        # result_dict = {'kw': (tuple of info from lyrics table) }
        # i = inclusive searching = all keywords should be in the result
        if searching_type.lower() == 'i':
            count = 0
            for x in result_dict.values():
                if count == 0:
                    results = x
                    count += 1
                else:
                    results = results.intersection(x)
        elif searching_type.lower() == 'e':  # e = exclusive searching, result can contain one of the keywords
            count = 0
            for x in result_dict.values():
                if count == 0:
                    results = x
                    count += 1
                else:
                    results = results ^ x  # values that are in either A or B, but not both
        else:
            print('Invalid choice')

        # numbers of result of searching
        print("Total:", len(results), "results")

        # query the Artists info of the result through link and make it become json type
        index = 1
        for x in results:
            # get the artist info of the song
            a = self.query_artist_by_link(x[0])
            if a != "No reference found":
                x = x + a  # concentrate 2 tuples
                # push to dict
                temp_result = {'id': index, 'Alink': x[0], 'SName': x[1],
                               'SLink': x[2], 'Lyric': x[3], 'Idiom': x[4],
                               'Artist': x[5], 'Songs': x[6], 'Popularity': x[7],
                               'Link': x[8], 'Genre': x[9], 'Genres': x[10]}
                json_result.append(temp_result)

                print(index, ": ", x[1], " By ", x[5])  # print results
                index += 1
            else:
                temp_result = {'id': index, 'Alink': x[0], 'SName': x[1],
                               'SLink': x[2], 'Lyric': x[3], 'Idiom': x[4],
                               'Artist': None, 'Songs': None, 'Popularity': None,
                               'Link': None, 'Genre': None, 'Genres': None}
                json_result.append(temp_result)
                pass
        return json_result


class User:
    def __init__(self):
        # create connection and cursor
        self._db = sqlite3.connect('src/user.db')
        self._cursor = None

    def open(self):
        try:
            self._cursor = self._db.cursor()
            print('Successfully connect to the database')
        except sqlite3.Error as e:
            print('Cannot connect to the database' + e)

    def close(self):
        try:
            self._cursor.close()
        except sqlite3.Error as e:
            print('Cannot close the database ' + e)
        try:
            self._db.close()
        except sqlite3.Error as e1:
            print('Cannot clos the cursor ' + e1)

    def query_email(self, email):
        query_command = "SELECT email FROM users WHERE email = (?)"
        par_ = (email,)
        self._cursor.execute(query_command, par_)
        result = self._cursor.fetchall()
        if len(result) != 0:
            return result
        else:
            return None

    def query_username(self, username):
        query_command = "SELECT username FROM users WHERE username = (?)"
        par_ = (username,)
        self._cursor.execute(query_command, par_)
        result = self._cursor.fetchall()
        if len(result) != 0:
            return result
        else:
            return None

    def query_password(self, email):
        query_command = "SELECT password FROM users WHERE email = (?)"
        par_ = (email,)
        self._cursor.execute(query_command, par_)
        result = self._cursor.fetchall()
        return result[0][0]

    def create_user(self, **kwargs):
        query_command = '''
        INSERT INTO users(username, email, password, create_at, updated_at)
        VALUES (?,?,?,?,?)
        '''
        par_ = (kwargs['username'], kwargs['email'],
                kwargs['password'], datetime.now().strftime("%d/%m/%Y %H:%M:%S"), datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        self._cursor.execute(query_command, par_)
        self._db.commit()
        return self._cursor.lastrowid

    def query_id(self, email):
        query_command = '''
            SELECT id
            FROM users
            WHERE email = (?)
        '''
        par_ = (email,)
        self._cursor.execute(query_command, par_)
        result = self._cursor.fetchall()
        return result[0][0]

    def query_username_by_id(self, id):
        query_command = '''
            SELECT username
            FROM users
            WHERE id = (?)
        '''
        par_ = (id,)
        self._cursor.execute(query_command, par_)
        result = self._cursor.fetchall()
        return result[0][0]

    def query_user_by_id(self, id):
        query_command = '''
            SELECT * 
            FROM users
            WHERE id = (?)
        '''
        par_ = (id,)
        self._cursor.execute(query_command, par_)
        result = self._cursor.fetchall()
        result_dict = dict()
        result_dict['id'] = result[0][0]
        result_dict['username'] = result[0][1]
        result_dict['email'] = result[0][2]
        result_dict['password'] = result[0][3]
        result_dict['created_at'] = result[0][4]
        result_dict['updated_at'] = result[0][5]
        return result_dict
