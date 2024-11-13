import discord
from discord.ext import commands

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

# Dictionary to store user skills
user_skills = {}

# Predefined skills
PREDEFINED_SKILLS = {"python", "c", "java", "full stack"}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Send a message to the specified channel when the bot starts
    channel = bot.get_channel(CHANNEL_ID)
    if channel is not None:
        await channel.send("Hello, I am your community bot! Type !help to see available commands.")
    else:
        print("Channel not found!")

@bot.command()
async def connect(ctx, *, skill):
    """Find users with a specific skill."""
    await ctx.send(f'Looking for users with the skill: {skill}')

@bot.command()
async def request_mentor(ctx):
    """Request a mentor."""
    await ctx.send(f'{ctx.author.name} is looking for a mentor!')

@bot.command()
async def form_team(ctx, *, project):
    """Form a project team."""
    await ctx.send(f'Creating a team for the project: {project}')

@bot.command()
async def challenge(ctx):
    """Start a group challenge."""
    await ctx.send('Join our weekly coding challenge! Submit your solutions by Friday!')

@bot.command()
async def meetup(ctx):
    """Announce a virtual meetup."""
    await ctx.send('Join us for a virtual meetup this Saturday at 5 PM!')

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
    """Connect users with a specific skill."""
    skill = skill.lower()
    connected_users = [user for user, skills in user_skills.items() if skill in skills]
    
    if connected_users:
        user_mentions = ', '.join([f'<@{user}>' for user in connected_users])
        await ctx.send(f'Users with the skill "{skill}": {user_mentions}')
    else:
        await ctx.send(f'No users found with the skill "{skill}".')

@bot.command()
async def list_skills(ctx):
    """List all skills of the user."""
    user_id = ctx.author.id
    skills = user_skills.get(user_id, set())
    if skills:
        await ctx.send(f'Your skills: {", ".join(skills)}')
    else:
        await ctx.send('You have no skills listed. Use !add_skill <skill> to add one.')

# Run the bot with your token
bot.run(BOT_TOKEN)