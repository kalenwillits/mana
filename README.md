# Mana

## Overview
**CURRENTLY UNFINISHED AND IN DEVELOPMENT**

Mana is an open source project management system built for developers and their
workflow. Written in Python 3.10 using the Django web framework as a backend.

Using mana should integrate closely with your git workflows and have as much 
usability put into git hooks as possible. 


### Mana cli examples

`mana new project TheGreatestGame` -> *Creates a new project in the mana hub called "TheGreatestGame"*
`mana use project TheGreatestGame` -> *Sets the project to active on the current user*
`mana pull project` -> *Generates a markdown representation of the project*

You can now create sprint(s) and task(s) the same way. 


In the future there will be more cli commands, however in the projets current state, elements need to be manually adjusted 
using the Django shell or Admin Panel.
