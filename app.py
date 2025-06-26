import datetime
import json
from typing import List, Dict

def schedule_tasks(topics: List[str], deadline: str) -> List[Dict]:
    try:
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    today = datetime.date.today()
    remaining_days = (deadline_date - today).days

    if remaining_days < 0:
        raise ValueError("Deadline must be in the future.")

    days_per_task = max(1, remaining_days // len(topics))
    study_plan = []
    current_day = today

    for topic in topics:
        end_day = current_day + datetime.timedelta(days=days_per_task - 1)
        study_plan.append({
            "topic": topic,
            "start_date": str(current_day),
            "end_date": str(end_day)
        })
        current_day = end_day + datetime.timedelta(days=1)

    return study_plan


def research_topics(topic: str) -> List[str]:
    return [
        f"What is {topic}? : https://www.wikipedia.org/wiki/{topic.replace(' ', '_')}",
        f"Video on {topic}: https://www.youtube.com/results?search_query={topic.replace(' ', '+')}",
        f"Research Paper on {topic}: https://scholar.google.com/scholar?q={topic.replace(' ', '+')}"
    ]


def summarize_topics(snippets: List[str]) -> str:
    return f"Summarized content:\n" + "\n".join(snippets)

def run_study_assistant():
    topics_input = input("What topics would you like to study today? (Separate them with commas): ")
    topics = [t.strip() for t in topics_input.split(",")]

    deadline = input("Enter your study deadline (YYYY-MM-DD): ")

    if not topics:
        print("No valid topics entered.")
        return

    try:
        study_plan = schedule_tasks(topics, deadline)
    except Exception as e:
        print(f"Error: {e}")
        return

    full_output = []
    for item in study_plan:
        topic = item['topic']
        print(f"\nResearching: {topic}")
        research = research_topics(topic)
        summary = summarize_topics(research)

        item_output = {
            "topic": topic,
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "summary": summary
        }
        full_output.append(item_output)

        print(f"Summary for {topic}:\n{summary}")

    with open("study_assistant_output.json", "w") as f:
        json.dump(full_output, f, indent=4)

    print("\nStudy plan and summaries saved in study_assistant_output.json")

if __name__ == "__main__":
    run_study_assistant()