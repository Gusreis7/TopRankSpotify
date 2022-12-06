import _json
import json
import os
import argparse

def calc_time(time_listened):
    time_listened /= 1000
    hours = time_listened // 3600
    time_listened %= 3600
    minutes = time_listened // 60
    time_listened %= 60
    total_time_str = str(int(hours)) + " hour(s) and " + str(int(minutes)) + " minute(s)"
    return total_time_str

def calcula_mus_artist(f,dicMus_art, artist_name):
    data = json.load(f)
    for musica in data:
        if musica['master_metadata_track_name'] not in dicMus_art and musica['master_metadata_album_artist_name'] == artist_name:
            dicMus_art[musica['master_metadata_track_name']] = musica['ms_played']
        elif musica['master_metadata_album_artist_name'] == artist_name:
            dicMus_art[musica['master_metadata_track_name']] += musica['ms_played']
    return dicMus_art

def calc_artist(f,dicArt):
    data = json.load(f)
    for artista in data:
        if artista['master_metadata_album_artist_name'] not in dicArt:
            dicArt[artista['master_metadata_album_artist_name']] = artista['ms_played']
        else:
            dicArt[artista['master_metadata_album_artist_name']] +=artista['ms_played']
    return dicArt

def calc_mus(f,dicMus):
    data = json.load(f)
    for musica in data:
        if musica['master_metadata_track_name'] not in dicMus:
            dicMus[musica['master_metadata_track_name']] = musica['ms_played']
        else:
            dicMus[musica['master_metadata_track_name']] += musica['ms_played']
    return dicMus

def aplly_function(option,files_endsong):
    dicMus_art = {"": 0}
    dicArt = {"": 0}
    dicMus = {"": 0}
    if option == 0:
        for arquivo in files_endsong:
            with open(f'{arquivo}', 'r', encoding='utf-8') as end_song:
                dicMus = calc_mus(end_song,dicMus)
        return dicMus
    elif option == 1 :
        for arquivo in files_endsong:
            with open(f'{arquivo}', 'r', encoding='utf-8') as end_song:
                dicArt = calc_artist(end_song,dicArt)
        return dicArt
    else:
        print("Inform the artist's name:")
        artist_name = str(input()).split('\n')[0]
        for arquivo in files_endsong:
            with open(f'{arquivo}', 'r', encoding='utf-8') as end_song:
                dicMus_art = calcula_mus_artist(end_song,dicMus_art,artist_name)
        return dicMus_art

def visualize_and_write(top_dic, rank,option,option_label):
    index = 0
    label = ''
    if option_label == 1:
        label = 'Artist:'
    else:
        label = 'Music:'
    name = str(option).split(' ')[0]+str(rank)+str(option).split(' ')[1]+'.txt'
    text  = open (f'{name}','w')
    for i in sorted(top_dic, key=top_dic.get, reverse=True):
        tempo = calc_time(top_dic[i])
        line = str(index)+ " |"+ str(tempo)+ " |"+label+str(i)
        print(line)
        text.write(line+'\n')
        index += 1
        if index ==  rank:
            break
    print('Rank saved in file: '+name)

def menu(files_endsong):
    options = ['Top musics','Top artists','Top musics by artist']
    print('Choose a function: ')
    print('1 - Calculate top musics')
    print("2 - Calculate top artists")
    print('3 - Calculate top musics by individual artist')
    answer = int(input())
    while answer < 1 or answer > 3:
        print("Please, select a valid option (1),(2),(3)")
        print('1 - Calculate top musics')
        print("2 - Calculate top artists")
        print('3 - Calculate top musics by individual artist')
        answer = int(input())
    
    print('Alrigth, you choose {option} . Inform what rank do you want:'.format(option = options[answer-1]))
    rank = int(input())
    dic_choosen = aplly_function(answer-1,files_endsong)
    visualize_and_write(dic_choosen,rank,options[answer-1],answer-1)

def check_json_paths(path):
    files_endsong  = []
    for diretorio, subpastas, arquivos in os.walk(path):
        for arquivo in arquivos:
            if 'endsong_' in os.path.basename(arquivo):
                pth = os.path.join(diretorio,arquivo)
                files_endsong.append(pth)
    files_endsong.sort()
    return files_endsong
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--endsongs_path',
        type=str,
        help="Path to a folder containing the endsong files"
    )
    args = parser.parse_args()
    endsong_paths = check_json_paths(args.endsongs_path)
    print('Welcome to the Gus Topspot')
    while True:
        menu(endsong_paths)
        print('Do you wanto to rerun the progam ?')
        print("y - yes")
        print('n - no')
        flag = str(input()).lower()
        if flag == 'n' or flag =='no':
            print('Bye bye')
            break

if __name__ == '__main__':
    main()