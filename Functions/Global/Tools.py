from tkinter import HIDDEN
import lib

async def send_messages(ctx, message, type="standard", delay=600, component={}):
    if type == "standard":
        await ctx.send(f"{message}", delete_after=delay)
    elif type == "embed":
        if component == {}:
            await ctx.send(embed=message, delete_after=delay)
        else:
            await ctx.send(embed=message, components=[component], delete_after=delay)