# Fear Demo

## Overview

## How to run app at the first time
0. Open terminal
1. Type the following commands in the terminal:
    ```
    cd .
    cd Desktop/fear_demo
    ```
2. Type in terminal:
    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
3. After installation, type in terminal:
    ```
    brew install python
    ```
4. Create virtual environment:
    ```
    python3 -m venv fear_demo_venv
    ```
5. Activate virtual environment:
    ```
    source fear_demo_venv/bin/activate
    ```
6. Type in terminal for installation python requirements:
    ```
    pip install -r requirements.txt
    ```
7. Type command in the terminal to run app:
    ```
    python3 app.py
    ```
8. If you want to kill app, press combination `control + C`

All screenshots of screens and webcam, you can check in folders:
- `fear_demo/screenshots/screen` - screen shot
- `fear_demo/screenshots/webcam` - webcam shot


## How to run app after installation
0. Open terminal
1. Type the following commands in the terminal:
    ```
    cd .
    cd Desktop/fear_demo
    ```
2. Activate virtual environment:
    ```
    source fear_demo_venv/bin/activate
    ```
3. Type command in the terminal to run app:
    ```
    python3 app.py
    ```
4. If you want to kill app, press combination `control + C`


## Parameterization
The application allows you to configure several parameters:
* `delay_between_screenshots` - set the time interval in seconds after which repeated screenshots are taken during 
continuous detection of the fear emotion. Set value in seconds. Default: 3.0
* `fear_buffer_seconds` - minimal time interval when allowed to do first screenshot after fear emotion detection. Set 
value in seconds. Default: 0.5
* `save_screenshots_with_boxes` - display face box with probability on saving screenshots. Set value in boolean format 
(True/False). Default: True (is on)
* `show_webcam_win` - show camera while app is working. Set value in boolean format (True/False). Default: True (is on)

Examples how to use argument in app:
```
python3 app.py --delay_between_screenshots 1.0 --show_webcam_win False
```

You can specify not all parameters and all in any order.
