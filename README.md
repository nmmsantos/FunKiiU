# FunKiiU

FunKiiU is a Python tool, compatible with Python 3.6+, to download Wii U content from N's CDN.

- It supports games, dlc, updates, virtual console, demos, **any** content.
- By default DLC will be patched to unlock all pieces of DLC.
- By default demos will be patched to remove any play count limits. *(does Wii U have this?)*


FunKiiU will accept keys and generate tickets, but you do not have to enter a key.
- You can choose to get the key automatically from an title key site.
- Or, you can choose to get a legit ticket from an title key site instead.
- You will need to provide the URL of a **wiiu title key site** by command line argument!

Using **keys** will generate a ticket that is not legit, the Wii U needs signature patches to accept it. (This is possible now, but a bit tricky to set up.)

Using **tickets** will download a ticket that is legit, and once installed, the content will work without any hacks at all. This is ideal, yet there are not and will not be tickets for **all** content that exists.

![running](http://i.imgur.com/YVsDqxE.png)

### Usage

Note: On Windows, you can use `py -3` instead of `python` for the commands below.

To download all games from EUR region to :
```sh
python3 FunKiiU.py --regions EUR --online-tickets --out-dir X:\WiiU --keysite http://title-key-site
```

To download Pikmin 3 EUR, by entering the Title ID and key:
```sh
python3 FunKiiU.py --titles 000500001012be00 --keys 32characterstitlekeyforpikmineur
```

To download Pikmin 3 EUR, by entering the Title ID and getting the key from the title key site:
```sh
python3 FunKiiU.py --titles 000500001012be00 --online-keys --keysite http://title-key-site
```
To download Pikmin 3 EUR, by entering the Title ID and getting the ticket from the title key site:
````sh
python3 FunKiiU.py --titles 000500001012be00 --online-tickets --keysite http://title-key-site
````
Download multiple things, one after another - (can use with `--online-keys` or `--online-tickets`):
````sh
python3 FunKiiU.py --titles TITLEID1 TITLEID2 TITLEID3 --keys KEY1 KEY2 KEY3
````
Downloads all content of a specific region (e.g. EUR) from the title key site, games, updates and dlc:
````sh
python3 FunKiiU.py --regions EUR --keysite http://title-key-site
````
Downloads all content of a specific region (e.g. USA,JPN) from the title key site, games, updates and dlc:
````sh
python3 FunKiiU.py --regions USA,JPN --keysite http://title-key-site
````
Simulates to do stuff, without actually downloading something:
````sh
python3 FunKiiU.py <options from above> --simulate
````
---
Content will be output to a folder with the Title ID, name (if using `--online-keys` or `--online-tickets`), and type (DLC or update), within the `install` directory by default.
![output](http://i.imgur.com/U1n66Zj.png)

The downloaded output can then be installed using **wupinstaller**, or any similar tool.
I recommend this wupinstaller mod - https://github.com/Yardape8000/wupinstaller/releases/latest
