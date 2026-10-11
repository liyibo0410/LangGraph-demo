import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    api_key=os.environ["ZHIPU_API_KEY"],
    base_url=os.environ["ZHIPU_BASE_URL"],
    model="glm-4-flash",
    temperature=0.7
)

print("==============================机试题 1：基础图构建与节点流转====================================")
class SimpleState(TypedDict):
    user_input: str
    processed_output: str

def process_node(state: SimpleState) -> SimpleState:
    input_text = state["user_input"]
    output_text = input_text + " -> 已处理完毕！"
    return {"processed_output": output_text}

graph_builder = StateGraph(SimpleState)
graph_builder.add_node("process_node", process_node)
graph_builder.add_edge(START, "process_node")
graph_builder.add_edge("process_node", END)
graph1 = graph_builder.compile()

init1 = {"user_input": "测试数据"}
out1 = graph1.invoke(init1)
print(out1["processed_output"])

print("\n==============================机试题 2：使用 Reducer 实现状态追加更新====================================")
class ListState(TypedDict):
    task_logs: Annotated[List[str], operator.add]

def step_1_node(state: ListState) -> ListState:
    return {"task_logs": ["执行第一步"]}

def step_2_node(state: ListState) -> ListState:
    return {"task_logs": ["执行第二步"]}

builder2 = StateGraph(ListState)
builder2.add_node("step_1_node", step_1_node)
builder2.add_node("step_2_node", step_2_node)
builder2.add_edge(START, "step_1_node")
builder2.add_edge("step_1_node", "step_2_node")
builder2.add_edge("step_2_node", END)
graph2 = builder2.compile()

init2 = {"task_logs": ["准备启动"]}
out2 = graph2.invoke(init2)
print(out2["task_logs"])
