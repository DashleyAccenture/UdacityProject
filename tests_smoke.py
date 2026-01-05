
from agent import UdaPlayAgent

questions = [
    'Who developed "FIFA 21"?',
    'When was "God of War Ragnarok" released?',
    'What platform was "Pokémon Red" launched on?',
    'What is Rockstar Games working on right now?'
]

def run_tests():
    agent = UdaPlayAgent()
    for q in questions:
        print("\n---", q, "---")
        print(agent.run(q)["markdown"])

if __name__ == "__main__":
    run_tests()
S