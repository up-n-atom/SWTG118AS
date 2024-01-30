# SWTG118AS and SWTG115AS RE

# Factory CGI

> Factory CGI can be accessed directly via the admin credentials

| CGI        | Description      |
| ---------- | ---------------- |
| ftdft.py   | Factory Defaults |
| ftlogo.py  | Factory Logo     | 
| ftcolor.py | Factory Colours  |

# Serial CLI


## Boot Log

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

## Password

The *"uboot"* password is `Switch321`

## Commands

* `gpio`
* `stp`


# Tools

## Update Firmware Validator and Updater

[switchup.py](/tools/switchup.py)
