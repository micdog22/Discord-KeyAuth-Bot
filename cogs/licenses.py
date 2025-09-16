from typing import Optional
            import json
            import discord
            from discord import app_commands, Interaction
            from discord.ext import commands

            from keyauth_api import KeyAuthAPI, KeyAuthConfig
            from utils.checks import has_admin_or_allowed

            class KeyAuthCog(commands.Cog):
                def __init__(self, bot: commands.Bot):
                    self.bot = bot
                    self.api = KeyAuthAPI(KeyAuthConfig.from_env())

                group = app_commands.Group(name="kauth", description="Comandos KeyAuth")

                @group.command(name="info", description="Consulta informações de uma key")
                @app_commands.describe(key="Chave a consultar")
                async def info(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.key_info(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Info da key:
```json
{text}
```", ephemeral=True)

                @group.command(name="gerar", description="Cria novas chaves")
                @app_commands.describe(amount="Quantidade", expiry_days="Dias de validade", level="Nível")
                async def gerar(self, interaction: Interaction, amount: int, expiry_days: Optional[int] = None, level: Optional[int] = None):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.create_keys(amount=amount, expiry_days=expiry_days, level=level)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado da geração:
```json
{text}
```", ephemeral=True)

                @group.command(name="ban", description="Bane uma key")
                @app_commands.describe(key="Chave")
                async def ban(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.ban_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado do banimento:
```json
{text}
```", ephemeral=True)

                @group.command(name="unban", description="Desbane uma key")
                @app_commands.describe(key="Chave")
                async def unban(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.unban_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado do desbanimento:
```json
{text}
```", ephemeral=True)

                @group.command(name="reset", description="Reseta HWID de uma key")
                @app_commands.describe(key="Chave")
                async def reset(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.reset_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado do reset:
```json
{text}
```", ephemeral=True)

                @group.command(name="deletar", description="Deleta uma key")
                @app_commands.describe(key="Chave")
                async def deletar(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.delete_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado da exclusão:
```json
{text}
```", ephemeral=True)

            async def setup(bot: commands.Bot):
                await bot.add_cog(KeyAuthCog(bot))
                bot.tree.add_command(KeyAuthCog.group)