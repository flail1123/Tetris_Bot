# Tetris_Bot
To use:
```
git clone https://github.com/flail1123/Tetris_Bot.git
cd Tetris_Bot
python3 tetris.py
```
If not working make sure all appropriate libraries are installed including pyautogui and PIL:
```
python3 -m pip install --upgrade pip
python3 -m pip install Pillow
python3 -m pip install pyautogui
```

Description:

Bot opens https://www.freetetris.org/game.php in default browser and starts playing the game on set level using pyautogui library. 
It uses computer's mouse and keyboard so user SHOULD NOT touch them when program is running.
When the game is over the bot will quit by itself.
