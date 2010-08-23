# CMake project file for COCCITOOLS

cmake_minimum_required(VERSION 2.6)

# Project Name
project(coccitools)

# Variables

file(
	GLOB_RECURSE
	python_libs
	lib/python/coccitools/*
)
# Installation
install(PROGRAMS bin/cocci DESTINATION bin)
install(FILES lib/python/argparse.py DESTINATION lib/python/)
install(FILES lib/python/configuration.py DESTINATION lib/python/)
install(FILES ${python_libs} DESTINATION lib/python/coccitools)
install(SCRIPT scripts/createdirs.cmake)

