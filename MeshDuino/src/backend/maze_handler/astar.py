from graph import Graph
from heapq import *
import random
import pygame

def heuristic(start, end):
	# returns manhattan distance between two points
	return abs(start[0]-end[0])+abs(start[1]-end[1])

def astar(start, end, grid): #implementation with heapq

	# initialize open set for points that have yet to be checked and
	# closed set for points that have already been checked
	closedSet = set()
	openSet = []

	# dictionary to hold a node and the node it came from 
	cameFrom = {}
	# dictionary to map the gScore of nodes
	gScore = {}
	# dictionary to map the fScore of nodes
	fScore = {}

	# initially map fScore and gScore of all nodes as infinity 
	for i in grid.get_vertices():
		gScore[i] = float("inf")
		fScore[i] = float("inf")

	# initialize fScore and gScore of starting position
	# cost from start to start is 0 and 
	# cost in beginning is just the heuristic 
	gScore[start] = 0
	fScore[start] = heuristic(start,end)

	# put the starting point in the heap (priority queue)
	heappush(openSet, (start, fScore[start]))

	# keep looping as long as there is something in the open set
	while openSet:
		# current point is the first index from the top of heap
		current = heappop(openSet)[0]

		if current == end:
			# if we have reached the end of the path then return the shortest path
			return reconstruct_path(cameFrom, current)

		# add current point into closed set because we will have checked it by the end of this iteration
		closedSet.add(current)


		for neighbour in grid.neighbours(current):

			# if the neighbour is already in the closed set, don't need to to anything
			if neighbour in closedSet:
				continue

			# if the neighbour is not already in the openSet, put it into the openSet
			if neighbour not in [i[0] for i in openSet]:
				heappush(openSet,(neighbour, fScore[neighbour]))

			# calculates the distance from current position to neighbour
			# if the distance is worse than its current neighbour, move on to next neighbour
			tentative_gScore = gScore[current] + heuristic(current, neighbour)
			if tentative_gScore >= gScore[neighbour]:
				continue

			# record the best path
			cameFrom[neighbour] = current
			gScore[neighbour] = tentative_gScore
			fScore[neighbour] = gScore[neighbour] + heuristic(neighbour, end)


def reconstruct_path(cameFrom, current):
	total_path = [current]

	while current in cameFrom.keys():
		current = cameFrom[current]
		total_path.append(current)

	return total_path[::-1]