from username import getUserName
import random
import asyncio

robotUser = None
semaphore = False

class MancalaBoard(object):
    class Pit(object):
        def __init__(self, owner: int, id: int, stone: int) -> None:
            self.owner = owner
            self.id = id
            self.stone = stone

        def __str__(self) -> str:
            return str(self.stone)
        
        def getLocation(self) -> tuple[int, int]:
            return (self.owner, self.id)

    def __init__(self, stoneNum: int=4, pitNum: int=6) -> None:
        try:
            stoneNum = int(stoneNum)
            pitNum = int(pitNum)
        except:
            raise TypeError()
        if pitNum not in range(2, 10) or stoneNum not in range(2, 11):
            raise ValueError()
        self.stoneNum = stoneNum
        self.pitNum = pitNum
        self.pits = [[MancalaBoard.Pit(0, 0, 0)], [MancalaBoard.Pit(1, 0, 0)]]
        for i in range(pitNum):
            self.pits[0].append(MancalaBoard.Pit(0, i + 1, stoneNum))
            self.pits[1].append(MancalaBoard.Pit(1, i + 1, stoneNum))
        self.pointer: self.Pit = None
        self.users: list = []
        self.nowUser: int = 0
        self.move: int = 0
        self.isAvailable: bool = True
        self.shuffle: bool = False
        self.handicap: bool = True

    def makeCopy(self) -> "MancalaBoard":
        newBoard = MancalaBoard(self.stoneNum, self.pitNum)
        newBoard.pits = [[MancalaBoard.Pit(0, 0, self.pits[0][0].stone)], [MancalaBoard.Pit(1, 0, self.pits[1][0].stone)]]
        for i in range(newBoard.pitNum):
            newBoard.pits[0].append(MancalaBoard.Pit(0, i + 1, self.pits[0][i + 1].stone))
            newBoard.pits[1].append(MancalaBoard.Pit(1, i + 1, self.pits[1][i + 1].stone))
        newBoard.pointer: newBoard.Pit = None
        newBoard.users: list = self.users
        newBoard.nowUser: int = self.nowUser
        newBoard.move: int = self.move
        newBoard.isAvailable: bool = self.isAvailable
        return newBoard

    def getName(self) -> str:
        return "Mancala"

    @staticmethod
    def getAnotherUser(user: int) -> int:
        return int(not(bool(user)))
    
    def __str__(self) -> str:
        if self.users:
            numberTag0 = '='.join(list(map(lambda x: '#' + str(x), list(range(1, self.pitNum + 1)))))
            numberTag1 = '='.join(list(map(lambda x: '#' + str(x), list(range(1, self.pitNum + 1))[::-1])))
            user0Line = "|  ->  {}  [{:>2}]| {} {}\n+======{}======+".format('|'.join(list(map(lambda x: "{:>2}".format(str(x)), self.pits[0][1:]))), str(self.pits[0][0]), getUserName(self.users[0].name, True), '<' if self.nowUser == 0 else "", numberTag0)
            user1Line = "+======{}======+\n|[{:>2}]  {}  <-  | {} {}".format(numberTag1, str(self.pits[1][0]), '|'.join(list(map(lambda x: "{:>2}".format(str(x)), self.pits[1][1:][::-1]))), getUserName(self.users[1].name, True), '<' if self.nowUser == 1 else "")
            return "```Mancala\n" + "M{}:  {}\n".format(self.move, getUserName(self.users[self.nowUser].name)) + user1Line + '\n' + user0Line + "```"
        else:
            return "Mancala Board"
    
    def findNextPit(self, user: int) -> Pit:
        if self.pointer:
            if self.pointer.id == self.pitNum:
                if user == self.pointer.owner:
                    return self.pits[user][0]
                else:
                    return self.pits[self.getAnotherUser(self.pointer.owner)][1]
            else:
                if self.pointer.id == 0:
                    return self.pits[self.getAnotherUser(user)][1]
                else:
                    return self.pits[self.pointer.owner][self.pointer.id + 1]
        else:
            raise ValueError()
    
    def putStone(self, user: int, stoneNum: int) -> None:
        for _ in range(stoneNum):
            self.pointer = self.findNextPit(user)
            self.pointer.stone += 1

    def takeMove(self, user: int, no: int) -> str:
        self.move += 1
        #print(list(map(lambda x: x.stone, self.pits[user])))
        if self.pits[user][no].stone == 0:
            return "WRONG"
        self.pointer = self.pits[user][no]
        stoneNum = self.pointer.stone
        self.pits[user][no].stone = 0
        self.putStone(user, stoneNum)
        if self.pointer.getLocation()[1] == 0:
            return "AGAIN"
        elif self.pointer.stone == 1 and self.pointer.getLocation()[0] == user and self.pits[MancalaBoard.getAnotherUser(user)][self.pitNum + 1 - self.pointer.getLocation()[1]].stone != 0:
            if user == 0 and self.handicap:
                return "HANDICAP"
            self.pits[user][0].stone += self.pits[MancalaBoard.getAnotherUser(user)][self.pitNum + 1 - self.pointer.getLocation()[1]].stone + 1
            self.pointer.stone = 0
            self.pits[MancalaBoard.getAnotherUser(user)][self.pitNum + 1 - self.pointer.getLocation()[1]].stone = 0
            return "SEIZURE"
        return "OK"

    def checkEmpty(self) -> bool:
        if sum(map(lambda x: x.stone, self.pits[0][1:])) * sum(map(lambda x: x.stone, self.pits[1][1:])) == 0:
            self.isAvailable = False
            return True
        else:
            return False

    async def endGame(self, msg) -> None:
        self.pits[0][0].stone += sum(map(lambda x: x.stone, self.pits[0][1:]))
        self.pits[1][0].stone += sum(map(lambda x: x.stone, self.pits[1][1:]))
        await msg.channel.send("**Eventus:**\n  {}  __**{}**__ : __**{}**__  {}".format(getUserName(self.users[0].name, True), self.pits[0][0].stone, self.pits[1][0].stone, getUserName(self.users[1].name, True)))
        if self.pits[0][0].stone == self.pits[1][0].stone:
            await msg.channel.send("Neuter lusor vicit.")
        else:
            winner = int(self.pits[0][0].stone < self.pits[1][0].stone)
            await msg.channel.send("{} vicit.".format(getUserName(self.users[winner].name)))
    
    async def showBoard(self, msg):
        await msg.channel.send(self)
        global semaphore; semaphore = True
        
    async def joinGame(self, user, msg, isRobot: bool=False) -> int:
        global robotUser
        if len(self.users) < 2:
            self.users.append(user)
            if isRobot:
                await msg.channel.send("Eusophius ludo Mancala intersum.")
                robotUser = user
            else:
                await msg.channel.send("Ludo Mancala interes.")
            if len(self.users) == 2:
                await msg.channel.send("Ludus Mancala agitatus est.")
                if self.shuffle:
                    random.shuffle(self.users)
                    await msg.channel.send("{} infert, {} defendit.".format(getUserName(self.users[0].name), getUserName(self.users[1].name)))
                await self.showBoard(msg)
                if robotUser:
                    return 1
                else:
                    return 0
            return 0
        else:
            await msg.channel.send("Jam duo lusores intersunt.")

    async def runRoutine(self, msg, no) -> int:
        if not self.isAvailable:
            return 0
        if no in range(1, self.pitNum + 1):
            stat = self.takeMove(self.nowUser, no)
            isEnd = self.checkEmpty()
            
            if stat == "OK":
                self.nowUser = MancalaBoard.getAnotherUser(self.nowUser)
                await self.showBoard(msg)
            elif stat == "SEIZURE":
                self.nowUser = MancalaBoard.getAnotherUser(self.nowUser)
                await msg.channel.send("**Comprehensio.**")
                await self.showBoard(msg)
            elif stat == "HANDICAP":
                self.nowUser = MancalaBoard.getAnotherUser(self.nowUser)
                self.handicap = False
                await msg.channel.send("**Comprehensio inferentis oppressa.**")
                await self.showBoard(msg)
            elif stat == "WRONG":
                await msg.channel.send("Nullus lapis in hoc puteo. Alium lege.")
            elif stat == "AGAIN":
                await self.showBoard(msg)
            
            if isEnd:
                await self.endGame(msg)
                return 0

            if stat == "AGAIN":
                await msg.channel.send("**Iterum.**")
                return 2

            return 1
        else:
            await msg.channel.send("Numerus pravus. Lege denuo.")
            return -1

    def evaluate(self, user: int, depth: int=0) -> tuple:
        score = {}
        pitNum = self.pitNum
        seizeMove = findSeizeMove(self, user)
        againMove = findAgainMove(self, user)
        for i in range(pitNum):
            score[i + 1] = 0
            p = self.pits[user][i + 1]
            if p.stone == 0:
                continue
            cycle = ((p.id + p.stone - pitNum - 1) // (2 * pitNum + 1) + 1)
            score[i + 1] += cycle
            if i + 1 in seizeMove.keys():
                score[i + 1] += seizeMove[i + 1]

            if i + 1 in againMove and depth < 5:
                nBoard = self.makeCopy()
                nBoard.takeMove(user, i + 1)
                nScore = nBoard.evaluate(user, depth=depth + 1)
                score[i + 1] += max(nScore.values())


            nBoard = self.makeCopy()
            nBoard.takeMove(user, i + 1)
            if nBoard.checkEmpty():
                score[i + 1] += sum(map(lambda x: x.stone, nBoard.pits[user][1:]))
                score[i + 1] -= sum(map(lambda x: x.stone, nBoard.pits[nBoard.getAnotherUser(user)][1:]))
            nBoard.nowUser = nBoard.getAnotherUser(nBoard.nowUser)
            beSeizedMove = findSeizeMove(nBoard, nBoard.nowUser)
            if beSeizedMove:
                score[i + 1] -= max(beSeizedMove.values())
            
        if depth == 0: print('/'.join(map(str, score.values())))
        return score

def findAgainMove(board: MancalaBoard, userId: int) -> list[int]:
    pitNum = board.pitNum
    rs = []
    for pit in board.pits[userId][1:]:
        if pit.id + pit.stone == pitNum + 1:
            rs.append(pit.id)
    return rs

def findSeizeMove(board: MancalaBoard, userId: int) -> dict[int, int]:
    pitNum = board.pitNum
    rs = {}
    for pit in board.pits[userId][1:]:
        no = (pit.id + pit.stone) % (2 * pitNum + 1)
        oNo = (pitNum - (pit.id + pit.stone)) % (2 * pitNum + 1) + 1
        if no in range(1, pitNum) and pit.stone != 0:
            if board.pits[userId][no].stone == 0:
                if board.pits[board.getAnotherUser(userId)][oNo].stone != 0:
                    rs[pit.id] = board.pits[board.getAnotherUser(userId)][oNo].stone + 1
    return rs

def decideMove(board: MancalaBoard, userId: int) -> int:
    pitNum = board.pitNum
    score = board.evaluate(userId)
    scoreReversed: dict[int, list] = {}
    for k, v in score.items():
        scoreReversed[v] = scoreReversed.get(v, []) + [k]
    evalTop = random.choice(scoreReversed[sorted(scoreReversed)[-1]])
    
    if board.pits[userId][evalTop].stone != 0:
        return evalTop
    else:
        while True:
            i = random.randint(1, pitNum)
            if board.pits[userId][i].stone != 0:
                return i

async def aiReceiveSemaphore(board: MancalaBoard, msg):
    global semaphore
    while not semaphore:
        await asyncio.sleep(0.1)

    if not board.isAvailable: return 0

    semaphore = False

    if board.users[board.nowUser] == robotUser:
        no = decideMove(board, board.nowUser)
        await asyncio.sleep(0.1)
        await msg.channel.send("$mv {}".format(no))
        stat = await board.runRoutine(msg, no)
        if stat == 2 or stat == -1:
            semaphore = True
            await aiReceiveSemaphore(board, msg)

def aiEndMancala():
    global robotUser; robotUser = None