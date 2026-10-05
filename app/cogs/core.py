import discord
from discord.ext import commands

class CoreCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context):
        guild = ctx.guild
        await self.bot.repo.ensure_guild(guild.id, guild.name)
        role = discord.utils.get(guild.roles, name="Proxima Mod")
        if not role:
            role = await guild.create_role(name="Proxima Mod", permissions=discord.Permissions(administrator=True), reason="Proxima setup")
        category = discord.utils.get(guild.categories, name="Proxima Private")
        if not category:
            overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False), role: discord.PermissionOverwrite(view_channel=True)}
            category = await guild.create_category("Proxima Private", overwrites=overwrites)
        for name in ("proxima-announcements", "proxima-logs"):
            if not discord.utils.get(category.text_channels, name=name):
                await guild.create_text_channel(name, category=category)
        await ctx.send("✅ Proxima SaaS tenant initialized.")

    @commands.command(name="help")
    async def help_cmd(self, ctx):
        e = discord.Embed(title="Proxima", description="Tournament and scrim management", color=0xC45AEC)
        e.add_field(name="Tournament", value="`!tsetup <slots> <mentions> <slots_per_group>`\n`!sttorny <id>` `!sptorny <id>` `!dltorny <id>`", inline=False)
        e.add_field(name="Scrims", value="`!ssetup <name> <slots> <mentions>`\n`!sttscrim <id>` `!spscrim <id>` `!dlscrim <id>`", inline=False)
        e.add_field(name="Utility", value="`!setup` `!clear <amount>`", inline=False)
        await ctx.send(embed=e)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: commands.Range[int, 1, 99]):
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Deleted {max(0, len(deleted)-1)} message(s).", delete_after=5)

async def setup(bot): await bot.add_cog(CoreCog(bot))
