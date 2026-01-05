# Udaplay Project

## Overview

Udaplay is an AI-powered research agent designed for the video game industry. This project demonstrates building an intelligent agent that can answer questions about video games using a combination of internal knowledge (via Retrieval-Augmented Generation or RAG) and external web searches. The agent maintains conversation state, returns structured outputs, and stores useful information for future interactions.

The project is divided into two main parts:

1. **Part 01 - Offline RAG**: Setting up a Vector Database using ChromaDB to store and query game data.
2. **Part 02 - Agent**: Building the AI agent that leverages the VectorDB, evaluation tools, and web search capabilities.

## Prerequisites

- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- API Keys:
  - OpenAI API Key (for embeddings and LLM interactions)
  - Tavily API Key (for web searches)

## Setup

1. **Clone or Download the Project**:
   - Ensure you have the project files in your workspace, including the `games/` folder with JSON data files.

2. **Install Dependencies**:
   - Install the required Python packages:
     ```
     pip install chromadb openai tavily-python python-dotenv pydantic
     ```
   - For Udacity workspace compatibility, the notebooks include code to handle `pysqlite3` if needed.

3. **Environment Variables**:
   - Create a `.env` file in the project root with the following:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     TAVILY_API_KEY=your_tavily_api_key_here
     ```
   - Ensure the keys are valid and have the necessary permissions.

4. **Data Preparation**:
   - The `games/` folder should contain JSON files, each representing a game with fields like `Name`, `Platform`, `Genre`, `Publisher`, `Description`, and `YearOfRelease`.

## Running the Notebooks

### Part 01: Udaplay_01_starter_project.ipynb

This notebook focuses on building the Vector Database.

1. **Setup Section**:
   - Loads environment variables and initializes the OpenAI client.
   - Tests the API key with a simple embedding request.

2. **VectorDB Instance**:
   - Creates a persistent ChromaDB client.

3. **Collection**:
   - Sets up an embedding function using OpenAI's text-embedding-3-small model.
   - Creates or retrieves a collection named "udaplay".

4. **Add Documents**:
   - Reads JSON files from the `games/` directory.
   - Embeds and adds game data to the Chroma collection.

Run the cells in order to populate the database. After completion, you'll have a searchable vector database of game information.

### Part 02: Udaplay_02_starter_project.ipynb

This notebook builds the AI agent.

1. **Setup**:
   - Imports necessary libraries and loads environment variables.

2. **Tools**:
   - **retrieve_game**: Searches the ChromaDB collection for relevant games based on a query.
   - **evaluate_retrieval**: Uses an LLM to assess if retrieved documents are sufficient to answer a question.
   - **game_web_search**: Performs web searches using Tavily for additional information.

3. **Agent**:
   - Defines a state machine-based agent (`UdaPlayAgent`) that orchestrates the tools.
   - The agent follows a flow: Ask → RAG → Evaluate → (Web Search if needed) → Parse → Store → Report.

4. **Invocation**:
   - Tests the agent with sample questions like:
     - "When was Pokémon Gold and Silver released?"
     - "Which one was the first 3D platformer Mario game?"
     - "Was Mortal Kombat X released for PlayStation 5?"

Run the notebook to see the agent in action. It will output structured responses in Markdown format.

## Key Features

- **RAG Integration**: Leverages ChromaDB for efficient semantic search over game data.
- **LLM Evaluation**: Uses OpenAI models to judge the quality of retrieved information.
- **Web Fallback**: Integrates Tavily for real-time web searches when internal data is insufficient.
- **Structured Outputs**: Returns consistent, parseable responses.
- **Memory Management**: Includes placeholders for long-term memory storage.

## Troubleshooting

- **API Key Issues**: Ensure your `.env` file is correctly set up and keys are valid. Test with the embedding probe in Part 01.
- **ChromaDB Errors**: If collection creation fails, check the path and ensure no conflicts with existing collections.
- **Web Search Failures**: Verify Tavily API key and internet connectivity.
- **Import Errors**: Install missing packages and ensure Python environment is set up correctly.

## Advanced Enhancements

- **Long-Term Memory**: Extend the agent to persist useful information across sessions.
- **State Machine Refinement**: Further develop the agent's state transitions for more complex workflows.
- **Additional Tools**: Integrate more tools for deeper analysis, such as sentiment analysis or trend prediction.

## License

This project is for educational purposes as part of the Udacity AI course. Refer to the course materials for licensing details.

## Contributing

Feel free to enhance the notebooks by adding more features, improving error handling, or optimizing performance.
