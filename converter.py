try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
import sys
import os.path

n = len(sys.argv)
if(n < 2):
  print("Usage: python3 converter.py [fileName.xml]")
  quit()

fileName = sys.argv[1]
if(fileName[-4:] != ".xml"):
  print("[!] Error: Wrong File Format.")
  print("[!] File: "+fileName)
  quit()
  
if(os.path.exists(fileName) == False):
  print("[!] Error: File Does Not Exist.")
  print("[!] File: "+fileName)
  quit()
  
index = fileName.find(".xml")
outputFileName = fileName[0:index] + ".ann"
  
tree = ET.ElementTree(file=fileName)
root = tree.getroot()
docu = root.find('document')
sentences = docu.find('sentences').findall('sentence')
output  = open(outputFileName, 'w')
rtypecount = 1
spanlist=[]
relationList=[]
visualListInitial=[]
visualListFinal=[]
visual = {}
for sentence in sentences:
	sentenceID = str(sentence.get('id'))
		 
	# Parse POS
	tokens = sentence.find('tokens').findall('token')
	for t in tokens:	
		tid = 'T'+ sentenceID + str(t.get('id'))
		pos = str(t.find('POS').text)
		sidx = str(t.find('CharacterOffsetBegin').text)
		eidx = str(t.find('CharacterOffsetEnd').text)
		word = str(t.find('word').text)
		if ":" in pos:
			if pos not in visualListInitial:
				visualListInitial.append(pos)
				pos = pos.replace(":", "_")
				visualListFinal.append(pos)
			else:
				pos = pos.replace(":", "_")
		if "." in pos:
				if pos not in visualListInitial:
					visualListInitial.append(pos)
					pos = pos.replace(".", "_dot")
					visualListFinal.append(pos)
				else:
					pos = pos.replace(".", "_dot")
		if "," in pos:
			if pos not in visualListInitial:
				visualListInitial.append(pos)
				pos = pos.replace(",", "_comma")
				visualListFinal.append(pos)
			else:
				pos = pos.replace(",", "_comma")
		if "$" in pos:
			if pos not in visualListInitial:
				visualListInitial.append(pos)
				pos = pos.replace("$", "_dollar")
				visualListFinal.append(pos)
			else:
				pos = pos.replace("$", "_dollar")
		if pos not in spanlist:
			spanlist.append(pos)
		output.write(tid+'\t'+pos+' '+sidx+' '+eidx+'\t'+word+'\n')
  
  # Parse enhanced plus plus relation
	targetDep = 0
	for dependency in sentence.findall('dependencies'):
		if dependency.get('type') == 'enhanced-plus-plus-dependencies':
			targetDep = dependency
			break
	for d in targetDep:
		rword = str(d.get('type'))
		if(rword != "root"):
			if ":" in rword:
				if rword not in visualListInitial:
					visualListInitial.append(rword)
					rword = rword.replace(":", "_")
					visualListFinal.append(rword)
				else:
					rword = rword.replace(":", "_")
			if "." in rword:
					if rword not in visualListInitial:
						visualListInitial.append(rword)
						rword = rword.replace(".", "_")
						visualListFinal.append(rword)
					else:
						rword = rword.replace(".", "_")
			if "," in rword:
				if rword not in visualListInitial:
					visualListInitial.append(rword)
					rword = rword.replace(",", "_")
					visualListFinal.append(rword)
				else:
					rword = rword.replace(",", "_")
			rid = 'R'+str(rtypecount)
			rtypecount+=1
			if rword not in relationList:
				relationList.append(rword)

			govidx = d.find('governor').get('idx')
			gov = 'T'+sentenceID+str(govidx)
			dpdidx = d.find('dependent').get('idx')
			dpd = 'T'+sentenceID+str(dpdidx)
			output.write(rid+'\t'+rword+' Arg1:'+gov+' Arg2:'+dpd+'\n')
output.close()

conf = open('annotation.conf', 'w')
conf.write('[entities]\n')
for sp in spanlist:
	conf.write(sp+'\n')
conf.write('\n[relations]\n')
for rl in relationList:
	conf.write(rl+'\t'+'Arg1:<ENTITY>,'+'\t'+' Arg2:<ENTITY>\n')
conf.close()

conf = open('visual.conf', 'w')
conf.write('[labels]\n')
for i in range(len(visualListInitial)):
  conf.write(visualListFinal[i]+" | "+ visualListInitial[i]+"\n")
conf.write('[drawing]\n')
conf.write('SPAN_DEFAULT	fgColor:black, bgColor:lightgreen, borderColor:darken\n')
conf.write('ARC_DEFAULT	color:black, dashArray:-, arrowHead:triangle-5, labelArrow:none\n')
conf.close()
