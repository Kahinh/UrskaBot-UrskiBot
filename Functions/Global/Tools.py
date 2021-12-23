import lib

async def send_messages(ctx, message, type="standard"):
    if type == "standard":
        await ctx.send(f"{message}", delete_after=lib.GlobalDict.Timer)
    elif type == "embed":
        await ctx.send(embed=message, delete_after=lib.GlobalDict.Timer)