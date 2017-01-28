import os
NUM_OF_FIELDS = 27

#create list of file names
filelist = []
for (dirpath, dirnames, filenames) in os.walk("."):
	filelist.extend(filenames)
	break

#create and open for writing spss-syntax file	
writef = open('result.sps','w')

#write in syntax-file begining of the syntax from separate file
with open('begin.txt') as f:
	content = f.readlines()
	for line in content:
		writef.write(line)

#write all lines with data from small syntax files to the whole one		
for (filename) in filelist:
	if '.sps' in filename:
	#loop should skip the result syntax file itself
		if 'result.sps' in filename:
			continue
		with open(filename) as f:
			content = f.readlines()
		output = False
		fields = NUM_OF_FIELDS
		#data is situated between lines with this names
		for line in content:
			if "BEGIN DATA" in line:
				output = True
				continue
			if "END DATA." in line:
				output = False
			#other lines script should skip
			if not output:
				continue
			if (fields == NUM_OF_FIELDS):
				writef.write(filename+";")
			writef.write(line)
			fields -= line.count(";")
			if fields <= 0:
				fields = NUM_OF_FIELDS
		print filename

#write in syntax-file ending of the syntax from separate file		
with open('end.txt') as f:
	content = f.readlines()
	for line in content:
		writef.write(line)