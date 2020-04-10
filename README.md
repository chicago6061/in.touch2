# in.touch2 wireless remote control for your spa

Simple Python class for controlling spa with an in.touch2 device (https://geckointouch.com/).

## Experimental Code!

Experimental code based on analysis of mobile app network traffic.

## Example

\# ./spa.py<br>
```
Channel: 30<br>
Setpoint: 70.  Current Temperature: 90.  Lights: 0.  Version: inYT 177 v3.0.  Base config: 5.
```

<br>
\# ./dumpall.py<br>
```
...
256 0x12 Hours, 
257 0x0 QuietState, 
258 0x0 UdP5(0),UdBL(1), 
259 0x0 UdP1(0),UdP2(2),UdP3(4),UdP4(6), 
260 0x20 P5(0),BL(1),CP(2),O3(3),L120(4),MSTR_HEATER(5),SLV_HEATER(6),Waterfall(7),Heating(5), 
261 0x2 P1(0),P2(2),P3(4),P4(6), 
262 0x5 FilterAccess(0),EconomyAccess(2),OnzenAccess(1), 
263 0x0 RemoteFiltAction, 
...
```
For 260, value is 0x20 => 0010 0000 => 5th bit is set and thus MSTR_HEATER(5) is on<br>
For 261, value ix 0x02 => 0000 0010 => 1st bit is set and thus P1 is on<br>
<br>

\# ./dumpreminders.py<br>
```
Connected.  ('192.168.2.231', 10022)
RinseFilter 30 days
CleanFilter 60 days
ChangeWater 90 days
CheckSpa -38 days
```

## TODO

<ul>
<li>Figure out initial handshake mechanism to obtain Source Connection(?) value.</li>
<li>Decode additional messages
  <ul>
  <li>Lines 1-6 of GetStatus</li>
  </ul>
</li>
</ul>

## Contributing

Contributions are welcome!
