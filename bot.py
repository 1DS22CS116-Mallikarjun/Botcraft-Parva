import discord
from discord.ext import commands
import random

# Create intents
intents = discord.Intents.default()
intents.presences = True  # Enable Presence Intent
intents.members = True    # Enable Server Members Intent
intents.message_content = True  # Enable Message Content Intent

# Bot token and channel ID
BOT_TOKEN = ""
CHANNEL_ID = ''

# Create a bot instance with the specified intents and command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# In-memory storage for user skills, teams, tasks, and competitions
user_skills = {}
teams = {}
tasks = {}
competitions = {}

# Predefined skills
PREDEFINED_SKILLS = {"python", "c", "java", "full stack","Front end","Back end"}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Send a message to the specified channel when the bot starts
    channel = bot.get_channel(CHANNEL_ID)
    if channel is not None:
        await channel.send("Hello, I am your community bot! Type !help to see available commands.")
    else:
        print("Channel not found!")

# User skills commands
@bot.command()
async def connect(ctx, *, skill):
    """Find users with a specific skill."""
    await ctx.send(f'Looking for users with the skill: {skill}')

@bot.command()
async def request_mentor(ctx):
    """Request a mentor."""
    await ctx.send(f'{ctx.author.name} is looking for a mentor!')

@bot.command()
async def form_team(ctx, team_name, skill):
    """Create a project team associated with a specific skill."""
    if team_name in teams:
        await ctx.send(f'Team "{team_name}" already exists.')
    else:
        teams[team_name] = {'members': [], 'skill': skill}  # Initialize the team with an empty member list and associated skill
        await ctx.send(f'Team "{team_name}" has been created with the skill "{skill}"!')

@bot.command()
async def add_member(ctx, team_name: str, member: discord.Member):
    """Add a member to a team."""
    if team_name in teams:
        if member.id not in teams[team_name]['members']:
            teams[team_name]['members'].append(member.id)
            await ctx.send(f'{member.name} has been added to team "{team_name}".')
        else:
            await ctx.send(f'{member.name} is already a member of team "{team_name}".')
    else:
        await ctx.send(f'Team "{team_name}" does not exist.')

@bot.command()
async def list_team_members(ctx, team_name):
    """List all members of a team."""
    if team_name in teams:
        member_names = [f'<@{member_id}>' for member_id in teams[team_name]['members']]
        await ctx.send(f'Members of team "{team_name}": {", ".join(member_names) if member_names else "No members yet."}')
    else:
        await ctx.send(f'Team "{team_name}" does not exist.')

@bot.command()
async def add_skill(ctx, *, skill):
    """Add a predefined skill for the user."""
    skill = skill.lower()
    if skill in PREDEFINED_SKILLS:
        user_id = ctx.author.id
        if user_id in user_skills:
            user_skills[user_id].add(skill)
        else:
            user_skills[user_id] = {skill}
        await ctx.send(f'Skill "{skill}" added for {ctx.author.name}.')
    else:
        await ctx.send(f'Invalid skill. Please choose from the following: {", ".join(PREDEFINED_SKILLS)}')

@bot.command()
async def connect_users(ctx, *, skill):
    """Connect users with a specific skill and show existing teams."""
    skill = skill.lower()
    connected_users = [user for user, skills in user_skills.items() if skill in skills]
    
    # Check for existing teams for the given skill
    existing_teams = [team for team in teams.keys() if teams[team]['skill'] == skill]

    if connected_users:
        user_mentions = ', '.join([f'<@{user}>' for user in connected_users])
        await ctx.send(f'Users with the skill "{skill}": {user_mentions}')
    else:
        await ctx.send(f'No users found with the skill "{skill}".')

    if existing_teams:
        await ctx.send(f'Existing teams for the skill "{skill}": {", ".join(existing_teams)}')
    else:
        await ctx.send(f'No teams found for the skill "{skill}". Would you like to create a new team? Use !form_team <team_name> <skill> to create one.')

@bot.command()
async def list_skills(ctx):
    """List all skills of the user."""
    user_id = ctx.author.id
    skills = user_skills.get(user_id, set())
    if skills:
        await ctx.send(f'{ctx.author.name}\'s skills: {", ".join(skills)}')
    else:
        await ctx.send(f'{ctx.author.name} has no skills listed. Use !add_skill <skill> to add one.')

@bot.command()
async def coworking_room(ctx):
    """Create a virtual coworking room with a Google Meet link."""
    # Simulate generating a Google Meet link
    google_meet_link = "https://meet.google.com/" + ''.join(random.choices('0123456789', k=10))
    
    await ctx.send(f'🛠️ **Virtual Coworking Room** 🛠️\nJoin others to work together! Use this channel to share your current tasks and progress. Let’s boost productivity!\n\nJoin the meeting here: {google_meet_link}')

@bot.command()
async def project_management(ctx, *, task):
    """Manage a project task."""
    await ctx.send(f'📋 **Project Management** 📋\nTask added: "{task}".\nKeep track of your tasks and collaborate with your team!')

@bot.command()
async def brainstorming_prompt(ctx):
    """Provide a brainstorming prompt."""
    prompts = [
        "What are three ways we can improve our current project?",
        "How can we make our product more user-friendly?",
        "What features would you like to see in our next update?",
        "If budget were no concern, what would you add to our project?",
        "What are some potential roadblocks we might face, and how can we overcome them?"
    ]
    prompt = random.choice(prompts)
    await ctx.send(f'💡 **Brainstorming Prompt** 💡\nHere’s a prompt to get your ideas flowing: {prompt}')

# Task management commands
@bot.command(name='add_task')
async def add_task(ctx, task_name: str, deadline: str):
    """Create a new task."""
    task_id = len(tasks) + 1  # Simple task id generation
    tasks[task_id] = {"task_name": task_name, "deadline": deadline, "completed": False}
    await ctx.send(f"Task added: {task_name} with a deadline of {deadline}.")

@bot.command(name='list_tasks')
async def list_tasks(ctx):
    """List all tasks."""
    if not tasks:
        await ctx.send("No tasks found.")
        return
    task_list = "\n".join([f"Task ID: {task_id} - {task['task_name']} (Deadline: {task['deadline']}) - {'Completed' if task['completed'] else 'Not Completed'}" 
                          for task_id, task in tasks.items()])
    await ctx.send(f"Here are your tasks:\n{task_list}")

@bot.command(name='complete_task')
async def complete_task(ctx, task_id: int):
    """Mark a task as completed."""
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        await ctx.send(f"Task {task_id} marked as completed.")
    else:
        await ctx.send(f"Task with ID {task_id} not found.")

@bot.command(name='delete_task')
async def delete_task(ctx, task_id: int):
    """Delete a task."""
    if task_id in tasks:
        del tasks[task_id]
        await ctx.send(f"Task {task_id} deleted.")
    else:
        await ctx.send(f"Task with ID {task_id} not found.")

# Competition management commands
@bot.command()
async def create_competition(ctx, name: str):
    """Create a new competition."""
    if name in competitions:
        await ctx.send(f'Competition "{name}" already exists!')
        return

    competitions[name] = {
        'participants': {},
        'entries': {},
        'winner': None
    }
    await ctx.send(f'Competition "{name}" created!')

@bot.command()
async def join_competition(ctx, name: str):
    """Join a competition."""
    if name not in competitions:
        await ctx.send(f'Competition "{name}" does not exist!')
        return

    user = ctx.author.name
    if user in competitions[name]['participants']:
        await ctx.send(f'You are already participating in "{name}".')
    else:
        competitions[name]['participants'][user] = 0  # Initialize score
        await ctx.send(f'You have joined the competition "{name}".')

@bot.command()
async def submit_entry(ctx, name: str, entry: str):
    """Submit an entry for a competition."""
    if name not in competitions:
        await ctx.send(f'Competition "{name}" does not exist!')
        return

    user = ctx.author.name
    if user not in competitions[name]['participants']:
        await ctx.send(f'You need to join the competition "{name}" first.')
        return

    competitions[name]['entries'][user] = entry
    await ctx.send(f'Entry submitted for "{name}": {entry}')

@bot.command()
async def leaderboard(ctx, name: str):
    """View the leaderboard for a competition."""
    if name not in competitions:
        await ctx.send(f'Competition "{name}" does not exist!')
        return

    leaderboard = "Leaderboard for *{}*:\n".format(name)
    for user, score in competitions[name]['participants'].items():
        entry = competitions[name]['entries'].get(user, "No entry submitted")
        leaderboard += f"{user}: Score: {score}, Entry: {entry}\n"

    await ctx.send(leaderboard)

@bot.command()
async def declare_winner(ctx, name: str, winner: str):
    """Declare a winner for a competition."""
    if name not in competitions:
        await ctx.send(f'Competition "{name}" does not exist!')
        return

    if winner not in competitions[name]['participants']:
        await ctx.send(f'{winner} is not a participant in "{name}".')
        return

    competitions[name]['winner'] = winner
    await ctx.send(f'The winner of "{name}" is {winner}!')
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    await ctx.send(f'Cleared {amount} messages.', delete_after=5)  

# Run the bot with your token
bot.run(BOT_TOKEN)