import urllib.request
import sqlite3
import datetime


def standing():

    conn = sqlite3.connect('BD.db')
    conn.execute("drop table if exists Standings")
    conn.execute("CREATE TABLE Standings(id int,Name text,pct real,pf int,pa int)")
    conn.commit()
    conn.close()

    response = urllib.request.urlopen('http://espn.go.com/nfl/standings')
    html = response.read()
    response.close

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')

    links2 = soup.find_all('span', class_='team-names')
    i = 0
    for link2 in links2:
        team = link2.contents[0]
        if (team.string != None):
            print(team.string)

        links = soup.findAll('tr')[i].find_all('td')
        for link in links:
            names = link.contents[0]

            if (names.string != None):
                print(names.string)

        print('')
        i = i + 1


        BDStanding(i,team.string,links[4].contents[0],links[9].contents[0],links[10].contents[0])



def PastSchedule():

    conn = sqlite3.connect('BD.db')
    conn.execute("drop table if exists PastScores")
    conn.execute("CREATE TABLE PastScores(Score text)")
    conn.commit()
    conn.close()
    Week = datetime.date.today().isocalendar()[1] - datetime.date(2015,9,3).isocalendar()[1]
    for ii in range (1, Week):
        response = urllib.request.urlopen('http://espn.go.com/nfl/schedule/_/week/' + str(ii))
        html = response.read()
        response.close

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, 'html.parser')

        rows = soup.find_all("tr")
        for row in rows:
            i = 0
            cols = row.find_all("td")

            for col in cols:
                aa = col.find_all("a")
                if(i == 2):
                    print(aa[0].contents[0])
                    BDPast(aa[0].contents[0])
                if(i==5):
                    i=0
                else:
                    i = i+1


def FutureSchedule():
    conn = sqlite3.connect('BD.db')
    conn.execute("drop table if exists Standings")
    conn.execute("CREATE TABLE Standings(id int,Name text,pct real,pf int,pa int)")
    conn.commit()
    conn.close()
    Week = datetime.date.today().isocalendar()[1] - datetime.date(2015,9,3).isocalendar()[1]
    print(Week)

    for ii in range (Week, 18):
        response = urllib.request.urlopen('http://espn.go.com/nfl/schedule/_/week/' + str(ii))
        html = response.read()
        response.close
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')






def BDStanding(i,team,pct,pf,pa):
    conn = sqlite3.connect('BD.db')
    conn.execute("INSERT INTO Standings VALUES (?,?,?,?,?)",(i,team,pct,pf,pa))
    conn.commit()
    conn.close()

def BDPast(score):
    conn = sqlite3.connect('BD.db')
    conn.execute("INSERT INTO PastScores VALUES (?)",(score,))
    conn.commit()
    conn.close()

#standing()
PastSchedule()
#FutureSchedule()