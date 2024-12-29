def itembefore (iterable: list | str | tuple | dict | range | set | frozenset | bytearray, index: int):

    if index > 0 and index <= len(iterable):

        return iterable[index-1]
    
    if index <= 0:

        return iterable[0]
    
    if index > len(iterable):

        return iterable[-1]

def itemafter (iterable: list | str | tuple | dict | range | set | frozenset | bytearray, index: int):

    if index >= 0 and index < len(iterable):

        return iterable[index+1]
    
    if index < 0:

        return iterable[0]
    
    if index >= len(iterable):

        return iterable[-1]

def datetimeparse(strarg, monthfirst: bool = True):

    monthindex, dateindex = 0 if monthfirst else 1, 1 if monthfirst else 0
    
    from re import finditer as re_finditer, sub as re_sub
    from datetime import datetime as dt

    long_months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    short_months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    dateexp, timeexp = r"\b(?:(?:(?:(?:(?:[1-2][0-9])|(?:3(?:0|1))|(?:0?[1-9]))(?:(?:(?<=4|5|6|7|8|9|0)|(?<=11|12|13))\s?th|(?<!1)3\s?rd|(?<!1)2\s?nd|(?<!1)1\s?st)?)|(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty(?:-|\s)first|twenty(?:-|\s)second|twenty(?:-|s)third|twenty(?:-|\s)fourth|twenty(?:-|\s)fifth|twenty(?:-|\s)sixth|twenty(?:-|\s)seventh|twenty(?:-|\s)eighth|twenty(?:-|\s)ninth|thirtieth|thirty(?:-|\s)first))(?:\sof)?|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:\/|\s|-)(?:(?:(?:(?:[1-2][0-9])|(?:3(?:0|1))|(?:0?[1-9]))(?:(?:(?<=4|5|6|7|8|9|0)|(?<=11|12|13))\s?th|(?<!1)3\s?rd|(?<!1)2\s?nd|(?<!1)1\s?st)?)|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:(?:\/|\s|-)(?:[0-9]{2}|[0-9]{4}))?\b", r"(?:(?:(?:0|1)?[1-9])|(?:2[0-3])|(?:00))(?::[0-5][0-9])?(?: ?(?:am|pm))?"
    raw_date, raw_time = re_finditer(pattern=dateexp, string=strarg.lower()), re_finditer(pattern=timeexp, string=strarg.lower())
    raw_date_tuple, raw_time_tuple = tuple(raw_date), tuple(raw_time)

    # 12-29-2024 12:12PM apparently one can only open the raw_date and raw_time iterators ONCE, so we need to store them as variables somewhere like up here and replace all references to tuple(raw_date) and such with the corresponding variables

    print(list(True if (len(anyitem[0]) >= 3) else False for anyitem in raw_time_tuple))

    raw_time_len_checker = False if True not in tuple(True if (len(anyitem[0]) >= 3) else False for anyitem in raw_time_tuple) else True
    if len(raw_time_tuple) > 0 and raw_time_len_checker:
        mid_time = tuple(anyitem for anyitem in raw_time_tuple if len(anyitem[0]) >= 3)[-1][0]

        hourmindict = {"hour": int(mid_time[0:2] if mid_time[1].isnumeric() else mid_time[0])}
        if ":" in mid_time:
            hourmindict["minute"] = int(mid_time[mid_time.index(":")+1:mid_time.index(":")+3])
        if mid_time[-2:] == "pm" and hourmindict["hour"] < 12:
            hourmindict["hour"] += 12
        if mid_time[-2:] == "am" and hourmindict["hour"] == 12:
            hourmindict["hour"] = 0
    
    elif len(raw_time_tuple) == 0 or not raw_time_len_checker:
        hourmindict = dict()

    if len(raw_date_tuple) > 0:
        mid_date = re_sub(r"\/|\s|-", " ", raw_date_tuple[-1][0]).split()
        if len(mid_date[0]) >= 3 and mid_date[0][0].isnumeric():
            mid_date = [mid_date[0][:-2]] + mid_date[1:]
        elif len(mid_date[1]) >= 3 and mid_date[1][0].isnumeric():
            mid_date = [mid_date[0], mid_date[1][:-2]] if len(mid_date) == 2 else [mid_date[0], mid_date[1][:-2], mid_date[2]]

        if (mid_date[0].isnumeric() and mid_date[1].isnumeric() and int(mid_date[monthindex]) <= 12 and int(mid_date[dateindex]) <= 31) or (mid_date[0].isalpha() and mid_date[1].isnumeric() and int(mid_date[1]) <= 31) or (mid_date[1].isalpha() and mid_date[0].isnumeric() and int(mid_date[0]) <= 31):

            # if there are three values in the list, take the final value as is if it's four digits or add 2000 if it's a two digit value, else just initiate the dict

            monthdateyeardict = {"year": int(mid_date[-1])} if (len(mid_date) == 3 and len(mid_date[-1]) == 4) else {"year": int(mid_date[-1]) + int(str(dt.today().year)[:2])*100} if (len(mid_date) == 3 and len(mid_date[-1]) == 2) else dict()
            # monthdateyeardict = {"year": int(mid_date[-1])} if (len(mid_date[-1]) == 4 and len(mid_date) == 3) else {"year": int(mid_date[-1]) + 2000}
            if mid_date[0].isalpha():
                if mid_date[0] in long_months:
                    monthdateyeardict["month"] = long_months.index(mid_date[0]) + 1
                elif mid_date[0] in short_months:
                    monthdateyeardict["month"] = short_months.index(mid_date[0]) + 1
                monthdateyeardict["date"] = int(mid_date[1])
            elif mid_date[1].isalpha():
                if mid_date[1] in long_months:
                    monthdateyeardict["month"] = long_months.index(mid_date[1]) + 1
                elif mid_date[1] in short_months:
                    monthdateyeardict["month"] = short_months.index(mid_date[1]) + 1
                monthdateyeardict["date"] = int(mid_date[0])
            elif mid_date[0].isnumeric() and mid_date[1].isnumeric():
                monthdateyeardict["month"] = int(mid_date[monthindex])
                monthdateyeardict["date"] = int(mid_date[dateindex])

        elif (mid_date[0].isalpha() and mid_date[1].isalpha()) or (mid_date[monthindex].isnumeric() and mid_date[dateindex].isnumeric() and (int(mid_date[monthindex]) > 12 or int(mid_date[dateindex]) > 31)) or (mid_date[0].isalpha() and mid_date[1].isnumeric() and int(mid_date[1]) > 31) or (mid_date[1].isalpha() and mid_date[0].isnumeric() and int(mid_date[0]) > 31):

            monthdateyeardict = dict()

    elif len(raw_date_tuple) == 0:
        monthdateyeardict = dict()

    # mid_date, mid_time = tuple(raw_date)[-1][0], tuple(anyitem for anyitem in tuple(raw_time) if len(anyitem[0]) >= 3)[-1][0]

    return_year, return_month, return_date, return_hour, return_minute = (monthdateyeardict.get("year") if monthdateyeardict.get("year") != None else dt.today().year), (monthdateyeardict.get("month") if monthdateyeardict.get("month") != None else dt.today().month), monthdateyeardict["date"], (hourmindict.get("hour") if hourmindict.get("hour") != None else 0), (hourmindict.get("minute") if hourmindict.get("minute") != None else 0)

    # return dt.fromisoformat(f"""{return_year}-{"0" + str(return_month) if len(str(return_month)) == 1 else return_month}-{"0" + str(return_date) if len(str(return_date)) == 1 else return_date}T{"0" + str(return_hour) if len(str(return_hour)) == 1 else return_hour}:{"0" + str(return_minute) if len(str(return_minute)) == 1 else return_minute}""")
    return dt(return_year, return_month, return_date, return_hour, return_minute)
    # return dt.fromisoformat(f"{monthdateyeardict.get("year") if }")
    
    # monthexp = r"(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
    # dateexp = r"[0-9]{1,2}"
    # yearexp = r"[0-9]{2,4}"
    # datecomboexp = r"\b[0-9]{1,2}(?:\/|\h|-)[0-9]{1,2}(?:(?:\/|\h|-)[0-9]{1,2})?\b"
    # # regex for full date combo, but doesn't yet restrict users to only one natural language month: 
    # # 
    # # \b(?:[0-9]{1,2}(?:(?:th|rd|nd|st)?(?: of)?)?|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:\/|\h|-)(?:[0-9]{1,2}(?:th|rd|nd|st)?|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:(?:\/|\h|-)(?:[0-9]{2}|[0-9]{4}))?\b
    # # \b(?:(?:(?:[0-9]{1,2}(?:th|rd|nd|st)?)|(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty(?:-|\h)first|twenty(?:-|\h)second|twenty(?:-|\h)third|twenty(?:-|\h)fourth|twenty(?:-|\h)fifth|twenty(?:-|\h)sixth|twenty(?:-|\h)seventh|twenty(?:-|\h)eighth|twenty(?:-|\h)ninth|thirtieth|thirty(?:-|\h)first))(?: of)?|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:\/|\h|-)(?:[0-9]{1,2}(?:th|rd|nd|st)?|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:(?:\/|\h|-)(?:[0-9]{2}|[0-9]{4}))?\b
    # #
    # datepullexp = rf"\b(?:{monthexp}|{dateexp})(?:\/|\h|-\.)(?:{monthexp}|{dateexp})(?:(?:\/|\h|-\.)(?:{yearexp}))?\b"
    # # first regex: three number dates/natural langauge months
    # # second regex: 2nd of january 2024 / january 2nd 2024?
    # # (?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty(?:-|\h)first|twenty(?:-|\h)second|twenty(?:-|\h)third|twenty(?:-|\h)fourth|twenty(?:-|\h)fifth|twenty(?:-|\h)sixth|twenty(?:-|\h)seventh|twenty(?:-|\h)eighth|twenty(?:-|\h)ninth|thirtieth|thirty(?:-|\h)first|)
    # \b(?:(?:(?:(?:(?:[1-2][0-9])|(?:3(?:0|1))|(?:0?[1-9]))(?:(?:11|12|13|4|5|6|7|8|9|0)\s?th|[^1]3\s?rd|2\s?nd|1\s?st)?)|(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty(?:-|\s)first|twenty(?:-|\s)second|twenty(?:-|s)third|twenty(?:-|\s)fourth|twenty(?:-|\s)fifth|twenty(?:-|\s)sixth|twenty(?:-|\s)seventh|twenty(?:-|\s)eighth|twenty(?:-|\s)ninth|thirtieth|thirty(?:-|\s)first))(?:\sof)?|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:\/|\s|-)(?:(?:(?:(?:[1-2][0-9])|(?:3(?:0|1))|(?:0?[1-9]))(?:(?:4|5|6|7|8|9|0)\s?th|3\s?rd|2\s?nd|1\s?st)?)|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(?:(?:\/|\s|-)(?:[0-9]{2}|[0-9]{4}))?\b

def qualifiersparse(strarg):

    from re import finditer as re_finditer

    return {(item.span()[0], item.span()[1]): item[0] for item in re_finditer(r"\b[a-z][0-9]\b", strarg)}

# Summon the list

# Order the list based on criteria

# Show the top 5 things in the list to users

# Permit users to resort them if they'd really like?

# Step-by-step "wizard" input or all-in-one quick input, ability to set default mode as one or the other

# Ask users for their input

def PanicUserInput():

    # userinput = input("Welcome to Python time! Input a new task and some attributes: ")
    userinput = "Will this work? 10-10-24 who knows! 3PM"

    qualifiers = qualifiersparse(userinput)
    # rawdatetime = tuple(tuple(anyitem) for anyitem in datetimeparse(userinput))
    # date, time = rawdatetime[0][-1][0] if len(rawdatetime[0]) >= 1 else None, rawdatetime[1][-1][0] if len(rawdatetime[1]) >= 1 else None

    # return date, time, qualifiers

    # userinput = input("Welcome to Python time! Input a new task and some attributes: ")
    # print(userinput)

    # firsttagindex = None

    # for counter, anychar in enumerate(userinput):

    #     try:
    #         charbefore = userinput[counter-1]
    #     except:
    #         charbefore = ""
    #     try:
    #         charafter = userinput[counter+2]
    #     except:
    #         charafter = ""
    #     print(charbefore + " " + charafter)

    # print(firsttagindex)

    # newuserinput = userinput.split()
    # print(newuserinput)

    # qualifiers_list = [anyinput for anyinput in newuserinput if len(anyinput) == 2 and anyinput[0].isalpha() and anyinput[-1].isnumeric()]
    # print(qualifiers_list)

# print(PanicUserInput())

print(datetimeparse("Steven goes to the farm 25th of august 2024"))

# Parse different parts from the user input if necessary

# Log the task into the list

