{
    "commands":
    [
        {"type":"cc", "color":"{f:0,0,0}"},
        {
            "type":"fade",
            "time":"10",
            "end":"{f:1,1,1}"
        }
    ],

    "triggers":
    [
        {
            "name":"test",
            "condition":"{c:{f:1,1,1}}",
            "repeat":1,
            "action":
            {
                "commands":[{"type":"fade", "time":"5", "end":"{f:0,0,0}"}]
            }
        }
    ]
}