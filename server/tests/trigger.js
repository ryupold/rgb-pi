{
    "triggers":
    [
        {
            "name":"energy saver",
            "condition":"{t:1,30,0}",
            "repeat":1,
            "action":
            {
                "commands":[{"type":"fade", "time":"5", "end":"{f:0,0,0}"}]
            }
        }
    ]
}