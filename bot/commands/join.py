def add_commands(client):
    @client.command(pass_context=True, no_pm=True)
    async def join(ctx):
        await client.join_voice_channel(ctx.message.author.voice_channel)
