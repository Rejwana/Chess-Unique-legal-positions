import csv
import chess
import chess.syzygy
#from syzygy_best_move import get_best_move

from sqlconnect import *


#Using syzygy tablebase the get perfect play informations
syzygy_path = "/EGTB/syzygy"
tablebase = chess.syzygy.open_tablebase(syzygy_path)


"""get the best moves for a given board position according to sygygy"""
def get_best_move(board):
    
    wdl = tablebase.probe_wdl(board)
    dtz = tablebase.probe_dtz(board)
    #print("checkmate:", board.is_checkmate(), ",stalemate:", board.is_stalemate(),",variant_win:",board.is_variant_win(),",variant_loss:",board.is_variant_loss(),",insufficient_material:",board.is_insufficient_material(),"wdl:",tablebase.probe_wdl(board),",dtz:",tablebase.probe_dtz(board),"moves:")
    loosing_moves = list()
    winning_moves = list()
    drawing_moves = list()
    best_move = list()
    
    if (wdl==0):
        best = 0
    else:
        best = float("-inf")
    for move in board.legal_moves:
        zeroing = board.is_zeroing(move)
        board.push(move)
        wdl_after_move = tablebase.probe_wdl(board)
        dtz_after_move = tablebase.probe_dtz(board)
        if (wdl_after_move>0):
            loosing_moves.append(move.uci())
        elif (wdl_after_move<0):
            winning_moves.append(move.uci())
        else:
            drawing_moves.append(move.uci())

        if ((wdl>0 and wdl_after_move<0) or (wdl<0)):
            if(dtz_after_move>best):
                best_move = list({move.uci()})
                best = tablebase.probe_dtz(board)
            elif (dtz_after_move==best):
                best_move.append(move.uci())

        elif(wdl==0 and wdl_after_move==0):
            best_move.append(move.uci())
                    
            
            
        #print("uci:",move,",zeroing:",zeroing,",checkmate:", board.is_checkmate(), ",stalemate:", board.is_stalemate(),",variant_win:",board.is_variant_win(),",variant_loss:",board.is_variant_loss(),",insufficient_material:",board.is_insufficient_material(),"wdl:",tablebase.probe_wdl(board),",dtz:",tablebase.probe_dtz(board))
        board.pop()

    

    return winning_moves,loosing_moves,drawing_moves,best_move,wdl,dtz


def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1
    
    
    
#create chess picision from pieces placed on the board
def create_fen(psn):
    black = psn+"b - - 0 1" #black to move
    white = psn+"w - - 0 1" #white to move
    board_btm = chess.Board (black)
    board_wtm = chess.Board(white)
    positions = []
    
    #check for legality
    if not (board_btm.is_check()):
        positions.append(board_wtm.fen())

    if not (board_wtm.is_check()):
        positions.append(board_btm.fen())       
    return positions


    
#incert in plaintext format
def  insert(psn):
    board = chess.Board(psn)
    
    #get the winning drawing and losing moves
    winning_moves,loosing_moves,drawing_moves,best_moves,WDL_score,dtz_score = get_best_move(board)
    
    #store all winning moves as varchar in thew same field
    winning = ','.join(winning_moves)
    loosing = ','.join(loosing_moves)
    drawing = ','.join(drawing_moves)
    best = ','.join(best_moves)


    if (WDL_score >0):
        WDL = 'W'
    elif(WDL_score <0):
        WDL = 'L'
    else:
        WDL = 'D'

    #create_table()
    #insert into MySQL table
    insert_into(psn,winning,loosing,drawing,best,WDL,WDL_score,dtz_score)


def main():
    TB_name = sys.argv[1]
    create_table(TB_name)
    file_name = "/Positions/"+TB_name+".csv"
    #the Unique positions for up to 5 pis are saved in positions folder
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    print(len(data))
    positions = list()
    for i in range (len(data)):
        psn = listToString(data[i])
        positions.extend(create_fen(psn))
    print(len(positions))

    for position in positions:
        insert(TB_name,position)


main()
