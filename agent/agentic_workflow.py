from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool


class GraphBuilder:
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()

        self.tools = [
            *self.weather_tools.weather_tool_list,
            *self.place_search_tools.place_search_tool_list,
            *self.calculator_tools.calculator_tool_list,
            *self.currency_converter_tools.currency_converter_tool_list,
        ]

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

        # ✅ FIX: Avoid nested SystemMessage
        if isinstance(SYSTEM_PROMPT, SystemMessage):
            self.system_prompt = SYSTEM_PROMPT
        else:
            self.system_prompt = SystemMessage(content=str(SYSTEM_PROMPT))

        self.graph = None

    def agent_function(self, state: MessagesState):
        try:
            user_messages = state.get("messages", [])

            normalized_messages = []

            # Always inject system prompt first
            normalized_messages.append(
                SystemMessage(content=str(self.system_prompt.content))
            )

            for msg in user_messages:
                if isinstance(msg, BaseMessage):
                    # Always re-wrap BaseMessages safely
                    if isinstance(msg, HumanMessage):
                        normalized_messages.append(
                            HumanMessage(content=str(msg.content))
                        )
                    else:
                        normalized_messages.append(
                            HumanMessage(content=str(msg.content))
                        )

                elif isinstance(msg, str):
                    normalized_messages.append(
                        HumanMessage(content=str(msg))
                    )

                else:
                    normalized_messages.append(
                        HumanMessage(content=str(msg))
                    )

            response = self.llm_with_tools.invoke(normalized_messages)
            return {"messages": [response]}

        except Exception as e:
            raise RuntimeError(f"Agent execution failed: {e}") from e

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
