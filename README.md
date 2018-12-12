krieg
=====

Retrieving and parsing Steams personal game data on TF2. And doing stuff with it, eventually.

Instructions
--
Currently not the most elegant solution, but here it goes. Tested only on Chromium browsers for now.
1. Go to https://steamcommunity.com/my/gcpd/440?tab=playermatchhistory
2. Open the developer tools (usually F12), tab 'Sources', tab 'Snippets'
3. Add new snippet, copy the contents of fetch.js. Ctrl+Enter or just click the run button
4. Wait till it's done, then save the console output (right click > 'Save as') with a .log ending in the krieg folder
5. Run extract.py
