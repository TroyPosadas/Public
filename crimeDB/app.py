@app.route('/search', methods =["GET", "POST"])
def crimeSearch():
    mycursor = mydb.cursor()
    pageParam = request.args.get('page')
    print("Page number = ",pageParam)

    if pageParam == None:
        page = 1
    else:
        page = int(pageParam)
		
    offset = (page - 1) *25
	
    sd = request.form.getlist("startDate")
    if sd:
        startDate = sd[0]
    else:
        startDate = request.args.get('startDate')

    print(startDate)
    startDateL = startDate.split("-");
    startDateL = [int(i) for i in startDateL]
    epochStart = datetime(startDateL[0],startDateL[1],startDateL[2],0,0).timestamp()

    ed = request.form.getlist("endDate")
    if ed:
        endDate = ed[0]
    else:
        endDate = request.args.get('endDate')

    print(endDate)
    endDateL = endDate.split("-");
    endDateL = [int(i) for i in endDateL]
    epochEnd = datetime(endDateL[0],endDateL[1],endDateL[2],0,0).timestamp()

    ct = request.form.getlist("crimeType")
    if ct:
        crimeType = ct
    else:
        crimeType = ""
    print(crimeType)

    
    StartReadable = datetime.strptime(startDate, '%Y-%m-%d').strftime('%B %d, %Y')
    EndReadable = datetime.strptime(endDate, '%Y-%m-%d').strftime('%B %d, %Y')

    sqlstr = """SELECT `Date`,`Block`,`IUCR`,`PrimaryType`,`Description`,
    `LocationDescription`,`Arrest` FROM `crimedata` WHERE `Epoch` 
    BETWEEN """ + str(epochStart) + " and " + str(epochEnd)+" LIMIT 25 OFFSET "+ str(offset) + ";"
    mycursor.execute(sqlstr)
    CrimebetweenDates = mycursor.fetchall()


    return render_template("form.html", startDate=StartReadable, endDate=EndReadable, crimes=CrimebetweenDates, page=page, originalStartDate = startDate, originalEndDate = endDate)
