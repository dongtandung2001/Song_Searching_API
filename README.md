# SongSearchingEngine

Project

Song Searching API
Oct 2021 – Nov 2021

Project descriptionIt was inspired by my final project of Data Structure class at De Anza College about finding songs that contain a keyword that we desire. However, the database is kinda small ( < 50 songs).

Thus, I enhanced it to an API to query songs, artists that contain multiple keywords that we desire with a much larger database (~200k songs, and 3000 artists). It was successfully deployed on Heroku, however, due to the limit of PostgreSQL add-on, I was only given 10,000 rows for free, and my database is more than 200k rows, so I shut down the server.


Search songs contains desired keywords from users using

It could be multiple keywords in lyrics or artist names.

For example, if you want to find songs whose lyric has keywords: evil, devil,

The API will return result of type JSON that contains all songs that are qualified.


There are 2 modes of searching: Inclusive, Exclusive

Inclusive means all keywords must exist in the lyric of a song in order to be in the result set

While Exclusive only need one of the keywords to exist


Since this github is used to deploy the API on Heroku so I used the Heroku PostgreSQL databse. You can change the database url to work with local postgresql database.

I manually coded SQL command for query from DataBase instead of using SQLAlchemy so that I could learn SQL.

