# SWTG118AS and SWTG115AS RE

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
| `web`                   | Sets the web mode                        ||

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

| Firmware Offset | Length     | Description              |
| --------------- | ---------- | ------------------------ |
| `0x001FC000`    | `0x00000006` | MAC address              |
| `0x001FD000`    | `0x0000023D` | Factory settings         |
| `0x001FE000`    | `0x00000A42` | User settings            |

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

## Update Firmware Validator and Updater

[switchup.py](/tools/switchup.py)

```bash
usage: switchup.py [-h] [-u] firmware

SWTG update firmware tool

positional arguments:
  firmware

options:
  -h, --help    show this help message and exit
  -u, --update  Re-calculate sums
```
