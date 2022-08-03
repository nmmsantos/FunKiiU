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

Note: On Windows, you call use `py` instead of `python` for the commands below.

To download all games from EUR region to :
```sh
$ python FunKiiU.py -region EUR -onlinetickets -outputdir X:\WiiU -keysite http://title-key-site
```

To download Pikmin 3 EUR, by entering the Title ID and key:
```sh
$ python FunKiiU.py -title 000500001012be00 -key 32characterstitlekeyforpikmineur
```

To download Pikmin 3 EUR, by entering the Title ID and getting the key from the title key site:
```sh
$ python FunKiiU.py -title 000500001012be00 -onlinekeys -keysite http://title-key-site
```
To download Pikmin 3 EUR, by entering the Title ID and getting the ticket from the title key site:
````sh
$ python FunKiiU.py -title 000500001012be00 -onlinetickets -keysite http://title-key-site
````
Download multiple things, one after another - (can use with *-onlinekeys* or *-onlinetickets*):
````sh
$ python FunKiiU.py -title TITLEID1 TITLEID2 TITLEID3 -key KEY1 KEY2 KEY3
````
Downloads all content of a specific region (e.g. EUR) from the title key site, games, updates and dlc:
````sh
$ python FunKiiU.py -region EUR -keysite http://title-key-site
````
Downloads all content of a specific region (e.g. USA,JPN) from the title key site, games, updates and dlc:
````sh
$ python FunKiiU.py -region USA,JPN -keysite http://title-key-site
````
Simulates to do stuff, without actually downloading something:
````sh
$ python FunKiiU.py <options from above> -simulate
````
---
Content will be output to a folder with the Title ID, name (if using *-onlinekeys* or *-onlinetickets*), and type (DLC or update), within the **'install'** directory.
![output](http://i.imgur.com/U1n66Zj.png)

The downloaded output can then be installed using **wupinstaller**, or any similar tool.
I recommend this wupinstaller mod - https://github.com/Yardape8000/wupinstaller/releases/latest
