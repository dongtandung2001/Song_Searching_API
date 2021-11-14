import psycopg2
import os
DATABASE_URL = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, database='d6al40t7nhrpei', user='dpczvuzpznqxln', password='fd34aced965ce0525f4072a8589e1607f53358f066b772ed8facbcaa66095565',
                        host='ec2-18-211-41-246.compute-1.amazonaws.com', port='5432')

cursor = conn.cursor()


def query_song_by_lyrics(lyrics, searching_type):
    results = set()  # info result
    result_dict = dict()  # result on each keyword
    json_result = []  # for api use
    # query all keywords
    for lyric in lyrics:
        # Keyword at the beginning of the paragraph or sentence
        # Keyword at the middle of the sentence
        a = "%" + lyric.lower().capitalize() + " %"
        b = "% " + lyric.lower() + " %"

        #cursor.execute("PRAGMA CASE_SENSITIVE_LIKE = 1;")
        query_command = """
        SELECT
            *
        FROM lyrics
        WHERE "Lyric" LIKE %s OR "Lyric" LIKE %s"""

        par_ = (a, b)
        cursor.execute(query_command, par_)
        # handle duplicate in the database
        results = set(cursor.fetchall())
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
        a = query_artist_by_link(x[0])
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


def query_artist_by_link(link):
    query_command = """
    SELECT 
        *
    FROM 
        artists 
    WHERE "Link" = %s
    """
    par_ = (link,)
    cursor.execute(query_command, par_)
    results = tuple(cursor.fetchall())
    if len(results) != 0:
        return results[0]
    else:
        return "No reference found"


result = query_song_by_lyrics(['evil', 'devil'], 'i')
for x in result:
    print(x['id'], x['SName'])
