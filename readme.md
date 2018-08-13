## ColorFight 

---
### File Description:
```
Project
   |----------- sever.py    //Include 
   |----------- game.py     //Include Game logic function
   |----------- player.py   //Define player attribute and set&get function
   |----------- ai.py       //Is a subclass of Class:Player , redefine "Get Attack" function by using RL
   |----------- settings.py //Define Global function and Global var
   |----------- index.html  //For web client
   |----- js
   |      |--------- start.js   //Start game and define 
   |      |--------- render.js  //Function for draw each element
   |      |--------- game.js    //Control game UI logic
   |      |--------- socket.js  //For deal message were send from WebSocket   
   |----- css
   |      |--------- main.css
```

### Prerequisites:

>- Using python 3.5+
>- Install aiohttp and async  

### Usage:
>- Edit your server address and Port at the end of sever.py
`web.run_app(app, host='YOUR SERVER ADDRESS', port=YOUR PORT)`
>- Change the url in initConnect function at socket.js to ServerAddress:Port/connect
>- enter the URL into your browser's address bar ,then you will begin game