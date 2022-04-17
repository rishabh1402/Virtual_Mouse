# Virtual_Mouse
## What it does
An AI-based mouse controller, that can be used as an alternative to the device.

## How it works
* Detects the **Index & Middle fingers**
* Detects which finger pointing up
* If **Index Finger Up (☝)** => *Move Operation :* The mouse will move according to your hand movements.
* If **Index & Middle Finger Up (✌)** => *Click Operation :* Click anything on the screen, like how we normally do.

## How to install
* Install Python 3 in you system from https://www.python.org/.
* Install the following libraries / packages using the command : **pip install _packageName_**
  1. cv2
  2. mediapipe
  3. math
  4. numpy
  5. os
* Keep both the files along with the *pallet* folder in same directory.
* Execute the **main.py** to run the program.

## How is it built
* **Hand Detection Module** : Class containing the *methods to detect hands & hand's postion*. 
* Python's **cv2 and mediapipe** libraries : Provide the *modules and methods to get hand landmarks and draw shapes* to mark them. 

## Prerequisite
* Pyhton >= 3.8.

## Steps to Download 
* Download and Extract the zip file.
* Open in the files in any text editor.
* Create an virtual environment to install the related libraries (in terminal).
```
py -m venv env
```
* Activate the virtual environment.
```
env\Scripts\activate
```
* Install the below mentioned libraries.
```
pip install opencv-python
```
```
pip install numpy
```
```
pip install pyautogui
```

## Demo

*Video Reference*: [<span style="color: #FE83C6">Virtual Mouse</span>](https://www.youtube.com/watch?v=p2APJ0ezTd0)
<br>
<br>

<hr>


