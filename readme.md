## ColorFight 

---
### File Description:
```
Project
   |----------- sever.py    //Include 
   |----------- game.py     //Include Game logic function
   |----------- player.py   //Define player attribute and set&get function
   |----------- ai.py       //Is a subclass of Class:Player , redefine "Get Attack" function by using RL
   |----------- settings.py //Define Global function and Global var for py
   |----------- index.html  //For web client
   |
   |----------- DeepQNetwork.py     //Class include framework of my network
   |----- my_net                    //File for record Network
   |
   |----- js
   |      |--------- start.js       //Start game and define 
   |      |--------- render.js      //Function for draw each element
   |      |--------- game.js        //Control game UI logic
   |      |--------- socket.js      //For deal message were send from WebSocket  
   |      |--------- settings.js    //Define Global function and Global var for js
   |----- css
   |      |--------- main.css
```

### Prerequisites:

>- Using python 3.5+
>- Install aiohttp and async  

### Usage:
>- Edit your server address and Port at the end of sever.py
>`web.run_app(app, host='YOUR SERVER ADDRESS', port=YOUR PORT)`
>- Change the url in initConnect function at socket.js to ServerAddress:Port/connect
>- enter the URL into your browser's address bar ,then you will begin game

### rules:
>- Only Up, Down, Left, Right and D keys can be used. 
>- The value of site is determined by the time character stays and represented by color's depth, which decays with time. 
>- When reaching the darkest color, a fence can be created (Defence is button D), and the value of the fence won't decay with time. 
>- Earn a point for each occupation. Defeat enemies to get half of their score.
