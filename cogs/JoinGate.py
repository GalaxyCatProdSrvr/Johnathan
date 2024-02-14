# cogs / JoinGate.py

# dpy
from discord.ext import commands
import datetime
import discord
from lib import Database as Database


class JoinGate(commands.Cog):
    def __init__(self, client):
        self.client = client  # sets the client variable so we can use it in cogs
        self.DBC = Database.DatabaseConnector()

    @commands.Cog.listener()
    async def on_ready(self):
        print("JoinGate Ready")

    # an example event with cogs

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member.created_at)

    async def log_action(self,chan,action,reason,member):

        LogChannel = await self.client.fetch_channel(chan)
        if LogChannel:

            if action in ["YoungAccount"]:
                if action == "youngAccount":
                    embed = discord.Embed(colour=discord.Colour(0x6cf8d3), description="Young Account!")

                    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
                    embed.set_author(name="author name",
                                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
                    embed.set_footer(text="Created with Love by GalaxyCatDev",
                                     icon_url=member.avatar)

                    embed.add_field(name="UserInfo", value="UserID: \nUsername: \nMention:\nAccount Age")
                    embed.add_field(name="ServerInfo", value="Minumum account age:")

            await LogChannel.send(embed=embed)

        pass
    async def young_account_age_module(self, member):
        try:
            minumum_account_age = self.DBC.get_setting(member.guild.id, "JoinGate", "min_account_age", default=5)
            action_to_take = self.DBC.get_setting(member.guild.id, "JoinGate", "young_accounts_action", default="Log")
            punish_dm_enabled = self.DBC.get_setting(member.guild.id, "JoinGate", "punish_dm_enabled", default=1)
            #print("action:", action_to_take)

            account_created_at = member.created_at.replace(tzinfo=None)
            current_date = datetime.datetime.utcnow()
            difference = current_date - account_created_at
            if difference.days >= minumum_account_age:
                #print(f"The account was created more than {minumum_account_age} days ago.")
                return
            else:
                print(f"The account was created within the last {minumum_account_age} days.")

                if action_to_take in ["Log", "Kick", "Timeout"]:
                    if action_to_take == "Log":
                        Log_chan_id = self.DBC.get_setting(member.guild.id, "logs_chan", "JoinGate", default=None)
                        if Log_chan_id is not None:  # maybe turn this into a function as this could be useful later
                            reason = "Account age was too young."
                            await self.log_action(Log_chan_id,"YoungAccount", reason)
                        else:
                            print(
                                "Log chan not set up: We see that you have the module enabled AND young accounts enabled and set to log however there is no log channel set up")
                    if action_to_take == "Kick":
                        if punish_dm_enabled:
                            await member.send(f"You were kicked because your discord account was too young for the server. ({minumum_account_age} days)")
                        # we might also want to log that we kicked the user.
                        # ctx.author.kick(
                        #    reason=f"The age of the account was too young. Account age: {difference.days} days.")

                        print(
                            f"The age of the account was too young. Account age: {difference.days} days and the setting is set to {minumum_account_age} days")
                    if action_to_take == "Timeout":
                        await member.send(
                            f"You were put in timeout because your discord account was too young for the server. ({minumum_account_age} days)")

                        pass
                else:
                    return
        except Exception as e:
            print(e)
    async def advertising_links_module(self, ctx):
        try:
            return True
            Log_chan_id = 1206920601009258496
            await self.log_action(Log_chan_id)
        except Exception as e:
            print(e)


    async def no_avatar_module(self, member:discord.Member):
        try:
            action_to_take = self.DBC.get_setting(member.guild.id, "JoinGate", "no_profile_picture_action", default="Log")
            punish_dm_enabled = self.DBC.get_setting(member.guild.id, "JoinGate", "punish_dm_enabled", default=1)

            if not member.avatar:
                if action_to_take in ["Log", "Kick", "Timeout"]:
                    Log_chan_id = self.DBC.get_setting(member.guild.id, "logs_chan", "JoinGate", default=None)
                    if Log_chan_id is not None:  # maybe turn this into a function as this could be useful later
                        print("log to:", Log_chan_id)

                    else:
                        print(
                            "Log chan not set up: We see that you have the module enabled AND young accounts enabled and set to log however there is no log channel set up")
                if action_to_take == "Kick":
                    if punish_dm_enabled:
                        await member.send("you were kicked because you do not have a avatar set up.")
                    await member.kick(
                        reason=f"At the time of the kick the user did not have a avatar.")
                if action_to_take == "Timeout":
                    pass


        except Exception as e:
            print(e)





    async def on_join_modules(self, member:discord.Member):
        # this will be moved to on join event in this file, for now it is triggered by command
        module_enabled = self.DBC.get_setting(member.guild.id, "JoinGate", "module_enabled", default=False)

        if module_enabled:
            advertising_links_enabled = self.DBC.get_setting(member.guild.id, "JoinGate",
                                                             "invite_links_in_username_enabled", default=False)

            no_avatar_enabled = self.DBC.get_setting(member.guild.id, "JoinGate",
                                                     "no_profile_picture_enabled", default=False)

            unauthorised_bots_enabled = self.DBC.get_setting(member.guild.id, "JoinGate",
                                                           "unauthorized_bots_enabled", default=False)

            unverified_bots_enabled = self.DBC.get_setting(member.guild.id, "JoinGate",
                                                     "unverified_bots_enabled", default=False)

            young_accounts_enabled = self.DBC.get_setting(member.guild.id, "JoinGate", "young_accounts_enabled",
                                                          default=False)

            if advertising_links_enabled:
                await self.advertising_links_module(member)

            if no_avatar_enabled:
                await self.no_avatar_module(member)

            if unauthorised_bots_enabled:
                await self.unauthorised_bots_module(member)

            if unverified_bots_enabled:
                await self.unverified_bots_module(member)

            if young_accounts_enabled:
                await self.young_account_age_module(member)



    @commands.command()
    async def join(self, ctx):

        await self.on_join_modules(ctx.author)





# an example command with cogs
async def setup(client):
    await client.add_cog(JoinGate(client))
    print("loaded JoinGate")
