```markdown
# ==============================================================================================
# 🚀 LangGraph-demo 项目完整说明文档 README.md
# 项目定位：循序渐进 LangGraph 全套实战 Demo 学习库 📚
# ==============================================================================================

# 一、项目总览
## 1. 项目简介 📖
本项目按照 **State状态 → Node节点 → Edge流程分支** 标准学习路线拆分模块，覆盖 LangGraph 全部核心功能，包含基础语法、性能优化、持久化会话、人机交互中断、循环分支、底层Pregel执行原理等完整实战案例。
所有代码均带小白级详细注释，可直接作为学习笔记、面试复习素材、Agent开发生产模板复用 ✅。

## 2. 完整目录树结构 📂
“
LangGraph-demo/
├─ 260615/
│  └─ 01_state/                  # 🧩 模块1：基础状态定义 & Reducer状态合并规则
│     ├─ 00_LangGraph快速入门.py
│     ├─ 01_Dict_user_state_demo.py
│     ├─ 02_TypedDict_UserState_demo.py
│     ├─ 03_TypedDict_AdvancedState_demo.py
│     ├─ 04_Pydantic_UserState_demo.py
│     ├─ 05_Pydantic_AgentState_demo.py
│     ├─ 06_dataclass_UserState_demo.py
│     ├─ 07_input_output_workflow_demo.py
│     ├─ 08_node_isolation_workflow_demo.py
│     ├─ 09_reducer_default_demo.py
│     ├─ 10_reducer_add_demo.py
│     ├─ 11_reducer_custom_demo.py
│     └─ 12_reducer_merge_node_state_demo.py
├─ 260616/
│  ├─ 01_state/                  # 💾 模块2：持久化检查点、会话恢复、底层Pregel原理
│  │  ├─ sqlite_data/
│  │  ├─ langgraph_checkpoint.db
│  │  ├─ 13_langchain_checkpointer_demo.py
│  │  ├─ 14_langgraph_checkpointer_demo.py
│  │  ├─ 15_state_recovery_demo.py
│  │  ├─ 16_pregel_algorithm_demo.py
│  │  └─ 17_state_history_demo.py
│  └─ 02_nodes/                  # ⚙️ 模块3：节点全特性（缓存/重试/流式/中断交互）
│     ├─ 01_node_parameters_demo.py
│     ├─ 02_node_output_wrong_demo.py
│     ├─ 03_node_output_right_demo.py
│     ├─ 04_intern_demo.py
│     ├─ 05_str_demo.py
│     ├─ 06_node_cache_demo.py
│     ├─ 07_node_default_retry_demo.py
│     ├─ 08_stream_demo.py
│     └─ 09_interrupt_demo.py
└─ 260617/
   └─ 03_edge/                   # 🔀 模块4：条件分支、循环流程、递归安全限制
      ├─ 01_condition_edge.py
      └─ 02_loop_with_recursion_limit.py
”

## 二、分模块文件功能详情

### 模块1：260615/01_state 🍀 基础状态管理（入门必学）

| 文件名 | 核心功能说明 |
| :----- | :----------- |
| 00_LangGraph快速入门.py | 🥳 极简 HelloWorld 示例，一次性看懂完整运行链路 |
| 01_Dict_user_state_demo.py | 原生字典定义State，无类型约束，最简入门写法 |
| 02_TypedDict_UserState_demo.py | 🔥 TypedDict 标准状态定义，带类型提示，企业项目通用方案 |
| 03_TypedDict_AdvancedState_demo.py | 📦 TypedDict 嵌套复杂结构（列表、子字典）高阶复合状态 |
| 04_Pydantic_UserState_demo.py | 🛡️ Pydantic 模型定义状态，自带数据校验、字段默认值 |
| 05_Pydantic_AgentState_demo.py | 🤖 Agent专用状态封装，内置对话消息、工具返回、思考链路段 |
| 06_dataclass_UserState_demo.py | 📊 dataclass 数据类实现状态，兼顾简洁性与强类型约束 |
| 07_input_output_workflow_demo.py | 📥 区分图初始输入、节点增量输出，规范输入输出隔离 |
| 08_node_isolation_workflow_demo.py | 🔒 节点状态隔离原理：禁止直接修改原始state，仅通过返回字典更新 |
| 09_reducer_default_demo.py | 🧩 框架默认Reducer合并规则，基础字段覆盖逻辑演示 |
| 10_reducer_add_demo.py | ➕ Annotated + operator.add 列表累加器，对话消息追加核心用法 |
| 11_reducer_custom_demo.py | 🛠️ 自定义Reducer归并函数，自由定制状态更新合并逻辑 |
| 12_reducer_merge_node_state_demo.py | ✨ 多并行节点状态合并冲突解决方案 |

## 模块2：260616/01_state 💾 持久化与底层原理（生产进阶）
| 文件名 | 核心功能说明 |
|--------|-------------|
| 13_langchain_checkpointer_demo.py | ⚖️ LangChain原生记忆持久化，与LangGraph检查点做对比 |
| 14_langgraph_checkpointer_demo.py | 🗄️ SqliteSaver 磁盘持久化会话，thread_id 隔离独立对话线程 |
| 15_state_recovery_demo.py | ♻️ interrupt中断后会话恢复，从历史快照断点继续执行流程 |
| 16_pregel_algorithm_demo.py | 🔬 LangGraph底层Pregel图计算执行模型完整拆解 |
| 17_state_history_demo.py | 📜 查询会话全量历史状态，回溯每一步执行快照数据 |
| langgraph_checkpoint.db | 📀 SQLite持久化数据库文件，存储所有会话检查点快照 |

## 模块3：260616/02_nodes ⚙️ 节点全套核心特性（业务开发核心）
| 文件名 | 核心功能说明 |
|--------|-------------|
| 01_node_parameters_demo.py | 🎛️ 节点完整入参详解：state、runtime、config 三类参数接收方式 |
| 02_node_output_wrong_demo.py | ❌ 错误示范：节点直接返回完整state，并发场景存在数据覆盖风险 |
| 03_node_output_right_demo.py | ✅ 行业标准规范：节点仅返回增量更新字典，框架自动合并全局状态 |
| 04_intern_demo.py | 🔗 Python字符串驻留底层原理，常量字符串内存复用机制 |
| 05_str_demo.py | 🔤 f-string动态字符串不触发自动驻留，`==`内容对比 vs `is`地址对比区分 |
| 06_node_cache_demo.py | ⚡ CachePolicy 节点TTL缓存，InMemoryCache复用重复输入结果，节约LLM调用成本 |
| 07_node_default_retry_demo.py | 🔁 RetryPolicy 自动重试策略，解决接口超时、临时服务故障等可恢复异常 |
| 08_stream_demo.py | 📡 五大流式输出模式：values/updates/custom/messages/debug，实现打字机对话、实时进度推送 |
| 09_interrupt_demo.py | ⏸️ interrupt 人机中断交互，流程暂停等待人工审批/修改参数后恢复执行 |

## 模块4：260617/03_edge 🔀 流程分支与循环控制（调度逻辑）
| 文件名 | 核心功能说明 |
|--------|-------------|
| 01_condition_edge.py | 🚦 add_conditional_edges 条件分支路由，根据状态动态切换下游执行节点 |
| 02_loop_with_recursion_limit.py | 🔄 闭环循环流程图 + recursion_limit 递归步数安全保护，双层机制防止死循环卡死程序 |

# 三、推荐学习路线（由浅入深）📖
1. 【入门基础 🌱】
   `00_LangGraph快速入门.py` → 全部 01_state 基础状态Demo
   目标：搞懂State定义、Reducer状态合并底层规则

2. 【节点核心能力 ⚙️】
   全部 02_nodes 节点Demo
   目标：掌握节点标准写法、缓存、重试、流式输出、人机中断交互

3. 【流程调度逻辑 🔀】
   03_edge 条件分支 + 循环控制Demo
   目标：实现多分支分流、多轮迭代Agent循环流程

4. 【生产环境进阶 🏭】
   260616/01_state 持久化、会话恢复、Pregel底层原理
   目标：掌握线上会话记忆、断点续跑、底层执行机制

# 四、环境依赖配置 🧪
## 1. 一键安装全部依赖
```bash
pip install langgraph langchain langchain-openai pydantic python-dotenv
```

## 2. 全局模型统一配置 lm_config.py
所有LLM相关Demo统一读取该文件，无需重复填写密钥：
```python
# lm_config.py 全局大模型配置 🤖
class lm_config:
    llm_model = "deepseek-chat"
    model_provider = "deepseek"
    base_url = "https://api.deepseek.com/v1"
    api_key = "替换为你的个人模型密钥"
```

# 五、项目核心知识点总览 💡
## 1. State 状态体系 🧩
1. 四种状态定义方案：原生Dict / TypedDict / Pydantic / dataclass
2. Reducer归并机制：内置列表累加器、自定义合并函数，解决并行节点状态覆盖问题

## 2. Node 节点开发规范 ⚙️
1. 强制规范：禁止返回完整state，仅返回需要更新的字段字典
2. 内置增强能力：TTL缓存、指数退避自动重试、runtime自定义流输出、interrupt流程暂停
3. 5种流式模式适配不同前端展示场景：全量状态、增量更新、自定义进度、LLM逐字Token、底层调试日志

## 3. Edge 流程控制 🔀
1. 普通固定边：`add_edge` 固定单向流转
2. 条件分支边：`add_conditional_edges` 动态路由多分支逻辑
3. 循环闭环 + recursion_limit 安全阈值，双层防护杜绝死循环

## 4. 持久化会话方案 💾
1. InMemorySaver：内存临时存储，仅本地调试使用，程序重启数据清空
2. SqliteSaver：磁盘持久化存储，多会话隔离、中断恢复、历史快照回溯，适配生产人机协同审批流程

# 六、项目适用场景 🎯
1. LangGraph 零基础系统自学、面试核心知识点复习 📝
2. Agent 业务开发模板复用：工具循环调用、人工审批流程、流式对话、接口异常容错、缓存性能优化 🤖
3. 企业级Agent流程框架参考：标准化状态管理、会话持久化、死循环安全防护机制 🏢
4. 课程教学分步演示，完整拆解LangGraph底层执行链路 👨‍🏫
# ==============================================
```
