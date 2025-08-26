import datetime
import os
import json

def save_note(title: str, research_summary, business_data: dict):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("notes", exist_ok=True)
    filename = f"notes/{title.replace(' ', '_')}_{ts}.md"

    # Ensure summary is a string
    summary_text = research_summary
    if isinstance(research_summary, dict):
        summary_text = research_summary.get("summary", "")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"Created: {datetime.datetime.now().isoformat()}\n\n")

        f.write("## Research Summary\n\n")
        f.write(summary_text + "\n\n")

        if isinstance(research_summary, dict) and "sources" in research_summary:
            f.write("## Sources\n\n")
            f.write("```json\n")
            f.write(json.dumps(research_summary["sources"], ensure_ascii=False, indent=2))
            f.write("\n```\n\n")

        f.write("## Business Data\n\n")
        f.write("```json\n")
        f.write(json.dumps(business_data, ensure_ascii=False, indent=2))
        f.write("\n```\n")

    return filename
