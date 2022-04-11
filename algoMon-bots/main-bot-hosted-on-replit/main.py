import discord
from replit import db
from keep_alive import keep_alive
from table2ascii import table2ascii as t2a, PresetStyle



client = discord.Client()
if "responding" not in db.keys():
  db["responding"] = True
  
if not "numOfCourses" in db.keys(): 
    db["numOfCourses"] = 0
if not "registeredUsers" in db.keys():
    db["registeredUsers"] = []
def addCourse(courseName,courseRequirements):
    if courseName in db.keys():
        return "Course Already Exists."
    else:
        totalCourses = db["numOfCourses"]
        totalCourses = totalCourses + 1
        preReq = []
        for course in courseRequirements:
            if int(course)>0 and int(course)<totalCourses:
                preReq.append(course)
            else:
                return "Course Requirement is incorrect."
        db["numOfCourses"] = totalCourses
        db["course"+str(totalCourses)] = courseName
        db[courseName] = preReq
        return "Course added successfully."

def updateRequirements(courseName,courseReqs):
    if not courseName in db.keys():
        return False
    else:
        for req in courseReqs:
            if req in db[courseName]:
                continue
            db[courseName].append(req)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
      
    msg = message.content
    if message.content.startswith('!hello'):
        embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.add_field(name="Field2", value="hi2", inline=False)
        await message.channel.send(embed=embedVar)

    user = message.author.id

    if msg.startswith(".register"):
        if str(user) in db.keys():
            embedVar = discord.Embed(title="User Registration", description="The user has been registered before.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
        else:
            db[str(user)] = []
            users = db["registeredUsers"]
            users.append(user)
            db["registeredUsers"] = users
            embedVar = discord.Embed(title="User Registration", description="User registered successfully.", color=0x00ff00)
            await message.channel.send(embed=embedVar)

    if msg.startswith(".list"):
        embedVar = discord.Embed(title="Algorithms available", description="We have {} algorithms.".format(db["numOfCourses"]), color=0x00ff00)
        for i in range(db["numOfCourses"]):
            courseNum = i + 1
            prereq = "> Pre-requisites:\n"
            for preq in db[db[str("course"+str(courseNum))]]:
                prereqName = db["course"+str(preq)]
                prereq = prereq + f"> {preq}. {prereqName}\n"
            courseName = db["course"+str(courseNum)]
            if len(db[db[str("course"+str(courseNum))]]) == 0:
                prereq = prereq + "> None"
            embedVar.add_field(name=f"{courseNum}. {courseName}", value= prereq+"\n", inline=False)
        await message.channel.send(embed=embedVar)

    if msg.startswith(".addCourse"):
        parts = msg.split()
        if len(parts) < 3:
            print(parts)
            embedVar = discord.Embed(title="Addition of Algorithms", description="Invalid command.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
        else:
            reqs = []
            valid = True
            for i in range(2,len(parts)):
                if parts[i].isnumeric():
                    if int(parts[i])!=0:
                      reqs.append(int(parts[i]))
                else:
                    valid = False
                    break
            if valid:
                returnMsg = addCourse(parts[1],list(reqs))
                embedVar = discord.Embed(title="Addition of Algorithms", description=returnMsg, color=0x00ff00)
                await message.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title="Addition of Algorithms", description="Invalid command.", color=0x00ff00)
                await message.channel.send(embed=embedVar)
    
    if msg.startswith(".user"):
        words = msg.split()
        if len(words)!=2:
            embedVar = discord.Embed(title="Progress of a user", description="Invalid command.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
        else:
            userID = words[1].strip("<")
            userID = userID.strip(">")
            userID = userID.strip("@")
            userID = userID.strip("!")
            if int(userID) in db["registeredUsers"]:
                completed = db[str(userID)]
                embedVar = discord.Embed(title="Progress of a user", description=f"The user has completed {len(completed)} algorithms.", color=0x00ff00)
                done = f"**Stats for** <@!{userID}>\n"
                done = done + "> Algorithms/Techniques completed:\n"
                num = 1
                for courseNo in completed:
                    algoName = db["course"+str(courseNo)]
                    done = done + f"> {num}. {algoName}\n"
                    num = num + 1
                if len(completed) == 0:
                    done = done + "> None"
                embedVar.add_field(name="** **", value= done, inline=False)
                await message.channel.send(embed=embedVar)
            else:
                embedVar = discord.Embed(title="Progress of a user", description="The user doesn't exist in database.", color=0x00ff00)
                await message.channel.send(embed=embedVar)

    if msg.startswith(".stats"):
        stats =[]
        num = 1
        for user in db["registeredUsers"]:
            userStat = [str(num)]
            num = num + 1
            userProfile = await client.fetch_user(user)
            userStat.append(str(userProfile.display_name))
            userStat.append(str(len(db[str(user)])))
            stats.append(userStat)
        output = "```" + t2a(
            header=["S.No.", "Name", "Algorithms completed"],
            body=list(stats), 
            first_col_heading=True
        ) + "```"
        embedVar = discord.Embed(title="Server Stats", description=output, color=0x00ff00)
        await message.channel.send(embed=embedVar)
        # await message.channel.send(f"```\n{output}\n```")
    
    if msg.startswith(".courseCompleted"):
        if int(user) != 760247935681560658:
            embedVar = discord.Embed(title="Course Completion", description="You are not allowed to enter this command.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return
        words = msg.split()
        if len(words)!= 3:
            embedVar = discord.Embed(title="Course Completion", description="Invalid command", color=0x00ff00)
            await message.channel.send(embed=embedVar)
        else:
            userID = words[1].strip("<")
            userID = userID.strip(">")
            userID = userID.strip("@")
            userID = userID.strip("!")
            valid = True
            if not int(userID) in list(db["registeredUsers"]):
                valid = False
            if not words[2].isnumeric():
                valid = False
            if not valid:
                embedVar = discord.Embed(title="Course Completion", description="Invalid command", color=0x00ff00)
                await message.channel.send(embed=embedVar)
            else:
                courseNum = int(words[2])
                if courseNum > 0 and courseNum <= db["numOfCourses"]:
                    completed = db[str(userID)]
                    completed.append(courseNum)
                    db[str(userID)] = completed
                    embedVar = discord.Embed(title="Course Completion", description="Course list updated.", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(title="Course Completion", description="Invalid Course", color=0x00ff00)
                    await message.channel.send(embed=embedVar)
    
    if msg.startswith(".learn"):
        words = msg.split()
        if len(words) != 2:
            embedVar = discord.Embed(title="Learning", description="Invalid command.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return
        if not user in db["registeredUsers"]:
            embedVar = discord.Embed(title="Learning", description="User not registered.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return
        courseNo = words[1]
        if not courseNo.isnumeric():
            embedVar = discord.Embed(title="Learning", description="The course number entered is invalid.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return
        if int(courseNo) in db[str(user)]:
            embedVar = discord.Embed(title="Learning", description="You have already acquired this skill!", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return

        if int(courseNo) < 1 or int(courseNo) > db["numOfCourses"]:
            embedVar = discord.Embed(title="Learning", description="The course number entered is invalid.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return
        preReqsSatisfied = True
        coursesCompleted = db[str(user)]
        for preq in db[db[str("course"+str(courseNo))]]:
            if not preq in coursesCompleted:
                preReqsSatisfied = False
        if not preReqsSatisfied:
            embedVar = discord.Embed(title="Learning", description="Pre-requisistes not satisfied by user.", color=0x00ff00)
            await message.channel.send(embed=embedVar)
            return
        courseName = db["course"+str(courseNo)]    
        embedVar = discord.Embed(title="Learning", description="All pre-requisites satisfied. User is ready to learn the algorithm" + courseName, color=0x00ff00)
        await message.channel.send(embed=embedVar)
                

    


for key in db.keys():
  print(key,db[str(key)])

BOT_TOKEN= ""

keep_alive()
client.run(BOT_TOKEN)

