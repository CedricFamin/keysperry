from utils.url import make_tiny
from utils.aws import get_s3_client


def add_commands(client):
    @client.command(pass_context=True, no_pm=True)
    async def download(ctx, user, *args):
        musicfilename = ' '.join(args)
        s3 = get_s3_client()
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'p4-keyboard',
                'Key': 'sounds/clean/%s/%s'% (user, musicfilename.replace('+', ' ')) # ugly but it works !
            }
        )
        await client.say("You can download '%s' from %s here : %s" % (musicfilename, user, make_tiny(url)))
