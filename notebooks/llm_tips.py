"""Gen AI layer: turns top alerts into friendly tips. Reads ANTHROPIC_API_KEY from env (never hard-coded).
Falls back to a template when no key/network so the demo never breaks."""
import os, json
def tips(alerts, n=3):
    # one tip per rule (best alert of each), so the tips are different from each other
    top = alerts.drop_duplicates("rule").head(n)[["device", "condition", "action", "hours", "saving_inr"]].to_dict("records")
    prompt = ("You are a friendly smart-home energy coach. For each item write ONE short tip (max 20 words), "
              "mention the rupee saving exactly as given, do not invent numbers.\n" + json.dumps(top))
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            import anthropic
            r = anthropic.Anthropic().messages.create(model="claude-sonnet-4-6", max_tokens=300,
                                                      messages=[{"role": "user", "content": prompt}])
            return r.content[0].text.strip().split("\n")
        except Exception as ex: print("LLM unavailable:", ex)
    return [f"{t['device']}: {t['action']} - rule: {t['condition']}. Saves about ₹{t['saving_inr']} this week." for t in top]
