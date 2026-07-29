#!/usr/bin/env python

# Created by: Moksh Chitkara
# Last Update: Jul 29th 2026
# v0.4.0
# Copyright (C) 2026  Moksh Chitkara
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime

# Global Variables
projectManager = resolve.GetProjectManager()
heroProject = projectManager.GetCurrentProject()
pathqueue = None
toqueue = None

def main_ui():

	# vertical group
	window = [ui.VGroup({"Spacing": 10}, [
				# Hero Timeline
				ui.HGroup({"Spacing": 1, "Weight": 0}, [
					ui.Label({"ID": "name_label","Text": "Powergrade name: ", "Weight": 0}),
					ui.LineEdit({"ID": "gradename", "Text": f"GradeGrab-{datetime.datetime.now():%m%d}-%02d-%02d-%02d" % (datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second), "Weight": 2}),
					ui.HGap(),
					ui.Label({"ID": "tl_label","Text": "Please select hero timeline: ", "Weight": 0}),
					ui.ComboBox({"ID": "timelines", "Weight": 2})
				]),
				# Checkboxes
				ui.HGroup({"Spacing": 0, "Weight": 0}, [
					ui.CheckBox({"ID": "case_check","Text": "Ignore capitalization", "Checked": False, "Weight": 1}),
					ui.CheckBox({"ID": "tc_check","Text": "Label stills with timecode", "Checked": True, "Weight": 1}),
					ui.CheckBox({"ID": "version_check","Text": "Ignore version number", "Checked": False, "Weight": 1}),
				]),
				
				# Two boxes
				ui.HGroup({"Spacing": 10}, [
					ui.VGroup({"Spacing": 10}, [
						ui.TextEdit({ "ID": "list","Text": 
"""
Projects to search will be listed here.

**Please ENABLE dynamic project switching** 
"""
									, "Weight": 20}),
						ui.HGroup({"Spacing": 10},[
							ui.HGap(),
							ui.Button({"ID": "grab","Text": "Grab Grades", "Enabled": False, "Weight": 1}),
							ui.Button({"ID": "clear","Text": "Clear", "Enabled": False, "Weight": 1}),
							ui.HGap(),
						]),
					]),
					ui.VGroup({"Spacing": 10}, [
						ui.Tree({"ID": "browser", 'SortingEnabled': True, 'AlternatingRowColors': True, 'SelectionMode': 'ExtendedSelection',
								'Events': {'ItemDoubleClicked': True, 'ItemClicked': True}, "Weight": 20}),
						ui.HGroup({"Spacing": 10},[
							ui.HGap(),
							ui.Button({"ID": "add","Text": "Add Selected", "Weight": 1}),
							ui.HGap(),
						]),
					]),
				]),
			])]

	return window

################################################################################################
# Window creation #
###################

ui = fu.UIManager # get UI utility from fusion
disp = bmd.UIDispatcher(ui) # gets display settings?

# window definition
window = disp.AddWindow({"WindowTitle": "Moksh's Grade Graber",
			"ID": "GGWin", 
			'WindowFlags': {'Window': True,'WindowStaysOnTopHint': True},
			"Geometry": [1000,300,1150,800], # x-position, y-position, width, height
			}, 
			main_ui())


itm = window.GetItems() # Grabs all UI elements to be manipulated

################################################################################################
# Functions #
#############

class PathList:

	def __init__(self, pathlist):
		log("PathList initialized")
		self.list = pathlist
		
	def __iter__(self):
		return iter(self.list)
		
	def __len__(self):
		return len(self.list)
		
	def __str__(self):
		self.sort()
		returnable = str(self.list[0])
		for pathmem in self.list[1:]:
			returnable = returnable + "\n" + str(pathmem)
		return returnable
		
	def strikestr(self):
		self.sort()
		returnable = (self.list[0]).strikestr()
		for pathmem in self.list[1:]:
			returnable = returnable + "\n" + pathmem.strikestr()
		return returnable
	
	def sort(self):
		self.list.sort(key=str)
	
	def append(self, newItm):
		if newItm == None:
			log("PathList cannot append None Type", 3)
			
		elif self.iscopy(newItm):
			log("PathList cannot append Duplicates", 3)
			
		else:
			self.list.append(newItm)
	
	def combine(self, newLst):
		if newLst == None:
			log("PathList cannot append None Type", 3)
		else:
			seen = {}
			for item in self.list:
				key = str(item)
				if key not in seen:
					seen[key] = item
			for item in newLst:
				key = str(item)
				if key not in seen:
					seen[key] = item
			self.list = list(seen.values())
		
	def pop(self, idx):
		return self.list.pop(idx)
		
	def undo(self):
		latest = self.pop(-1)
		latest.pop(-1)
		self.append(latest)
		
	def update(self, new):
		latest = self.pop(-1)
		latest.append(new)
		self.append(latest)

class PathMem:
	
	# all this class needs is a timeline item
	def __init__(self, initial):
		log("PathMem initialized")
		self.initial = initial
		self.path = [initial]
		self.tl = None
		self.searched = False

	def __str__(self):
		if len(self.path) > 1:
			return ' > '.join(self.path) 
		else:
			return str(self.path[0])
		
	def strikestr(self):
		if len(self.path) > 1:
			if self.searched:
				return strike(' > '.join(self.path))
			else:
				return ' > '.join(self.path) 
		else:
			return str(self.path[0])
			
	def __iter__(self):
		return self.path
			
	def append(self, newItm, tl = None):
		if newItm == None:
			log("PathMem cannot append None Type", 3)
			
		elif self.tl != None:
			log("PathMem is complete to timeline", 3)
			
		else:
			self.path.append(newItm)
			self.tl = tl
			return True
			
		return False

	def pop(self, idx):
		if self.tl:
			self.tl = None
			return self.path.pop(idx)
		else:
			return self.path.pop(idx)
		
	def resest(self):
		self.tl = None
		self.path = []


	def multiply(self, kids):
		pathlist = []
		for kid in kids:
			newpath = PathMem(self.initial)
			newpath.path = newpath.path + self.path[1:]
			newpath.append(kid, kids[kid])
			pathlist.append(newpath)
		return pathlist

	def open(self):
		log("Following folder path " + str(self))
		projectManager.GotoRootFolder() # Goes to root in project manager 

		i = 0
		for folder in self.path:
			if not projectManager.OpenFolder(folder):
				log("Path followed to " + folder)
				break
			i += 1

		if projectManager.LoadProject(self.path[i]):
			log("Opened project " + self.path[i])
			current = projectManager.GetCurrentProject()
			if current.SetCurrentTimeline(tlReturn(current, self.path[i+1])):
				log("Opened timeline " + self.path[i+1])
		else:
			return False
		return True
			
		

class Clip:

	# all this class needs is a timeline item
	def __init__(self, tl_item):
		self.item = tl_item
		self.media = self.getMedia()
		self.isMedia = self.isMedia()
		
	def __str__(self):
		return "Clip Item [" + str(self.filename()) + "]"

	# confirms self is in the mediapool and not a redx or 2pop
	# input: none
	# output: Bool
	def isMedia(self):
		if self.media == None:
			return False
		elif self.media.GetClipProperty('File Name') == "RedX_1min_alpha.mov":
			return False
		elif self.media.GetClipProperty('File Name') == "2pop_uhd.tif":
			return False
		else:
			return True
			
	def getMedia(self):
		return self.item.GetMediaPoolItem()

	# returns fps of self
	# input: none
	# output: float
	def fps(self):
		if self.isMedia:
			numb = float(self.media.GetClipProperty('FPS'))
		else:
			numb = float(23.976)
		return numb
	
	# determines if media has df
	# input: none
	# output: Bool
	def dropframe(self):
		drop = self.media.GetClipProperty('Drop frame')
		if drop == "0":
			return False
		else:
			return True

	# shortcut to get timeline frame number of start and end
	# input: none
	# output: int
	def tlStartFrame(self):
		return int(self.item.GetStart())
	def tlEndFrame(self):
		return int(self.item.GetEnd())
		
	# gets start frame of media in mediapool
	# input: none
	# output: int
	def mediaStartFrame(self):

		tc = self.media.GetClipProperty('Start TC')	# this is in ##:##:##:## format
		
		# check to see if framerate is matching
		if int(tc[9:]) > self.fps():
			raise ValueError ('Timecode to frame rate mismatch.', tc, self.fps)
			
		# convert all strings to ints
		hours = int(tc[:2])
		minutes = int(tc[3:5])
		seconds = int(tc[6:8])
		frames = int(tc[9:])
		
		totalMinutes = int(60 * hours + minutes)	# convert hours to mins and sum
		
		# Drop Frame Calc
		if self.dropframe():
			
			dropFrames = int(round(self.fps() * 0.066666))
			timeBase = int(round(self.fps()))
			
			hourFrames = int(timeBase * 60 * 60)
			minuteFrames = int(timeBase * 60)
			
			frm = int(((hourFrames * hours) + (minuteFrames * minutes) + (timeBase * seconds) + frames) - (dropFrames * (totalMinutes - (totalMinutes // 10))))
		
		# non df calc
		else:
			frameBase = int(round(self.fps()))
			frm = int((totalMinutes * 60 + seconds) * frameBase + frames)
			
		return frm
		
	# Shortcuts to get mediapool endframe, effective startframe, and effective endframe
	# where an effective endframe is the in-out points of media on timeline but as source frame numbers
	# input: none
	# output: int
	def mediaEndFrame(self):
		return self.startFrame() + int(self.media.GetClipProperty('Frames'))
	def startFrame(self):
		return self.mediaStartFrame() + int(self.item.GetLeftOffset())
	def endFrame(self):
		handles = int(self.item.GetEnd()) - int(self.item.GetStart()) - int(self.item.GetRightOffset())
		return self.mediaEndFrame() + handles
			
	# shortcut to get filename of self
	# input: none
	# output: str or None
	def filename(self):
		if self.isMedia:
			return self.media.GetClipProperty('File Name')
		else:
			return None

	def remove_version(self):
	
		name = self.filename()
		upper_name = name.upper()				# uppercase it
		ver_idx = upper_name.rfind("_V")		# find version tag
		
		if ver_idx != -1:						# if we found a version, cut it off and return 
			if (ver_idx + 2 < len(upper_name)) and (upper_name[ver_idx + 2].isdigit()):
				return name[:ver_idx + 2]
		return name								# otherwise return original

	# Checks if self and search have the same file name
	# input: search [another Clip]
	# output: Bool
	def fileMatch(self, search):

		if (not self.isMedia) or (not search.isMedia):	# checks both are media
			return False
			
		# now we get the file name taking version ignore into account
		if itm['version_check'].Checked:
			search_str = search.remove_version()
			item_str = self.remove_version()
		else:
			search_str = search.filename()
			item_str = self.filename()

		# if case_check is checked then make both uppercase
		if itm['case_check'].Checked:
			search_str = search_str.upper()
			item_str = item_str.upper()

		if item_str == search_str:	# if they are exact match return true
			return True

		for i in range(len(search_str), 16, -1):	# reading filename backwards to min length 16 see if they match
			if (item_str.find(search_str[:i]) == 0):
				return True
				
		return False	# if nothing else return false
	
	# checks if search clip is overlapping with self
	# by checking if either end of search is within self
	# input: search [another Clip]
	# output: Bool, Frame
	def isInside(self, search):
		
		if self.fileMatch(search):	# they must have matching filenames for this
			if search.startFrame() in range(self.startFrame(), self.endFrame(), 1):	
				return True, search.startFrame()
			elif self.startFrame() in range(search.startFrame(), search.endFrame(), 1):	
				return True, self.startFrame()
			elif search.endFrame() in range(self.startFrame(), self.endFrame(), 1):
				return True, search.endFrame()
			elif self.endFrame() in range(search.startFrame(), search.endFrame(), 1):
				return True, self.endFrame()
		return False, 0
	
	# Finds timeline frame number matching with match clip's start
	# input: match [another Clip]
	# output: tl frame [int] or False [if no match]
	def frameMatch(self, match):
		found, frame = self.isInside(match)
		if found:	# confirms that match is inside self
			return self.tlStartFrame() + (frame - self.startFrame())
		else:
			return False


def log(info, level = 1):

	if level == 1:
		level = "INFO"
	elif level == 2:
		level = "WARN"
	else:
		level = "EROR"
	
	time = datetime.datetime.now()
	
	fullLog = [str(time), level, info]
	print(" | ".join(fullLog))	

# strike through text provided and return
# input: text [string]
# output: result [string]
def strike(text):
	#result = text[0] + "\u0336"
	result = ""
	for c in text:
		result += c + "\u0336"
	#return result[1:]
	return result

# creates sorted list of all timelines in project
# input: project [item]
# output: tl_lst [list]
def tlLst(project):
	
	tl_lst = [] # placeholder will be filled
	current_tl = project.GetCurrentTimeline().GetName()
	# gets every tl name in project and appends to lst
	for i in range(1, project.GetTimelineCount()+1):
		name = project.GetTimelineByIndex(i).GetName()	
		if current_tl != name:
			tl_lst.append(name)

	tl_lst = sorted(tl_lst)
	tl_lst.insert(0, current_tl)

	return tl_lst # return the list
	
def projTree():

	log("Building Project Tree")

	global state
	state = "project"

	itm["add"].Enabled = False
	itm["browser"].Clear()
	
	header = itm["browser"].NewItem()
	header.Text[0] = "Projects"
	itm["browser"].SetHeaderItem(header)
	itm["browser"].ColumnCount = 1
	itm["browser"].ColumnWidth[0] = 300
	
	folderLst = projectManager.GetFolderListInCurrentFolder()
	projLst = projectManager.GetProjectListInCurrentFolder()
	
	for proj in sorted(projLst + folderLst):
		newRow = itm["browser"].NewItem()
		newRow.Text[0] = str(proj)
		itm["browser"].AddTopLevelItem(newRow)
	
	itm["browser"].SortByColumn(0, "AscendingOrder")
	
	newRow = itm["browser"].NewItem()
	newRow.Text[0] = " * GO TO PARENT FOLDER * "
	itm["browser"].AddTopLevelItem(newRow)
	
	log("Project Tree Built")
	
def tlTree(project):

	log("Building Timeline Tree")

	global state
	state = "timeline"

	itm["add"].Enabled = True
	itm["browser"].Clear()
	
	header = itm["browser"].NewItem()
	header.Text[0] = "Projects"
	itm["browser"].SetHeaderItem(header)
	itm["browser"].ColumnCount = 1
	itm["browser"].ColumnWidth[0] = 300
	
	for tl in tlLst(project):
		newRow = itm["browser"].NewItem()
		newRow.Text[0] = tl
		itm["browser"].AddTopLevelItem(newRow)
	
	itm["browser"].SortByColumn(0, "AscendingOrder")
	
	newRow = itm["browser"].NewItem()
	newRow.Text[0] = " * GO TO PARENT FOLDER * "
	itm["browser"].AddTopLevelItem(newRow)
	
	log("Timeline Tree Built")
			
# gets timeline item based on name
# input: project [item], tl_name [str]
# output: tl [Timeline Item]
def tlReturn(project, tlName):
	for i in range(1,project.GetTimelineCount()+1):
		name = project.GetTimelineByIndex(i).GetName()
		if name == tlName:
			return project.GetTimelineByIndex(i)

# fill lst with all clips in given timeline
# input: tl [item]
# output: clip_lst [lst of items]
def clipReturn(tl):
	clip_lst = [] # list to be filled
	# for every video track get every clip and add to list
	for i in range(1, tl.GetTrackCount("video")+1):
		for clipItem in tl.GetItemListInTrack("video",i):
			clip = Clip(clipItem)
			if clip.isMedia:
				clip_lst.append(clip)
	return clip_lst

def createPowergrade():
	if itm["gradename"].Text == "":
		albumName = f"GradeGrab-{datetime.datetime.now():%m%d}-%02d-%02d-%02d" % (datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second)
	else:
		albumName = itm["gradename"].Text
	
	project = projectManager.GetCurrentProject()
	gallery = project.GetGallery()
	galleryStillAlbum = gallery.CreateGalleryPowerGradeAlbum()
	if gallery.SetAlbumName(galleryStillAlbum, albumName):
		log("Powergrade album created")
		return galleryStillAlbum
	else:
		log("Powergrade album creation failed", 3)
		return False

# Converts frame count to SMPTE timecode.
# input: frame [int], timeline
# output: timecode in format "##:##:##:##"
def get_tc(frames, timeline):
		frames = abs(frames)
		fps = float(timeline.GetSetting("timelineFrameRate"))
		df = bool(int(timeline.GetSetting("timelineDropFrameTimecode")))

		# Drop frame calculation using the Duncan/Heidelberger method.
		if df:

			spacer = ':'
			spacer2 = ';'

			dropFrames         = int(round(fps * .066666))
			framesPerHour      = int(round(fps * 3600))
			framesPer24Hours   = framesPerHour * 24
			framesPer10Minutes = int(round(fps * 600))
			framesPerMinute    = int(round(fps) * 60 - dropFrames)

			frames = frames % framesPer24Hours

			d = frames // framesPer10Minutes
			m = frames % framesPer10Minutes

			if m > dropFrames:
				frames = frames + (dropFrames * 9 * d) + dropFrames * ((m - dropFrames) // framesPerMinute)

			else:
				frames = frames + dropFrames * 9 * d

			frRound = int(round(fps))
			hr = int(frames // frRound // 60 // 60)
			mn = int((frames // frRound // 60) % 60)
			sc = int((frames // frRound) % 60)
			fr = int(frames % frRound)

		# Non drop frame calculation.
		else:

			fps = int(round(fps))
			spacer  = ':'
			spacer2 = spacer

			frHour = fps * 3600
			frMin  = fps * 60

			hr = int(frames // frHour)
			mn = int((frames - hr * frHour) // frMin)
			sc = int((frames - hr * frHour - mn * frMin) // fps)
			fr = int(round(frames -  hr * frHour - mn * frMin - sc * fps))

		# Return SMPTE timecode string.
		return(
				str(hr).zfill(2) + spacer +
				str(mn).zfill(2) + spacer +
				str(sc).zfill(2) + spacer2 +
				str(fr).zfill(2)
				)

# grabs stills to given album
# input: grabFrame [int], tl [timeline item], heroFrame [int], stillAlbum [gallery still album]
# output: none
def grabStill(grabFrame, tl, heroFrame, stillAlbum):

	tl_tc = get_tc(grabFrame, tl)

	# set current timecode in while loop cause it doesn't work sometimes	
	while tl.GetCurrentTimecode() != tl_tc:
		tl.SetCurrentTimecode(tl_tc)

	if resolve.GetCurrentPage() != "color":
		log("Moved to color page")
		resolve.OpenPage("color")
	
	still = tl.GrabStill()		# grabs still
	heroTC = get_tc(heroFrame, tl)
	if itm['tc_check'].Checked:
		stillAlbum.SetLabel(still, heroTC)
		
# gets list of all TCs where clips are found in given timeline
# input: heroClips [lst of clip classed items], album [powergrade album]
# output: grabs stills
def gradeGrab(heroClips, album):

	# placeholders
	tcs = []
	mediaIds = []

	for path in pathqueue:
		if path.searched:
			continue
		path.open()
		project = projectManager.GetCurrentProject()
		gallery = project.GetGallery()																								# for every queued path
		tl = path.tl
		
		for i in range(1, tl.GetTrackCount("video")+1):																				# for every video track
			trackLabel = "V" + str(i)
			trackItems = tl.GetItemListInTrack("video",i)
			loadingCounter = 0
			loadingTotal = len(trackItems)
			for searchClipItem in trackItems:																						# and item in that track
				loadingCounter += 1
				loadingLabel = "{:.2%}".format(float(loadingCounter)/float(loadingTotal))
				itm["list"].Text = trackLabel + ": " + loadingLabel + "\n\n" + pathqueue.strikestr()
				searchClip = Clip(searchClipItem)																					# make it into class
				if searchClip.isMedia and (searchClip.getMedia().GetMediaId() not in mediaIds):										# if it hasn't been hit
					currentId = searchClip.getMedia().GetMediaId()																	# get the id
					for hero in heroClips:																							# compare to every recap clip
						grabTC = searchClip.frameMatch(hero) 																		# get the matching timeline timecode
						if (grabTC != False) and (grabTC not in tcs):																# confirm it is a hit

							gallery.SetCurrentStillAlbum(album)
							grabStill(grabTC, tl, hero.tlStartFrame(), album)														# grab a still
							
							mediaIds.append(currentId)																				# add to hit list, and do it again
							for f in range(searchClip.tlStartFrame(), searchClip.tlEndFrame(), 1): 
								tcs.append(f)

		path.searched = True
		itm["list"].Text = "\n\n" + pathqueue.strikestr()

def _add(ev):

	log("Adding selected timelines to Queue")

	itm["grab"].Enabled = True
	itm["clear"].Enabled = True

	selected = itm["browser"].SelectedItems()
	
	if len(selected) < 1:
		return
	project = projectManager.GetCurrentProject()
	tlDict = {}
	
	for key in selected:
		item = selected[key].Text[0]
		tlDict[item] = tlReturn(project, item)
	
	pathlist = toqueue.multiply(tlDict)
	
	global pathqueue
	if pathqueue == None:
		pathqueue = PathList(pathlist)
	else:
		pathqueue.combine(pathlist)
		
	itm["list"].Text = str(pathqueue)

	log("Queue Updated")

def _clear(ev):

	log("Clearing Queue")

	global pathqueue
	pathqueue = None

	itm["list"].Text = "Projects to search will be listed here.\n\n**Please ENABLE dynamic project switching**"
	itm["grab"].Enabled = False
	itm["clear"].Enabled = False

def _tree(ev):
	
	global toqueue
	selected = itm["browser"].SelectedItems()
	
	for key in selected:
		folder = selected[key].Text[0]

	if selected == {}:
		toqueue.reset()
		projectManager.GotoRootFolder() # Goes to root in project manager 
		projTree()

	elif str(folder) == " * GO TO PARENT FOLDER * ":
		if state == "project":
			projectManager.GotoParentFolder()
		toqueue.pop(-1)
		projTree()
	
	elif projectManager.OpenFolder(str(folder)):	# opens folder if it is selected
		if toqueue == None:
			toqueue = PathMem(str(folder))
		else:
			toqueue.append(str(folder))
		projTree()
		
	elif projectManager.LoadProject(str(folder)):
		toqueue.append(str(folder))
		project = projectManager.GetCurrentProject()
		tlTree(project)
	
	else:
		log("Unknown input", 3)
		

def _main(ev):
	itm["add"].Enabled = False
	itm["grab"].Enabled = False
	itm["clear"].Enabled = False

	album = createPowergrade()	# create powergrade albume
	heroClips = clipReturn(tlReturn(heroProject, itm["timelines"].CurrentText))
	gradeGrab(heroClips, album)
	
	log("Grade Grab Completed")
	
	itm["add"].Enabled = True
	itm["grab"].Enabled = True
	itm["clear"].Enabled = True

# needed to close window
def _close(ev):
	disp.ExitLoop()

################################################################################################
# GUI Elements #
# manipulations
itm["timelines"].AddItems(tlLst(heroProject))
projectManager.GotoRootFolder()
projTree()
# button presses
window.On.GGWin.Close = _close
window.On.browser.ItemDoubleClicked = _tree
window.On.grab.Clicked = _main
window.On.clear.Clicked = _clear
window.On.add.Clicked = _add
# window loops
window.Show()
disp.RunLoop()
window.Hide()
#################################################################################################
