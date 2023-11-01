import server

games = []

def createNewGame():
    games.append(server)
    
def closeGame(gameNumber):
    games.pop(gameNumber)