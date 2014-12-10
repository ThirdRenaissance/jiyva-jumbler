#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Jiyva Jumbler - stats for Dungeon Crawl Stone Soup logs
# Copyright (C) 2014 Third Renaissance
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


# Your log or hiscore file
CrawlLogFile = "/home/user/.crawl/saves/logfile"

# Display only stats for species/background/god/char
# with at least this amount of played games
MinGames = 5

# Display at least this many stat lines, regardless of MinGames
MinDisplay = 10

# Show recent scores in a graph
ShowGraph = True


import sys
import os
import fileinput
import re
import statistics as stats
import random
import datetime


usageline = "Usage: [python3] {} [logfile]".format(sys.argv[0])

if len(sys.argv) > 2:
	print("Wrong number of arguments. Quote file names containing spaces.")
	print(usageline)
	exit(1)
elif len(sys.argv) == 2:
	CrawlLogFile = sys.argv[1]

if os.path.isfile(CrawlLogFile) == False:
	print("\"{}\" does not exist.".format(CrawlLogFile))
	print(usageline)
	exit(1)


ProgramVersion = "0.1"

GameCount = 0
DurationTotal = 0
DurationList = []
TurnTotal = 0
TurnList = []
DepthTotal = 0
DepthList = []
ScoreTotal = 0
ScoreList = []
RuneTotal = 0
RuneList = []
PlaceCount = {}
PlaceList = []
KillerCount = {}
KillerList = []
SpeciesCount = {}
SpeciesTotalScore = {}
SpeciesHighScore = {}
BackgroundCount = {}
BackgroundTotalScore = {}
BackgroundHighScore = {}
CharacterCount = {}
CharacterTotalScore = {}
CharacterHighScore = {}
GodCount = {}
GodTotalScore = {}
GodHighScore = {}
XlTotal = 0
XlList = []
XlSpecies = {}
XlBackground = {}

TimeScoreList = []

SpeciesMaxXl = {}
BackgroundMaxXl = {}
CharacterMaxXl = {}
GodMaxXl = {}
SpeciesMaxTurn = {}
BackgroundMaxTurn = {}
GodMaxTurn = {}
SpeciesMaxRune = {}
BackgroundMaxRune = {}
CharacterMaxRune = {}
GodMaxRune = {}


# Process log
for line in fileinput.input(CrawlLogFile):
	if line.startswith('v='):
		GameCount += 1
		
		# Duration
		duration_search = re.search('(?<=dur=)[0-9]+(?=:)', line)
		duration = int(duration_search.group())
		
		DurationTotal += duration
		DurationList.append(duration)
		
		# Turns
		turn_search = re.search('(?<=turn=)[0-9]+(?=:)', line)
		turn = int(turn_search.group())
		
		TurnTotal += turn
		TurnList.append(turn)
		
		# Depth
		depth_search = re.search('(?<=absdepth=)[0-9]+(?=:)', line)
		depth = int(depth_search.group())
		
		DepthTotal += depth
		DepthList.append(depth)
		
		# Score
		score_search = re.search('(?<=sc=)[0-9]+(?=:)', line)
		score = int(score_search.group())
		
		ScoreTotal += score
		ScoreList.append(score)
		
		# Runes
		rune_search = re.search('(?<=nrune=)[0-9]+(?=:)', line)
		if rune_search == None:
			rune = 0
		else:
			rune = int(rune_search.group())
		
		RuneTotal += rune
		RuneList.append(rune)
		
		# Place of death
		place_search = re.search('(?<=place=)[a-zA-Z\-\' ]+(\:\:)?[0-9]*(?=:)', line)
		place = str.replace(str.replace(place_search.group(), "::", ":"), "D", "Dungeon")
	
		PlaceList.append(place)
		
		if place in PlaceCount:
			PlaceCount[place] = PlaceCount[place] + 1
		else:
			PlaceCount[place] = 1
		
		# Killer
		killer_search = re.search('(?<=killer=)[a-zA-Z\-\' ]+(?=:)', line)
		if killer_search == None:
			killer = 'killed by environment'
		else:
			killer = re.sub('^(a |an )','', killer_search.group())
	
		KillerList.append(killer)
		
		if killer in KillerCount:
			KillerCount[killer] = KillerCount[killer] + 1
		else:
			KillerCount[killer] = 1
		
		# Species
		species_search = re.search('(?<=race=)[a-zA-Z ]+(?=:)', line)
		species = species_search.group()
		
			# set colored Draconians to base name
		if re.search('Draconian', species):
			species = 'Draconian'
	
		if species in SpeciesCount:
			SpeciesCount[species] = SpeciesCount[species] + 1
			SpeciesTotalScore[species] = SpeciesTotalScore[species] + score
		else:
			SpeciesCount[species] = 1
			SpeciesTotalScore[species] = score
		
		if SpeciesHighScore.get(species, 0) < score:
			SpeciesHighScore[species] = score
	
		# Background
		background_search = re.search('(?<=cls=)[a-zA-Z ]+(?=:)', line)
		background = background_search.group()
		
		if background in BackgroundCount:
			BackgroundCount[background] = BackgroundCount[background] + 1
			BackgroundTotalScore[background] = BackgroundTotalScore[background] + score
		else:
			BackgroundCount[background] = 1
			BackgroundTotalScore[background] = score
		
		if BackgroundHighScore.get(background, 0) < score:
			BackgroundHighScore[background] = score
		
		# Character
		character_search = re.search('(?<=char=)[a-zA-Z]+(?=:)', line)
		character = character_search.group()
		
		if character in CharacterCount:
			CharacterCount[character] = CharacterCount[character] + 1
			CharacterTotalScore[character] = CharacterTotalScore[character] + score
		else:
			CharacterCount[character] = 1
			CharacterTotalScore[character] = score
		
		if CharacterHighScore.get(character, 0) < score:
			CharacterHighScore[character] = score
		
		# God
		god_search = re.search('(?<=god=)[a-zA-Z ]+(?=:)', line)
		if god_search == None:
			god = 'no god'
		else:
			god = str.title(god_search.group())
		
		if god in GodCount:
			GodCount[god] = GodCount[god] + 1
			GodTotalScore[god] = GodTotalScore[god] + score
		else:
			GodCount[god] = 1
			GodTotalScore[god] = score
		
		if GodHighScore.get(god, 0) < score:
			GodHighScore[god] = score
			
		# XL
		xl_search = re.search('(?<=xl=)[0-9]+(?=:)', line)
		xl = int(xl_search.group())
		
		XlTotal += xl
		XlList.append(xl)
		
		if species in XlSpecies:
			XlSpecies[species] = XlSpecies[species] + xl
		else:
			XlSpecies[species] = xl
	
		if background in XlBackground:
			XlBackground[background] = XlBackground[background] + xl
		else:
			XlBackground[background] = xl
		
		# Graph
		endtime_search = re.search('(?<=end=)[0-9]+(?=[^0-9])', line)
		endtime = int(endtime_search.group())
		
		TimeScoreList.append([endtime, score])
		
		# Challenge specific
		if SpeciesMaxXl.get(species, 0) < xl:
			SpeciesMaxXl[species] = xl
		if BackgroundMaxXl.get(background, 0) < xl:
			BackgroundMaxXl[background] = xl
		if CharacterMaxXl.get(character, 0) < xl:
			CharacterMaxXl[character] = xl
		if GodMaxXl.get(god, 0) < xl:
			GodMaxXl[god] = xl
		
		if SpeciesMaxTurn.get(species, 0) < turn:
			SpeciesMaxTurn[species] = turn
		if BackgroundMaxTurn.get(background, 0) < turn:
			BackgroundMaxTurn[background] = turn
		if GodMaxTurn.get(god, 0) < turn:
			GodMaxTurn[god] = turn
		
		if SpeciesMaxRune.get(species, 0) <= rune:
			SpeciesMaxRune[species] = rune
		if BackgroundMaxRune.get(background, 0) <= rune:
			BackgroundMaxRune[background] = rune
		if CharacterMaxRune.get(character, 0) <= rune:
			CharacterMaxRune[character] = rune
		if GodMaxRune.get(god, 0) <= rune:
			GodMaxRune[god] = rune
	
	else:
		break


if GameCount == 0:
	print("\"{}\" is not a valid log file.".format(CrawlLogFile))
	print(usageline)
	exit(1)


def DurationConverter(dur):
	m, s = divmod(int(dur), 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	return "{}:{:0>2}:{:0>2}".format(d, h, m)


def IfNotZero(n):
	if n > 0:
		return n
	else:
		return ""


def GenerateGraph():
	#pips = "⎽⎼⎻⎺"
	#maxpip = "⎺"
	#pips = "▄▀"
	#maxpip = "▀"
	pips = "▪"
	maxpip = "▣"
	#pips = "-"
	#maxpip = "+"
	
	numgames = 56 # width
	if GameCount < numgames and GameCount >= 10:
		numgames = GameCount
	elif GameCount < 10:
		return 1
	
	height = 10
	TimeScoreList.sort(reverse=True)
	
	maxscore = 0
	minscore = max(ScoreList)
	# get local max and min
	for i in range(0, numgames):
		if TimeScoreList[i][1] > maxscore:
			maxscore = TimeScoreList[i][1]
		if TimeScoreList[i][1] < minscore:
			minscore = TimeScoreList[i][1]
	
	piprange = (maxscore - minscore) / (len(pips) * height)
	
	# create sparse graph matrix
	graph = []
	for i in range(0, height):
		sparse = []
		for j in range(0, numgames):
			sparse.append(" ")
		graph.append(sparse)
	
	for x in range(numgames - 1, -1, -1):
		sc = TimeScoreList[x][1]
		#print("{}\t{}\t{}\t{}".format(x, sc, 
			#round((TimeScoreList[x][1] - minscore) / piprange) // len(pips), 
			#round((TimeScoreList[x][1] - minscore) / piprange) % len(pips)))
		slot, pipid = divmod(round((sc - minscore) / piprange), len(pips))
		
		if slot >= height:
			slot = height - 1
			pipid = len(pips) - 1
		if sc == maxscore:
			graph[height - 1 - slot][numgames - 1 - x] = maxpip
		else:
			graph[height - 1 - slot][numgames - 1 - x] = pips[pipid]
	
	leftborder = 10
	print("Score distribution recent games:".upper())
	for y in range(0, height):
		if y == 0:
			print("{:>{w},} ┐".format(maxscore, w=leftborder), end='')
		elif y == height // 2:
			print("{:>{w}} │".format("Score", w=leftborder), end='')
		#elif y == height // 2:
			#print("{:>{w},} ┤".format((maxscore - minscore) // 2, w=leftborder), end='')
		elif y == height - 1:
			print("{:>{w},} ┤".format(minscore, w=leftborder), end='')
		else:
			print("{:{w}} │".format("", w=leftborder), end='')
			
		for x in range(0, numgames):
			print(graph[y][x], end='')
		
		if y == 0:
			print("╷")
		else:
			print("│")
	print("{:>{w}} └┬{:─^{w2}}┬┘".format("", " Games ", w=leftborder, w2=numgames-2))
	if numgames > 15:
		print("{:>{w}}  {:<16}{:^{w2}}{:>16}".format("", "└ {} games ago".format(numgames),"", "last game ┘", w=leftborder, w2=numgames-(leftborder*2)-12))
	
	return 0


def DicTopPos(dic, pos):
	if len(dic) <= pos:
		return ""
	else:
		a = sorted(dic, key=dic.get, reverse=True)[pos]
		ax = dic[a]
		width = len(str(dic[sorted(dic, key=dic.get, reverse=True)[0]]))
		return "{:>{w}} ✕ {}".format(ax, a, w = width)


def a(word):
	if word.startswith(("a", "A", "e", "E", "i", "I", "o", "O", "u", "U")):
		return "an"
	else:
		return "a"


def GenerateChallenge():
	if GameCount < 10 or len(SpeciesCount) < 6 or len(BackgroundCount) < 6 or max(XlList) < 6:
		return "Venture deeper into the dungeon."
	
	# same random output for any given day
	random.seed(str(datetime.date.today()))
	# for testing:
	#random.seed()
	
	# Compile a list with all spec/backgr/gods in the format "adjustedcore type name"
	ChallengeList = []
	for k in SpeciesCount:
		ChallengeList.append("{:0>10} species {}".format(SpeciesHighScore[k] // 2 + (SpeciesTotalScore[k] // SpeciesCount[k]), k))
	for k in BackgroundCount:
		ChallengeList.append("{:0>10} background {}".format(BackgroundHighScore[k] // 2 + (BackgroundTotalScore[k] // BackgroundCount[k]), k))
	for k in GodCount:
		if k != 'no god':
			ChallengeList.append("{:0>10} god {}".format(GodHighScore[k] // 2 + (GodTotalScore[k] // GodCount[k]), k))
	ChallengeList.sort()
	
	# pick an entry roughly from the middle 50%
	pick = ChallengeList[random.randint(len(ChallengeList) // 4, int(len(ChallengeList) // 1.3))].split(maxsplit=1)[1]
	part1_object = pick.split(maxsplit=1)[1]
	part1_object_type = pick.split(maxsplit=1)[0]
	
	if part1_object_type == "species":
		part1_action = "Embody {}".format(a(part1_object))
		part2_value_list = [SpeciesMaxXl[part1_object], SpeciesMaxTurn[part1_object], SpeciesMaxRune[part1_object]]
	elif part1_object_type == "background":
		part1_action = "Become {}".format(a(part1_object))
		part2_value_list = [BackgroundMaxXl[part1_object], BackgroundMaxTurn[part1_object], BackgroundMaxRune[part1_object]]
	elif part1_object_type == "god":
		part1_action = "Worship"
		part2_value_list = [GodMaxXl[part1_object], GodMaxTurn[part1_object], GodMaxRune[part1_object]]
	#print(part2_value_list, part1_object)
	
	# 0 = xl, 1 = turns, 2 = runes
	if len(RuneList) > 4 and part2_value_list[2] > 0:
		part2_object_type = random.randint(0, 2)
	else:
		part2_object_type = random.randint(0, 1)
	
	# 1-up the current max values
	if part2_object_type == 0:
		part2_action = "reach XL {}".format(part2_value_list[0] + 1)
	elif part2_object_type == 1:
		part2_action = "survive {:,} turns".format(int(round(part2_value_list[1] * 1.1, -3)))
	elif part2_object_type == 2:
		part2_action = "gather {} runes".format(part2_value_list[2] + 1)

	return "{} {} and {}.".format(part1_action, part1_object, part2_action)


# Output
print("Jiyva Jumbler {} - stats for Dungeon Crawl Stone Soup logs".format(ProgramVersion))
print("Log file: {} ({} games)".format(CrawlLogFile, GameCount))
print("")
print("{:15}{:>15}{:>15}{:>15}{:>15}".format("", "TOTAL", "HIGH", "AVERAGE", "MEDIAN"))
print("{:15}{:15,d}{:15,d}{:15,.0f}{:15,.0f}".format("Score", ScoreTotal, max(ScoreList), stats.mean(ScoreList), stats.median(ScoreList)))
print("{:15}{:15,d}{:15,d}{:15,.2f}{:15,.2f}".format("Runes", RuneTotal, max(RuneList), stats.mean(RuneList), stats.median(RuneList)))
print("{:15}{:15,d}{:15,d}{:15.1f}{:15.1f}".format("XL", XlTotal, max(XlList), stats.mean(XlList), stats.median(XlList)))
print("{:15}{:15,d}{:15,d}{:15.1f}{:15.1f}".format("Depth", DepthTotal, max(DepthList), stats.mean(DepthList), stats.median(DepthList)))
print("{:15}{:15,d}{:15,d}{:15,.0f}{:15,.0f}".format("Turns", TurnTotal, max(TurnList), stats.mean(TurnList), stats.median(TurnList)))
print("{:15}{:>15}{:>15}{:>15}{:>15}".format("Time (D:hh:mm)", DurationConverter(DurationTotal), DurationConverter(max(DurationList)), DurationConverter(stats.mean(DurationList)), DurationConverter(stats.median(DurationList))))
print()

# Format constants
# widths 19 5 16 12 12 15  = 79
w1 = 19 # name, "Earth Elementalist" is 18
w2 = 5  # games
w3 = 16 # total score
w4 = 12 # high score
w5 = 12 # avg score
w6 = 5  # hixl
w7 = 5  # hirunes
w8 = 5  # wins
headerformat = "{:{w1}}{:>{w2}}{:>{w3}}{:>{w4}}{:>{w5}}{:>{w6}}{:>{w7}}{:>{w8}}"
statsformat = "{:{w1}}{:{w2},d}{:{w3},d}{:{w4},d}{:{w5},.0f}{:{w6}}{:{w7}}"
headertitle = ["SPECIES", "BACKGROUND", "GOD", "CHARACTER"]
statlist = ([SpeciesCount, SpeciesTotalScore, SpeciesHighScore, SpeciesMaxXl, SpeciesMaxRune], 
	[BackgroundCount, BackgroundTotalScore, BackgroundHighScore, BackgroundMaxXl, BackgroundMaxRune], 
	[GodCount, GodTotalScore, GodHighScore, GodMaxXl, GodMaxRune], 
	[CharacterCount, CharacterTotalScore, CharacterHighScore, CharacterMaxXl, CharacterMaxRune])

# Stat Loop
for i in range(0, 4):
	print(headerformat.format(headertitle[i], "GAMES", "TOTAL SCORE", 
		"HIGH SCORE", "AVG SCORE", 
		"HiXL", "HiRU", "WINS", 
		w1=w1,w2=w2,w3=w3,w4=w4,w5=w5,w6=w6,w7=w7,w8=w8))
	loop = 0
	for key in sorted(statlist[i][0], key=statlist[i][0].get, reverse=True):
		if statlist[i][0][key] >= MinGames or loop < MinDisplay:
			print(statsformat.format(key, statlist[i][0][key], statlist[i][1][key], 
				statlist[i][2][key], statlist[i][1][key] / statlist[i][0][key], 
				statlist[i][3][key], IfNotZero(statlist[i][4][key]), 
				w1=w1,w2=w2,w3=w3,w4=w4,w5=w5,w6=w6,w7=w7,w8=w8))
			loop += 1
	print()

print("{:{w}}{:{w}}".format("PLACES OF DEATH", "PLAYER KILLERS", w=26))
for i in range(0, 5):
	print("{:{w}}{:{w}}".format(DicTopPos(PlaceCount, i), DicTopPos(KillerCount, i), w=26))
print()

if ShowGraph is True:
	print()
	GenerateGraph()
	print("\n")

print("Challenge of the day: {}".format(GenerateChallenge()))
print()
