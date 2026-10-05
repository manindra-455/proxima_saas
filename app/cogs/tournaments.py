import random, string
import discord
from discord.ext import commands

class TournamentCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tsetup(self, ctx, slots: commands.Range[int, 12, 1000], mentions: commands.Range[int, 0, 10], slots_per_group: commands.Range[int, 1, 25]):
        category = await ctx.guild.create_category(f"Tournament-{ctx.message.id}")
        manager = await ctx.guild.create_role(name=f"{category.name} Tournament Manager")
        await ctx.guild.create_role(name=f"{category.name} Confirmed")
        for name in ("info", "updates", "register-here", "confirmed-teams", "queries", "ss-verify", "tag-check"):
            channel = await ctx.guild.create_text_channel(name, category=category)
            if name in {"info", "updates", "confirmed-teams"}:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
                await channel.set_permissions(manager, send_messages=True)
        tournament_id = "".join(random.choices(string.digits, k=4))
        data = {"category_id": category.id, "slots": slots, "mentions_required": mentions, "slots_per_group": slots_per_group, "active": False}
        await self.bot.repo.create_tournament(ctx.guild.id, tournament_id, data)
        await self.bot.repo.set_registration(ctx.guild.id, category.id, data)
        await ctx.send(embed=discord.Embed(title="Tournament created", description=f"ID: `{tournament_id}`", color=0xC45AEC))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sttorny(self, ctx, tournament_id: str): await self._active(ctx, tournament_id, True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sptorny(self, ctx, tournament_id: str): await self._active(ctx, tournament_id, False)

    async def _active(self, ctx, tournament_id, active):
        item = await self.bot.repo.get_tournament(ctx.guild.id, tournament_id)
        if not item: return await ctx.send("Tournament not found.")
        item["active"] = active
        await self.bot.repo.create_tournament(ctx.guild.id, tournament_id, item)
        await ctx.send(f"Tournament `{tournament_id}` {'started' if active else 'stopped'}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dltorny(self, ctx, tournament_id: str):
        item = await self.bot.repo.get_tournament(ctx.guild.id, tournament_id)
        if not item: return await ctx.send("Tournament not found.")
        category = ctx.guild.get_channel(item["category_id"])
        if category:
            for channel in category.channels: await channel.delete(reason="Tournament deleted")
            await category.delete(reason="Tournament deleted")
        await self.bot.repo.delete_tournament(ctx.guild.id, tournament_id)
        await ctx.send(f"Tournament `{tournament_id}` deleted.")

async def setup(bot): await bot.add_cog(TournamentCog(bot))
