# Changes made following [CVE-2021-45105](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-45105)

## Affected saves

| 1.7 – 1.11.2 | 1.12 – 1.16.5      | 1.17         | 1.18  |
| ------------ | ------------------ | ------------ | ----- |
| NWSC 1       | NWSC 2.2           | NWSC 5       | *n/a* |
| NWSC 2       | NWSC 3             | ~~NWSC 6~~*  |
|              | NWSC 4             | ~~Parkour~~* |
|              | NWSC 4.2           |
|              | ~~Ubuntu Test 1~~* |
|              | ~~Ubuntu Test 2~~* |

> \* These saves are upgraded to 1.18.1 (or later, if compatible) since there is no need for them to be hosted on their original version.
>
> \* NWSC 6 was updated to 1.18.1.


## Changes

### Launch script

The launch script will now look for a `mp_args.txt` file in the server folder and will use its content to append the launch arguments.

### Save folders

Save folders of the affected versions are monkey-patched with the appropriate Log4j configuration files to be loaded by the launch arguments.

Affected saves will contain:

* An `mp_args.txt` file that contains the additional launch arguments.

* *For servers running on versions 1.7 – 1.11.2,* a Log4j config file `log4j2_17-111.xml`.

* *For servers running on versions 1.12 – 1.16.5,* a Log4j config file `log4j2_112-116.xml`.
   > *Servers on version 1.17 and above do not need an additional configuration file.*


# From [minecraft.net](https://www.minecraft.net/en-us/article/important-message--security-vulnerability-java-edition)

### GAME SERVER

If you’re hosting your own Minecraft: Java Edition server, you'll need to take *different* steps depending on which version you’re using, in order to secure it.

* 1.18: Upgrade to 1.18.1, if possible. If not, use the same approach as for 1.17.x:

* 1.17: Add the following JVM arguments to your startup command line:
-Dlog4j2.formatMsgNoLookups=true

* 1.12-1.16.5: Download [this file](https://launcher.mojang.com/v1/objects/02937d122c86ce73319ef9975b58896fc1b491d1/log4j2_112-116.xml) to the working directory where your server runs. Then add the following JVM arguments to your startup command line:
-Dlog4j.configurationFile=log4j2_112-116.xml

* 1.7-1.11.2: Download [this file](https://launcher.mojang.com/v1/objects/4bb89a97a66f350bc9f73b3ca8509632682aea2e/log4j2_17-111.xml) to the working directory where your server runs. Then add the following JVM arguments to your  startup command line:
-Dlog4j.configurationFile=log4j2_17-111.xml

* Versions below 1.7 are not affected

