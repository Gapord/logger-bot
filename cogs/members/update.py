import datetime
import disnake
from disnake.ext import commands
from database.getfromdb import getchan, getcolor


class UpdateMember(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(
        self, before: disnake.Member, after: disnake.Member
    ):
        log = self.bot.get_channel(await getchan(after.guild.id))
        changes = []

        if before.nick != after.nick:
            changes.append(
                f"Никнейм изменён с {before.nick or 'None'} на {after.nick or 'None'}"
            )

        if before.roles != after.roles:
            removed_roles = [
                role for role in before.roles if role not in after.roles
            ]
            added_roles = [
                role for role in after.roles if role not in before.roles
            ]

            if removed_roles:
                changes.append(
                    f"Роли удалены: {', '.join(role.mention for role in removed_roles)}"
                )
            if added_roles:
                changes.append(
                    f"Роли добавлены: {', '.join(role.mention for role in added_roles)}"
                )

        if before.pending != after.pending:
            changes.append(
                f"Статус ожидания изменён на {'ожидает' if after.pending else 'не ожидает'}"
            )

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if changes:
            embed = disnake.Embed(
                title="Обновление профиля участника",
                color=await getcolor(after.guild.id),
            )
            embed.add_field(name="Пользователь", value=after.mention)
            embed.add_field(name="Дата изменения", value=current_time)
            embed.add_field(
                name="Изменения", value="\n".join(changes), inline=False
            )
            await log.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(UpdateMember(bot))
