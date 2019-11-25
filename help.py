# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging
import inspect

from telethon import functions, types
logger = logging.getLogger(__name__)
from telethon.tl.functions.channels import JoinChannelRequest

def register(cb):
    cb(HelpMod())

class HelpMod(loader.Module):
    """Prevents people sending you unsolicited private messages"""
    def __init__(self):
        super().__init__()
        self.name = _("Help")
        self.allmodules = None
        self.client = None
        
    async def supportcmd(self, message):
    	"""Joins the support chat"""
    	await self.client(JoinChannelRequest("https://t.me/friendlytgbot"))
    	await message.edit(_("<code>Join to</code> <a href='https://t.me/friendlytgbot'>support chat</a>"))

    async def client_ready(self, client, db):
    	self.client = client    
        
    async def helpcmd(self, message):
        """Block this user to PM without being warned"""
        raph = "<b>Available Commands in RaphielGang section:<b>\n<b>—–—–—–—–—–——–––—–—–———</b>\n<i>To unload</i><code>.unloadmod RaphielGang</code><i>(num)</i>\n"
        uni = "<b>Available Commands in Uniborg section:<b>\n<b>—–—–—–—–—–——–––—–—–———</b>\n<i>To unload</i><code>.unloadmod UniBorg</code><i>(num)</i>\n"
        ftg = "<b>Available Commands in Friendly-Telegram section:</b>\n<b>—–—–—–—–—–——–––—–—–———</b>\n<i>To unload</i><code>.unloadmod</code><i>modulename</i>\n"
        all = "<b>Available Commands:</b>\n"
        args = utils.get_args_raw(message)
        if not args:
        	await message.edit(
        	"<b>Please choose a section to see your modules:</b>\n<b>—–—–—–—–—–——–––—–—–———</b>"
        	"\n\n\n<code>.help raph</code>:<i> Shows all your PP and PPE originated modules.</i>\n"
        	"\n<code>.help uni</code>:<i><b> Shows all your Uniborg originated modules.</b></i>\n"
        	"\n<code>.help ftg</code>:<i><b> Shows all your native modules.</b></i>\n"
        	"\n<code>.help all:</code><i><b> Shows all your modules.</b></i>")
        	return
        for mod in self.allmodules.modules:
        	if mod.name.find("RaphielGang") != -1:
        		raph += "\n\n<b>" + mod.name + "</b>: "
        		for cmd in mod.commands:
        			raph += "<code>" + cmd + "</code>, "
        		raph = raph[:-2:]
        		raph = raph.replace("Raphielgang Configuration Placeholder:", "")
        	if mod.name.find("UniBorg") != -1:
        		uni += "\n\n<b>" + mod.name + "</b>: "
        		for cmd in mod.commands:
        			uni += "<code>" + cmd + "</code>, "
        		uni = uni[:-2:]
        		uni = uni.replace("Uniborg Configuration Placeholder:", "")
        	if mod.name.find("UniBorg") == -1 and mod.name.find("RaphielGang") == -1:
        		ftg += "\n\n<b>" + mod.name + "</b>: "
        		for cmd in mod.commands:
        			ftg += "<code>" + cmd + "</code>, "
        		ftg = ftg[:-2:]
        		ftg = ftg.replace("Raphielgang Configuration Placeholder:", "")
        		ftg = ftg.replace("Uniborg Configuration Placeholder:", "")
        	all += "\n\n<b>" + mod.name + "</b>: "
        	for cmd in mod.commands:
        		all += "<code>" + cmd + "</code>, "
        	all = all[:-2:]
        if args == "uni":
        	await message.edit(uni)
        	return
        if args == "raph":
        	await message.edit(raph)
        	return
        if args == "ftg":
        	await message.edit(ftg)
        	return
        if args == "all":
        	await message.edit(all)
        	return
        else:
        	module = None
        	for mod in self.allmodules.modules:
        		if mod.name.lower() == args.lower():
        			module = mod
        	if module is None:
        		await message.edit("<code>" + _("Invalid module name specified") + "</code>")
        		return
        	reply = "<b>" + _("Help for</b> <code>{}</code>:").format(utils.escape_html(_(module.name))) + "\n  "	
        	if module.__doc__:
        		reply += utils.escape_html(inspect.cleandoc(module.__doc__))
        	else:
        		logger.warning("Module %s is missing docstring!", module)
        	for name, fun in module.commands.items():
        		reply += f"\n  <code>{name}</code>\n"
        		if fun.__doc__:
        			reply += utils.escape_html("\n".join(["    " + x for x in 
        			_(inspect.cleandoc(fun.__doc__)).splitlines()]))
        		else:
        			reply += _("There is no documentation for this command")
        	await utils.answer(message, reply)
