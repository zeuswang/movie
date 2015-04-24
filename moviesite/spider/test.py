def get_date_from_string(strdate):
    date = 0
    if '-' in strdate:
        try:
            numlist = strdate[0:10].split('-')
            date = int(numlist[0])*10000 +int(numlist[1])*100 +int(numlist[2])
        except:  
            date = 0
    elif len(strdate)>=4:
        try:
            date = int(strdate[0:4])*10000
        except:
            date =0
    return date


print get_date_from_string("2014-10-10")
