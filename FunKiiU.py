#!/usr/bin/python3

__VERSION__ = "2.2"

import base64
import binascii
import json
import logging
import os
import re
import socket
import sys
import zlib
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from http.client import RemoteDisconnected
from typing import Iterator, MutableSequence, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from unidecode import unidecode

SIZE_UNITS = ("B", "KB", "MB", "GB", "T", "P", "E", "Z", "Y")
MAGIC = binascii.a2b_hex(
    "00010003704138EFBBBDA16A987DD901326D1C9459484C88A2861B91A312587AE70EF6237EC50E1032DC39DDE89A96A8E859D76A98A6E7E36A0CFE352CA893058234FF833FCB3B03811E9F0DC0D9A52F8045B4B2F9411B67A51C44B5EF8CE77BD6D56BA75734A1856DE6D4BED6D3A242C7C8791B3422375E5C779ABF072F7695EFA0F75BCB83789FC30E3FE4CC8392207840638949C7F688565F649B74D63D8D58FFADDA571E9554426B1318FC468983D4C8A5628B06B6FC5D507C13E7A18AC1511EB6D62EA5448F83501447A9AFB3ECC2903C9DD52F922AC9ACDBEF58C6021848D96E208732D3D1D9D9EA440D91621C7A99DB8843C59C1F2E2C7D9B577D512C166D6F7E1AAD4A774A37447E78FE2021E14A95D112A068ADA019F463C7A55685AABB6888B9246483D18B9C806F474918331782344A4B8531334B26303263D9D2EB4F4BB99602B352F6AE4046C69A5E7E8E4A18EF9BC0A2DED61310417012FD824CC116CFB7C4C1F7EC7177A17446CBDE96F3EDD88FCD052F0B888A45FDAF2B631354F40D16E5FA9C2C4EDA98E798D15E6046DC5363F3096B2C607A9D8DD55B1502A6AC7D3CC8D8C575998E7D796910C804C495235057E91ECD2637C9C1845151AC6B9A0490AE3EC6F47740A0DB0BA36D075956CEE7354EA3E9A4F2720B26550C7D394324BC0CB7E9317D8A8661F42191FF10B08256CE3FD25B745E5194906B4D61CB4C2E000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F7400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001434130303030303030330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007BE8EF6CB279C9E2EEE121C6EAF44FF639F88F078B4B77ED9F9560B0358281B50E55AB721115A177703C7A30FE3AE9EF1C60BC1D974676B23A68CC04B198525BC968F11DE2DB50E4D9E7F071E562DAE2092233E9D363F61DD7C19FF3A4A91E8F6553D471DD7B84B9F1B8CE7335F0F5540563A1EAB83963E09BE901011F99546361287020E9CC0DAB487F140D6626A1836D27111F2068DE4772149151CF69C61BA60EF9D949A0F71F5499F2D39AD28C7005348293C431FFBD33F6BCA60DC7195EA2BCC56D200BAF6D06D09C41DB8DE9C720154CA4832B69C08C69CD3B073A0063602F462D338061A5EA6C915CD5623579C3EB64CE44EF586D14BAAA8834019B3EEBEED3790001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100042EA66C66CFF335797D0497B77A197F9FE51AB5A41375DC73FD9E0B10669B1B9A5B7E8AB28F01B67B6254C14AA1331418F25BA549004C378DD72F0CE63B1F7091AAFE3809B7AC6C2876A61D60516C43A63729162D280BE21BE8E2FE057D8EB6E204242245731AB6FEE30E5335373EEBA970D531BBA2CB222D9684387D5F2A1BF75200CE0656E390CE19135B59E14F0FA5C1281A7386CCD1C8EC3FAD70FBCE74DEEE1FD05F46330B51F9B79E1DDBF4E33F14889D05282924C5F5DC2766EF0627D7EEDC736E67C2E5B93834668072216D1C78B823A072D34FF3ECF9BD11A29AF16C33BD09AFB2D74D534E027C19240D595A68EBB305ACC44AB38AB820C6D426560C000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000143503030303030303062000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000137A080BA689C590FD0B2F0D4F56B632FB934ED0739517B33A79DE040EE92DC31D37C7F73BF04BD3E44E20AB5A6FEAF5984CC1F6062E9A9FE56C3285DC6F25DDD5D0BF9FE2EFE835DF2634ED937FAB0214D104809CF74B860E6B0483F4CD2DAB2A9602BC56F0D6BD946AED6E0BE4F08F26686BD09EF7DB325F82B18F6AF2ED525BFD828B653FEE6ECE400D5A48FFE22D538BB5335B4153342D4335ACF590D0D30AE2043C7F5AD214FC9C0FE6FA40A5C86506CA6369BCEE44A32D9E695CF00B4FD79ADB568D149C2028A14C9D71B850CA365B37F70B657791FC5D728C4E18FD22557C4062D74771533C70179D3DAE8F92B117E45CB332F3B3C2A22E705CFEC66F6DA3772B000100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010004919EBE464AD0F552CD1B72E7884910CF55A9F02E50789641D896683DC005BD0AEA87079D8AC284C675065F74C8BF37C88044409502A022980BB8AD48383F6D28A79DE39626CCB2B22A0F19E41032F094B39FF0133146DEC8F6C1A9D55CD28D9E1C47B3D11F4F5426C2C780135A2775D3CA679BC7E834F0E0FB58E68860A71330FC95791793C8FBA935A7A6908F229DEE2A0CA6B9B23B12D495A6FE19D0D72648216878605A66538DBF376899905D3445FC5C727A0E13E0E2C8971C9CFA6C60678875732A4E75523D2F562F12AABD1573BF06C94054AEFA81A71417AF9A4A066D0FFC5AD64BAB28B1FF60661F4437D49E1E0D9412EB4BCACF4CFD6A3408847982000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526F6F742D43413030303030303033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000158533030303030303063000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000137A0894AD505BB6C67E2E5BDD6A3BEC43D910C772E9CC290DA58588B77DCC11680BB3E29F4EABBB26E98C2601985C041BB14378E689181AAD770568E928A2B98167EE3E10D072BEEF1FA22FA2AA3E13F11E1836A92A4281EF70AAF4E462998221C6FBB9BDD017E6AC590494E9CEA9859CEB2D2A4C1766F2C33912C58F14A803E36FCCDCCCDC13FD7AE77C7A78D997E6ACC35557E0D3E9EB64B43C92F4C50D67A602DEB391B06661CD32880BD64912AF1CBCB7162A06F02565D3B0ECE4FCECDDAE8A4934DB8EE67F3017986221155D131C6C3F09AB1945C206AC70C942B36F49A1183BCD78B6E4B47C6C5CAC0F8D62F897C6953DD12F28B70C5B7DF751819A98346526250001000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
)
TIKTEM = binascii.a2b_hex(
    "00010004d15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11ad15ea5ed15abe11a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000526f6f742d434130303030303030332d585330303030303030630000000000000000000000000000000000000000000000000000000000000000000000000000feedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedfacefeedface010000cccccccccccccccccccccccccccccccc00000000000000000000000000aaaaaaaaaaaaaaaa00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010014000000ac000000140001001400000000000000280000000100000084000000840003000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
)
TK = 0x140
ALL_REGIONS = {"ALL", "EUR", "USA", "JPN"}
DOWNLOAD_TYPES = {"0000", "000c", "000e"}
USER_AGENT_HEADER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
DEFAULT_TIMEOUT = 120

RE_16_HEX = re.compile(r"^[0-9a-f]{16}$", re.IGNORECASE)
RE_32_HEX = re.compile(r"^[0-9a-f]{32}$", re.IGNORECASE)

check_title_id = RE_16_HEX.match
check_title_key = RE_32_HEX.match


def b64decompress(d: str) -> bytes:
    return zlib.decompress(base64.b64decode(d))


def bytes2human(n: int, f: str = "%(value).2f %(symbol)s") -> str:
    n = int(n)
    if n < 0:
        raise ValueError("n < 0")
    prefix = {}
    for i, s in enumerate(SIZE_UNITS[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(SIZE_UNITS[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return f % locals()
    return f % dict(symbol=SIZE_UNITS[0], value=n)


def retry(count: int) -> Iterator[int]:
    for i in range(1, count + 1):
        if i > 1:
            print(f"*Attempt {i} of {count}")
        yield i


def progress_bar(
    part: int, total: int, length: int = 10, char: str = "#", blank: str = " ", left: str = "[", right: str = "]"
) -> str:
    percent = int((float(part) / float(total) * 100) % 100)
    bar_len = int((float(part) / float(total) * length) % length)
    bar = char * bar_len
    blanks = blank * (length - bar_len)
    return f"{left}{bar}{blanks}{right} {bytes2human(part)} of {bytes2human(total)}, {percent}%" + " " * 20


def download_file(
    url: str,
    outfname: str,
    retry_count: int = 3,
    ignore_404: bool = False,
    expected_size: Optional[int] = None,
    chunk_size: int = 2**16,
):
    for _ in retry(retry_count):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT_HEADER})
            infile = urlopen(request, timeout=DEFAULT_TIMEOUT)
            # start of modified code
            if os.path.isfile(outfname):
                statinfo = os.stat(outfname)
                diskFilesize = statinfo.st_size
            else:
                diskFilesize = 0
            log(f"-Downloading {outfname}.\n-File size is {expected_size}.\n-File in disk is {diskFilesize}.")

            if expected_size != diskFilesize:  # noqa: WPS504 # default branch should be first
                with open(outfname, "wb") as outfile:
                    downloaded_size = 0
                    while True:
                        buf = infile.read(chunk_size)
                        if not buf:
                            break
                        downloaded_size += len(buf)
                        if expected_size and len(buf) == chunk_size:
                            print(f" Downloaded {progress_bar(downloaded_size, expected_size)}", end="\r")
                        outfile.write(buf)
            else:
                print("-File skipped.")
                downloaded_size = statinfo.st_size
            # end of modified code

            if expected_size is not None:
                if os.path.getsize(outfname) == expected_size:
                    print(f"Download complete: {bytes2human(downloaded_size)}\n" + " " * 40)
                else:
                    print("Content download not correct size\n")
                    continue
        except HTTPError as e:
            if e.code == 404 and ignore_404:
                # We are ignoring this because its a 404 error, not a failure
                return True
            logging.warning("Failed to download file %s: %s", url, e)
        except (ConnectionError, URLError, RemoteDisconnected, socket.timeout) as e:
            logging.warning("Failed to download file %s: %s", url, e)
        else:
            return True

    return False


def patch_ticket_dlc(tikdata: bytearray) -> None:
    tikdata[TK + 0x164 : TK + 0x210] = b64decompress("eNpjYGQQYWBgWAPEIgwQNghoADEjELeAMTNE8D8BwEBjAABCdSH/")


def patch_ticket_demo(tikdata: bytearray) -> None:
    tikdata[TK + 0x124 : TK + 0x164] = bytes([0x00] * 64)


def make_ticket(
    title_id: str,
    title_key: str,
    title_version: bytes,
    out_path: str,
    patch_demo: bool = False,
    patch_dlc: bool = False,
) -> None:
    tikdata = bytearray(TIKTEM)
    tikdata[TK + 0xA6 : TK + 0xA8] = title_version
    tikdata[TK + 0x9C : TK + 0xA4] = binascii.a2b_hex(title_id)
    tikdata[TK + 0x7F : TK + 0x8F] = binascii.a2b_hex(title_key)
    # not sure what the value at 0xB3 is... mine is 0 but some i see 5.
    # or 0xE0, the reserved data is...?
    typecheck = title_id[4:8]
    if typecheck == "0002" and patch_demo:
        patch_ticket_demo(tikdata)
    elif typecheck == "000c" and patch_dlc:
        patch_ticket_dlc(tikdata)
    with open(out_path, "wb") as f:
        f.write(tikdata)


def safe_filename(filename: str) -> str:
    """Strip any non-path-safe characters from a filename
    >>> print(safe_filename("Pokémon"))
    Pokémon
    >>> print(safe_filename("幻影異聞録♯ＦＥ"))
    幻影異聞録_ＦＥ
    """
    keep = " ._"
    return re.sub(r"_+", "_", "".join(c if (c.isalnum() or c in keep) else "_" for c in filename)).strip("_ ")


def process_title_id(
    title_id: str,
    title_key: str,
    output_dir: str,
    name: Optional[str] = None,
    region: Optional[str] = None,
    retry_count: int = 3,
    onlinetickets: bool = False,
    patch_demo: bool = False,
    patch_dlc: bool = False,
    simulate: bool = False,
    tickets_only: bool = False,
    keysite: Optional[str] = None,
) -> None:
    if name:
        dirname = f"{region}_{unidecode(name.replace(' ', '_').replace('.', ''))}_{title_id.upper()}"
    else:
        dirname = title_id.upper()

    typecheck = title_id[4:8]
    if typecheck == "000c":
        dirname = dirname + "_DLC"
    elif typecheck == "000e":
        dirname = dirname + "_Update"

    rawdir = os.path.join(output_dir, safe_filename(dirname))

    if simulate:
        log(f'Simulate: Would start work in in: "{rawdir}"')
        return

    log(f'Starting work in: "{rawdir}"')

    if not os.path.exists(rawdir):
        os.makedirs(rawdir)

    # download stuff
    print("Downloading TMD...")

    baseurl = f"http://ccs.cdn.c.shop.nintendowifi.net/ccs/download/{title_id}"
    tmd_path = os.path.join(rawdir, "title.tmd")
    if not download_file(baseurl + "/tmd", tmd_path, retry_count):
        print("ERROR: Could not download TMD...")
        print("MAYBE YOU ARE BLOCKING CONNECTIONS TO NINTENDO? IF YOU ARE, DON'T...! :)")
        print("Skipping title...")
        return

    with open(os.path.join(rawdir, "title.cert"), "wb") as f:
        f.write(MAGIC)

    with open(tmd_path, "rb") as f:
        tmd = f.read()

    title_version = tmd[TK + 0x9C : TK + 0x9E]

    # get ticket from keysite, from cdn if game update, or generate ticket
    if typecheck == "000e":
        print("\nThis is an update, so we are getting the legit ticket straight from Nintendo.")
        if not download_file(baseurl + "/cetk", os.path.join(rawdir, "title.tik"), retry_count):
            print("ERROR: Could not download ticket from {}".format(baseurl + "/cetk"))
            print("Skipping title...")
            return
    elif onlinetickets:
        tikurl = f"{keysite}/ticket/{title_id}.tik"
        if not download_file(tikurl, os.path.join(rawdir, "title.tik"), retry_count):
            print(f"ERROR: Could not download ticket from {keysite}")
            print("Skipping title...")
            return
    else:
        make_ticket(title_id, title_key, title_version, os.path.join(rawdir, "title.tik"), patch_demo, patch_dlc)

    if tickets_only:
        print("Ticket, TMD, and CERT completed. Not downloading contents.")
        return

    print("Downloading Contents...")
    content_count = int(binascii.hexlify(tmd[TK + 0x9E : TK + 0xA0]), 16)

    total_size = 0
    for i in range(content_count):
        c_offs = 0xB04 + (0x30 * i)
        total_size += int(binascii.hexlify(tmd[c_offs + 0x08 : c_offs + 0x10]), 16)
    print(f"Total size is {bytes2human(total_size)}\n")

    for i in range(content_count):
        c_offs = 0xB04 + (0x30 * i)
        c_id = binascii.hexlify(tmd[c_offs : c_offs + 0x04]).decode()
        # c_type = binascii.hexlify(tmd[c_offs + 0x06:c_offs + 0x8])
        expected_size = int(binascii.hexlify(tmd[c_offs + 0x08 : c_offs + 0x10]), 16)
        print(f"Downloading {i + 1} of {content_count}.")
        outfname = os.path.join(rawdir, c_id + ".app")
        outfnameh3 = os.path.join(rawdir, c_id + ".h3")

        if not download_file(f"{baseurl}/{c_id}", outfname, retry_count, expected_size=expected_size):
            print("ERROR: Could not download content file... Skipping title")
            return
        if not download_file(f"{baseurl}/{c_id}.h3", outfnameh3, retry_count, ignore_404=True):
            print("ERROR: Could not download h3 file... Skipping title")
            return

    log(f'\nTitle download complete in "{dirname}"\n')


def main(
    titles: MutableSequence[str],
    keys: MutableSequence[str],
    output_dir: str,
    onlinekeys: bool = False,
    onlinetickets: bool = False,
    download_regions: Optional[Tuple[str, ...]] = None,
    retry_count: int = 3,
    patch_demo: bool = True,
    patch_dlc: bool = True,
    simulate: bool = False,
    tickets_only: bool = False,
    keysite: Optional[str] = None,
):
    titlekeys_data = []

    if download_regions and (titles or keys):
        print("If using '-region', don't give Title IDs or keys, it gets all titles from the keysite")
        sys.exit(0)
    if keys and (len(keys) != len(titles)):
        print("Number of keys and Title IDs do not match up")
        sys.exit(0)
    if titles and (not keys and not onlinekeys and not onlinetickets):
        print("You also need to provide '-keys' or use '-onlinekeys' or '-onlinetickets'")
        sys.exit(0)

    if download_regions or onlinekeys or onlinetickets:

        if keysite is None:
            print("-keysite not specified")
            sys.exit(1)

        print(f"Downloading/updating data from {keysite}")

        if not download_file(f"{keysite}/json", "titlekeys.json", retry_count):
            print("ERROR: Could not download data file... Exiting.\n")
            sys.exit(1)

        print("Downloaded data OK!")

        with open("titlekeys.json", encoding="utf-8") as f:
            titlekeys_data = json.load(f)

    for title_id in titles:
        title_id = title_id.lower()
        if not check_title_id(title_id):
            print("The Title ID(s) must be 16 hexadecimal characters long")
            print(f"{title_id} - is not ok.")
            sys.exit(0)
        title_key = None
        name = None
        region = None

        patch = title_id[4:8] == "000e"

        if keys:
            title_key = keys.pop()
            if not check_title_key(title_key):
                print("The key(s) must be 32 hexadecimal characters long")
                print(f"{title_id} - is not ok.")
                sys.exit(0)
        elif onlinekeys or onlinetickets:
            title_data = next((t for t in titlekeys_data if t["titleID"] == title_id.lower()), None)

            if not patch:
                if not title_data:
                    print(f"ERROR: Could not find data on {keysite} for {title_id}, skipping")
                    continue
                elif onlinetickets:
                    if title_data["ticket"] == "0":
                        print(f"ERROR: Ticket not available on {keysite} for {title_id}")
                        sys.exit(1)

                elif onlinekeys:
                    title_key = title_data["titleKey"]

            if title_data:
                name = title_data.get("name", None)
                region = title_data.get("region", None)

        if not (title_key or onlinetickets or patch):
            print(f"ERROR: Could not find title or ticket for {title_id}")
            continue

        # assert title_key is not None
        process_title_id(
            title_id,
            title_key,
            output_dir,
            name,
            region,
            retry_count,
            onlinetickets,
            patch_demo,
            patch_dlc,
            simulate,
            tickets_only,
            keysite,
        )

    if download_regions:
        for title_data in titlekeys_data:
            title_id = title_data["titleID"]
            title_key = title_data.get("titleKey", None)
            name = title_data.get("name", None)
            region = title_data.get("region", None)
            typecheck = title_id[4:8]

            if region is not None and region not in ALL_REGIONS:
                logging.error("Found unknown region `%s` for titleid: %s", region, title_id)

            if region not in download_regions:
                continue
            # only get games+dlcs+updates
            if typecheck not in DOWNLOAD_TYPES:
                continue
            if onlinetickets and (not title_data["ticket"]):
                continue
            elif onlinekeys and title_key is None:
                continue

            assert title_key is not None
            process_title_id(
                title_id,
                title_key,
                output_dir,
                name,
                region,
                retry_count,
                onlinetickets,
                patch_demo,
                patch_dlc,
                simulate,
                tickets_only,
                keysite,
            )


def log(output: str) -> None:
    if sys.stdout:
        _bytes = output.encode(sys.stdout.encoding, errors="replace")
        output = _bytes.decode(sys.stdout.encoding, errors="replace")
    print(output)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="FunKiiU by cearp and the cerea1killer", formatter_class=ArgumentDefaultsHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--regions",
        nargs="+",
        choices=ALL_REGIONS,
        help="Downloads/gets tickets for the specified regions from the keyfile. ALL means region free games, not all regions compbined.",
    )
    group.add_argument(
        "--titles",
        nargs="+",
        metavar="TITLE",
        default=[],
        help="Give TitleIDs to be specifically downloaded",
    )
    parser.add_argument(
        "--keys",
        nargs="+",
        metavar="KEY",
        default=[],
        help="Encrypted Title Key for the Title IDs. Must be in the same order as TitleIDs if multiple",
    )
    parser.add_argument(
        "--out-dir",
        default="install",
        help="The custom output directory to store output in, if desired",
    )
    parser.add_argument(
        "--online-keys",
        action="store_true",
        help="Gets latest titlekeys.json file from the title key site, saves (overwrites) it and uses as input",
    )
    parser.add_argument(
        "--online-tickets",
        action="store_true",
        help="Gets ticket file from the title key site, should create a 'legit' game",
    )
    parser.add_argument(
        "--retry-count",
        type=int,
        default=4,
        choices=range(0, 10),
        help="How many times a file download will be attempted",
    )
    parser.add_argument("--patch-dlc", action="store_true", help="Unlocking all DLC content")
    parser.add_argument("--patch-demo", action="store_true", help="Patch the demo play limit")
    parser.add_argument("--simulate", action="store_true", help="Don't download anything, just do like you would.")
    parser.add_argument(
        "--tickets-only",
        action="store_true",
        help="Only download/generate tickets (and TMD and CERT), don't download any content",
    )
    parser.add_argument("--keysite", help="URL of the keysite. For example `https://aaa.bbb.ccc`")
    parser.add_argument("--version", action="version", version=__VERSION__)
    args = parser.parse_args()

    main(
        titles=args.titles,
        keys=args.keys,
        output_dir=args.out_dir,
        onlinekeys=args.online_keys,
        onlinetickets=args.online_tickets,
        download_regions=args.regions,
        retry_count=args.retry_count,
        patch_demo=args.patch_demo,
        patch_dlc=args.patch_dlc,
        simulate=args.simulate,
        tickets_only=args.tickets_only,
        keysite=args.keysite,
    )
