
import argparse
from indexer import build_index
from agent import UdaPlayAgent

def run():
    parser = argparse.ArgumentParser(description="UdaPlay AI Research Agent")
    parser.add_argument("--index", action="store_true", help="Build/refresh local index from data/games/*.json")
    parser.add_argument("--ask", type=str, help="Ask a question about a video game")
    args = parser.parse_args()

    if args.index:
        build_index()

    if args.ask:
        agent = UdaPlayAgent()
        result = agent.run(args.ask)
        print(result["markdown"])

if __name__ == "__main__":
    run()
