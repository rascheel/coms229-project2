from random import *
import string, sys, os, errno
def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise

n = 2;
if (len(sys.argv)!=3):
  print "usage: python fuzzy.py testdir execdir"
  sys.exit(0)

testdir = sys.argv[1]
execdir = sys.argv[2]

mkdir_p(testdir)
mkdir_p(testdir+"/generatedaut")
mkdir_p(testdir+"/showgenoutput")

for counter in range(0,n):
  random = Random()
  random.seed(counter)
  """
  commands are of the form
  ./showgen -g 0 -a -tx 0,3 -ty 2,3 -wx 4,5 -wy 6,7
  """
  exe = execdir + "/showgen "
  gen = ""
  a = ""
  tx = ""
  ty = ""
  wx = ""
  wy = ""

  fname = "test" + str(counter) + ".aut"
  #assign to none now. If the odds are in their favor, they will be assigned
  #values by the args below
  wxLow = None
  wxHigh = None
  wyLow = None
  wyHigh = None
  xLow = None
  xHigh = None
  yLow = None
  yHigh = None
  runToGen = 0

  if random.uniform(0,1) < 0.7:
    runToGen = random.randint(0,1000)
    gen = "-g " + str(runToGen) + " "
  if random.choice([True, False]):
    a = "-a "
  if random.choice([True, False]):
    xLow = random.randint(-50,50)
    xHigh = xLow + random.randint(0,50)
    tx = "-tx " + str(xLow) + "," + str(xHigh) + " "
  if random.choice([True, False]):
    yLow = random.randint(-50,50)
    yHigh = yLow + random.randint(0,50)
    ty = "-ty " + str(yLow) + "," + str(yHigh) + " "
  if random.choice([True, False]):
    wxLow = random.randint(-50,50)
    wxHigh = wxLow + random.randint(0,50)
    wx = "-wx " + str(wxLow) + "," + str(wxHigh) + " "
  if random.choice([True, False]):
    wyLow = random.randint(-50,50)
    wyHigh = wyLow + random.randint(0,50)
    wy = "-wy " + str(wyLow) + "," + str(wyHigh) + " "

  command = exe + gen + a + tx + ty + wx + wy 
  if (random.choice([True,False])):
    command += " < " #to read as stdin instead of file
  command += testdir + "/generatedaut/" + fname

  if a != "":
    command += " | " + exe 
  command += " > " + testdir + "/showgenoutput/test" + str(counter) + ".229"

  autxLow = random.randint(-50,50)
  autxHigh = autxLow + random.randint(0,50)

  autyLow = random.randint(-50,50)
  autyHigh = autyLow + random.randint(0,50)

  #see if they were give values by chance. If not, the values presented
  #in the autx file remain the defaults, so assign them as such here
  if(xLow == None):
    xLow = autxLow
    xHigh = autxHigh
  if(yLow == None):
    yLow = autyLow
    yHigh = autyHigh

  f = open(testdir + "/generatedaut/" + fname, "w")
  f.write("Xrange " + str(autxLow) + " " + str(autxHigh) + ";\n")
  f.write("Yrange " + str(autyLow) + " " + str(autyHigh) + ";\n")

  f.write('Name "Generated by Ryan mwahaha";\n')

  rd = random.randint(0,255)
  gd = random.randint(0,255)
  bd = random.randint(0,255)
  ra = random.randint(0,255)
  ga = random.randint(0,255)
  ba = random.randint(0,255)

  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  liveChar = random.randint(0,255)
  deadChar = random.randint(0,255)
  f.write("Colors (" + str(rd) + ", " + str(gd) + ", " + str(bd) + "), (" + str(ra) + ", " + str(ga) + ", " + str(ba) + ");\n")
  f.write("Chars " + str(deadChar) + ", " + str(liveChar) + ";\n")

  f.write("Initial {\n")
  firstX = True
  oracleList = [ [0]*((xHigh-xLow)+1) for b in range(yHigh-yLow+1) ]
  for y in range(autyLow, autyHigh+1):
    if(random.choice([True,False])):
      f.write("Y = " + str(y) + " : ")
      written = False
      for x in range(autxLow, autxHigh+1):
        #also print input stuff for 308 program
        if(random.choice([True,False])):
          if(y >= yLow and y <= yHigh and x >= xLow and x <= xHigh):
            oracleList[y-yLow][x-xLow] = 1
          if (firstX):
            written = True
            f.write(str(x))
            firstX = False
          else:
            written = True
            f.write("," + str(x))
        else:
          #these are constricted ranges presented by the args. This
          #output is used for 308-file calculations
          if(y >= yLow and y <= yHigh and x >= xLow and x <= xHigh):
            oracleList[y-yLow][x-xLow] = 0
      if (not written):
        randomInt = random.randint(autxLow, autxHigh)
        f.write(str(randomInt))
        if(y >= yLow and y <= yHigh and randomInt >= xLow and randomInt <= xHigh):
          oracleList[y-yLow][randomInt-xLow] = 1
      f.write(";\n")
      firstX = True
    else:
      for x in range(autxLow, autxHigh+1):
        #these are constricted ranges presented by the args. This
        #output is used for 308-file calculations
        if(y >= yLow and y <= yHigh and x >= xLow and x <= xHigh):
          oracleList[y-yLow][x-xLow] = 0
  f.write("};\n")
  f.flush()
  os.fsync(f.fileno())
  f.close()
  """ using command from above!"""
  if (wxLow is None):
    wxLow = xLow
    wxHigh = xHigh
  if (wyLow is None):
    wyLow = yLow
    wyHigh = yHigh

  print "\n" + command
  os.system(command)

  #we know ranges here
  #xLow, xHigh, yLow, yHigh
  #wxLow, wxHigh, wyLow, wyHigh

  #generate oracle
  tmp = oracleList[:][:]
  #for EVEN generations, oracleList is PREV
  #for ODD generations, tmp is PREV
  for genNum in range(0,runToGen):
    #for y in range(0,yHigh-yLow):
    #for y in range(len(oracleList)): 
    for y in range(wyLow-yLow, (wyLow-yLow)+(wyHigh-wyLow)+1):
      #for x in range(0,xHigh-xLow):
      #for x in range(len(oracleList[y])):
      for x in range(wxLow-xLow, (wxLow-xLow)+(wxHigh-wxLow)+1):
        liveNeighbors = 0
        i = y-1
        j = x-1
        #convoluted way of counting the live neighbors
        #Don't judge me foo!
        while(i <= y+1):
          while(j <= x+1):
            if(i >= yLow and i <= yHigh and j >= xLow and j <= xHigh):
              if(i != y and j != x):
                if (i >= 0 and i < len(oracleList) and j >= 0 and j < len(oracleList[0])):
                  if (genNum%2 == 0):
                    liveNeighbors += oracleList[i][j]
                  else:
                    liveNeighbors += tmp[i][j]
            j+=1
          i+=1
        #calculated the state for the next generation

        preval = 0
        nowval = 0
        if(y >= yLow and y <= yHigh and x >= xLow and x <= xHigh):
          if (genNum%2 == 0):
            preval = oracleList[y][x]
          else:
            preval = tmp[y][x]
        else:
            preval = 0

        if(preval == 1):
          if(liveNeighbors == 2 or liveNeighbors == 3):
            nowval = 1
          else:
            nowval = 0
        elif(preval == 0):
          if(liveNeighbors == 3):
            nowval = 1
          else:
            nowval = 0
        if (genNum%2 == 0):
          if(y >= yLow and y <= yHigh and x >= xLow and x <= xHigh):
            tmp[y][x] = nowval
        else:
          if(y >= yLow and y <= yHigh and x >= xLow and x <= xHigh):
            oracleList[y][x]= nowval
  if (runToGen%2 == 0):
    #now oracleList contains the current values either way
    oracleList = tmp[:][:]
  #crop and diff

  testF = open(testdir + "/showgenoutput/test" + str(counter) + ".229")
  testPassed = True
  for y in range((wyLow-yLow)+(wyHigh-wyLow), wyLow-yLow+1):
    for x in range(wxLow-xLow, (wxLow-xLow)+(wxHigh-wxLow)+1):
      cell = testF.read(1)

      #cell is outside the terrain, so the index will be invalid
      if (y > yHigh or y < yLow or x > xHigh or x < xLow):
        if (cell != deadChar):
          testPassed = False
          print "Test " + str(counter) + " failed at window index ("+str(x)+","+str(y)+")"
      else:
        if((cell != liveChar and oracleList[y][x] == 1)):
          testPassed = False
          print "Test " + str(counter) + " failed at window index ("+str(x)+","+str(y)+")"
        elif((cell != deadChar and oracleList[y][x] == 0)):
          testPassed = False
          print "Test " + str(counter) + " failed at window index ("+str(x)+","+str(y)+")"
    returnStatement = testF.read(1)
    if(returnStatement != '\n'):#TODO will this fail on windows machines (not that I care)?
      testPassed = False
      print "Test " + str(counter) + " failed at y=" + str(y) + "with no return statement"
  testF.flush()
  testF.close()
  if(testPassed):
    print "Test " + str(counter) + " passed!"
  else:
    print "Test " + str(counter) + " failed."

  print "######################################################################"

