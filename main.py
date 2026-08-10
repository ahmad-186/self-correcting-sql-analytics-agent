from app.graph.graph import graph

initial_state = {
    "question": "Show most selling product.",
    "retry_count": 0
}

result = graph.invoke(initial_state)

print(result)