from random import choice,shuffle,randint,seed
from datetime import datetime
seed()
stars = 21
maxRounds = 3
  
def gameList(g,w,l,n):
  # g -> Game Num
  # w -> Win array
  # l -> Lost Array
  # n -> Neutral Array
  shuffle(n)
  if len(w)%2==0:
    x=choice([2,4])
  else:
    x=choice([1,3])
  neutW = n[:x]
  neutL = n[x:]
  if g%2==0:
    w=w[::-1]
    l=l[::-1]
  elif g%3==0:
    w=w[:len(w)//2]+w[len(w)//2:]
    l=l[:len(w)//2]+l[len(w)//2:]
  w = w[g:]+w[:g] + neutW
  l = l[:g]+l[g:] + neutL
  return w + l

def buildRound(gList,lC,tC,nC):
  R={}
  for i in range(0,15):
    if (nC < lC) or (nC < tC):
      searchFor = ["L","T"]
    else:
      searchFor = ["L","N","T"]
    play=[]
    j=0
    for _ in range(2):
      j+=1
      while gList[j-1][0] not in searchFor:
        j+=1
      play.append(gList[j-1])
      if play[_].startswith('L'):lC-=1
      if play[_].startswith('N'):nC-=1
      if play[_].startswith('T'):tC-=1
      if play[_].startswith(('L','T')):
        searchFor.remove(play[_][0])
      elif (lC>nC or tC>nC):
        searchFor.remove(play[_][0])
    if play[0].startswith('L') or play[1].startswith('T'):
      R[play[0]] = play[1]
    elif play[0].startswith('T'):
      R[play[1]] = play[0]
    else:
      R[play[1]] = play[0]
    gList.remove(play[0])
    gList.remove(play[1])
  return R

def printRound(r,R):
  if r+1>1:
    print("")
  print(f"ROUND {r+1}")
  print("*"*stars)
  for i in range(0,15):
      print(f"Board {str(i+1).zfill(2)} -> {list(R[r].keys())[i]} v {list(R[r].values())[i]}")
  for i in range(0,15):
    for s in range(0,r):
      # Check Loyalists
      if list(R[r].keys())[i]==list(R[s].keys())[i]:
        print(f"{r+1} => {s+1}: {list(R[r].keys())[i]} -> Board {i+1}: Loyalist")
      # Check Neutrals
      if list(R[r].keys())[i]==list(R[s].values())[i]:
        print(f"{r+1} => {s+1}: {list(R[r].keys())[i]} -> Board {i+1}: Now a Loyalist")
      if list(R[r].values())[i]==list(R[s].keys())[i]:
        print(f"{r+1} => {s+1}: {list(R[r].values())[i]} -> Board {i+1}: Now a Traitor ")
      # Check Traitors
      if list(R[r].values())[i]==list(R[s].values())[i]:
        print(f"{r+1} => {s+1}: {list(R[r].values())[i]} -> Board {i+1}: Traitor")

def gamesWon(R):
  wins = []
  lost = []
  LWinC = 0
  print("*"*stars)
  for i in range(0,15):
    #win = input(f"Did (L)oyalists or (T)raitors win board {str(i+1).zfill(2)}? ")
    win = choice(['L','T'])
    while win.upper() not in ['L','T']:
      print("Sorry, try again!")
      win = input(f"Did (L)oyalists or (T)raitors win board {str(i+1).zfill(2)}? ")
    if win.upper() == "L":
      if list(R.keys())[i][0]=="L": wins.append(list(R.keys())[i])
      if list(R.values())[i][0]=="T": lost.append(list(R.values())[i])
      LWinC+=1
    else:
      if list(R.keys())[i][0]=="L": lost.append(list(R.keys())[i])
      if list(R.values())[i][0]=="T": wins.append(list(R.values())[i])
  return wins, lost, LWinC

def __main__():
  LWinCount = 0
  Ls = [f"L{str(x).zfill(2)}" for x in range(1,27,2)]
  Ts = [f"T{str(x).zfill(2)}" for x in range(2,28,2)]
  Ns = [f"N{str(x).zfill(2)}" for x in range(27,31)]

  initG = Ls + Ts
  shuffle(initG)
  Wins = initG[:13]
  Lost = initG[13:]
  R = []
  for r in range(maxRounds):
    Game = gameList(1,Wins,Lost,Ns)
    R.append(buildRound(Game,len(Ls),len(Ts),len(Ns)))
    printRound(r,R)
    Wins, Lost, LWinInc = gamesWon(R[r])
    LWinCount+=LWinInc

  print(f"Loyalists have won {LWinCount} times")
  print(f"Traitors  have won {(maxRounds * 15) - LWinCount} times")
  
if __name__=="__main__":
  __main__()
