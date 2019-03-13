import discord
from discord.ext import commands
import asyncio
import logging
import boto3
import youtube_dl

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix=commands.when_mentioned_or('$'))

def get_s3_client():
    return boto3.client(
        's3'
        , region_name='eu-west-3')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command(pass_context=True, no_pm=True)
async def join(ctx):
    await client.join_voice_channel(ctx.message.author.voice_channel)

@client.command(pass_context=True, no_pm=True)
async def get_sounds(ctx, user):
    s3_client = get_s3_client()

    results = s3_client.list_objects(
        Bucket='p4-keyboard'
        , Prefix='sounds/clean/%s/' % user
    )

    files = []
    message = ["""Liste des musiques de %s:""" % user]
    for result in results['Contents']:
        filename = result['Key'].split('/')[-1]
        if filename != '':
            files.append(filename)
            message.append('- %s' % filename)

    await client.say('\n'.join(message))

@client.command(pass_context=True, no_pm=True)
async def play(ctx, user, *args):
    musicfilename = ' '.join(args)
    s3 = get_s3_client()
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'p4-keyboard',
            'Key': 'sounds/clean/%s/%s'% (user, musicfilename)
        }
    )

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(player.title))


client.run('token', bot=True)
