import urllib.request
import sqlite3


def Parse():

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


        BD(i,team.string,links[4].contents[0],links[9].contents[0],links[10].contents[0])




def BD(i,team,pct,pf,pa):
    conn = sqlite3.connect('BD.db')
    conn.execute("INSERT INTO Standings VALUES (?,?,?,?,?)",(i,team,pct,pf,pa))
    conn.commit()
    conn.close()

Parse()