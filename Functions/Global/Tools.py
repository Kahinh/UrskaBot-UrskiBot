import lib

async def send_messages(ctx, message, type="standard", delay=lib.GlobalDict.Timer):
    if type == "standard":
        await ctx.send(f"{message}", delete_after=delay)
    elif type == "embed":
        await ctx.send(embed=message, delete_after=delay)