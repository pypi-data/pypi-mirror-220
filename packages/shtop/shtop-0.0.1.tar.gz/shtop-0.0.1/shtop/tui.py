import os

LINE_TYPE_FNC = 1
LINE_TYPE_TXT = 2

class Line:
    def __init__(self, typeo, lines):
        self.type = typeo
        self.line = lines

class Tui:
    def __init__(self):
        self.header = []
        self.lines  = []
        self.vars   = {}

    def update(self):
        os.system('clear')
        self._drawTui()

    def addHeader(self, line):
        self.header.append(line)

    def addTextLine(self, txt):
        lineo = Line(LINE_TYPE_TXT, txt)
        self.lines.append(lineo)

    def addFuncLine(self, fnc):
        lineo = Line(LINE_TYPE_FNC, fnc)
        self.lines.append(lineo)

    def setVar(self, name, val):
        self.vars[name] = val

    def _drawTui(self):

        for header in self.header:
            print(header)

        print()

        for line in self.lines:
            if line.type == LINE_TYPE_TXT:
                
                line = line.line
                for k, v in self.vars.items():
                    line = line.replace('%%%s%%' % k, str(v))

                print(line)
                
            elif line.type == LINE_TYPE_FNC:
                line.line()
