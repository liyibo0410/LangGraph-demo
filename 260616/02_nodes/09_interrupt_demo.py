# 04_nodes/09_interrupt_demo.py
"""
业务场景演示：转账流程，走到审核节点主动暂停，交给人工确认/修改信息后再继续执行
核心依赖：checkpointer 持久化会话 + interrupt() 中断函数 + Command(resume=xxx) 恢复流程
"""
from typing import Any
from typing_extensions import TypedDict

# LangGraph 中断、状态存储、图相关导入
from langgraph.checkpoint.memory import InMemorySaver  # 内存会话存储器，保存中断前状态
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt  # interrupt暂停，Command用于恢复传参


# ====================== 1. 定义转账流程全局状态 ======================
class TransferState(TypedDict):
    recipient: str    # 收款人名
    amount: int       # 转账金额
    memo: str         # 转账备注
    approved: bool    # 人工是否批准转账
    final_status: str # 转账最终结果状态


# ====================== 2. 人工审核节点（核心中断逻辑） ======================
def review_transfer(state: TransferState) -> dict[str, Any]:
    """
    转账审核节点：生成待审核单据，调用interrupt暂停整个流程图
    流程图卡在当前行，外部代码拿到中断信息，人工输入决策后再恢复执行
    """
    print("\n[Node] review_transfer：生成待执行的转账请求")

    # 打包当前待审核的转账数据
    pending_transfer = {
        "recipient": state["recipient"],
        "amount": state["amount"],
        "memo": state["memo"],
    }

    # ========== 关键：触发流程中断 ==========
    # interrupt(传入自定义交互数据)
    # 1. 程序运行到这里直接暂停，退出当前invoke
    # 2. 外部可以拿到括号内的字典，展示给前端/人工
    # 3. 后续通过 Command(resume=返回值) 把人工输入传回该变量，继续往下走代码
    user_review = interrupt(
        {
            "title": "转账审核",
            "pending_transfer": pending_transfer,
            "instruction": "请返回 bool(是否批准) 或 dict(修改字段)",
        }
    )
    # =======================================

    # 恢复执行后，处理人工传回的决策数据
    approved = False
    updated_transfer = dict(pending_transfer)  # 复制原始单据

    # 分支1：人工只传布尔值，仅决定是否通过
    if isinstance(user_review, bool):
        approved = user_review
    # 分支2：人工传字典，可以同时修改收款人/金额/备注 + 是否批准
    elif isinstance(user_review, dict):
        approved = bool(user_review.get("approved", True))
        # 遍历允许修改的字段，覆盖更新
        for k in ("recipient", "amount", "memo"):
            if k in user_review:
                updated_transfer[k] = user_review[k]

    print(f"[Node] review_transfer：用户决策 approved={approved}")

    # 把人工修改后的最新单据、审批结果更新到全局状态
    return {
        "approved": approved,
        "recipient": updated_transfer["recipient"],
        "amount": updated_transfer["amount"],
        "memo": updated_transfer["memo"],
    }


# ====================== 3. 转账执行节点 ======================
def execute_transfer(state: TransferState) -> dict[str, str]:
    """根据审核结果，决定执行转账还是取消"""
    if not state["approved"]:
        print("\n[Node] execute_transfer：用户未批准，取消转账")
        return {"final_status": "已取消：用户未批准"}

    print("\n[Node] execute_transfer：模拟执行转账...")
    return {
        "final_status": f"成功转账 {state['amount']} 元给 {state['recipient']}"
    }


# ====================== 4. 搭建并编译流程图 ======================
def build_graph():
    graph = StateGraph(TransferState)
    # 注册两个节点：审核节点、转账执行节点
    graph.add_node("review_transfer", review_transfer)
    graph.add_node("execute_transfer", execute_transfer)

    # 串行流程：起点 → 人工审核(会中断) → 执行转账 → 结束
    graph.add_edge(START, "review_transfer")
    graph.add_edge("review_transfer", "execute_transfer")
    graph.add_edge("execute_transfer", END)

    # 重点：开启中断必须传入 checkpointer
    # InMemorySaver 内存存储，每个thread_id独立保存会话状态，中断后不会丢失数据
    return graph.compile(checkpointer=InMemorySaver())


# ====================== 5. 主程序演示中断+恢复完整流程 ======================
if __name__ == "__main__":
    app = build_graph()
    # thread_id：会话唯一标识，同一个对话/转账流程必须共用同一个id，用来找回中断前状态
    config = {"configurable": {"thread_id": "transfer-thread-01"}}

    # 初始化转账单据
    initial_state = {
        "recipient": "Alice",
        "amount": 100,
        "memo": "午餐AA",
        "approved": False,
        "final_status": "",
    }

    print("=== 第一次调用：触发中断 ===")
    # 第一次运行，执行到interrupt自动暂停，返回结果里携带__interrupt__中断信息
    result = app.invoke(initial_state, config=config)

    # 取出中断抛出的交互数据，展示给人工/前端
    interrupt_val = result["__interrupt__"][0]
    print(f"系统暂停，等待审核。待审核数据: {interrupt_val.value}")

    print("\n=== 第二次调用：恢复执行 ===")
    # 模拟人工操作：修改金额、修改备注、批准转账
    user_decision = {"approved": True, "amount": 80, "memo": "实付80元"}

    # Command(resume=xxx)：把人工决策传回interrupt变量，恢复中断处继续执行
    final_result = app.invoke(Command(resume=user_decision), config=config)

    # 流程全部走完，输出最终转账结果
    print(f"最终结果: {final_result['final_status']}")