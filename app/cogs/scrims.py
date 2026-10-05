import random, string
import discord
from discord.ext import commands

class ScrimCog(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command(name="ssetup")
    @commands.has_permissions(administrator=True)
    async def scrim_setup(self, ctx, name: str, slots: commands.Range[int, 12, 25], mentions: commands.Range[int, 0, 10]):
        category = await ctx.guild.create_category(f"Scrim-{name}")
        role = await ctx.guild.create_role(name=f"{name} IDP")
        registration = await ctx.guild.create_text_channel(f"{name}-registration", category=category)
        idp = await ctx.guild.create_text_channel(f"{name}-idp", category=category)
        await idp.set_permissions(ctx.guild.default_role, send_messages=False)
        await idp.set_permissions(role, send_messages=True)
        scrim_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        await self.bot.repo.create_scrim(ctx.guild.id, scrim_id, {"name": name, "category_id": category.id, "role_id": role.id, "channel_id": registration.id, "idp_channel_id": idp.id, "slots": slots, "mentions_required": mentions, "active": False, "teams": []})
        await ctx.send(embed=discord.Embed(title="Scrim created", description=f"ID: `{scrim_id}`", color=0xC45AEC))

    @commands.command(name="sttscrim")
    @commands.has_permissions(administrator=True)
    async def start_scrim(self, ctx, scrim_id: str): await self._active(ctx, scrim_id, True)

    @commands.command(name="spscrim")
    @commands.has_permissions(administrator=True)
    async def stop_scrim(self, ctx, scrim_id: str): await self._active(ctx, scrim_id, False)

    async def _active(self, ctx, scrim_id, active):
        item = await self.bot.repo.get_scrim(ctx.guild.id, scrim_id)
        if not item: return await ctx.send("Scrim not found.")
        await self.bot.repo.update_scrim(ctx.guild.id, scrim_id, {"active": active})
        channel = ctx.guild.get_channel(item["channel_id"])
        if channel: await channel.send(f"Scrim **{item['name']}** {'started' if active else 'stopped'}.")
        await ctx.send(f"Scrim `{scrim_id}` {'started' if active else 'stopped'}.")

    @commands.command(name="dlscrim")
    @commands.has_permissions(administrator=True)
    async def delete_scrim(self, ctx, scrim_id: str):
        item = await self.bot.repo.get_scrim(ctx.guild.id, scrim_id)
        if not item: return await ctx.send("Scrim not found.")
        category = ctx.guild.get_channel(item["category_id"])
        if category:
            for channel in category.channels: await channel.delete(reason="Scrim deleted")
            await category.delete(reason="Scrim deleted")
        role = ctx.guild.get_role(item["role_id"])
        if role: await role.delete(reason="Scrim deleted")
        await self.bot.repo.delete_scrim(ctx.guild.id, scrim_id)
        await ctx.send(f"Scrim `{scrim_id}` deleted.")

async def setup(bot): await bot.add_cog(ScrimCog(bot))
