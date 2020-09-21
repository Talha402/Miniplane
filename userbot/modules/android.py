# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to android"""

import re
from requests import get
from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.events import register


GITHUB = 'https://github.com'
MAGISK_REPO = f'{GITHUB}/topjohnwu/Magisk/releases'
DEVICES_DATA = 'https://raw.githubusercontent.com/androidtrackers/' \
               'certified-android-devices/master/devices.json'


@register(outgoing=True, pattern="^.magisk$")
async def magisk(request):
    """ magisk latest releases """
    if not request.text[0].isalpha(
    ) and request.text[0] not in ("/", "#", "@", "!"):
        page = BeautifulSoup(get(MAGISK_REPO).content, 'lxml')
        links = '\n'.join([i['href'] for i in page.findAll('a')])
        releases = 'Latest Magisk Releases:\n'
        try:
            latest_apk = re.findall(r'/.*MagiskManager-v.*apk', links)[0]
            releases += f'[{latest_apk.split("/")[-1]}]({GITHUB}{latest_apk})\n'
        except IndexError:
            releases += "`Can't find latest APK !!`"
        try:
            latest_zip = re.findall(r'/.*Magisk-v.*zip', links)[0]
            releases += f'[{latest_zip.split("/")[-1]}]({GITHUB}{latest_zip})\n'
        except IndexError:
            releases += "`Can't find latest ZIP !!`"
        try:
            latest_uninstaller = re.findall(r'/.*Magisk-uninstaller-.*zip', links)[0]
            releases += f'[{latest_uninstaller.split("/")[-1]}]({GITHUB}{latest_uninstaller})\n'
        except IndexError:
            releases += "`Can't find latest uninstaller !!`"
        await request.edit(releases)


@register(outgoing=True, pattern=r"^.twrp(?: |$)(\S*)")
async def twrp(request):
    """ get android device twrp """
    if not request.text[0].isalpha()\
            and request.text[0] not in ("/", "#", "@", "!"):
        textx = await request.get_reply_message()
        device = request.pattern_match.group(1)
        if device:
            pass
        elif textx:
            device = textx.text.split(' ')[0]
        else:
            await request.edit("`Usage: .twrp <codename>`")
            return
        url = get(f'https://dl.twrp.me/{device}/')
        if url.status_code == 404:
            reply = f"`Couldn't find twrp downloads for {device}!`\n"
            await request.edit(reply)
            return
        page = BeautifulSoup(url.content, 'lxml')
        download = page.find('table').find('tr').find('a')
        dl_link = f"https://dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        reply = f'**Latest TWRP for {device}:**\n' \
            f'[{dl_file}]({dl_link}) - __{size}__\n' \
            f'**Updated:** __{date}__\n'
        await request.edit(reply)


@register(outgoing=True, pattern=r"^.evo(?: |$)(\S*)")
async def evo(event):
    if event.from_id is None:
        return

    try:
        device_ = event.pattern_match.group(1)
        device = urllib.parse.quote_plus(device_)
    except Exception:
        device = ''

    if device == "example":
        reply_text = ("Why are you trying to get the example device?")
        await event.edit(reply_text, link_preview=False)
        return

    if device == "x00t":
        device = "X00T"

    if device == "x01bd":
        device = "X01BD"

    if device == '':
        reply_text = (
            "Please type your device **codename**!\nFor example, `.{} raphael`").format("evo")
        await event.edit(reply_text, link_preview=False)
        return

    fetch = get(
        f'https://raw.githubusercontent.com/Evolution-X-Devices/official_devices/master/builds/{device}.json'
    )

    if fetch.status_code in [500, 504, 505]:
        await event.edit(
            "MiniPlane have been trying to connect to Github User Content, It seem like Github User Content is down"
        )
        return

    if fetch.status_code == 200:
        try:
            usr = json.loads(fetch.content)
            filename = usr['filename']
            url = usr['url']
            version = usr['version']
            maintainer = usr['maintainer']
            maintainer_url = usr['telegram_username']
            size_a = usr['size']
            size_b = sizee(int(size_a))

            reply_text = ("**Download:** [{}]({})\n").format(filename, url)
            reply_text += ("**Build Size:** `{}`\n").format(size_b)
            reply_text += ("**Android Version:** `{}`\n").format(version)
            reply_text += ("**Maintainer:** {}\n").format(
                f"[{maintainer}](https://t.me/{maintainer_url})")
            reply_text += ("[Click here to Download]({})").format(url)
            await event.edit(reply_text, link_preview=False)
            return

        except ValueError:
            reply_text = (
                "Tell the rom maintainer to fix their OTA json. I'm sure this won't work with OTA and it won't work with this bot too :P")
            await event.edit(reply_text, link_preview=False)
            return

    elif fetch.status_code == 404:
        reply_text = ("Couldn't find any results matching your query.")
        await event.edit(reply_text, link_preview=False)
        return


@register(outgoing=True, pattern=r"^.bootleggers(?: |$)(\S*)")
async def bootleggers(event):
    if event.from_id is None:
        return

    try:
        codename_ = event.pattern_match.group(1)
        codename = urllib.parse.quote_plus(codename_)
    except Exception:
        codename = ''

    if codename == '':
        reply_text = (
            "Please type your device **codename**!\nFor example, `.{} raphael`").format("bootleggers")
        await event.edit(reply_text, link_preview=False)
        return

    fetch = get('https://bootleggersrom-devices.github.io/api/devices.json')
    if fetch.status_code == 200:
        nestedjson = json.loads(fetch.content)

        if codename.lower() == 'x00t':
            devicetoget = 'X00T'
        else:
            devicetoget = codename.lower()

        reply_text = ""
        devices = {}

        for device, values in nestedjson.items():
            devices.update({device: values})

        if devicetoget in devices:
            for oh, baby in devices[devicetoget].items():
                dontneedlist = ['id', 'filename', 'download', 'xdathread']
                peaksmod = {
                    'fullname': 'Device name',
                    'buildate': 'Build date',
                    'buildsize': 'Build size',
                    'downloadfolder': 'SourceForge folder',
                    'mirrorlink': 'Mirror link',
                    'xdathread': 'XDA thread'
                }
                if baby and oh not in dontneedlist:
                    if oh in peaksmod:
                        oh = peaksmod.get(oh, oh.title())

                    if oh == 'SourceForge folder':
                        reply_text += f"\n**{oh}:** [Here]({baby})\n"
                    elif oh == 'Mirror link':
                        if not baby == "Error404":
                            reply_text += f"\n**{oh}:** [Here]({baby})\n"
                    else:
                        reply_text += f"\n**{oh}:** `{baby}`"

            reply_text += ("**XDA Thread:** [Here]({})\n").format(
                devices[devicetoget]['xdathread'])
            reply_text += ("**Download:** [{}]({})\n").format(
                devices[devicetoget]['filename'],
                devices[devicetoget]['download'])
        else:
            reply_text = ("Couldn't find any results matching your query.")

    elif fetch.status_code == 404:
        reply_text = ("Couldn't reach the API.")
    await event.edit(reply_text, link_preview=False)


@register(outgoing=True, pattern=r"^.los(?: |$)(\S*)")
async def los(event):
    if event.from_id is None:
        return

    try:
        device_ = event.pattern_match.group(1)
        device = urllib.parse.quote_plus(device_)
    except Exception:
        device = ''

    if device == '':
        reply_text = (
            "Please type your device **codename**!\nFor example, `.{} raphael`").format("los")
        await event.edit(reply_text, link_preview=False)
        return

    fetch = get(f'https://download.lineageos.org/api/v1/{device}/nightly/*')
    if fetch.status_code == 200 and len(fetch.json()['response']) != 0:
        usr = json.loads(fetch.content)
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']

        reply_text = ("**Download:** [{}]({})\n").format(filename, url)
        reply_text += ("**Build Size:** `{}`\n").format(buildsize_b)
        reply_text += ("**Version:** `{}`\n").format(version)
        reply_text += ("[Click here to Download]({})").format(url)
        await event.edit(reply_text, link_preview=False)
        return

    else:
        reply_text = ("Couldn't find any results matching your query.")
    await event.edit(reply_text, link_preview=False)


@register(outgoing=True, pattern=r"^.phh")
async def phh(event):
    if event.from_id is None:
        return

    fetch = get(
        "https://api.github.com/repos/phhusson/treble_experimentations/releases/latest"
    )
    usr = json.loads(fetch.content)
    reply_text = ("**Phh's latest GSI release(s)**\n")
    for i in range(len(usr)):
        try:
            name = usr['assets'][i]['name']
            url = usr['assets'][i]['browser_download_url']
            reply_text += f"[{name}]({url})\n"
        except IndexError:
            continue
    await event.edit(reply_text)


CMD_HELP.update(
    {
        "android": [
            'Android', " - `magisk`: Get the latest Magisk releases.\n"
            " - `twrp` <codename>: Get the latest TWRP download for an Android device.\n\n"
            "**Thanks to @HarukaAyaBot:**\n"
            " - `evo <device>`: Get the latest Evolution X ROM for a device\n"
            " - `bootleggers <device>`: Get the latest Bootleggers ROM for a device\n"
            " - `los <device>`: Get the latest LineageOS ROM for a device\n"
            " - `phh`: Get the latest Phh AOSP GSI!\n\n"
            ]
})