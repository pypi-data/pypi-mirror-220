import os
import pathlib
import subprocess

class File:
	FOLDER   = 0x3
	JSON     = 0x4
	TEXT     = 0x5
	LICENCE  = 0x6
	MARKDOWN = 0x7
	PYTHON   = 0x8
	FILE     = 0x9

DEFAULT_FOLDERS = {
	"Assets": File.FOLDER,
	"Scripts": File.FOLDER,
	"config": File.JSON,
	"LICENCE": File.LICENCE,
	"README": File.MARKDOWN,
	"main": File.PYTHON,
}

DEFAULT_SCRIPT = """import GameMaker as gm

window = gm.Window(screen_size=(800,450))

while window.RUNNING:
	window.update()
"""

def GetDefaultPath() -> str:
	return str(pathlib.Path(__name__).parent.resolve())

def ImportProject(path: str = GetDefaultPath()) -> tuple[dict,dict]:
	if path[-1] != '\\': path += '\\'

	ASSETS = {}
	SCRIPTS = {}

	if os.path.exists(path + 'Assets'):
		for file in os.listdir(path + 'Assets'):
			with open(path + 'Assets\\' + file, 'rb') as asset:
				ASSETS[file] = asset.read()

	return ASSETS, SCRIPTS

def Setup_Project(path: str = GetDefaultPath(),open_folder: bool = False, project: dict = DEFAULT_FOLDERS) -> bool:
	if path[-1] != '\\': path += '\\'

	print("Setting up in:",path)

	if not os.path.exists(path): os.mkdir(path)

	try:
		for item in project:
			match project[item]:
				case File.FOLDER:
					if not os.path.exists(path + item): os.mkdir(path + item)
				case File.JSON:
					with open(path + item + '.json','w') as f:
						f.write('{\n\t"": ""\n}')
				case File.TEXT:
					open(path + item + '.txt','w').close()
				case File.LICENCE:
					open(path + item + '.licence','w').close()
				case File.MARKDOWN:
					open(path + item + '.md','w').close()
				case File.PYTHON:
					with open(path + item + '.py','w') as f:
						f.write(DEFAULT_SCRIPT)
				case File.FILE:
					open(path + item,'w').close()
				case _:
					pass
	except Exception as error:
		print(error)
		return False

	if open_folder: subprocess.Popen(f'explorer {path}')

	return True