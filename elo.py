#ELO
#python 3.4.3

PLAYERS = ["Toto", "Titi", "Tata"]

import math
import json

class ELOPlayer:
    name      = ""
    place     = 0
    eloPre    = 0
    eloPost   = 0
    eloChange = 0
    
class ELOMatch:
    players = []
    
    def addPlayer(self, name, place, elo):
        player = ELOPlayer()
        
        player.name    = name
        player.place   = place
        player.eloPre  = elo
        
        self.players.append(player)
        
    def getELO(self, name):
        for p in self.players:
            if p.name == name:
                return p.eloPost
            
        return 1500;

    def getELOChange(self, name):
        for p in self.players:
            if p.name == name:
                return p.eloChange;
                
        return 0;
 
    def calculateELOs(self):
        n = len(self.players)
        K = 32 / (n - 1);
        
        for i in range(n):
            curPlace = self.players[i].place;
            curELO   = self.players[i].eloPre;
                        
            for j in range(n):
                if i != j:
                    opponentPlace = self.players[j].place
                    opponentELO   = self.players[j].eloPre  
                    
                    #work out S
                    if curPlace < opponentPlace:
                        S = 1.0
                    elif curPlace == opponentPlace:
                        S = 0.5
                    else:
                        S = 0.0
                    
                    #work out EA
                    EA = 1 / (1.0 + math.pow(10.0, (opponentELO - curELO) / 400.0))
                    
                    #calculate ELO change vs this one opponent, add it to our change bucket
                    #I currently round at this point, this keeps rounding changes symetrical between EA and EB, but changes K more than it should
                    self.players[i].eloChange += round(K * (S - EA))

                    #add accumulated change to initial ELO for final ELO   
                    
            self.players[i].eloPost = self.players[i].eloPre + self.players[i].eloChange

class Scoreboard:
  scoreboard = None

  @classmethod
  def __init__(self):
    if self.scoreboard == None:
      with open("scoreboard.json", "r") as read_file:
        self.scoreboard = json.load(read_file)

  def has_player(self, name):
    for p in self.scoreboard:
      if p["name"] == name:
        return True
    return False

  def add_player(self, name):
    self.scoreboard.append({"name":name,"elo":1000})

  def save(self):
    with open("scoreboard.json", "w") as write_file:
      json.dump(self.scoreboard, write_file)

  def get_player_elo(self, name):
    for p in self.scoreboard:
      if p["name"] == name:
        return p["elo"]

  def set_player_elo(self, name, value):
    for p in self.scoreboard:
      if p["name"] == name:
        p["elo"] = value

  def __str__(self):
    res = ""

    self.scoreboard.sort(key=lambda x: x["elo"], reverse=True)
    for i in range(0, len(self.scoreboard)):
      name = self.scoreboard[i]["name"]
      res += str(i+1) + ". " + str(name) + "(" + str(self.get_player_elo(name)) + ")\n"
    return res

def play_game(players, scoreboard):
  game = ELOMatch()
  
  # setup the game's players
  for p in range(0, len(players)):
    game.addPlayer(players[p], p+1, scoreboard.get_player_elo(players[p]))

  # run the game
  game.calculateELOs()

  # change scores in scoreboard
  for p in game.players:
    scoreboard.set_player_elo(p.name, game.getELO(p.name))

  # print score diff
  for p in game.players:
    result_line = p.name+" "+str(game.getELO(p.name))+"("
    if game.getELOChange(p.name) >= 0:
      result_line += "+"
    result_line += str(game.getELOChange(p.name))+")"
    print(result_line)

scoreboard = Scoreboard()

# create players if not in scoreboard
for p in PLAYERS:
  if not scoreboard.has_player(p):
    scoreboard.add_player(p)

print(scoreboard)
print("")

print("Playing game...")
play_game(PLAYERS, scoreboard)

print("")
print(scoreboard)

save = input("Save? (yes/no)")

if save == "yes":
  scoreboard.save()
