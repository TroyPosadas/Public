@app.route('/', methods =["GET", "POST"])
def genre():
    mycursor = mydb.cursor()
    genres = request.form.getlist("genre")
    genreStr= ".*"#regex to match all I think?
    actorStr= ".*"
    """if a && b:
    else if a:
    else if b:
    else return
    """      
    actors = request.form["actor"]  
    if genres and actors:
        genreStr = ""
        for genre in genres:
            genreStr = genreStr + genre + "|"
        genreStr = genreStr[:-1]
        genreStr = "\"" +genreStr+  "\""
        actorStr = actors.replace(", ","|")
        actorStr = "\"" +actorStr+  "\""				
        sqlstr = """SELECT T1.Title,T1.Genre,T2.Cast FROM (SELECT movietable.movieID, movietable.Title, genretable.Genre FROM `genretable` inner join movietable on genretable.MovieID = movietable.movieID where genretable.Genre REGEXP """+ genreStr + """) AS T1 Inner join (SELECT movietable.movieID, casttable.Cast from casttable join movietable on casttable.MovieID = movietable.movieID where casttable.Cast REGEXP """ + actorStr+ """) AS T2 on t1.movieID = T2.movieID;"""
    
    elif genres:
        genreStr = ""
        for genre in genres:
            genreStr = genreStr + genre + "|"
        genreStr = genreStr[:-1]
        genreStr = "\"" +genreStr+  "\""
        sqlstr = "select * from movietable where MovieID in (SELECT genretable.MovieID FROM `genretable` WHERE `Genre` REGEXP "+genreStr+");" 
    
    
    elif actors:
        actorStr = actors.replace(", ","|")
        actorStr = "\"" +actorStr+  "\""
        sqlstr = "SELECT movietable.Title, casttable.Cast from casttable join movietable on casttable.MovieID = movietable.movieID where casttable.Cast REGEXP "+actorStr+";" 
    
    else:
        return render_template("form.html")

 
    mycursor.execute(sqlstr)
    movies = mycursor.fetchall()
    
    return render_template("form.html", movies=movies, actor=actors, genres=genres)
