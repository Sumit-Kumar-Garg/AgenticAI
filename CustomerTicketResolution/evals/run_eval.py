"""Score the agent against human-labelled tickets.   python -m evals.run_eval

data/golden_tickets.csv columns: ticket_id,text,true_category,true_priority,true_team
Keep these tickets OUT of data/resolved_tickets.csv, or retrieval will leak the answers.
"""
import os
import time

import pandas as pd
from dotenv import load_dotenv

from app.runner import run_ticket

load_dotenv()


def main(path: str = "data/golden_tickets.csv"):
    df = pd.read_csv(path)
    delay = float(os.getenv("EVAL_DELAY", "2"))
    rows = []
    for _, r in df.iterrows():
        out = run_ticket(str(r["ticket_id"]), r["text"], mode="batch")
        rows.append(
            {
                "ticket_id": r["ticket_id"],
                "route": out["route"],
                "pred_category": out["category"],
                "pred_priority": out["priority"],
                "pred_team": out["team"],
                "confidence": out["confidence"],
                "reasons": "; ".join(out["reasons"]),
                "true_category": r["true_category"],
                "true_priority": r["true_priority"],
                "true_team": r["true_team"],
            }
        )
        time.sleep(delay)

    res = pd.DataFrame(rows)
    res["cat_ok"] = res.pred_category == res.true_category
    res["prio_ok"] = res.pred_priority == res.true_priority
    res["team_ok"] = res.pred_team == res.true_team
    res["all_ok"] = res.cat_ok & res.prio_ok & res.team_ok
    auto = res[res.route == "auto_assigned"]

    print(f"\nTickets evaluated        : {len(res)}")
    print(f"Category accuracy        : {res.cat_ok.mean():.0%}")
    print(f"Priority accuracy        : {res.prio_ok.mean():.0%}")
    print(f"Team (routing) accuracy  : {res.team_ok.mean():.0%}")
    print(f"Sent to humans           : {(res.route != 'auto_assigned').mean():.0%}")
    if len(auto):
        print(f"Accuracy on auto-assigned: {auto.all_ok.mean():.0%}  (the number to watch before going live)")
    print("\nTeam accuracy by true category:")
    print(res.groupby("true_category").team_ok.mean().map("{:.0%}".format).to_string())

    res.to_csv("evals/results.csv", index=False)
    print("\nDetails saved to evals/results.csv")


if __name__ == "__main__":
    main()
