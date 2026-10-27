# ---------- CONTEXT ROT: dump everything ----------

def build_context_rot(question):
    prompt = "You are a helpful assistant.\n"
    prompt += all_chat_history()          # weeks of old chat, incl. Sprint 9 answer
    prompt += all_tickets()               # 500+ tickets, full text
    prompt += all_activity_logs()         # 2,000 log lines
    prompt += question                    # buried at the end of a huge pile
    return prompt                         # ~48,000 tokens


# ---------- CONTEXT ENGINEERING: pick only what matters ----------

def build_engineered_context(question):
    sprint  = get_current_sprint()                         # only today's sprint
    blocked = get_tickets(sprint=sprint, status="blocked") # 3 tickets, not 500
    notes   = get_recent_chat(sprint=sprint, limit=4)      # drop old sprints' chat
    logs    = get_logs(tickets=blocked, limit=5)           # last few relevant lines

    prompt  = "## Role\nYou are a sprint assistant. Use only the facts below.\n"
    prompt += f"## Current sprint\n{sprint.goal}, {sprint.start} to {sprint.end}\n"
    prompt += "## Blocked tickets\n" + format_list(blocked)
    prompt += "## Recent notes\n"     + format_list(notes)
    prompt += "## Recent activity\n"  + format_list(logs)
    prompt += "## Question\n" + question                   # clear, at the end
    return prompt                                          # ~200 tokens


# ---------- Compare ----------

question = "Why is Sprint 14 running late?"

bad_answer  = llm(build_context_rot(question))
# -> "Design work is not finished."  (old Sprint 9 reason)

good_answer = llm(build_engineered_context(question))
# -> "PM-212 is blocked waiting on the payments team's API keys.
#     PM-215 and PM-218 depend on it."
