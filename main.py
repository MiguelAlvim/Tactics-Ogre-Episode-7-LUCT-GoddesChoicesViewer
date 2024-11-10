from parse import Oferings,Actions,Order as Stats
from choicesResults import ChoicesResults
import FreeSimpleGUI as g

#Initalization
#Left
layoutLeft = [[g.Push(),g.Text("Inquisition Answers"),g.Push()]]

Goddeses = ["Hahnela","Zoshonell","Bartha","Gurza"]
GoddesesColors = {"Hahnela":'yellow',"Zoshonell":'#db272a',"Bartha":'lightgreen',"Gurza":'blue'}
layoutLeft.append(
	[
		g.Text("\t"),
  		g.Text(Goddeses[0]+"\t",key="_"+Goddeses[0],text_color='red'),
		g.Text(Goddeses[1]+"\t",key="_"+Goddeses[1],text_color='red'), 
		g.Text(Goddeses[2]+"\t",key="_"+Goddeses[2],text_color='red'),
		g.Text(Goddeses[3]+"\t",key="_"+Goddeses[3],text_color='red')
	]
)

ActionsPlus = Actions
ActionsPlus.append("----")
ComboLines = {}
for offer in Oferings:
	line = [g.Text(offer+"\t",key=offer+"_text",text_color='red')]
	ComboLines[offer] = []
	for goddes in Goddeses:
		line.append(g.Combo(
			ActionsPlus,
			default_value="----", 
			key =offer+"_"+goddes, 
			enable_events = True
			)
		)
		ComboLines[offer].append(offer+"_"+goddes)
	layoutLeft.append(line)

layoutLeft.append([g.HorizontalSeparator()])
layoutLeft.append([g.Push(),g.Text("Expected Initial Values"),g.Push()])
layoutLeft.append([g.Text("\t"),g.Text("Initial"+"\t"),g.Text("Modifier"+"\t"),g.Text("Final")])
BaseStats = {"HP":68,"MP":4,"STR":27,"VIT":25,"INT":26,"MEN":24,"AGI":20,"DEX":26}
for stat in Stats:
	layoutLeft.append([g.Text(stat+"\t"),g.Text(str(BaseStats[stat])+"\t"),g.Text("0"+"\t",key=stat+"_modifier"),g.Text(str(BaseStats[stat]),key=stat+"_final")])

#Right
layoutRight = [[g.Push(),g.Text("Inquisition Values"),g.Push()]]
StatsPlus = Stats
StatsPlus.insert(0,"Answer")
for goddes in Goddeses:
	layoutRight.append([g.Push(),g.Text(goddes,text_color=GoddesesColors[goddes]),g.Push()])
	tableValues = []
	for entry in ChoicesResults[goddes]:
		for offer in ChoicesResults[goddes][entry]:
			line = []
			line.append(entry+"|"+offer)
			for stat in ChoicesResults[goddes][entry][offer]:			
				line.append(ChoicesResults[goddes][entry][offer][stat])
			tableValues.append(line)
		
	table = g.Table(values=tableValues,
					headings=[stat for stat in StatsPlus],
					auto_size_columns=True,
					display_row_numbers=False,
					expand_y=True,
					expand_x=True,
					justification='center')
	layoutRight.append([table])

window = g.Window("Inquisition Checker",[[g.Column(layoutLeft,vertical_alignment='top'),g.VerticalSeparator(),g.Column(layoutRight)]])

#Integrity Check
def validateLines(windowValues):
	InvalidLines = []
	#Validating Lines
	for line in ComboLines:
		totalAnswers = 0
		for entry in ComboLines[line]:
			if windowValues[entry] != '----':
				totalAnswers = totalAnswers + 1
		#if the line is invalid
		if(totalAnswers != 1):
			InvalidLines.append((line+"_text",True))
		else:
			InvalidLines.append((line+"_text",False))
	return InvalidLines

def validateAnswers(windowValues):
	#You can only pray, offer and vow once per Goddess
	invalidGoddesses = []
	for goddes in Goddeses:
		hasPray = False
		hasVow = False
		hasOffer = False
		isRepeated = False
		for offer in Oferings:
			value = windowValues[offer+"_"+goddes]
			if value == "Pray":
				if not hasPray:
					hasPray = True
				else:
					isRepeated = True
					break
			if value == "Vow":
				if not hasVow:
					hasVow = True
				else:
					isRepeated = True
					break
			if value == "Offer":
				if not hasOffer:
					hasOffer = True
				else:
					isRepeated = True
					break
		if(isRepeated or not hasPray or not hasVow or not hasOffer):
			invalidGoddesses.append(("_"+goddes,True))
		else:
			invalidGoddesses.append(("_"+goddes,False))
		
	return invalidGoddesses
		
	
#updating expected Denim Modifiers and Final stats
def calculateValues(windowValues):
	hpModifier = 0
	mpModifier = 0
	strModifier = 0
	vitModifier = 0
	intModifier = 0
	menModifier = 0
	agiModifier = 0
	dexModifier = 0
	for line in ComboLines:
		for entry in ComboLines[line]:
			choice = windowValues[entry]
			if(choice!="----"):
				split = entry.split('_')
				values = ChoicesResults[split[1]][split[0]][choice]
				hpModifier = hpModifier + values["HP"]
				mpModifier = mpModifier + values["MP"]
				strModifier = strModifier + values["STR"]
				vitModifier = vitModifier + values["VIT"]
				intModifier = intModifier + values["INT"]
				menModifier = menModifier + values["MEN"]
				agiModifier = agiModifier + values["AGI"]
				dexModifier = dexModifier + values["DEX"]
	#Updating the texts
	return [
		("HP_modifier",hpModifier),
		("HP_final",BaseStats['HP']+hpModifier),
		("MP_modifier",mpModifier),
		("MP_final",BaseStats['MP']+mpModifier),
		("STR_modifier",strModifier),
		("STR_final",BaseStats['STR']+strModifier),
		("VIT_modifier",vitModifier),
		("VIT_final",BaseStats['VIT']+vitModifier),
		("INT_modifier",intModifier),
		("INT_final",BaseStats['INT']+intModifier),
		("MEN_modifier",menModifier),
		("MEN_final",BaseStats['MEN']+menModifier),
		("AGI_modifier",agiModifier),
		("AGI_final",BaseStats['AGI']+agiModifier),
		("DEX_modifier",dexModifier),
		("DEX_final",BaseStats['DEX']+dexModifier),
	]

#Window And Event Handling
while True:
	event, values = window.read()
	if event == g.WIN_CLOSED or event == "Cancel":
		break
	#updating visuals
	invalidLines = validateLines(values)
	for line in invalidLines:
		if(line[1]):
			window[line[0]].update(text_color='red')
		else:
			window[line[0]].update(text_color='white')
	invalidGoddesses = validateAnswers(values)
	for goddes in invalidGoddesses:
		if(goddes[1]):
			window[goddes[0]].update(text_color='red')
		else:
			window[goddes[0]].update(text_color='white')
	newValues = calculateValues(values)
	for values in newValues:
		window[values[0]].update(str(values[1])+"\t")
		

window.close()