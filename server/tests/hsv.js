{
    "commands":[
        {
            "type":"loop",
            "condition":"{b:1}",
            "commands":
            [
                {
                    "type":"fade",
                    "time":"10",
                    "end":"{f:1,0,0}"
                },
				{
                    "type":"fade",
                    "time":"10",
                    "end":"{f:1,1,0}"
                },
				{
                    "type":"fade",
                    "time":"10",
                    "end":"{f:0,1,0}"
                },
				{
                    "type":"fade",
                    "time":"10",
                    "end":"{f:0,1,1}"
                },
				{
                    "type":"fade",
                    "time":"10",
                    "end":"{f:0,0,1}"
                },
				{
                    "type":"fade",
                    "time":"10",
                    "end":"{f:1,0,1}"
                }
            ]
        }
    ]
}

