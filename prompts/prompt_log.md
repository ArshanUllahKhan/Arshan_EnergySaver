# Prompt Log (Gen AI usage)
| # | Prompt (summary) | What AI returned | What I did |
|---|---|---|---|
| 1 | "Design if-then rules for a smart-home energy assistant (AC, geyser, lights, TV, washing machine)" | 6 rules with conditions/actions | Kept 6, added comfort + confidence scores |
| 2 | "Write a weighted priority score for alerts" | Savings-only ranking | Changed to 50% savings, 30% comfort, 20% confidence |
| 3 | "Write the rule engine in pandas" | Working engine | Tested against independent hand check |
| 4 | LLM tip prompt: "one short tip, use the rupee saving exactly as given, do not invent numbers" | Tips in plain language | Constrained prompt after testing |

## One thing the AI got wrong (and how I caught it)
The first engine version flagged the same AC hours under BOTH R1 (room empty) and R6 (long run), so savings were counted twice (Rs 239.89 instead of Rs 218.97).
Caught by: independent overlap check (6 hours counted by both rules) and a new test `test_no_double_counting`. Fix: R6 now only looks at hours where the room is occupied.
