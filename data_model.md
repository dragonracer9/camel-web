```mermaid
---
title: Bank Data Layout
---
classDiagram
    Bet <|-- User
    note for User "Obvs has all other usual user things (username, passwd, etc...)"
    Bet : +Owners: |users|
    Bet : +int Value
    Bet : +String Name (Defaults to first User of side 1 and side 2 + date)
    Bet : +String Description
    Bet : +Bool: open
    Bet : +Winner (probs as like an int or something to determine what user won)
    class User{
        +String beakColor
        +swim()
        +quack()
    }
```