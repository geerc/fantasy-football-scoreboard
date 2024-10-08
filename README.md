Forked from: https://github.com/mikemountain/fantasy-football-scoreboard

# fantasy-football-scoreboard
![I promise to change this picture when I actually build my own](imgs/Scoreboard.jpg)

Display your favourite fantasy football team score on an raspberry pi powered LED matrix. Currently supports 64x32 boards only, and EITHER the Sleeper OR YAHOO fantasy platforms! We have Yahoo!!!

### NFL LED Scoreboard
Hey, I also made an [NFL LED scoreboard](https://github.com/mikemountain/nfl-led-scoreboard), which you really should go check out and star. Because, let's face it, you're gonna hate seeing your fantasy team after a while.

### Credit and inpsiration
This project was inspired by the [nhl-led-scoreboard](https://github.com/riffnshred/nhl-led-scoreboard), who based THEIR project off of the [mlb-led-scoreboard](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard). Go check them out, and start watching hockey if you don't already (and baseball too but I love hockey more (go Leafs!)).

### Donate
<a href="https://paypal.me/themikemountain/"><img src="https://github.com/andreostrovsky/donate-with-paypal/blob/master/dark.svg" height="40"></a>

If you enjoyed this project, my NFL project, or if you're just feeling generous, consider buying me a beer. Cheers! :beers: 
You can also PM me on reddit under /u/mikemountain if you need help but don't think it requires an issue!

## Features (v1.0.0)

### UPGRADING TO v1.0.0
There have been some decent changes since v0.0.5. Check the Troubleshooting section if you get any errors running the following steps, but to get to this latest version:
1. Run the command `git stash`. This will take any "local changes" you made (such as to the config, etc) and "store" them so that you can update the local code
2. Run the command `git fetch && git checkout master`. This will tell your scoreboard to look for new updates, and then switch to the main code branch.
3. Run the command `git pull`. This will pull down all the latest changes to your board.
4. Run the command `cp config.json.example config.json`. This will make a copy of the example config to use as your regular config file.
5. Run the command `nano config.json` and then edit in the fields you require (steps for Yahoo and ESPN are further below in the README)
6. After you've set up the config.json, run the board as normal `sudo python3 main.py` with whatever flags you choose to use.
7. Watch your team lose, try not to cry, cry a lot.

### YAHOO SETUP STUFF
Okay, so Yahoo is gonna be a bit funky. 
1. First, go to https://developer.yahoo.com/ then 'My Apps' and then 'YDN Apps'.
2. On the lefthand panel, click 'Create an App'.
3. Name the app something like "Fantasy Football Scoreboard" in the 'Application Name' block.
4. In the Redirect URL section, just enter https://localhost:8080.
5. Under the 'API Permissions' sections select 'Fantasy Sports' and then make sure that 'Read' is selected.
6. Click create app.
Woo, you've technically created a Yahoo App and you will see two important pieces of information: the Client ID (Consumer Key), and Client Secret(Consumer Secret), which will look like long strings of random letters and numbers.
You will need to enter these two pieces of information into the config, along with your League ID. 
When you run this for the first time, you're going to get some Yahoo stuff happening - a browser window will pop up (if possible), and a link to that browser window will also appear in the console. It'll look similar to something like `https://api.login.yahoo.com/oauth2/request_auth?client_id=CLIENTIDHERE&redirect_uri=oob&language=en-us&response_type=code` and this is normal. If you don't get the browser window popping up, copy and paste this URL into a browser window, and log into Yahoo to authorise the scoreboard. Once you log in, you'll be given a code, which you'll need to type into the console. This is just to authorise the app, and a `token.json` file will be generated into an `./auth` directory so that this doesn't happen every time.

After this, run `sudo pip install yahoo_oauth` so that you have the required library to interact with Yahoo.

I _think_ this should be all the info people need - feel free to reach out if you need more help!

### ESPN SETUP STUFF
You'll need a few pieces of info for ESPN to work - namely some cookies, your league ID and your team ID. You can get your league ID and team ID by just simply looking at the url when you click your team homepage/roster page. In Chrome, you can go to Preferences -> Advanced -> Content Settings -> Cookies -> See all cookies and site data, look for ESPN, and put the "content" of the SWID and the ESPN_S2 cookies in the config, INCLUDING THE {CURLY BRACES} of the SWID.
Note!!! ESPN allows SVGs as team images. There's no easy way for the project to display SVGs, or even convert them to PNGs, so the actual best solution is this:
1. Run the project. If there are SVGs it will download the files, then alert you, and then fail to run properly.
2. Run `sudo apt-get update && sudo apt-get install inkscape`
3. Run `cd logos; find -name "*.svg" -exec sh -c 'sudo inkscape $1 --export-png=${1%.svg}.png' _ {} \;`
Ignore any messages that say "failed to get connection"; if you see `Bitmap saved as:` lines, you should be able to `cd ..` back into the project and run it again, and it should work. I apologise that it's a bit annoying but it's the way she goes (for now).

### Pregame
Currently shows your opponent's avatar, and their name (if it's 12 characters or less, otherwise it won't fit, see the picture at the top of the README). ![nameless and shameless](imgs/no_team_name_preview.jpg) Hoping to incorporate projections in future releases.

### Live scoring updates 
Starting at ~8pm Eastern Thursday, the score will be updated every 20s during game times (Thursday 8pm-12am, Sunday 1pm-12am, Monday 8pm-12am). ![live matchup](imgs/live_matchup.jpg) The colours will change red if a score goes down, and green if a score goes up. ![colour score](imgs/score_changes.jpg) There is also a "big play" notifier of when a team's score goes up by more than 5 points, because that's exciting. The team's score will go gold to show who got the big play. ![big play](imgs/big_play_capture.jpg)

Here's a gif that shows you what this would look like (excuse the shaky hands please, I was updating my testing REST API with one hand and filming with the other). ![score gif](imgs/big_play_and_updates.gif)

I plan to set this so that it only does these checks during actual game times, because there's no real point in checking for game updates on non-game days or during non-game times on gamedays. Eventually, I'd like to only check for score updates if there's a player in the matchup who's playing.

### Postgame
The board will stay in a post-game state until the next week, and will easily disappoint you with a quick glance. Loser is red, winner is green, with LOSS or WIN in between for that extra oomph. ![post game recap](imgs/accurate_postgame.jpg)

### Off season
It displays a message that it's the off season. ![man it's offseason, take a break](imgs/off_season.jpg) You should just turn it off and plan to be heartbroken again next year.

## Roadmap

Future plans include:
* cycle through league scores on off-game times during the week (Post game could cycle through each matchup's result)
* different animations for good plays vs bad plays (nobody wants to see "BIG PLAY" and then see it's your opponent getting the points)
* cycle through multiple teams in multiple leagues so you don't just have to pick your favourite team (although we all have one best league)
* maybe some fun stuff for the draft like who just drafted whom and a countdown clock or something I don't know but it'll be flashy (can't do this yet with current sleeper api)
* analyze your team weaknesses and help with waiver pickups (will not do this)

## Installation
### Hardware Assembly
The [mlb-led-scoreboard guys made a great wiki page to cover the hardware part of the project](https://github.com/MLB-LED-Scoreboard/mlb-led-scoreboard/wiki). There's also this [very handy howchoo page](https://howchoo.com/g/otvjnwy4mji/diy-raspberry-pi-nhl-scoreboard-led-panel) which is what I mainly followed.

### Software Installation
#### Raspbian Distribution
It is recommended you install the Lite version of Raspbian from the [Raspbian Downloads Page](https://www.raspberrypi.org/downloads/raspbian/). This version lacks a GUI, allowing your Pi to dedicate more system resources to drawing the screen.

#### Requirements
You need Git for cloning this repo and PIP for installing the scoreboard software.
```
sudo apt-get update
sudo apt-get install git python-pip
```

#### Installing the software
This installation process might take some time because it will install all the dependencies listed below.

```
git clone --recursive https://github.com/mikemountain/fantasy-football-scoreboard
cd fantasy-football-scoreboard/
sudo chmod +x install.sh
sudo ./install.sh
```
[rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python#building): The open-source library that allows the Raspberry Pi to render on the LED matrix.

[requests](https://requests.kennethreitz.org/en/master/): To call the API and manipulate the received data.

## Testing & Optimization (IMPORTANT)
If you have used a LED matrix on a raspberry pi before and know how to run it properly, then you can skip this part. 

If you just bought your LED matrix and want to run this software right away, reference the [rpi-rgb-led-matrix library](https://github.com/hzeller/rpi-rgb-led-matrix/). Check out the section that uses the python bindings and run some of their examples on your screen. For sure you will face some issues at first, but don't worry, more than likely there's a solution you can find in their troubleshooting section.
Once you found out how to make it run smoothly, come back here and do what's next.

### Adafruit HAT/bonnet
If you are using any thing from raspberry pi 3+ to the newest versions with an Adafruit HAT or Bonnet, here's what [RiffnShred](https://github.com/riffnshred) did to run his board properly. It seems these are more recommendations than things you 100% absolutely need to do, but are probably beneficial anyway.

* Do the hardware mod found in the [Improving flicker section ](https://github.com/hzeller/rpi-rgb-led-matrix#improving-flicker).
* Disable the on-board sound. You can find how to do it from the [Troubleshooting sections](https://github.com/hzeller/rpi-rgb-led-matrix#troubleshooting)
* From the same section, run the command that remove the bluetooth firmware, unless you use any bluetooth device with your pi.

Finally, here's the command to get 'er goin':
```
sudo python3 main.py --led-gpio-mapping=adafruit-hat-pwm --led-brightness=60 --led-slowdown-gpio=2
```

### Configuration
Copy the config.json.example file from the root folder, save it as config.json and set the values you need:

```
platform - set this to either sleeper, yahoo, or espn.

ESPN
league_id               Set this to your ESPN league ID. This is a code that can be found in the URL after leagueId= when you visit your team homepage/roster page.
team_id                 Set this to your ESPN team ID. This is a number that can be found in the URL after teamId= when you visit your team homepage/roster page.
swid                    In Chrome, go to Preferences -> Advanced -> Content Settings -> Cookies -> See all cookies and site data, look for ESPN, copy the SWID Content data and paste it here INCLUDING THE { BRACES }.
espn_s2                 In Chrome, go to Preferences -> Advanced -> Content Settings -> Cookies -> See all cookies and site data, look for ESPN, copy the espn_s2 Content data and paste it here.

SLEEPER
league_id               This value can be found in your Sleeper league's URL: https://sleeper.app/leagues/<league_id>/team
user_id                 Run the following command, value will be listed in the output. Replace <username> with the username that you use to login to Sleeper: curl "https://api.sleeper.app/v1/user/<username>"

YAHOO
consumer_key            This will be found in the YDN info that you generate using the Yahoo Setup Stuff section above.
consumer_secret         This will be found in the YDN info that you generate using the Yahoo Setup Stuff section above.
league_id               You should be able to find this info in the URL, I'm not positive where but it should be in there (haven't seen it)
team_id                 You should be also able to find this info in the URL, I'm not positive where but it should be in there (haven't seen it)
game_code               Don't change this! It corresponds to "NFL" for some reason in the Yahoo API. It changes yearly. This needs to be automated but I have forgotten how I figured this info out because I've been working on this stuff for _way_ too long recently.

debug                   Just a flag that prints out more debug info.
testing                 Flag that sets testing (but this is broken, lol)
```

Now, in a terminal, cd to the fantasy-football-scoreboard folder and run this command. 
```
sudo python main.py 
```
**If you run your screen on an Adafruit HAT or Bonnet, you need to supply this flag.**
```
sudo python main.py --led-gpio-mapping=adafruit-hat
```

### Troubleshooting
* If you run `git fetch` or something and get `error: cannot open .git/FETCH_HEAD: Permission denied` then run the command `sudo chown -R $(whoami) .git/` which will fix the permissions for git. Re-run the failed command.
* If using Yahoo, you may need to run `mkdir auth; sudo chmod 0777 auth/` if you get an `IOError: [Errno 13] Permission denied` error.

### Flags
Use the same flags used in the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix/) library to configure your screen.
```
--led-rows                Display rows. 16 for 16x32, 32 for 32x32. (Default: 32)
--led-cols                Panel columns. Typically 32 or 64. (Default: 32)
--led-chain               Daisy-chained boards. (Default: 1)
--led-parallel            For Plus-models or RPi2: parallel chains. 1..3. (Default: 1)
--led-pwm-bits            Bits used for PWM. Range 1..11. (Default: 11)
--led-brightness          Sets brightness level. Range: 1..100. (Default: 100)
--led-gpio-mapping        Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm
--led-scan-mode           Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)
--led-pwm-lsb-nanosecond  Base time-unit for the on-time in the lowest significant bit in nanoseconds. (Default: 130)
--led-show-refresh        Shows the current refresh rate of the LED panel.
--led-slowdown-gpio       Slow down writing to GPIO. Range: 0..4. (Default: 1)
--led-no-hardware-pulse   Don't use hardware pin-pulse generation.
--led-rgb-sequence        Switch if your matrix has led colors swapped. (Default: RGB)
--led-pixel-mapper        Apply pixel mappers. e.g Rotate:90, U-mapper
--led-row-addr-type       0 = default; 1 = AB-addressed panels. (Default: 0)
--led-multiplexing        Multiplexing type: 0 = direct; 1 = strip; 2 = checker; 3 = spiral; 4 = Z-strip; 5 = ZnMirrorZStripe; 6 = coreman; 7 = Kaler2Scan; 8 = ZStripeUneven. (Default: 0)
```

## Licensing
This project uses the GNU General Public License v3.0. If you intend to sell these, the code must remain open source and you at least have to tell your leaguemates how cool I am (please, I need this).

