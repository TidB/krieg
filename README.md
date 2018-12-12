krieg
=====

Retrieving and parsing Steams personal game data on TF2. And doing stuff with it, eventually.

Instructions
--
Currently not the most elegant solution, but here it goes. Tested only on Chromium browsers for now.
1. Go to https://steamcommunity.com/id/my/gcpd/440?tab=playermatchhistory
2. Open the developer tools (usually F12), tab 'Sources', tab 'Snippets'
3. Add new snippet, copy the contents of fetch.js. Ctrl+Enter or just click the run button
4. Wait till its done, then copy the output into a *.log file
5. Run extract.py