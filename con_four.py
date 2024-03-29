from inflection import extractName

class ConFourBoard():
    EMPTY_TOKEN = '-'
    USER0_TOKEN = 'O'
    USER1_TOKEN = 'X'

    def __init__(self, width: int=7, height: int=6) -> None:
        self.width = width; self.height = height
        self.holes = []
        self.nowUser = 0
        self.users = []
        self.isAvailable = True
        for _ in range(height):
            self.holes.append([self.EMPTY_TOKEN] * width)

    def getName(self) -> str:
        return "Connect Four"
    
    def __str__(self) -> str:
        mark = lambda x, y: '<' if x == y else "" 
        user0Line = "{}: {} {}\n".format(self.USER0_TOKEN, extractName(self.users[0].name), mark(self.nowUser, 0))
        user1Line = "{}: {} {}\n".format(self.USER1_TOKEN, extractName(self.users[1].name), mark(self.nowUser, 1))
        return "```Con4\n" + user0Line + user1Line + '\n'.join(map(lambda x: ' '.join(x),self.holes)) + '\n' + '_' * (self.width * 2 - 1) + '\n' + ' '.join(list(map(str, range(1, self.width + 1)))) + "\n```"
    
    def getUserToken(self, user: int) -> str:
        return self.USER0_TOKEN if user == 0 else self.USER1_TOKEN
    
    @staticmethod
    def getAnotherUser(user: int) -> int:
        return int(not(bool(user)))
    
    def checkConnect(self, user: int, column: int, row: int) -> int:
        if row < self.height - 3:
            # DOWNWARD SEARCH:
            for i in range(4):
                #await msg.channel.send("d", i)
                if self.holes[row + i][column] != self.getUserToken(user):
                    break
                if i == 3:
                    return user
            
            if column >= 3:
                # LEFTWARD SEARCH:
                for i in range(4):
                    #await msg.channel.send("l", i)
                    if self.holes[row][column - i] != self.getUserToken(user):
                        break
                    if i == 3:
                        return user

                # LEFTDOWNWARD SEARCH:
                for i in range(4):
                    #await msg.channel.send("ld", i)
                    if self.holes[row + i][column - i] != self.getUserToken(user):
                        break
                    if i == 3:
                        return user
            
            if column < self.width - 3:
                # RIGHTWARD SEARCH:
                for i in range(4):
                    #await msg.channel.send("r", i)
                    if self.holes[row][column + i] != self.getUserToken(user):
                        break
                    if i == 3:
                        return user

                # RIGHTDOWNWARD SEARCH:
                for i in range(4):
                    #await msg.channel.send("rd", i)
                    if self.holes[row + i][column + i] != self.getUserToken(user):
                        break
                    if i == 3:
                        return user
            return -1
        else:
            if column >= 3:
                # LEFTWARD SEARCH:
                for i in range(4):
                    #await msg.channel.send("l", i)
                    if self.holes[row][column - i] != self.getUserToken(user):
                        break
                    if i == 3:
                        return user

            if column < self.width - 3:
                # RIGHTWARD SEARCH:
                for i in range(4):
                    #await msg.channel.send("r", i)
                    if self.holes[row][column + i] != self.getUserToken(user):
                        break
                    if i == 3:
                        return user        
            return -1

    def dropToken(self, user: int, column: int) -> str:
        if column not in range(1, self.width + 1):
            return "WRONG"
        column -= 1
        row = None
        if self.holes[0][column] == self.EMPTY_TOKEN:
            for i in range(1, self.height + 1):
                if i == self.height:
                    self.holes[i - 1][column] = self.getUserToken(user)
                    row = i - 1
                    break
                elif self.holes[i][column] != self.EMPTY_TOKEN:
                    self.holes[i - 1][column] = self.getUserToken(user)
                    row = i - 1
                    break
            stat = self.checkConnect(user, column, row)
            if stat == -1:
                for i in self.holes:
                    if self.EMPTY_TOKEN in i:
                        return "OK"
                return "DRAW"
            else:
                return "WIN{}".format(stat)
        else:
            return "FULL"
    
    async def runRoutine(self, msg, no: int) -> int:
        stat = self.dropToken(self.nowUser, no)
        if stat == "OK":
            self.nowUser = self.getAnotherUser(self.nowUser)
            await msg.channel.send(self)
        elif stat == "FULL":
            await msg.channel.send("Haec columna plena est.")
        elif stat == "WRONG":
            await msg.channel.send("Numerus columnae pravus est.")
        elif stat.startswith("WIN"):
            await msg.channel.send(self)
            await msg.channel.send("{} vicit.".format(extractName(self.users[self.nowUser].name)))
            self.isAvailable = False
            return 0
        elif stat.startswith("DRAW"):
            await msg.channel.send(self)
            await msg.channel.send("Neuter lusor vicit.")
            self.isAvailable = False
            return 0
        return 1