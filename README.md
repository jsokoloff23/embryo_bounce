<!--
MIT License

Copyright (c) 2021 Othneil Drew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rplab/LS_Pycro_App">
    <img src="https://raw.githubusercontent.com/jsokoloff23/embryo_bounce/main/embryo.PNG" alt="Logo" width="80" height="80">
  </a>

## embryo_bounce

  <p align="left">
    embry_bounce is a pygame-based pong-style game with zebrafish assets and hand motion controls! 
  </p>
</div>

## About
<p align="left">
    Hello! My name is Jonah and I'm a research assistant in the Parthasarathy lab in the Department 
    of Physics at the University of Oregon. This game was created as part of an interview process at CZBiohub.
  </p>

## Design

### Core
<p align="left">
    embryo_bounce is pygame-based and uses many of its core systems, such as its display, drawing, sound,
    surfaces, and event updates.
  </p>

  <p align="left">
    To better modularize the code, embryo bounce uses managers to manage certain aspects of the game.
    The managers include PositionManager, CollisionManager, DrawManager, DisplayManager, HighScoreManager,
    and SoundManager.
  </p>

### Controls
  <p align="left">
    For embryo_bounce's hand motion controls, it uses an OpenCV's VideCapture instance in a worker thread to create
    a constant stream of images. The images are then processed by MediaPipe, a Google ML and AI library. 
    MediaPipe's Hand Landmarks Detection is able to process images and determine if a hand is present as 
    well as the location of its prominent features (landmarks), which is returned as a Results object. 
    Each Result instance includes x,y coordinates (given as normalized floats) of each landmark, which 
    are then used to update the paddle position in the game!
  </p>

### Other Aspects
 <p align="left">
    The code style adheres to PEP8 for the most part. I usually use a linter but Line limits are broken when readability would be
    sacrificed (I'm a general proponent of 100 character limit). 
  </p>

### Assets
 <p align="left">
    The assets in the game are all zebrafish related (perhaps the sounds are debatable). Zebrafish are
    the primary imaging specimen used in our lab and one that is of great importance in modern biology.
 </p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This program has only been tested on Python 3.10.1 and 3.10.11 on macOS and Windows 11. 
Other operating systems and Python versions may work but use at your own risk.

For macOS users, MediaPipe version 0.10.10 does NOT work correctly on macOS. Version 0.10.9 is 
completely fine. As long as modules from requirements.txt are installed, this shouldn't be an issue.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jsokoloff23/embryo_bounce
   ```
2. Install dependencies from requirements.txt file
   ```sh
   pip install -r <cloned_repo_directory>/requirements.txt
   ```

### Starting

1. Run the `main.py` file located in the embryo_bounce folder and enjoy!
 ```sh
 python <cloned_repo_directory>/embry_bounce/main.py
 ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## How to Play
<p align="left">
  Once the game is launched, you'll be met with the main menu! It uses the arrow keys
  and enter to control. Hit start and move your hand up and down to move the paddle.
  Controls are much like original pong where the ball location on the paddle determines
  its angle.
</p>

<p align="left">
  If a high score is achieved, enter your name and press enter! Check out the high scores
  from the main menu. When prompted to play again, hit y to restart the game or n to return
  to the main menu. You may also hit escape during the game to return to the main menu.
</p>

<p align="left">
  To exit, select the exit button on the main menu.
</p>

<p align="left">
  (I considered showing off more assets and an image of the gameplay here but I want it
  to be a surprise)
</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Email: jsokoloff23@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Code Acknowledgments
* [Pygame](https://github.com/pygame/)
* [MediaPipe](https://github.com/google/mediapipe)
* [OpenCV](https://github.com/opencv/opencv)

## Asset Acknowledgements
* zebrafish.png taken from [CNN](https://www.cnn.com/2021/02/04/americas/zebrafish-fins-limbs-scn/index.html)
* embryo.png taken from [Pinterest](https://www.pinterest.com/pin/405183297731630365/)
* Background.jpg taken from [OpenGameArt](https://lpc.opengameart.org/content/underwater-background-0)
* All sounds and music from [Pixabay](https://pixabay.com/)


<!-- ONLINE RESOURCES -->
## Online Resources
* A _LOT_ of [Stack Overflow](https://stackoverflow.com/)
* [MediaPipe](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
* [NumPy](https://numpy.org/)
* [LearnOpenCV](https://learnopencv.com/)
* [discuss python forums](https://discuss.python.org/)
* [GeeksforGeeks](https://www.geeksforgeeks.org/)
* [ChatGPT](https://chat.openai.com/) (mostly for formatting/best practices)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
