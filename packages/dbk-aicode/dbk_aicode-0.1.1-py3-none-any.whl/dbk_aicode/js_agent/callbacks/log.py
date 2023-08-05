from typing import List, Dict, Optional, Any, Union

from langchain.callbacks.base import BaseCallbackHandler
from langchain.input import print_text, get_colored_text
from langchain.schema import AgentAction, AgentFinish, LLMResult

from dbk_aicode.db.base import push_logs

class LoggerCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to std out."""

    def __init__(self, run_id: str, project_id: str, color: Optional[str] = None) -> None:
        """Initialize callback handler."""
        self.run_id = run_id
        self.project_id = project_id
        self.color = color
        self.logs = []

    def push_log(self, log: Optional[str]) -> None:
        if log is not None:
            self.logs.append(log)
            push_logs(run_id=self.run_id, project_id=self.project_id, logs=self.logs)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Do nothing."""
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Do nothing."""
        pass

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized["name"]
        log = f"\n\n\033[1m> Entering new {class_name} chain...\033[0m"
        self.push_log(log)
        print(log)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        log = "\n\033[1m> Finished chain.\033[0m"
        self.push_log(log)
        print(log)

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """Do nothing."""
        pass

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        c = color if color else self.color
        log = get_colored_text(action.log, c)
        self.push_log(log)
        print_text(action.log, color=c)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        c = color if color else self.color

        log = f"\n{observation_prefix}\n"
        log += get_colored_text(output, c)
        log += f"\n{llm_prefix}\n"
        self.push_log(log)

        print_text(f"\n{observation_prefix}")
        print_text(output, color=c)
        print_text(f"\n{llm_prefix}")

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Do nothing."""
        pass

    def on_text(
        self,
        text: str,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Optional[str],
    ) -> None:
        """Run when agent ends."""
        c = color if color else self.color

        log = get_colored_text(text, c) + f"\n{end}"
        self.push_log(log)

        print_text(text, color=c, end=end)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        c = color if color else self.color

        log = get_colored_text(finish.log, c) + "\n\n"
        self.push_log(log)

        print_text(finish.log, color=color if self.color else color, end="\n")