import os
import requests
import json
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
#Discord_tok = os.getenv('Discord_tok')
Apex_tok = os.getenv('Apex_tok')

def Extract_Apex_func(platform,player_name): #sole purpose is to send a request for info
    txt_output = 'players' #folder path to save txt files of player jsons
    if not os.path.exists(txt_output): #creates folder if path doesnt exist
        os.makedirs(txt_output)

    url = f'https://api.mozambiquehe.re/bridge?player={player_name}&platform={platform}' #url to extract player info
    headers = {'Authorization':Apex_tok} #loads headers with token  
    response =requests.get(url, headers = headers) #sends request with player info and token
    if response.ok == True: #checks if response 200...data recieved
        print(f'Data was recieved for {player_name}!') 
        player_info = response.text
        path = os.path.join(txt_output,player_name) 
        with open(f'{path}.txt','w',encoding='utf-8') as file:
            file.write(str(player_info))
        return Read_Apex(player_name)
    else:
        print(f'Player {player_name} not found...')   

def Read_Apex(player_name):
    rank_number = ""
    txt_input = 'players'
    json_files = [file for file in os.listdir(txt_input) if file.endswith('.txt')] #gets any text files and checks for playername in files
    if f'{player_name}.txt' in json_files:
        file_path = os.path.join(txt_input, f'{player_name}.txt')
        with open(file_path, 'r',encoding='utf-8') as json_file: #open unicode 8 to include japanese/any characters
            player_json  = json.load(json_file)
        #Data to be taken in 
        IGN = player_json.get('global').get('name') # extracts info from player json
        UID = player_json.get('global').get('uid')
        platform = player_json.get('global').get('platform')
        level = player_json.get('global').get('level')
        rankScore = player_json.get('global').get('rank').get('rankScore')
        rankName = player_json.get('global').get('rank').get('rankName')

        imgRANKURL = player_json.get('global').get('rank').get('rankImg') #Gets rank image URL for download
        download_image(imgRANKURL,f'{player_name}_rankImg')
        for char in imgRANKURL: #Extracts division rank from URL
            if char.isdigit():
                rank_number += char
                break
        true_rank = f'{rankName} {rank_number}' 
        #print(imgRANKURL)
        imgAVATARURL = player_json.get('global').get('avatar')
        download_image(imgAVATARURL,f'{player_name}_AvatarImg')
        #print(f'In game name: {IGN}\nUnique playerID: {UID}\nPlayer Platform: {platform}\nPlayer level: {level}\nRanked points: {rankScore}\nRank: {rankName}\n')
        reply = f'In game name: {IGN}\nUnique playerID: {UID}\nPlayer Platform: {platform}\nPlayer level: {level}\nRanked points: {rankScore}\nRank: {true_rank}\n' #string reply
        image_edit(player_name)
        return reply

def image_edit(player_name): #image resizing and combiniation
    size = (150,150)
    for filename in os.listdir('images'): #resizes images
        if filename.endswith('.png'):
            img_path = os.path.join('images',filename)
            img = Image.open(img_path)
            img.thumbnail(size)
            img.save(f'images/{filename}')
    
    image1 = Image.open(os.path.join('images', f"{player_name}_rankImg.png")) #opens images to be used in combination
    image2 = Image.open(os.path.join('images', f"{player_name}_AvatarImg.png"))

    width1, height1 = image1.size
    width2, height2 = image2.size

    total_width = width1 + width2
    max_height = max(height1, height2)

    combined_image = Image.new('RGBA', (total_width, max_height)) #new image converted to RGBA else will give ugly warning
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (width1, 0)) #pastes images side by side
    #combined_image.convert("RGBA")
    output_path = os.path.join('images', f"{player_name}_combined_image.png") #creates image path to save image as combined image
    combined_image.save(output_path)
    combined_image.close()
    image1.close()
    image2.close() 

    os.remove(f'images/{player_name}_rankImg.png') #frees space from now unused images
    os.remove(f'images/{player_name}_AvatarImg.png')


def download_image(url,player_name): #general download image function
    output_folder = 'images'
    if not os.path.exists(output_folder): #creates folder if path doesnt exist
        os.makedirs(output_folder)

    response = requests.get(url)
    
    with open(f'{output_folder}/{player_name}.png','wb') as file:
        file.write(response.content)