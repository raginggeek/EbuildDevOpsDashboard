from flask import Flask
from flask import render_template
import json
from configparser import ConfigParser,ExtendedInterpolation
from UtilFunctions import get_script_path

app = Flask(__name__)


@app.route('/')
def hello_world():
    parsedpretend = parse_pretend()
    return render_template('pretendresults.html', title="", ebuilds=parsedpretend)

@app.route('/world/json')
def json_world_data():
    parsedpretend = parse_pretend()
    return json.dumps(parsedpretend)

def parse_pretend():
    output = []
    with open(worldpretendcache) as file:
        data = file.readlines()
    for line in data:
        parsedline = {}
        parsedline["buildtype"] = "ebuild"
        packageflags = []
        packagecompflags = {}
        parsedline["packagename"] = ""
        parsedline["previousversion"] = ""
        parsedline["size"] = ""
        if line.startswith("["):
            flagsplit = line.split(" ] ")
            flags = flagsplit[0].lstrip("[")
            remainingline = flagsplit[1]
            if flags.startswith("ebuild"):
                buildtype = "ebuild"
                flags = flags.lstrip("ebuild")
            elif flags.startswith("blocks"):
                buildtype = "blocker"
                flags = flags.lstrip("blocks")
            flags = flags.strip()
            for flag in flags:
                packageflags.append(flag)
            quotebreak = remainingline.split("\"")
            quotebreak[1::2] = (string.replace(" ", "|") for string in quotebreak[1::2])
            remainingline = "\"".join(quotebreak)
            lineparts = remainingline.split()
            sizefound = False
            for part in lineparts:
                if parsedline["packagename"] == "":
                    parsedline["packagename"] = part
                elif part.startswith("["):
                    parsedline["previousversion"] = part
                elif '=' in part:
                    flagpieces = part.split('=')
                    packagecompflags[flagpieces[0]] = flagpieces[1].replace("|", " ").strip("\"")
                elif part.isnumeric():
                    sizefound = True
                    parsedline["size"] = part
                elif sizefound:
                    parsedline["size"] += " " + part
            parsedline["buildflags"] = packageflags
            parsedline["useflags"] = packagecompflags
            output.append(parsedline)
    return output

basepath = get_script_path()
configFile = basepath + '/config/defaults.ini'
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(configFile)
worldpretendcache = ""
if 'GentooWorldDash' in config:
    worldpretendcache = config['GentooWorldDash']['CacheFile']
if __name__ == '__main__':
    app.run()

