# Utilities for dealing with langchain

import asyncio
import json
import logging
import os
import time
import uuid
from itertools import zip_longest
from typing import Any, Dict, List, Optional, TypeVar, Union
from uuid import UUID

import aiohttp
from langchain.callbacks.base import BaseCallbackHandler
from langchain.load.load import loads
from langchain.prompts import (
    BaseChatPromptTemplate,
    BasePromptTemplate,
    StringPromptTemplate,
)
from langchain.prompts.chat import (
    BaseChatPromptTemplate,
    BaseMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import (
    AgentAction,
    AgentFinish,
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    LLMResult,
    SystemMessage,
)

from im_openai import client

logger = logging.getLogger(__name__)

from functools import wraps


def format_langchain_value(value: Any) -> Any:
    if isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, (list, tuple)):
        return [format_langchain_value(v) for v in value]
    if isinstance(value, dict):
        return {k: format_langchain_value(v) for k, v in value.items()}
    if isinstance(value, StringPromptTemplate):
        inputs = {k: f"{{{k}}}" for k in value.input_variables}
        return value.format(**inputs)
    if isinstance(value, BaseMessage):
        return format_chat_template([value])[0]
    return format_chat_template(value)


def format_chat_template(
    messages: List[
        Union[BaseMessagePromptTemplate, BaseChatPromptTemplate, BaseMessage, List[Any]]
    ]
) -> List[Dict]:
    """Format a chat template into something that Imaginary Programming can deal with"""
    lists = [_convert_message_to_dicts(message) for message in messages]
    # Flatten the list of lists
    return [item for sublist in lists for item in sublist]


def _convert_message_to_dicts(
    message: Union[
        BaseMessagePromptTemplate, BaseChatPromptTemplate, BaseMessage, List[Any]
    ]
) -> List[dict]:
    if isinstance(message, ChatMessage):
        return [{"role": message.role, "content": message.content}]
    elif isinstance(message, HumanMessage):
        return [{"role": "user", "content": message.content}]
    elif isinstance(message, AIMessage):
        formatted_messages = {"role": "assistant", "content": message.content}
        if "function_call" in message.additional_kwargs:
            formatted_messages["function_call"] = message.additional_kwargs[
                "function_call"
            ]
        return [formatted_messages]
    elif isinstance(message, SystemMessage):
        return [{"role": "system", "content": message.content}]
    elif isinstance(message, MessagesPlaceholder):
        formatted_messages = {
            "role": "chat_history",
            "content": f"{{{message.variable_name}}}",
        }
        return [formatted_messages]
    elif isinstance(message, (BaseMessagePromptTemplate, BaseChatPromptTemplate)):
        vars = message.input_variables
        # create a fake dictionary mapping name -> '{name}'
        vars_as_templates = {v: f"{{{v}}}" for v in vars}
        formatted_messages = message.format_messages(**vars_as_templates)
        return format_chat_template(formatted_messages)  # type: ignore
    elif isinstance(message, dict):
        return [message]
    else:
        raise ValueError(f"Got unknown type {type(message)}: {message}")


class PromptWatchCallbacks(BaseCallbackHandler):
    project_key: str
    api_name: str

    template_chat: List[Dict] | None
    template_text: str | None

    runs: Dict[UUID, Dict[str, Any]] = {}
    """A dictionary of information about a run, keyed by run_id"""
    parent_run_ids: Dict[UUID, UUID] = {}
    """In case self.runs is missing a run, we can walk up the parent chain to find it"""

    server_event_ids: Dict[UUID, str | None] = {}
    """Mapping of run_id to server event id"""

    def __init__(
        self,
        project_key: str,
        api_name: str,
        *,
        template_text: Optional[str] = None,
        template_chat: Optional[
            List[Union[BaseMessagePromptTemplate, BaseMessage]]
        ] = None,
    ):
        """Initialize the callback handler

        Args:
            project_key (str): The Imaginary Programming project key
            api_name (str): The Imaginary Programming API name
            template_text (Optional[str], optional): The template to use for completion events. Defaults to None.
            template_chat (Optional[List[Union[BaseMessagePromptTemplate, BaseMessage]]], optional): The template to use for chat events. Defaults to None.
        """
        self.project_key = project_key or os.environ.get("PROMPT_PROJECT_KEY", "")
        if not self.project_key:
            raise ValueError("project_key must be provided")
        self.runs = {}
        self.api_name = api_name
        if template_text is not None:
            self.template_text = template_text
        elif template_chat is not None:
            self.template_chat = format_chat_template(template_chat)
        else:
            self.template_chat = None
        self.parent_run_ids = {}

    def _get_run(self, run_id: UUID):
        if run_id in self.runs:
            return self.runs[run_id]
        if run_id in self.parent_run_ids:
            return self._get_run(self.parent_run_ids[run_id])
        return None

    def _get_run_info(self, run_id: UUID, metadata_key: str):
        """Walk up the parent chain looking for the nearest run with the metadata_key defined"""
        if run_id in self.runs and metadata_key in self.runs[run_id]:
            return self.runs[run_id][metadata_key]
        if run_id in self.parent_run_ids:
            return self._get_run_info(self.parent_run_ids[run_id], metadata_key)
        return None

    def _get_server_event_id(self, run_id: UUID):
        """Lazily insert a server event id if it doesn't exist. This will get filled in later when the initial event is sent"""
        if run_id not in self.server_event_ids:
            self.server_event_ids[run_id] = None
        return self.server_event_ids[run_id]

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_chain_start      %s [%s] %s",
            self._format_run_id(run_id),
            ", ".join(inputs.keys()),
            ".".join(serialized["id"]),
        )

        self.runs[run_id] = {
            "inputs": inputs,
            "parent_run_id": parent_run_id,
            "prompt_event_id": uuid.uuid4(),
        }

        # super hack to extract the prompt if it exists
        prompt_obj = serialized.get("kwargs", {}).get("prompt")
        if prompt_obj:
            prompt_template = loads(json.dumps(prompt_obj))
            if isinstance(prompt_template, BasePromptTemplate):
                self.runs[run_id]["prompt_template"] = prompt_template

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_agent_action     %s %s",
            self._format_run_id(run_id),
            action.tool,
        )
        """Run on agent action."""

    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run on agent end."""
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_agent_finish    %s %s",
            self._format_run_id(run_id),
            finish.log,
        )

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        """Run when a text-based LLM runs"""
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_llm_start %s (%s prompts)",
            self._format_run_id(run_id),
            len(prompts),
        )

        run = self._get_run(run_id)
        if not run:
            logger.warning("on_llm_start Missing run %s", run_id)
            return
        run["prompts"] = prompts
        run["now"] = time.time()
        template_text = self._resolve_completion_template(run_id)
        # TODO: need to generate a new event id for each prompt
        asyncio.run(
            self._async_send_completion(
                run_id,
                template_text,
                run["inputs"],
                prompts,
                parent_event_id=parent_run_id,
            )
        )

    def on_chat_model_start(
        self,
        serialized,
        messages: List[List[BaseMessage]],
        run_id,
        parent_run_id,
        tags,
        metadata=None,
        **kwargs,
    ):
        """Runs when a chat-based LLM runs"""
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_chat_model_start %s (%s prompts)",
            self._format_run_id(run_id),
            len(messages),
        )
        run = self._get_run(run_id)
        if not run:
            return
        run["messages"] = messages
        run["now"] = time.time()

        template_chat = self._resolve_chat_template(run_id)
        asyncio.run(
            self._async_send_chat(
                run_id,
                template_chat,
                run["inputs"],
                messages,
                parent_event_id=parent_run_id,
            )
        )

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ):
        """Runs when either a text-based or chat-based LLM ends"""
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_llm_end          %s (%s responses)",
            self._format_run_id(run_id),
            len(response.generations),
        )

        run = self._get_run(run_id)
        if not run:
            logger.warning("on_llm_end Missing run %s", run_id)
            return
        now = time.time()
        response_time = (now - run["now"]) * 1000

        if "messages" in run:
            template_chat = self._resolve_chat_template(run_id)
            asyncio.run(
                self._async_send_chat(
                    run_id,
                    template_chat,
                    run["inputs"],
                    run["messages"],
                    response,
                    response_time,
                    parent_event_id=parent_run_id,
                )
            )
        elif "prompts" in run:
            template_text = (
                self._get_run_info(run_id, "prompt_template_text") or self.template_text
            )
            asyncio.run(
                self._async_send_completion(
                    run_id,
                    template_text,
                    run["inputs"],
                    run["prompts"],
                    response,
                    response_time,
                    parent_event_id=parent_run_id,
                )
            )
        else:
            logger.warning("Missing prompts or messages in run %s %s", run_id, run)

    def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM errors."""

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        if parent_run_id:
            self.parent_run_ids[run_id] = parent_run_id
        logger.info(
            "on_chain_end        %s [%s]",
            self._format_run_id(run_id),
            ", ".join(outputs.keys()),
        )
        if run_id in self.runs:
            del self.runs[run_id]

    async def _async_send(
        self,
        run_id: UUID,
        template: List[Dict] | str | None,
        inputs: Dict,
        iterations: List[str] | List[List[BaseMessage]],
        result: LLMResult | None = None,
        response_time: float | None = None,
        parent_event_id: UUID | None = None,
        is_chat: bool = False,
    ):
        async with aiohttp.ClientSession() as session:
            generations_lists = result.generations if result else []
            for iteration, generations in zip_longest(iterations, generations_lists):
                response_text = (
                    "".join(g.text for g in generations) if generations else None
                )
                json_inputs = {
                    key: format_langchain_value(value) for key, value in inputs.items()
                }

                if is_chat:
                    prompt = (
                        {"chat": format_chat_template(iteration)}  # type: ignore
                        if not template
                        else None
                    )
                    prompt_template_text = None
                    prompt_template_chat = template
                else:
                    prompt = {"completion": iteration} if not template else None
                    prompt_template_text = template
                    prompt_template_chat = None

                # TODO: gather these up and send them all at once
                prompt_event_id = self._get_server_event_id(run_id)
                id = await client.send_event(
                    session,
                    project_key=self.project_key,
                    api_name=self.api_name,
                    prompt_template_text=prompt_template_text,  # type: ignore
                    prompt_template_chat=prompt_template_chat,  # type: ignore
                    prompt_params=json_inputs,
                    prompt_event_id=prompt_event_id,
                    chat_id=None,
                    response=response_text,
                    response_time=response_time,
                    prompt=prompt,
                    parent_event_id=str(parent_event_id) if parent_event_id else None,
                )
                if id:
                    self.server_event_ids[run_id] = id

    async def _async_send_chat(
        self,
        run_id: UUID,
        template_chats: List[Dict] | None,
        inputs: Dict,
        messages_list: List[List[BaseMessage]],
        result: LLMResult | None = None,
        response_time: float | None = None,
        parent_event_id: UUID | None = None,
    ):
        await self._async_send(
            run_id,
            template_chats,
            inputs,
            messages_list,
            result,
            response_time,
            parent_event_id,
            is_chat=True,
        )

    async def _async_send_completion(
        self,
        prompt_event_id: UUID,
        template_text: str | None,
        inputs: Dict,
        prompts: List[str],
        result: LLMResult | None = None,
        response_time: float | None = None,
        parent_event_id: UUID | None = None,
    ):
        await self._async_send(
            prompt_event_id,
            template_text,
            inputs,
            prompts,
            result,
            response_time,
            parent_event_id=parent_event_id,
            is_chat=False,
        )

    def _format_run_id(self, run_id: UUID) -> str:
        """Generates a hierarchy of run_ids by recursively walking self.parent_ids"""
        if run_id in self.parent_run_ids:
            return f"{self._format_run_id(self.parent_run_ids[run_id])} -> {run_id}"
        return str(run_id)

    def _resolve_chat_template(self, run_id: UUID):
        """Resolve the template_chat into a list of dicts"""
        template: Optional[BasePromptTemplate] = self._get_run_info(
            run_id, "prompt_template"
        )
        inputs: Optional[Dict[str, Any]] = self._get_run_info(run_id, "inputs")
        template_chat = None
        if template and inputs:
            stub_inputs = make_stub_inputs(inputs)
            # Some of the templat formatters get upset if you pass in extra keys
            filtered_stub_inputs = {
                k: v for k, v in stub_inputs.items() if k in template.input_variables
            }
            if isinstance(
                template, (BaseMessagePromptTemplate, BaseChatPromptTemplate)
            ):
                # We can't go through format_prompt because it doesn't like formatting the wrong types
                template_chat = template.format_messages(**filtered_stub_inputs)

            elif isinstance(template, StringPromptTemplate):
                template_chat = template.format_prompt(
                    **filtered_stub_inputs
                ).to_messages()
            else:
                raise ValueError(f"Unknown template type {type(template)}")
            template_chat = format_chat_template(template_chat)  # type: ignore
        return template_chat

    def _resolve_completion_template(self, run_id: UUID):
        """Resolve the template_chat into a list of dicts"""
        template = self._get_run_info(run_id, "prompt_template")
        inputs = self._get_run_info(run_id, "inputs")
        template_text: str | None = None
        if template and inputs:
            stub_inputs = make_stub_inputs(inputs)
            filtered_stub_inputs = {
                k: v for k, v in stub_inputs.items() if k in template.input_variables
            }
            if isinstance(template, BaseChatPromptTemplate):
                # We can't go through format_prompt because it doesn't like formatting the wrong types
                template_text = template.format(**filtered_stub_inputs)
            elif isinstance(template, StringPromptTemplate):
                template_text = template.format_prompt(
                    **filtered_stub_inputs
                ).to_string()
            else:
                raise ValueError(f"Unknown template type {type(template)}")
            # template_text = format_chat_template(template_text)  # type: ignore
        return template_text


def make_stub_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    return make_stub_inputs_raw(inputs, "")  # type: ignore


def make_stub_inputs_raw(inputs: Any, prefix: str):
    if isinstance(inputs, dict):
        dict_prefix = f"{prefix}." if prefix else ""
        return {
            k: make_stub_inputs_raw(v, prefix=f"{dict_prefix}{k}")
            for k, v in inputs.items()
        }
    if isinstance(inputs, (str, int, float, bool)):
        return f"{{{prefix}}}"
    if isinstance(inputs, list):
        # TODO: figure out a way to collapse lists. Right now this will create stuff like:
        # [
        #     {
        #         "role": "{agent_history[0].role}",
        #         "content": "{agent_history[0].content}",
        #     },
        #     {
        #         "role": "{agent_history[1].role}",
        #         "content": "{agent_history[1].content}",
        #     },
        # ]
        # return [f"{{{prefix}}}"] * len(inputs)
        return [
            make_stub_inputs_raw(v, prefix=f"{prefix}[{i}]")
            for i, v in enumerate(inputs)
        ]
    if isinstance(inputs, tuple):
        return tuple(
            make_stub_inputs_raw(v, prefix=f"{prefix}[{i}]")
            for i, v in enumerate(inputs)
        )
    resolved = make_stub_inputs_raw(format_langchain_value(inputs), prefix=prefix)
    return resolved
