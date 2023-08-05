import discord
from discord import app_commands
from discord.ext import commands
import os

token = "" #insert inside the "" the bot token



intents = discord.Intents.default()
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.event
async def on_ready():
    for server in bot.guilds:
        await bot.tree.sync(guild=discord.Object(id=server.id))
    print("Ready!")
    
    
@bot.tree.command(name = "makestats", description = "Make or refresh stats for your server, or for the current channel") #id a delete
@app_commands.describe(location = "channel or server")
async def makestats(ctx: discord.Interaction, location: str):
    
    if location == "channel" or location == "Channel" or location == "salon" or location == "Salon": #determine location in order to make stats
        await ctx.response.send_message("Processing...") #to prevent "application not responding"


################ Variables
        cci = ctx.channel.id
        cgi = ctx.guild.id
        count = 0
        folder = r'.\data_guild_' + str(cgi)
        Lcount = [100, 200, 500, 1000, 2000, 5000, 1000, 2000, 5000, 10000, 20000] + [i*20000 for i in range(2, 100)]

################


################Create folder and/or file
        if not os.path.exists(folder): #verifying if the data folder of the server(guild) exists
            
            os.makedirs(folder)
            os.chdir(folder)
            
            file = open("data_channel_"+str(cci)+".txt", "x") #automatically creates new file for the current channel
            file.close()
            
            data = []
            lim = False
            Lauthor = []
            L_change_author = []
            L_decal_author = []
            n = 0
            
        else:
            os.chdir(folder)
            try: #try to open the file if it already exists, and read data inside it
                
                file = open("data_channel_"+str(cci)+".txt", "r+") #read the file if it cans
                data = file.readlines()
                file.close()
################                


################Data reading and structuring                
                n = len(data)
                for i in range(n):
                    data[i] = data[i].rstrip("\n").split("@@@@")
                    m = len(data[i])
                    for j in range(1, m):
                        data[i][j] = data[i][j].split("@@@")
                        l = len(data[i][j])
                        for k in range(1, l):
                            data[i][j][k] = data[i][j][k].split("@@")
                            o = len(data[i][j][k])
                            for q in range(o):
                                data[i][j][k][q] = data[i][j][k][q].split("@")
                

                limitdate = str(data[0][1][0]).split(" ")[0] #limit date that needs to be refresh
                L = limitdate.split("-") #limit date list
                limitdateY = int(L[0])
                limitdateM = int(L[1])
                limitdateD = int(L[2])
                
                
                lim = True
                Lauthor = [e[0] for e in data]
                
                L_change_author = [1 for e in data]
                L_decal_author = [1 for e in data]
                
                for i in range(n): #reset data of the limit day
                    if limitdate == data[i][1][0]:
                        m = len(data[i][1][1])
                        for j in range(m):
                            data[i][1][1][j][1] = 0

                
            except:
                file = open("data_channel_"+str(cci)+".txt", "x") #create the new data file with the current channel
                file.close()
                
                lim = False
                data = []
                Lauthor = []
                L_change_author = []
                L_decal_author = []
                n = 0
################

        
################Scannig messages
        
        
        async for message in bot.get_channel(cci).history(limit=None): #analyze old messages
################
            
            
################Variables
            mauthor = str(message.author)
            mdate = str(message.created_at).split(" ")[0]
            L = mdate.split("-")
            mdateY = int(L[0])
            mdateM = int(L[1])
            mdateD = int(L[2])
            mtype = str(message.type)
            n2 = len(Lauthor)
            Lcount = [100, 200, 500, 1000, 2000, 5000, 1000, 2000, 5000, 10000, 20000] + [i*20000 for i in range(2, 100)]
################          


################Creating data      
            if mauthor not in Lauthor:  #if the author is new
                Lauthor.append(mauthor)
                L_change_author.append(1)
                L_decal_author.append(1)
                c = 1
                d = 1
                data.append([mauthor, [mdate, [[mtype, 1]]]])     #creates the data of this author and its msg
################
                

################Data Analyzing of not new author
            
            
            else: #the author isn't new

                n = len(data)
                i = 0
                while i <= n and Lauthor[i] != mauthor:
                    i += 1
                c = L_change_author[i]
                d = L_decal_author[i]
################
                    
                    
################Refreshing data
                
                if lim:  #if there is a limit=just need to refresh data
                    
                    
                    if limitdateY > mdateY:
                        break
                    elif limitdateY == mdateY:
                        if limitdateM > mdateM:
                            break
                        elif limitdateM == mdateM:
                            if limitdateD > mdateD: #if the date of the msg is now lower than the limit, it stops analyzing
                                break
      
                    if data[i][d][0] == mdate:
                        m = len(data[i][d][1])
                        j = 0

                        while j < m and data[i][d][1][j][0] != mtype: #searching if the type of data is already present
                            j += 1
                        if j < m:
                            count += 1
                            data[i][d][1][j][1] = int(data[i][d][1][j][1]) + 1   #add one to stats
                        else:
                            count += 1
                            data[i][d][1].insert(1, [mtype, 1])  #insert at the start the new type
                            


                    elif mdate == limitdate:
                        
                        d += 1
                        m = len(data[i][d][1])
                        j = 0

                        while j < m and data[i][d][1][j][0] != mtype: #searching if the type of data is already present
                            j += 1
                        if j < m:
                            count += 1
                            data[i][d][1][j][1] = int(data[i][d][1][j][1]) + 1   #add one to stats
                        else:
                            count += 1
                            data[i][d][1].insert(1, [mtype, 1])  #insert at the start the new type                  
                        L_decal_author[i] = d
                        
                        
                    else:
                        data[i].insert(c, [mdate, [[mtype, 1]]])
                        c += 1
                        if c != 2:
                            d = c - 1
                        L_change_author[i] = c
                        L_decal_author[i] = d
                        count += 1
                        
################
                        
            
################Creating data             
                else:
                    if data[i][-1][0] == mdate: #if a messsage from the author has already been sent the same day
                        m = len(data[i][-1][1])
                        j = 0
                        
                        while j < m and data[i][-1][1][j][0] != mtype: #searching if the type of data is already present
                            j += 1
                            
                        if j < m:
                            data[i][-1][1][j][1] = int(data[i][-1][1][j][1]) + 1   #add one to stats
                            count += 1
                        else:
                            data[i][-1][1].append([mtype, 1])   #append data type if it doesn't exist
                            count += 1   
                    
                    else:    #creates new date data if it doesn't exist
                        data[i].append([mdate, [[mtype, 1]]])                  
                        count += 1
################
                        

################Counting operations                             
            if count in Lcount:
                await ctx.channel.send(str(count)+" messages have been processed. Please wait more...")
################
   
   
################Stringing data
        n = len(data) 
        str_data = "" #[[author, [date, [[type, n], [type, n]]], [date, [[type, n], [type, n], [type, n]]]]]
        for i in range(n): #[author, [date, [[type, n], [type, n]]], [date, [[type, n], [type, n], [type, n]]]]
            
            str_data = str_data + str(data[i][0])  #author, 
            n3 = len(data[i])  
            for j in range(1, n3): #[date, [[type, n], [type, n]]]
                
                str_data = str_data + "@@@@" + str(data[i][j][0]) + "@@@" #date, 
                n4 = len(data[i][j]) 
                for k in range(1, n4): #[[type, n], [type, n]]
                    
                    n5 = len(data[i][j][k]) - 1
                    for l in range(n5): #[type, n]
                        
                        str_data = str_data + str(data[i][j][k][l][0]) + "@" + str(data[i][j][k][l][1]) +"@@" #type and n      #forbidden character: @, #, :, ```   https://discord.com/developers/docs/resources/user#usernames-and-nicknames
                    str_data = str_data + str(data[i][j][k][n5][0]) + "@" + str(data[i][j][k][n5][1])

            str_data += "\n"
################
            

################Writing data                         
        file = open("data_channel_"+str(cci)+".txt", "w")
        file.write(str_data)
        file.close()
        os.chdir('..\ ')
################


################Ending
        await ctx.channel.send("Done! " + str(count) +" messages were analyzed")
        count = 0
################        
              
              
               
              
              

    elif location == "server" or location == "Server" or location == "serveur" or location == "Serveur": #faire stats tout serveur
        await ctx.response.send_message("Processing...")
        count = 0
        ccount = 0
        
        for chan in ctx.guild.channels:
            if str(chan.type) == "text":

                
                
        ################ Variables
                cci = chan.id
                cgi = ctx.guild.id
                folder = r'.\data_guild_' + str(cgi)
                fic = ".\data_channel_" + str(cci) + ".txt"
                Lcount = [100, 200, 500, 1000, 2000, 5000, 1000, 2000, 5000, 10000, 20000] + [i*20000 for i in range(2, 100)]

        ################


        ################Create folder and/or file
                if not os.path.exists(folder): #verifying if the data folder of the server(guild) exists
                    
                    os.makedirs(folder)
                    os.chdir(folder)
                    
                    file = open(fic, "x") #automatically creates new file for the current channel
                    file.close()
                    
                    data = []
                    lim = False
                    Lauthor = []
                    L_change_author = []
                    L_decal_author = []
                    n = 0
                    
                else:
                    os.chdir(folder)
                    if os.path.exists(fic):   
                        file = open(fic, "r+") #read the file 
                        data = file.readlines()
                        file.close()
        ################                


        ################Data reading and structuring                
                        n = len(data)
                        for i in range(n):
                            data[i] = data[i].rstrip("\n").split("@@@@")
                            m = len(data[i])
                            for j in range(1, m):
                                data[i][j] = data[i][j].split("@@@")
                                l = len(data[i][j])
                                for k in range(1, l):
                                    data[i][j][k] = data[i][j][k].split("@@")
                                    o = len(data[i][j][k])
                                    for q in range(o):
                                        data[i][j][k][q] = data[i][j][k][q].split("@")
                        

                        limitdate = str(data[0][1][0]).split(" ")[0] #limit date that needs to be refresh
                        L = limitdate.split("-") #limit date list
                        limitdateY = int(L[0])
                        limitdateM = int(L[1])
                        limitdateD = int(L[2])
                        
                        
                        lim = True
                        Lauthor = [e[0] for e in data]
                        
                        L_change_author = [1 for e in data]
                        L_decal_author = [1 for e in data]
                        
                        for i in range(n): #reset data of the limit day
                            if limitdate == data[i][1][0]:
                                m = len(data[i][1][1])
                                for j in range(m):
                                    data[i][1][1][j][1] = 0

                        
                    else:
                        file = open(fic, "x") #create the new data file with the current channel
                        file.close()
                        
                        lim = False
                        data = []
                        Lauthor = []
                        L_change_author = []
                        L_decal_author = []
                        n = 0
        ################
                        

        ################Scannig messages
                
                
                async for message in bot.get_channel(cci).history(limit=None): #analyze old messages
        ################
                    
                    
        ################Variables
                    mauthor = str(message.author)
                    mdate = str(message.created_at).split(" ")[0]
                    L = mdate.split("-")
                    mdateY = int(L[0])
                    mdateM = int(L[1])
                    mdateD = int(L[2])
                    mtype = str(message.type)
                    n2 = len(Lauthor)
        ################          


        ################Creating data      
                    if mauthor not in Lauthor:  #if the author is new
                        Lauthor.append(mauthor)
                        L_change_author.append(1)
                        L_decal_author.append(1)
                        c = 1
                        d = 1
                        data.append([mauthor, [mdate, [[mtype, 1]]]])     #creates the data of this author and its msg
        ################
                        

        ################Data Analyzing of not new author
                    
                    
                    else: #the author isn't new

                        n = len(data)
                        i = 0
                        while i <= n and Lauthor[i] != mauthor:
                            i += 1
                        c = L_change_author[i]
                        d = L_decal_author[i]
                        
        ################
                            
                            
        ################Refreshing data
                        
                        if lim:  #if there is a limit=just need to refresh data
                            
                            
                            if limitdateY > mdateY:
                                break
                            elif limitdateY == mdateY:
                                if limitdateM > mdateM:
                                    break
                                elif limitdateM == mdateM:
                                    if limitdateD > mdateD: #if the date of the msg is now lower than the limit, it stops analyzing
                                        break
              
                            if data[i][d][0] == mdate:
                                m = len(data[i][d][1])
                                j = 0

                                while j < m and data[i][d][1][j][0] != mtype: #searching if the type of data is already present
                                    j += 1
                                if j < m:
                                    count += 1
                                    data[i][d][1][j][1] = int(data[i][d][1][j][1]) + 1   #add one to stats
                                else:
                                    count += 1
                                    data[i][d][1].insert(1, [mtype, 1])  #insert at the start the new type
                                    


                            elif mdate == limitdate:
                                
                                d += 1
                                m = len(data[i][d][1])
                                j = 0

                                while j < m and data[i][d][1][j][0] != mtype: #searching if the type of data is already present
                                    j += 1
                                if j < m:
                                    count += 1
                                    data[i][d][1][j][1] = int(data[i][d][1][j][1]) + 1   #add one to stats
                                else:
                                    count += 1
                                    data[i][d][1].insert(1, [mtype, 1])  #insert at the start the new type                  
                                L_decal_author[i] = d
                                
                                
                            else:
                                data[i].insert(c, [mdate, [[mtype, 1]]])
                                c += 1
                                if c != 2:
                                    d = c - 1
                                L_change_author[i] = c
                                L_decal_author[i] = d
                                count += 1
                                
        ################
                                
                    
        ################Creating data             
                        else:
                            if data[i][-1][0] == mdate: #if a messsage from the author has already been sent the same day
                                m = len(data[i][-1][1])
                                j = 0
                                
                                while j < m and data[i][-1][1][j][0] != mtype: #searching if the type of data is already present
                                    j += 1
                                    
                                if j < m:
                                    data[i][-1][1][j][1] += 1   #add one to stats
                                    count += 1
                                else:
                                    data[i][-1][1].append([mtype, 1])   #append data type if it doesn't exist
                                    count += 1   
                            
                            else:    #creates new date data if it doesn't exist
                                data[i].append([mdate, [[mtype, 1]]])                  
                                count += 1
        ################
                                

        ################Counting operations                             
                    if count in Lcount:
                        await ctx.channel.send(str(count)+" messages have been processed. Please wait more...")
        ################
           
           
        ################Stringing data
                n = len(data) 
                str_data = "" #[[author, [date, [[type, n], [type, n]]], [date, [[type, n], [type, n], [type, n]]]]]
                for i in range(n): #[author, [date, [[type, n], [type, n]]], [date, [[type, n], [type, n], [type, n]]]]
                    
                    str_data = str_data + str(data[i][0])  #author, 
                    n3 = len(data[i])  
                    for j in range(1, n3): #[date, [[type, n], [type, n]]]
                        
                        str_data = str_data + "@@@@" + str(data[i][j][0]) + "@@@" #date, 
                        n4 = len(data[i][j]) 
                        for k in range(1, n4): #[[type, n], [type, n]]
                            
                            n5 = len(data[i][j][k]) - 1
                            for l in range(n5): #[type, n]
                                
                                str_data = str_data + str(data[i][j][k][l][0]) + "@" + str(data[i][j][k][l][1]) +"@@" #type and n      #forbidden character: @, #, :, ```   https://discord.com/developers/docs/resources/user#usernames-and-nicknames
                            str_data = str_data + str(data[i][j][k][n5][0]) + "@" + str(data[i][j][k][n5][1])

                    str_data += "\n"
        ################
                    

        ################Writing data                         
                file = open("data_channel_"+str(cci)+".txt", "w")
                file.write(str_data)
                file.close()
                os.chdir('..\ ')
                ccount += 1
        ################


    ################Ending
        await ctx.channel.send("Done! "+str(ccount)+" channels and "+ str(count)+" messages were analyzed")
    ################        
                  
              

        
        
    else: #renvoie erreur
        await ctx.response.send_message("Error, the command is: `/makestats [location]`, with [location] = channel or [location] = server")
        
        
        
             
@bot.tree.command(name = "numberofmessages", description = "Count every messages in the server", guild=discord.Object(id=678273039154282496)) #id a delete
async def numberofmessages(ctx: discord.Interaction):
    count = 0
    cgi = ctx.guild.id
    folder = ".\data_guild_" + str(cgi)
    if not os.path.exists(folder):
        await ctx.response.send_message("Error, you must make stats of this server with `/makestats server`")
        
    if os.path.exists(folder):
        os.chdir(folder)
        for chan in ctx.guild.channels:
            cci = chan.id
            if str(chan.type) == "text":
                 
                fic = ".\data_channel_" + str(cci) + ".txt"
                file = open(fic, "r")
                data = file.readlines()
                file.close()
                n = len(data)
                for i in range(n):
                     
                    data[i] = data[i].rstrip("\n").split("@@@@")
                    
                    m = len(data[i])
                    for j in range(1, m):
                        data[i][j] = data[i][j].split("@@@")
                        l = len(data[i][j])
                        for k in range(1, l):
                            data[i][j][k] = data[i][j][k].split("@@")
                            o = len(data[i][j][k])
                            for q in range(o):
                                data[i][j][k][q] = data[i][j][k][q].split("@")
                                count += int(data[i][j][k][q][1])

            
        await ctx.response.send_message(str(count)+" messages have been sent in this server")
        os.chdir('..\ ')

@bot.tree.command(name = "numberofdifferentmembers", description = "Count every members in the server") #id a delete
async def numberofmessages(ctx: discord.Interaction):
    Lcount = []
    cgi = ctx.guild.id
    folder = ".\data_guild_" + str(cgi)
    if not os.path.exists(folder):
        await ctx.response.send_message("Error, you must make stats of this server with `/makestats server`")
        
    if os.path.exists(folder):
        os.chdir(folder)
        for chan in ctx.guild.channels:
            cci = chan.id
            if str(chan.type) == "text":
                 
                fic = ".\data_channel_" + str(cci) + ".txt"
                file = open(fic, "r")
                data = file.readlines()
                file.close()
                n = len(data)
                for i in range(n): 
                    data[i] = data[i].rstrip("\n").split("@@@@")
                    if data[i][0] not in Lcount:
                        Lcount.append(data[i][0])
          
        await ctx.response.send_message(str(len(Lcount))+" different members have sent one message(or more) in this server")
        os.chdir('..\ ')
                
                                     
                
    else:
        await ctx.response.send_message("Error, not every channels of this server were analyzed. You need first to write the command: `/makestats server`")
        
                
    

    
bot.run(token)
