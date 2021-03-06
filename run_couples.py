#!/usr/bin/python

import sys
import random
import smtplib

def main():
  if len(sys.argv)<3:
    print "usage: %s <peoplefile> <smtpserver>"%sys.argv[0]
    sys.exit(0)
  couples=[x.strip().split(',') for x in open(sys.argv[1]).readlines()]
  people={}
  partners={}
  
  for x in couples:
    people[x[0]] = x[1]
    people[x[2]] = x[3]
    partners[x[0]] = x[2]
    partners[x[2]] = x[0]

  # remove emails 
  couples = [[x[0],x[2]] for x in couples]

  ok=False
  while not(ok):
    ok = True
    names = people.keys()

    random.shuffle(names)
    random.shuffle(couples)
    
    p2p={}
    for i in range(len(names)):
      fr=names[i]
      to=names[(i+1)%len(names)]
      p2p[fr]=to
      if partners[to]==fr: # p2p should not be between partners
        ok = False
    
    c2c={}
    for i in range(len(couples)):
      fr = couples[i]
      to = couples[(i+1)%len(couples)]
      c2c[fr[0]]=to
      c2c[fr[1]]=to
      for x in [p2p[fr[0]],p2p[fr[1]]]:
        for y in [to[0],to[1]]:
          if x==y:
            ok=False
          if p2p[x] == p2p[partners[y]]:
            ok=False
          if p2p[partners[x]] == p2p[y]:
            ok=False
   
  server=smtplib.SMTP(sys.argv[2])
  for fr,to in p2p.iteritems():
    msg="Subject: De kerstman\nFrom: \"Kerstman\" <karel.vervaeke@telenet.be>\n\nBeste %s,\nJe mag dit jaar een cadeautje kopen voor %s.  Samen met %s mag je een cadeautje kopen voor %s en %s.  Gelieve nog even te bevestigen dat je deze mail gekregen hebt, dat spaart verwarring achteraf uit. Veel plezier!"%(fr,to,partners[fr],c2c[fr][0],c2c[fr][1])
    dbg="%s voor %s en voor %s"%(fr,to,c2c[fr])
    
    print(dbg)
    
    server.set_debuglevel(1)
    server.sendmail('Kerstman <karel.vervaeke@telenet.be>',people[fr], msg)

if __name__=='__main__':
  main()
