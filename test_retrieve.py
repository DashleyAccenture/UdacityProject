# test_retrieve.py
from tools_retrieve import retrieve_game

def show(results):
    for r in results:
        print(f"{r['Name']} [{r['Platform']}] ({r['YearOfRelease']}) | score={r['score']} | id={r['id']}")

print("\n--- Test: Developer-style question ---")
res = retrieve_game('Who developed "FIFA 21"?', n_results=5)
show(res)
