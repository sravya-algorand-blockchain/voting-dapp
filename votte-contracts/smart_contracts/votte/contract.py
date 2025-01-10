from algopy import ARC4Contract, UInt64, String, LocalState, Txn, Global,op,urange
from algopy.arc4 import abimethod

class Voting(ARC4Contract):
    title: String
    description: String
    noOfOptions: UInt64
    option1: String
    option2: String
    option3: String
    option4: String
    option1Votes: UInt64
    option2Votes: UInt64
    option3Votes: UInt64
    option4Votes: UInt64
    startsAt: UInt64
    endsAt: UInt64
    vote_status: UInt64

    def __init__(self) -> None:
        self.title = String("")
        self.description = String("")
        self.noOfOptions = UInt64(0)
        self.option1 = String("")
        self.option2 = String("")
        self.option3 = String("")
        self.option4 = String("")
        self.option1Votes = UInt64(0)
        self.option2Votes = UInt64(0)
        self.option3Votes = UInt64(0)
        self.option4Votes = UInt64(0)
        self.startsAt = UInt64(0)
        self.endsAt = UInt64(0)
        self.vote_status = UInt64(0)
        self.localState = LocalState(UInt64)

    @abimethod()
    def create_vote(self,title:String,description:String,noOfOptions:UInt64,option1:String,option2:String,option3:String,option4:String,endsAt:UInt64) -> None:
        assert self.vote_status == 0, "Vote already created"
        assert noOfOptions>=2 and noOfOptions<=4, "Number of options should be between 2 and 4"
        assert Global.latest_timestamp < endsAt, "Invalid end time"
        self.title = title
        self.description = description
        self.noOfOptions = noOfOptions
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.option1Votes = UInt64(0)
        self.option2Votes = UInt64(0)
        self.option3Votes = UInt64(0)
        self.option4Votes = UInt64(0)
        self.startsAt = Global.latest_timestamp
        self.endsAt = endsAt
        self.vote_status = UInt64(1)

    @abimethod()
    def vote(self, option: UInt64) -> None:
        assert Global.latest_timestamp < self.endsAt, "Voting has ended"
        assert Global.latest_timestamp > self.startsAt, "Voting has not started"
        assert option>=1 and option<=self.noOfOptions, "Invalid option"

        val,exist = self.localState.maybe(Txn.sender)
        assert not exist, "Already voted"
        self.localState[Txn.sender] = option
        match option:
            case 1:
                self.option1Votes += 1
            case 2:
                self.option2Votes += 1
            case 3:
                self.option3Votes += 1
            case 4:
                self.option4Votes += 1
            case _:
                op.exit(0)

    @abimethod(allow_actions=['OptIn'])
    def opt_in(self) -> None:
        pass
