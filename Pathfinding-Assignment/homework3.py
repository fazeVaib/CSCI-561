from collections import deque
import heapq

class Trail:
    def __init__(self, path):
        self.path = path
        self.readInput()
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                           (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def readInput(self):
        with open(self.path, 'r') as file:

            inputLines = [line.strip() for line in file]

            self.algo = inputLines[0]
            self.cols, self.rows = map(int, inputLines[1].split(" "))
            y, x = map(int, inputLines[2].split(" "))
            self.start = (x, y)
            self.maxClimb = int(inputLines[3])
            numSettlePoints = int(inputLines[4])
            temp = 5
            self.settlePoints = []
            for i in range(numSettlePoints):
                y, x = map(int, inputLines[temp + i].split(" "))
                self.settlePoints.append((x, y))

            temp += numSettlePoints

            self.matrix = []

            for i in range(self.rows):
                self.matrix.append(
                    [int(ele) for ele in inputLines[temp + i].strip().split(" ") if ele != ""])

            file.close()

class FindPath:
    
    def __init__(self, t : Trail):
        self.trail = t

   
    def searchPath(self):
        if self.trail.algo == "BFS":
            return self.bfs()
        if self.trail.algo == "UCS":
            return self.ucs()
        if self.trail.algo == "A*":
            return self.astar()
    
   
    def checkHeight(self, x, y, adjX, adjY):
        h1 = 0 if self.trail.matrix[x][y] >= 0 else self.trail.matrix[x][y]
        h2 = 0 if self.trail.matrix[adjX][adjY] >= 0 else self.trail.matrix[adjX][adjY]

        return abs(h1 - h2)
   
   
    def checkMovement(self, x, y, adjX, adjY):

        if adjX < 0 or adjX == self.trail.rows or adjY < 0 or adjY == self.trail.cols:
            return False

        if self.checkHeight(x, y, adjX, adjY) > self.trail.maxClimb:
            return False

        return True

    
    def bfs(self):
        
        queue = deque([self.trail.start])
        startx, starty = self.trail.start
        visited = {(startx, starty)}
        path = {}

        while queue:
            k = len(queue)
            for _ in range(k):
                
                x, y = queue.popleft()

                for dx, dy in self.trail.directions:
                    
                    adjX, adjY = x + dx, y + dy

                    if not self.checkMovement(x, y, adjX, adjY):
                        continue

                    if (adjX, adjY) not in visited:
                        queue.append((adjX, adjY))
                        visited.add((adjX, adjY))
                        path[(adjX, adjY)] = (x, y)

        res = [0 for _ in range(len(self.trail.settlePoints))]

        for i, val in enumerate(self.trail.settlePoints):

            currx, curry = val

            if (currx, curry) not in path.keys():
                res[i] = "FAIL"

            else:
                res[i] = []
                while (currx, curry) != self.trail.start:
                    res[i].append([currx, curry])
                    currx, curry = path[(currx, curry)]
                res[i].append(self.trail.start)

        return res


    def ucs(self):

        queue = []
        startx, starty = self.trail.start
        path = {}
        g = [[float('inf')] * self.trail.cols for _ in range(self.trail.rows)]
        g[startx][starty] = 0
        heapq.heappush(queue, (0, self.trail.start))

        while queue:

            currcost, currcell = heapq.heappop(queue)
            x, y = currcell

            for dx, dy in self.trail.directions:

                adjX, adjY = x + dx, y + dy

                if not self.checkMovement(x, y, adjX, adjY):
                    continue
                
                newcost = 0
                
                if abs(dx - dy) == 1:
                    newcost = currcost + 10
                else:
                    newcost = currcost + 14
                
                if newcost < g[adjX][adjY]:
                    g[adjX][adjY] = newcost
                    path[(adjX, adjY)] = (x, y)
                    heapq.heappush(queue, (newcost, (adjX, adjY)))

        res = [0 for _ in range(len(self.trail.settlePoints))]
        
        for i, val in enumerate(self.trail.settlePoints):

            currx, curry = val
            
            if (currx, curry) not in path.keys():
                res[i] = "FAIL"
            
            else:
                res[i] = []
                while (currx, curry) != self.trail.start:
                    res[i].append([currx, curry])
                    currx, curry = path[(currx, curry)]
                res[i].append(self.trail.start)

        return res


    def heuristics(self, x, y, goalx, goaly):
        dx = abs(x - goalx)
        dy = abs(y - goaly)
        return 10 * (dx + dy) - (6* min(dx, dy))
        

    def astar(self):

        res = [0 for _ in range(len(self.trail.settlePoints))]
        
        for i, settlepoint in enumerate(self.trail.settlePoints):

            startx, starty = self.trail.start
            g = [[float('inf')] * self.trail.cols for _ in range(self.trail.rows)]
            f = [[float('inf')] *
                 self.trail.cols for _ in range(self.trail.rows)]
            goalx, goaly = settlepoint
            queue = []
            path = {}
            fount = False
            g[startx][starty] = 0
            f[startx][starty] = self.heuristics(startx, starty, goalx, goaly)
            heapq.heappush(queue, (f[startx][starty], self.trail.start))

            while queue:

                currcost, currcell = heapq.heappop(queue)
                x, y = currcell

                if (x, y) == (goalx, goaly):
                    break

                for dx, dy in self.trail.directions:

                    adjX, adjY = x + dx, y + dy

                    if not self.checkMovement(x, y, adjX, adjY):
                        continue
                    
                    travel_cost = 0
                    mud_value = self.trail.matrix[adjX][adjY] if self.trail.matrix[adjX][adjY] > 0 else 0

                    travel_cost += self.checkHeight(x, y, adjX, adjY)
                    travel_cost += mud_value

                    if abs(dx - dy) == 1:
                        newcost = g[x][y] + 10 + travel_cost
                    else:
                        newcost = g[x][y] + 14 + travel_cost
                    
                    if newcost < g[adjX][adjY]:
                        g[adjX][adjY] = newcost
                        f[adjX][adjY] = g[adjX][adjY] + self.heuristics(adjX, adjY, goalx, goaly)
                        heapq.heappush(queue, (f[adjX][adjY], [adjX, adjY]))
                        path[(adjX, adjY)] = (x, y)

            currx, curry = settlepoint
            if (currx, curry) in path.keys():
                res[i] = []
                while (currx, curry) != self.trail.start:
                    res[i].append([currx, curry])
                    currx, curry = path[(currx, curry)]
                res[i].append(self.trail.start)

            else:
                res[i] = "FAIL"
        
        return res


def outputfile(arr):

    f = open("./output.txt", "w")
    l = len(arr)

    for i in range(l):
        if arr[i] == "FAIL":
            f.write(arr[i].strip())
        else:
            temp = []
            for p in arr[i][::-1]:
                temp.append(str(p[1]) + "," + str(p[0]) + " ")
            f.write("".join(temp).strip())
        
        if i != l - 1:
            f.write("\n")
    
    f.close()


if __name__ == "__main__":

    t1 = Trail("./input.txt")
    fp = FindPath(t1)
    outputfile(fp.searchPath())
