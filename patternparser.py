import re
from note import *


class Pattern():
    def __init__(self, bmsfile_location):
        self.bmsfile = open(bmsfile_location, 'r', encoding='utf-8')
        self.noteq_1 = []
        self.noteq_2 = []
        self.noteq_3 = []
        self.noteq_4 = []
        self.total_notes = 0
        self.note_add_status = 0
        self.loading_percent = 0
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
            if linedata[0] == '*':
                pass
            elif linedata[0] == '#':
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
                    current_note_data_list.remove('\n')
                    #print(current_note_data_list)
                    self.add_note(current_barnum, current_linenum, current_note_data_list)
            
        except:
            pass


    def add_note(self, barnum, linenum, note_data_list):
    # for문을 돌면서 해당 마디 해당 라인에 있는 노트를 전부 리스트에 저장한다.
        for i in range(len(note_data_list)):
            if note_data_list[i] != "00":
                detail_beat = barnum + (i / len(note_data_list))
                note_expect_hit_time = self.calculate_time(self.bpm, detail_beat)
                #print(note_expect_hit_time)
                self.note_add_status += 1

                if linenum == 1:
                    self.noteq_1.append(Note(1, note_expect_hit_time))
                elif linenum == 2:
                    self.noteq_2.append(Note(2, note_expect_hit_time))
                elif linenum == 3:
                    self.noteq_3.append(Note(3, note_expect_hit_time))
                elif linenum == 4:
                    self.noteq_4.append(Note(4, note_expect_hit_time))


    def calculate_time(self, bpm, detail_beat):
        time = detail_beat * ((1.0 / bpm) * 60 * 4)
        #time = self.clean_decimal(time)
        return time
    

    def calculate_percent(self, current, total):
        return round((current / total) * 100)
    


#test_pt = Pattern('pattern/jumuck.bms')

#for note in test_pt.noteq_1:
    #print(note.exact_hit_time)

    #exact_hit_time이 제대로 계산되지 않는 문제가 있다
    #노트 개수는 제대로 계산되고 있는가?