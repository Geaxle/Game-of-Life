from cx_Freeze import setup, Executable

# On appelle la fonction setup
includes = ["libtcopy.py"]

setup(
	name = "game of life",
	version = "0.1",
	description = "Game of Life by Geaxle",
	executables = [Executable("game of life.py")],
	)
