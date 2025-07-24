# SWTG###AS RE

- SWTG118AS
- SWTG115AS
- SWTG124AS

# Web UI

## Passwords

| User        | Password        | Internal MD5 Hash                  | CGI           |   |
| ---------- | ---------------- | ---------------------------------- | ------------- | - |
| admin      | admin            | `f6fdffe48c908deb0f4c3bd36c032e72` | login.cgi    | ✔|
| hengrui    | ❓               | `81d57ea79621e8887914f40ee4122185` | login_ft.cgi  | ❌ |

## Factory CGI

> Factory CGI can be accessed directly via the admin credentials

| CGI                              | Description      |
| -------------------------------- | ---------------- |
| <http://192.168.2.1/menu_ft.cgi> | Factory Menu     |
| <http://192.168.2.1/ftdft.cgi>   | Factory Defaults |
| <http://192.168.2.1/ftlogo.cgi>  | Factory Logo     | 
| <http://192.168.2.1/ftcolor.cgi> | Factory Colours  |

# Serial CLI

## Pinout

> [!WARNING]
> The orientation is different for both boards

| Pin  | SWTG115AS | SWTG118AS | Notes               |
| ---- | --------- | --------- | ------------------- |
| 1    | TX        | TX        | **Square Pad**      |
| 2    | GND       | GND       |                     |
| 3    | RX        | RX        |                     |
| 4    | VCC       | VCC       | ‼️ **Don't connect** |

## Baudrate

|           | Unmanaged | Web Managed |
| --------- | --------- | ----------- |
| Speed     | 9600      | 57600       |
| Parity    | None      | None        | 
| Data-bits | 8         | 8           |
| Stop-bits | 1         | 1           |

## Web Managed

### Boot Log

```bash
==========Loader start===========
Press any key to start the normal procedure.
To run SPI flash viewer, press [v]
To enforce the download of the runtime kernel, press [ESC] .....
  cmd -1
    Check Runtime Image.....
    Chksum Correct!
    RunTime Kernel Starting....  
Ver8373_72: C
Not rtl8221b and skip init flow...id = c849 
###SDS FW Load finished !!



===========================Config Area pre-check Starts.=====================.
Pre-Check the config size structure is equal or not.
(sizeof(configCache)) a36.
(FLSH_ADDR_END-FLSH_CONFIG_ADDR_START) a36. 
(FLSH_CONFIG_ADDR_START) 1fe000.
(FLSH_ADDR_END) 1fea36.
It seems no risk!..................
==============================Config Area pre-check ends.===================.



SalFlshCopyFlshToCache()
sal_sys_config_restore()
Restore dhcp state is: 0

Restore ip is: 192.168.2.1

...OK
sal_mirror_config_restore()...OK
sal_qos_config_restore()...OK
sal_vlan_config_restore()...OK
sal_rate_config_restore()...OK
sal_trunk_config_restore()...OK
sal_l2_config_restore()...OK
sal_loop_config_restore()...OK
sal_eee_config_restore()...OK
sal_stp_config_restore()...OK
sal_igmp_config_restore()...OK
sal_port_config_restore()...OK



#############According to the flash setting to set the WEB/DUMB mode

#############Read the web/dumb mode.....!!!###

#############web_dumb_cfg.vld_flag=-1, web_dumb_cfg.mode=-1
#############Begin to set the web mode



################################################################

############Login Menu ############
### Please input uboot password below: ###

```

### *uboot* Password

| Switch Model                                  | *"uboot"* Password |
| --------------------------------------------- | ------------------ |
| **SWTG118AS** / **SWTG115AS** / **SWTG124AS** | `Switch321`        |
| **SWTGW215AS**                                | `Hs2021cfgmg`      |

```bash
Login OK.





RTL8372:

```

### Commands

| Command                 | Description                              | Notes            |
| ----------------------- | ---------------------------------------- | --------------- |
| `dft`                   | Resets the default factory configuration | ⚠️ Uses the defaults at `0x005DB50` and colours at `0x000DE520` |
| `fiber `                | Displays SFP+ port status                ||
| `gpio`                  | Displays GPIO 54 status                  ||
| `poe`                   | Displays PoE status                      ||
| `regset <reg> <value>`  | Sets a register to a specified value     ||
| `regget <reg>`          | Display the specified registers value    ||
| `reboot`                | Reboots the switch                       ||
| `reset`                 | Resets the user configuration            ||
| `showip`                | Displays the system information          ||
| `stp`                   | Displays the Spanning Tree details       ||
| `web`                   | Sets the web mode                        | Sets web config offsets `0x001FC026` and `0x001FC027` to `1`    |

### Firmware Upload Failsafe

If the runtime fails, the loader will fallback to the firmware upload sequence at `http://192.168.1.1`. It may also be triggered over serial by holding `ESC` on power on.


```bash
==========Loader start===========
Press any key to start the normal procedure.
To run SPI flash viewer, press [v]
To enforce the download of the runtime kernel, press [ESC] .
  cmd 27
sal_sys_runtime_crc_set
loader start
load MAC from nvcfg
  IP:192.168.1.1
Mask:255.255.255.0
  GW:192.168.1.254
 MAC:AA.BB.CC.DD.EE.FF
```

### SPI Flash Viewer

```bash
=========================SPI FLASH VIEWER=============================
    b: reboot
    e <addr>: Erase flash with the address of <addr>
    ev <addr>: Erase flash with the address of <addr> and then Verify
    r <addr> <len>: read flash from the address of <addr> and then dump
    c: check runtime kernel without boot
    cb: check runtime kernel and boot if checksum is pass
    h: print header
    l: load runtime kernel
    v: show verobose information
    m: print this menu
    q: quit from spi flash view
>
```

### Protected Regions

```bash
There 2 protected region(s).
    Portected region 0: 0x000000-0x001000
    Portected region 1: 0x004000-0x01c000
```

### Firmware Mapping

| Firmware Offset | Length       | Description              | Notes                                                       |
| --------------- | ------------ | ------------------------ | ----------------------------------------------------------- |
| `0x00030F38`    | `0x00000010` | uboot Password           |
| `0x000DD55F`    | `0x00000010` | AES Key                  | For lower case flash unique ID                              |
| `0x000DD57F`    | `0x00000010` | AES Key                  | For upper case flash unique ID                              |
| `0x001FC000`    | `0x00000006` | MAC address              |                                                             |
| `0x001FC026`    | `0x00000002` | Web/Dumb mode            | `0x00` = Dumb Mode, `0x01` = Web Mode, `0xFF` = Auto detect |
| `0x001FD000`    | `0x0000023D` | Factory settings         |                                                             |
| `0x001FE000`    | `0x00000A42` | User settings            |                                                             |

### Firmware to Update Mapping

| Firmware Offset | Length       | Update Offset | Length       |
| --------------- | ------------ | ------------- | ------------ |
| `0x00001000`    | `0x00002ffe` | `0x00000014`  | `0x00002ffe` |
| `0x0001C000`    | `0x00001000` | `0x00003012`  | `0x00001000` |
| `0x0001D000`    | `0x001DF000` | `0x00003ffe`  | eof          |

## Unmanaged

### Boot Log

```bash
error SDS_MODE 
LINE 2178

RTL8371B start aas
RTL8371B:
```

### Commands

```bash
RTL8371B:?                                                                        
    rst:        -reset chip                                                       
the following is set IOL test mode                                                
        f:    -fix pattern: please input port: 0-7;                               
        r:    -random pattern: please input port: 0-7;                            
        10:   -10M MDI: please input port: 0-7;
        11:   -10M MDIx: please input port: 0-7;
        100:    -100M MDI: please input port: 0-7;
        101:    -100M MDIX: please input port: 0-7;
        g1:   -giga mode1: please input port: 0-7;
        g2:   -giga mode2: please input port: 0-7;
        g3:   -giga mode3: please input port: 0-7;
        g4:   -giga mode4: please input port: 0-7;
        1:    -2.5G mode1: please input port: 0-7;
        2:    -2.5G mode2: please input port: 0-7;
        3:    -2.5G mode3: please input port(0~7) and lp;
        4:    -2.5G mode4: please input tone(1~5) and port(0~7);
        5:    -2.5G mode5: please input port: 0-7;
        6:    -2.5G mode6: please input port: 0-7;
the following is set sds test mode,chip sel:8373/8372: 3, 8224: 4;
        sd:    -please input chip: 3 or 4; prbs31:31; sds: 0~1; on/off:1 or 0;
        sd:    -please input chip: 3 or 4; prbs9:9; sds: 0~1; on/off:1 or 0; 
        sd:    -please input chip: 3 or 4; tx_8081: 8; sds: 0~1; onoff:1 or 0;
        pre:   -please input chip: 3 or 4; sds: 0~1; pre: 0~63, endis:0~1;
        main:  -please input chip: 3 or 4; sds: 0~1; mamp: 0~63, boost:0~1, endis: 0~1;
        post:  -please input chip: 3 or 4; sds: 0~1; post: 0~63, endis: 0~1;
        tx:    -please input chip: 3 or 4; sds: 0~1; z0:0~15;
        eye:   -please input chip: 3 or 4; sds: 0~1; phyad: 0; frame:0~x;

 dump:   -dump amp cfg;please input chip: 3 or 4; sds:0~1;
```

# Tools

## Update Firmware Checksum Calculator

[calcsum.py](/tools/calcsum.py)

```bash
usage: calcsum.py [-h] [-u] firmware

SWTG Update Firmware Checksum Calculator

positional arguments:
  firmware

options:
  -h, --help    show this help message and exit
  -u, --update  Re-calculate sums
```

## Generate Flash Security Register/Sector Data (Web Managed)

### CH341A Mini Programmer Setup

3.3V mod https://www.eevblog.com/forum/repair/ch341a-serial-memory-programmer-power-supply-fix/

![CH341A](https://github.com/user-attachments/assets/a40722e8-7620-4263-a019-2814289d137b)

### Dump Unique ID ie. command 42h

#### Linux

[IMSProg](https://github.com/bigbigmdm/IMSProg)

![Unique ID](https://github.com/user-attachments/assets/7fffc7ec-c8cb-433a-a0f1-45f65d04ba8e)

#### Windows

[AsProgrammer](https://github.com/nofeletru/UsbAsp-flash)

![Unique ID](https://github.com/user-attachments/assets/74aa02ff-ce02-4172-9834-d4d7a9ca14da)

### Generate 16-byte Data

#### Linux

> [!IMPORTANT]
> Replace the `uid` to match the first 4 bytes of the dumped unique id

```bash
uid='10093f30' bash -c 'echo -n "${uid,,}${uid,,}"' | openssl enc -nopad -aes-128-ecb -K $(printf '59494F4754fff00\0' | xxd -p | tr -d \n) | xxd -l 8 -p | tr -d \n | xxd -p
```

#### OS Agnostic

A simple python script

> [!IMPORTANT]
> Pass in the first 4 bytes of the dumped unique ID as the first argument. By default it will use the FM25Q16A unique ID used in the web managed products.

[encuid.py](/tools/encuid.py)

```shell
python -m venv .venv
source .venv/bin/activate
python3 -m pip install pycrypto
python3 encuid.py
```

### Write Security Register

> [!WARNING]
> This section is incomplete due the lack of software support.

#### Linux

flashrom requires an [abandoned patchset](https://review.coreboot.org/q/otp) and most likely requires changes
to `flashchips.c` to add the `.otp` field for supported chips.

Additionally, check the help `flashrom -h` to learn how to use the `--otp-X` args after compiling.

```bash
sudo apt-get install git make binutils build-essential ca-certificates libpci-dev libftdi-dev libusb-1.0-0-dev
git clone https://review.coreboot.org/flashrom.git
cd flashrom
git fetch https://review.coreboot.org/flashrom refs/changes/13/59713/7 && git checkout FETCH_HEAD
make
```

#### Windows

[AsProgrammer](https://github.com/nofeletru/UsbAsp-flash)

Scripts are required and need to be modified for each vendor/flash. e.g.

The [FM25Q16A_SS.pas](/tools/FM25Q16A_SS.pas) script is a modification of https://github.com/nofeletru/UsbAsp-flash/blob/master/scripts/GPR25L3203F_OTP.pas for the FM25Q16A https://www.fmsh.com/nvm/FM25Q16A_ds_eng.pdf
