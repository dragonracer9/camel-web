```mermaid
graph TD;
    User-->Balance;
    User-->[Bet];
    Bet-->Owners: [Users];
    Bet-->Winner: [Users];
    Bet-->Value;
    Bet-->Entered: Date;
    Bet-->Due: Date;
    Bet-->Status: {oepn/closed}
```