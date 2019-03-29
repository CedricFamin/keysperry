from utils.aws import get_s3_client

def add_commands(client):
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