# Background
Ever since I visited Çanakkale many many years ago I always wondered what it would be like to operate one of those fortress guns the Ottomans used as coastal artillery against the combined British-French fleet.

![Ottoman artillery piece](https://www.navyingallipoli.com/images/Artillery/240_35_rm02.jpg)

Sure, there are movies out there with lots of gunfire but most of those are artistic depictions of a war and do not focus much on the technicalities and practicalities of the guns in particular. So I looked up some
stuff about the guns (mainly here: https://www.navyingallipoli.com/Artillery_Heavy.asp) and decided to recreate it on my own.

The 240 mm L/35 Krupp Fortress Gun appears it can shoot a shell of 215 kg up to a range of 11-15 km or so. That's apparently the type of gun the infamous Binbaşı (Corporal) Seyit was stationed at. I assumed a max. muzzle velocity 
of 700 m/s-ish for a late 1800's gun, a maximum elevation of 30 degrees and tried to adjust the shell drag coefficient such that the range maxes out at 12-13 km. I know I "made up" some of the numbers and assumptions here but
just wait until you see how much worse my map building is :)

The (enemy) ships are all the same, which are 21 m wide and 128 m long. That nearly matches that of pre-dreadnought HMS Ocean's size (from the Wikipedia page) which struck a mine during the naval battle at Gallipoli and sunk.

![HMS Ocean](https://upload.wikimedia.org/wikipedia/commons/8/82/HMS_Ocean_QE2_66.jpg)

Lastly, the work on recrating the map is terrible because in immediate OpenGL mode I can not get the computer to render complex terrain without freezing and the motherboard blowing up. So the map is a rectangle essentially.

The actual Çanakkale Strait is about this large:

<img width="997" height="764" alt="canakkale_meas" src="https://github.com/user-attachments/assets/1d962acb-1c8c-425a-b855-3f8d57d281a4" />

The game map area is about this large:

<img width="1920" height="1080" alt="game_area" src="https://github.com/user-attachments/assets/4200f178-9658-4621-bd9f-815770e847de" />

...so basically, all things considered, this is a weak simulator recreation of a Fortress Gun. BUT, it should give folks an idea about the length scales, time scales and the precision required to aim the cannons.

Plus, there are further simplifications. There is only one cannon on the game map, and only 3 ships at a time. Mine fields are not placed historically, and there is an impenetrable minefield 150 meters ahead of the map origin. 
Rest of the waters are clear. Currently, the ships do not maneuver or shoot back at all. The cannon reloading is absurdly fast (otherwise it gets boring, even though this is meant to be a recreation). Also keep in mind that
there is no wind and each shot and shell are perfectly and excellently identical - no manufacturing imperfections and such.

Please understand this is not a naval combat simulator game, but a ballpark order-of-magnitude recreation of a coastal defense cannon.

# Controls
WASD to rotate (azimuth and elevation) the cannon

R/F to increase/decrease amount of propellant charges

X to fire

Shift + mouse movement to rotate camera

Y to switch to cannon camera

U to switch to ship camera

O to switch to shell camera (if there is an artillery shell in flight)

<img width="1584" height="545" alt="ships" src="https://github.com/user-attachments/assets/4cb9ed0d-7d88-49ff-b24f-1a05a4fb086d" />

<img width="1100" height="715" alt="cannon" src="https://github.com/user-attachments/assets/dc3ae9a8-5a5f-4316-b3d1-09640bb5475c" />

# Further Work

If you have more in-depth info on the cannons, and especially if you can help model the equipment, terrain, ships etc. or do anything at all to help, all is welcome.

# Background Music Credits

"Exciting Trailer" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ 

"Industrial Revolution" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/ 

(This is also written in the _music_copyright.txt file).
