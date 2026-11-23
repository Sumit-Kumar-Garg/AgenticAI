
from uuid import uuid4

from langgraph.types import Command
from app.agents.support_graph import support_graph


if __name__ == "__main__":

    ticket_id = "TKT00001"

    # Each investigation gets a unique workflow ID.
    config = {
        "configurable": {
            "thread_id": f"{ticket_id}-{uuid4()}"
        }
    }

    print("\nStarting support investigation...")

    # First invocation: graph runs until human review.
    result = support_graph.invoke(
        {"ticket_id": ticket_id},
        config=config
    )

    print("\n========== HUMAN REVIEW REQUEST ==========")

    interrupts = result.get("__interrupt__", [])

    if not interrupts:
        print("No human review interrupt was returned.")
        print(result)
        raise SystemExit(1)

    for item in interrupts:
        print(item.value)

    # Simulate a human reviewer using terminal input.
    approval = input(
        "\nApprove recommendation? (yes/no): "
    ).strip().lower()

    comment = input("Reviewer comment: ").strip()

    decision = {
        "approved": approval == "yes",
        "reviewer": "local-test-user",
        "comment": comment
    }

    print("\nResuming workflow...")

    # Resume from the saved checkpoint.
    final_result = support_graph.invoke(
        Command(resume=decision),
        config=config
    )

    print("\n========== FINAL WORKFLOW STATUS ==========")
    print(final_result.get("final_status"))

    print("\n========== HUMAN DECISION ==========")
    print(final_result.get("human_decision"))

    print("\n========== THREAD ID ==========")
    print(config["configurable"]["thread_id"])
