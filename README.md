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

| CGI         | Description      |
| ----------- | ---------------- |
| menu_ft.cgi | Factory Menu     |
| ftdft.cgi   | Factory Defaults |
| ftlogo.cgi  | Factory Logo     | 
| ftcolor.cgi | Factory Colours  |

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

### Password

The *"uboot"* password is `Switch321`

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

## Generate Flash Security Register Data (Web Managed)

### Dump Unique ID ie. command 42h

#### Linux

[IMSProg](https://github.com/bigbigmdm/IMSProg) - Available from the **Chip Info** dialog

#### Windows

[AsProgrammer](https://github.com/nofeletru/UsbAsp-flash) 

### Generate 16-byte Data

#### Linux

Replace uid with the first 4 bytes of the unique id

```bash
uid='10093f30' bash -c 'echo -n "${uid,,}${uid,,}"' | openssl enc -nopad -aes-128-ecb -K $(printf '59494F4754fff00\0' | xxd -p) | xxd -l 8 -p | xxd -p
```

#### OS Agnostic

Replace uid with the first 4 bytes of the unique id

```python
#!/usr/bin/python3

from Crypto.Cipher import AES

uid = b'10093f30'
key = b'59494F4754fff00\0'

pt = uid + uid

aes = AES.new(key, AES.MODE_ECB)

dat = aes.encrypt(pt)

print(dat[:8].hex().encode('ascii').hex())
```

### Write Security Register

> [!WARNING]
> This section is incomplete due the lack of software support.

#### Linux

Requires addtional changes to `flashchips.c` to add the `.otp` field to supported chips.

Check the help for how to use the`--otp-X` args after compiling.

```bash
sudo apt-get install git make binutils build-essential ca-certificates libpci-dev libftdi-dev libusb-1.0-0-dev
git clone https://github.com/flashrom/flashrom
cd flashrom
git fetch https://review.coreboot.org/flashrom refs/changes/13/59713/7 && git checkout FETCH_HEAD
make
```

#### Windows

[AsProgrammer](https://github.com/nofeletru/UsbAsp-flash) - Scripts are required (read datasheet)

```
// FM25Q16A

{$eraseSS} // Erase Security Sector
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  SPIWrite(1, 1, $06); //write enable
  SPIWrite(0, 4, $44, 0,0,0);

  //Busy?
  sreg := 0;
  repeat
    SPIWrite(0, 1, $05);
    SPIRead(1, 1, sreg);
  until((sreg and 1) <> 1);

  SPIExitProgMode();
end

{$readSS} // Read Security Sectors
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  PageSize := 256;
  SectorSize := 1024;
  ProgressBar(0, (SectorSize / PageSize)-1, 0);

  for i:=0 to (SectorSize / PageSize)-1 do
  begin
    SPIWrite(0, 5, $48, 0,0,i,0);
    SPIReadToEditor(1, PageSize);
    ProgressBar(1);
  end;

  ProgressBar(0, 0, 0);
  SPIExitProgMode();
end

{$readSS} // Write Security Sectors
begin
  if not SPIEnterProgMode(_SPI_SPEED_MAX) then LogPrint('Error setting SPI speed');

  PageSize := 256;
  SectorSize := 1024;
  ProgressBar(0, (SectorSize / PageSize)-1, 0);

  for i:=0 to (SectorSize / PageSize)-1 do
  begin
    SPIWrite(1, 1, $06); //write enable
    SPIWrite(0, 4, $42, 0,0,i);
    SPIWriteFromEditor(1, PageSize, i*PageSize); //write data

    //Busy?
    sreg := 0;
    repeat
      SPIWrite(0, 1, $05);
      SPIRead(1, 1, sreg);
    until((sreg and 1) <> 1);

    ProgressBar(1);
  end;

  ProgressBar(0, 0, 0);
  SPIExitProgMode();
end
```

