{
    "commands":
    [
        {"type":"cc", "color":"{f:0.5,0.5,0.5}"}
    ],

    "triggers":
    [
        {
            "name":"test",
            "condition":"{c:{f:1,1,1}}",
            "action":
            {
                "commands":[{"type":"fade", "time":"5", "end":"{f:0,0,0}"}]
            }
        }
    ]
}