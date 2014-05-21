{
    "commands":[
        {
            "type":"loop",
            "condition":"{b:1}",
            "commands":
            [
                {
                    "type":"fade",
                    "time":"{r:10,20}",
                    "end":"{r:0-1,0-1,0-1}"
                }
            ]
        }
    ],

    "filters":[
        {
            "type":"volumefade",
            "onfinish":"stop",
            "progress":"lower",
            "limit":0
        }
    ],

    "request":
    {
        "type":"runtime",
        "variable":"color"
    }
}

