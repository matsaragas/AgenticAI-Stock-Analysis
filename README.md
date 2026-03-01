# AgenticAI-A2A  for Stock-Analysis

An agentic AI system that uses ADK-A2A to plan and execute comprehensive stock financial analysis, 
with user authorization.

![alt text](assets/financial_agent.png)

The UI that allows us to interact with the Agentic AI:


![alt text](assets/financial_ui.png)

## Setup and Deployment

---

Before running the app locally, ensure you have the following:

1. uv: The python package management tool. To create a virtual environment and
   install all listed dependencies, run:
   ```shell
   uv install
   ```
2. python 3.13 is required to run a2a-sdk
3. set up .env
* Create an `.env` file in the folders: `host`, `financial_agent`, `cashflow_agent`, `balancesheet_agent` and `search_agents` with the following content:
 ```shell
GOOGLE_API_KEY="your_api_key_here" 
GOOGLE_GENAI_MODEL="gemini-2.5-flash"
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_LOCATION="global"
```

You can customize the `.env` file in each agent based on the needs of the application.




## 1. Run Financial Agent
___

```shell
cd src/financial_agent
uv run main.py
```


## 2. Run Cash Flow Agent
___

```shell
cd src/cashflow_agent
uv run main.py
```

## 3. Run Balance Sheet Agent
___

```shell
cd src/balancesheet_agent
uv run main.py
```

## 4. Run the Search Agent 

```shell
cd src/search_agents
uv run main.py
```

## 4. Run Host Agent
___                                                                                                                                                                                  

```shell
cd src/host
uv run main.py
```

## 5. Access and Test the agentic solution on the UI
___

```shell
http://localhost:8083/
```