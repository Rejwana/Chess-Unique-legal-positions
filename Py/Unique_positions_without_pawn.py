 
import random
import copy
import csv
 
#board = [[" " for x in range(8)] for y in range(8)]
piece_list = ["K","R", "N", "B", "Q", "P", "k", "r", "n", "b", "q"]
white_pices = ["Q","R","N","B"]
black_pices = ["q","r","n","b"]


#to get the index where a piece is present
def occupied_index(board, v):
    for i, x in enumerate(board):
        if v in x:
            return (i, x.index(v))
    return (-1,-2)




#add new piece
def add_piece(board,piece):
    Kpiecevk = list()
    #holds occupied index
    rank = list()
    file = list()
    second_pis = 0
    for pis in piece_list:
        r,f = occupied_index(board, pis)
        if (r!= -1 and f!=-2):  #if piece is not in the board don't add on occupied index
            
            if(pis==piece):     #if two same pices
                second_pis = 1
            rank.append(r)
            file.append(f)

    

    #find if have KQQk/KRRk/KBBk/KNNk type board
    
    #if all the existing pieces are on diagonal cell, placing another piece will be diagonally symmetric
    is_diagonal = all ((rank[i]==file[i]) for i in range(len(rank)))
    #if adding a piece which is already on the board, add the piece on only one side of the diagonal
    if(second_pis==1):
        for piece_rank in range(8):
            for piece_file in range(piece_rank+1):
                brd = copy.deepcopy(board)
                if brd[piece_rank][piece_file] == " ":
                    brd[piece_rank][piece_file] = piece
                    Kpiecevk.append(brd)
            
    #if all different pices from the same side
    else:
        if is_diagonal:
            #if doagonal take only unique from diagonal mirror ppositions
            for piece_rank in range(8):
                for piece_file in range(piece_rank+1):
                    brd = copy.deepcopy(board)
                    if brd[piece_rank][piece_file] == " ":
                        brd[piece_rank][piece_file] = piece
                        Kpiecevk.append(brd)

        else:
            for piece_rank in range(8):
                for piece_file in range(8):
                    brd = copy.deepcopy(board)
                    if brd[piece_rank][piece_file] == " ":
                        brd[piece_rank][piece_file] = piece
                        Kpiecevk.append(brd)
    return Kpiecevk
                
            
 
def fen_from_board(brd):
	fen = ""
	for x in brd:
		n = 0
		for y in x:
			if y == " ":
				n += 1
			else:
				if n != 0:
					fen += str(n)
				fen += y
				n = 0
		if n != 0:
			fen += str(n)
		fen += "/" if fen.count("/") < 7 else ""
	fen += " "
	return fen
 
def pawn_on_promotion_square(pc, pr):
	if pc == "P" and pr == 0:
		return True
	elif pc == "p" and pr == 7:
		return True
	return False

#place kings first 
def place_kings():
    king_brd = list()
    for rank_white in range(4):
        for file_white in range(rank_white+1):

            if (rank_white == file_white):
                for rank_black in range(8):
                    for file_black in range(rank_black+1):
                        diff_list = [abs(rank_white - rank_black),  abs(file_white - file_black)]
                        brd = [[" " for x in range(8)] for y in range(8)]                   
                        if sum(diff_list) > 2 or set(diff_list) == set([0, 2]):
                        
                            brd[rank_white][file_white], brd[rank_black][file_black] = "K", "k"
                        
                            king_brd.append(brd)
            else:            
                for rank_black in range(8):
                    for file_black in range(8):
                        diff_list = [abs(rank_white - rank_black),  abs(file_white - file_black)]
                        brd = [[" " for x in range(8)] for y in range(8)]                    
                        if sum(diff_list) > 2 or set(diff_list) == set([0, 2]):
                        
                            brd[rank_white][file_white], brd[rank_black][file_black] = "K", "k"
                        
                            king_brd.append(brd)
            
                    
                    
    return king_brd

#write position in csv
def write_pos(positions, pis):
    #print("kkn length",len(positions))
    filename = pis+"test.csv"

    with open(filename, 'w') as myfile:
     wr = csv.writer(myfile, delimiter = ',')

     for i in range(len(positions)):
         position = ""
         position +=fen_from_board(positions[i])
         wr.writerow(position)



#Ex KQRvsk 4piece
def generate_nvs1(king_positions):
    for pis1 in white_pices:    
        pic_3 = list()
        for brd in king_positions:
            pic_3.extend(add_piece(brd,pis1))
        print("3piece length",len(pic_3))
        write_pos(pic_3,pis1)
        pis_1_index = white_pices.index(pis1)
        
        for pis2 in white_pices[pis_1_index:]:
            pic_4 = list()
            for brd in pic_3:
                pic_4.extend(add_piece(brd,pis2))
            #pis_4_unique = unique_check(pic_4)
            print("4 piece length",len(pic_4))
            write_pos(pic_4,pis1+pis2)
        
        
                   
            

#Ex KQvskq,KQvskr 4piece
def generate_nvsm(king_positions):
    for pis1 in white_pices:
        pic_3 = list()
        for brd in king_positions:
            pic_3.extend(add_piece(brd,pis1))
        print("3piece length",len(pic_3))
        #write_pos(pic_3,pis1)
        pis_1_index = white_pices.index(pis1)
        for pis2 in black_pices[pis_1_index:]:
            pic_4 = list()
            for brd in pic_3:
                pic_4.extend(add_piece(brd,pis2))
            print("4 piece length",len(pic_4))
            write_pos(pic_4,"K"+pis1+"k"+pis2)

#Ex KQRvskq 5piece
def generate_abvsc(pic_4,pis3):
    pic_5 = list()
    for brd in pic_4:
        pic_5.extend(add_piece(brd,pis3))
    print("5 piece length",len(pic_5))
    
    return pic_5

    '''
#with all piece list
    for pis1 in white_pices:
        pic_3 = list()
        for brd in king_positions:
            pic_3.extend(add_piece(brd,pis1))
        print("3piece length",len(pic_3))
        #write_pos(pic_3,pis1)
        pis_1_index = white_pices.index(pis1)
        for pis2 in black_pices[pis_1_index:]:
            pic_4 = list()
            for brd in pic_3:
                pic_4.extend(add_piece(brd,pis2))
            print("4 piece length",len(pic_4))
            write_pos(pic_4,"K"+pis1+"k"+pis2)
            for pis3 in white_pices:
                pic_5 = list()
                for brd in pic_4:
                    pic_5.extend(add_piece(brd,pis3))
                print("5 piece length",len(pic_5))
                write_pos(pic_5,"KQ"+pis1+pis3+"kq"+pis2)
    '''


def start():
#place the kings first on pawnless tablebase
    king_positions = place_kings()
    print("Kk length",len(king_positions))
    write_pos(king_positions,"Kk")
    
    #create 4 piece unique legal position
    piece_4 = generate_nvsm(king_positions)

    #create 5 piece unique legal positions. Only KQRkq created for experiments.
    piece_5 = generate_abvsc(piece_4,"R")

    


start()
