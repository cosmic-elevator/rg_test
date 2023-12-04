import re
import math


class NoteParse():
    def __init__(self, bmsfile_location):
        self.bmsfile = open(bmsfile_location, 'r', encoding='utf-8')
        self.temp_note_list_1 = []
        self.temp_note_list_2 = []
        self.temp_note_list_3 = []
        self.temp_note_list_4 = []
        self.read_bms()


    def read_bms(self):
        while True:
            line = self.bmsfile.readline()
            self.process(line)
            if not line: break


    def process(self, linedata):
        if linedata == None: 
            return
        try:
            if linedata[0] == '#':
                # sepcharlist = [' ', ':']
                self.stringlist = re.split(' |:', linedata)

                if self.stringlist[0] == "#BPM":
                    #print("bpm", self.stringlist[1])
                    self.bpm = int(self.stringlist[1])
                elif self.stringlist[0] == "#PLAYER":
                    pass
                elif self.stringlist[0] == "#GENRE":
                    pass
                elif self.stringlist[0] == "#TITLE":    # 사실 그냥 여기다가 곡제목/아티스트 저장해서 파싱해도 되는데.. 
                    pass
                elif self.stringlist[0] == "#ARTIST":
                    pass
                elif self.stringlist[0] == "#PLAYLEVEL":
                    pass
                elif self.stringlist[0] == "#RANK":
                    pass
                elif self.stringlist[0] == "#VOLWAV":
                    pass
                elif self.stringlist[0] == "#STAGEFILE":
                    pass
                elif self.stringlist[0] == "#TOTAL":
                    pass
                elif self.stringlist[0] == "#LNTYPE":
                    pass
                else:  # playable notes
                    current_barnum = int(self.stringlist[0][1:4])
                    #print(self.current_barnum)
                    current_linenum = int(self.stringlist[0][5])
                    #self.current_note_datas = self.stringlist[1]
                    current_note_data_list = [self.stringlist[1][i:i+2]
                                                    for i in range(0, len(self.stringlist[1]), 2)]
                    self.add_note(current_barnum, current_linenum, current_note_data_list)
            
        except:
            pass