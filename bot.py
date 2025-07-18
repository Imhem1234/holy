import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# HELLO COMMAND
@bot.command()
async def hello(ctx):
    await ctx.send("HELLO! I'M YOUR CUSTOM BOT.")

# SENDBIG COMMAND (PLAIN TEXT FEATURES)
@bot.command()
async def sendbig(ctx):
    message = """
🏀 HOLY SERVICES
┓┓┓┓┓┓┓┓┓┓┓┓┓┓┓┓
HOLY SERVICES SCRIPT FEATURES
 ━━━━━━━━━━━━━━━━

ARCADE BASKETBALL:
• PLAYER SPEED
• AUTO GREEN
• INFINITE STAMINA
• UNLOCK ALL — THIS IS SERVER SIDED. EVERYONE CAN SEE IT AND IT STICKS, INCLUDING MASCOTS
• FULL CONTROLLER SUPPORT

ALL STARS REMASTERED:
• AUTO GREEN
• INFINITE STAMINA
• DUNK FROM ANYWHERE
• PLAYER SPEED
• CONTROLLER SUPPORT
"""
    await ctx.send(message)

# TICKET INFO (PLAIN TEXT)
@bot.command()
async def ticketinfo(ctx):
    message = """
🎟️ CREATE A TICKET
 ━━━━━━━━━━━━━━━━
CREATE A TICKET IF YOU ARE PURCHASING OR NEED SUPPORT.

💵 PRICING:
• WEEKLY: $3
• MONTHLY: $6
• LIFETIME: $12

💳 METHODS:
• ROBUX
• CASHAPP
• APPLE PAY
• GIFTCARDS
"""
    await ctx.send(message)

# HOLY FEATURES GUI
@bot.command()
async def holyfeatures(ctx):
    embed = discord.Embed(
        title="🏀 HOLY SERVICES – SCRIPT FEATURES",
        description="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="🔹 ARCADE BASKETBALL",
        value="""
yaml
• Player Speed
• AUTO GREEN
• INFINITE STAMINA
• UNLOCK ALL — SERVER SIDED (VISIBLE TO ALL, INCLUDES MASCOTS)
• FULL CONTROLLER SUPPORT
""",
        inline=False
    )

    embed.add_field(
        name="⭐ ALL STARS REMASTERED",
        value="""
yaml
• AUTO GREEN
• INFINITE STAMINA
• DUNK FROM ANYWHERE
• PLAYER SPEED
• CONTROLLER SUPPORT
""",
        inline=False
    )

    embed.set_footer(text="🏀 HOLY SERVICES • PREMIUM SCRIPTS")
    embed.set_image(url="https://i.imgur.com/iaLU1SY.png")
    await ctx.send(embed=embed)

# HOLY GAMES GUI
@bot.command()
async def holygames(ctx):
    embed = discord.Embed(
        title="🎮 HOLY SERVICES – SUPPORTED GAMES",
        description="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="✅ CURRENTLY SUPPORTED",
        value="""
yaml
• Arcade Basketball
• All Stars Remastered
""",
        inline=False
    )

    embed.add_field(
        name="🕒 COMING SOON",
        value="""
yaml
• RH2
• RBW5
• Many other games...
""",
        inline=False
    )

    embed.set_footer(text="🏀 HOLY SERVICES • GAME SUPPORT LIST")
    embed.set_image(url="https://i.imgur.com/iaLU1SY.png")
    await ctx.send(embed=embed)

# CLOSE TICKET VIEW
class CloseTicketView(View):
    def __init__(self, ticket_channel, author, staff_role):
        super().__init__(timeout=None)
        self.ticket_channel = ticket_channel
        self.author = author
        self.staff_role = staff_role

    @discord.ui.button(label="❌ Close Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        if interaction.user == self.author or self.staff_role in interaction.user.roles:
            await interaction.response.send_message("🔐 Closing this ticket in 5 seconds...", ephemeral=True)
            await self.ticket_channel.send(f"🔐 Ticket closed by {interaction.user.mention}. Deleting...")
            await asyncio.sleep(5)
            await self.ticket_channel.delete()
        else:
            await interaction.response.send_message("❌ You don't have permission to close this ticket.", ephemeral=True)

# TICKET PANEL VIEW
class TicketPanel(View):
    @discord.ui.button(label="🎟️ Create Ticket", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        author = interaction.user

        existing_channel = discord.utils.get(guild.channels, name=f"ticket-{author.name.lower()}")
        if existing_channel:
            await interaction.response.send_message(f"📌 You already have a ticket open: {existing_channel.mention}", ephemeral=True)
            return

        staff_role = discord.utils.get(guild.roles, name="Staff")
        if not staff_role:
            await interaction.response.send_message("❌ No role named Staff found.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        category = discord.utils.get(guild.categories, name="Tickets")
        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{author.name}",
            overwrites=overwrites,
            reason=f"Support ticket for {author}",
            category=category
        )

        view = CloseTicketView(ticket_channel=ticket_channel, author=author, staff_role=staff_role)

        await ticket_channel.send(
            f"🎛 {author.mention}, welcome to your ticket! A staff member will be with you shortly.\nUse the button below to close the ticket when you're done.",
            view=view
        )

        await interaction.response.send_message(f"✅ Ticket created: {ticket_channel.mention}", ephemeral=True)

# TICKETPANEL GUI
@bot.command()
async def ticketpanel(ctx):
    embed = discord.Embed(
        title="🎟️ HOLY SERVICES SUPPORT CENTER",
        description=(
            "**Need help? Want to purchase a package?**\n"
            "Click the button below to create a private support ticket.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "**📌 WHAT WE OFFER:**\n"
            "• Fast Support\n"
            "• Professional Help\n"
            "• Secure Transactions\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        color=discord.Color.purple()
    )

    embed.add_field(
        name="💵 PRICING PLANS",
        value="""
yaml
• WEEKLY: $3
• MONTHLY: $6
• LIFETIME: $12
""",
        inline=False
    )

    embed.add_field(
        name="💳 ACCEPTED PAYMENT METHODS",
        value="""
yaml
• ROBUX
• CASHAPP
• APPLE PAY
• GIFT CARDS
""",
        inline=False
    )

    embed.set_image(url="https://i.imgur.com/iaLU1SY.png")
    embed.set_footer(text="🚇 HOLY SERVICES • OPEN A TICKET BELOW")

    await ctx.send(embed=embed, view=TicketPanel())

# RUN THE BOT
bot.run("MTM5NTA4NTA3NDY3NTc5ODA2Nw.G1OiIe.ef02Jl603iNW91AwOj0Zs77nrTKRUH4p9X1fuM")
