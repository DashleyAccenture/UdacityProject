from tools import evaluate_retrieval
# test_evaluate.py
from tools_retrieve import retrieve_game
from tools_evaluate import evaluate_retrieval

query = 'Who developed "FIFA 21"?'
results = retrieve_game(query, n_results=5)

print("\nRetrieved Results:")
for r in results:
    print(f"{r['Name']} | score={r['score']} | Year={r['YearOfRelease']}")

print("\nEvaluation Metrics:")
metrics = evaluate_retrieval(query, results)
for k, v in metrics.items():
    print(f"{k}: {v}")
