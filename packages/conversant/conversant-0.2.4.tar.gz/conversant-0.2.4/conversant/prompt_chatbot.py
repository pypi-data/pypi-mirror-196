# Copyright (c) 2022 Cohere Inc. and its affiliates.
#
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License in the LICENSE file at the top
# level of this repository.

import json
import logging
import os
import warnings
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Dict, Tuple

import cohere
import jsonschema

import conversant
from conversant.chatbot import Chatbot, Interaction
from conversant.prompts.chat_prompt import ChatPrompt
from conversant.prompts.prompt import Prompt

MAX_GENERATE_TOKENS = 2048
TOKENS_PER_REQUEST = 10
PERSONA_MODEL_DIRECTORY = f"{os.path.dirname(conversant.__file__)}/personas"
PERSONA_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "chatbot_config": {
            "type": "object",
            "properties": {
                "max_context_examples": {"type": "integer"},
                "avatar": {"type": "string"},
            },
        },
        "client_config": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "max_tokens": {"type": "integer"},
                "temperature": {"type": "number"},
                "frequency_penalty": {"type": "number"},
                "presence_penalty": {"type": "number"},
                "stop_sequences": {"type": "array"},
            },
        },
        "prompt_config": {
            "type": "object",
        },
    },
}


class PromptChatbot(Chatbot):
    """Use prompt templates and LLM generation to define a chatbot.

    This bot makes no use of external knowledge sources.
    """

    def __init__(
        self,
        client: cohere.Client,
        prompt: Prompt,
        persona_name: str = "",
        chatbot_config: Dict[str, Any] = {},
        client_config: Dict[str, Any] = {},
    ):
        """Enriches init by adding a prompt.

        Args:
            client (cohere.Client): Cohere client for API
            prompt (Prompt): Prompt object to direct behavior.
            persona_name (str, optional): Bot's persona name. Defaults to empty string.
            chatbot_config: (Dict[str, Any], optional): Bot's chat config. Defaults to
                empty dict.
            client_config (Dict[str, Any], optional): Bot's client config. Defaults to
                empty dict.
        """

        super().__init__(client)
        self.prompt = prompt
        self.persona_name = persona_name

        self.configure_chatbot(chatbot_config)
        self.configure_client(client_config)
        self.chat_history = []
        self.prompt_size_history = []
        self.prompt_history = [self.prompt.to_string()]
        self.curr_max_context_examples = self.chatbot_config["max_context_examples"]

        # For the generation models, the maximum token length is 2048
        # (prompt and generation). So the prompt sent to .generate should be
        # MAX_GENERATE_TOKENS minus max tokens generated
        self.max_prompt_size = MAX_GENERATE_TOKENS - self.client_config["max_tokens"]
        self._check_prompt_size()

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4, default=str)

    @property
    def user_name(self):
        """
        Returns:
            str: The name of the user, defined in the prompt. Defaults to "User".
        """
        if hasattr(self.prompt, "user_name"):
            return self.prompt.user_name
        else:
            return "User"

    @property
    def bot_name(self):
        """
        Returns:
            str: The name of the chatbot, defined in the prompt. Defaults to
                "PromptChatbot".
        """
        if hasattr(self.prompt, "bot_name"):
            return self.prompt.bot_name
        else:
            return "PromptChatbot"

    @property
    def latest_prompt(self) -> str:
        """Retrieves the latest prompt.

        Returns:
            str: The prompt most recently added to the prompt history.
        """
        return self.prompt_history[-1]

    def _update_max_context_examples(
        self, prompt_size: int, max_context_examples: int
    ) -> int:
        """Adjust max_context_examples until a possible prompt size.

        if this is not possible, send an error message.

        Args:
            prompt_size (int): Number of tokens of the prompt
            max_context_examples (int): The length of the chat history for
            the chatbot to use in reply.

        Returns:
           int: updated max_context_examples
        """
        # Store original values
        original_size = prompt_size
        # If the size of chat_history is smaller than max_context_examples
        # the value of the variable is already updated with the size value
        trimmed_max_examples = min(len(self.chat_history), max_context_examples)

        # Check if the max_context_examples is bigger than 0 so it can be reduced
        if max_context_examples > 0:
            # Reduce max_context_examples until the number of token of the prompt
            # is less than maximum or reaches 1
            for size in self.prompt_size_history[-max_context_examples:]:
                prompt_size -= size
                trimmed_max_examples -= 1
                if prompt_size <= self.max_prompt_size:
                    if self.curr_max_context_examples == trimmed_max_examples:
                        warnings.warn(
                            "The parameter max_context_examples continues "
                            f"{self.curr_max_context_examples}"
                            ", so that the total amount of tokens does not"
                            f" exceed {MAX_GENERATE_TOKENS}."
                        )
                    else:
                        warnings.warn(
                            "The parameter max_context_examples was changed for"
                            f" this turn, from {self.curr_max_context_examples} to "
                            f"{trimmed_max_examples}, so that "
                            "the total amount of tokens does not"
                            f" exceed {MAX_GENERATE_TOKENS}."
                        )
                    self.curr_max_context_examples = trimmed_max_examples
                    return trimmed_max_examples

        raise ValueError(
            "The total number of tokens (prompt and prediction) cannot exceed "
            f"{MAX_GENERATE_TOKENS}. Try using a shorter start prompt, sending "
            "smaller text messages in the chat, or setting a smaller value "
            "for the parameter max_tokens. More details:\n"
            f" - Start Prompt: {self.start_prompt_size} tokens\n"
            f" - Messages sent in chat: {original_size - self.start_prompt_size} "
            f"tokens\n - Parameter max_tokens: {self.client_config['max_tokens']} "
            "tokens"
        )

    def _dispatch_concurrent_generate_call(self, **kwargs) -> Future:
        """Dispatches a concurrent call to co.generate.

        This allows a network bound co.generate call to proceed while also
        yielding the current response in a partial reply generator.

        Args:
            kwargs: Keyword arguments for the call to co.generate.

        Returns:
            Future: A future object that will be called to retrieve the result of
                co.generate.
        """
        with ThreadPoolExecutor(max_workers=1) as exe:
            future = exe.submit(self.co.generate, **kwargs)
        return future

    def get_stop_seq(self, response: str) -> str:
        """Given a response, returns the stop sequence it has if any.

        Args:
            response (str): Response coming from prompt chatbot.

        Returns:
            str: The stop sequence in the response. If no stop sequence is found, then
                an empty string is returned.

        """
        for stop_seq in self.client_config["stop_sequences"]:
            if stop_seq in response:
                return stop_seq
        return ""

    def generate_prompt_update_examples(self, query: str) -> str:
        """Generate prompt from query and update max context examples if necessary

        Args:
            query (str): A query passed to the prompt chatbot.

        Returns:
            current_prompt (str): Returns the current prompt using
            query and chat history

        """
        # The current prompt is assembled from the initial prompt,
        # from the chat history with a maximum of max_context_examples,
        # and from the current query

        current_prompt = self.get_current_prompt(query)

        current_prompt_size = self.co.tokenize(current_prompt).length

        if current_prompt_size > self.max_prompt_size:
            max_context_examples = self._update_max_context_examples(
                current_prompt_size, self.chatbot_config["max_context_examples"]
            )
            current_prompt = self.get_current_prompt(query, max_context_examples)

        elif (
            self.curr_max_context_examples
            != self.chatbot_config["max_context_examples"]
        ):
            warnings.warn(
                "The max_context_examples value returned"
                f" to {self.chatbot_config['max_context_examples']} - "
                f"value set in the original config"
            )
        return current_prompt

    def partial_reply(self, query: str) -> Tuple[str, str]:
        """Generates (partial) reply to a query given a chat history.

        Args:
            query (str): A query passed to the prompt chatbot.

        Yields:

            Tuple[str, str]: A tuple of the response before the co.generate call,
                and the response after.
        """
        current_prompt = self.generate_prompt_update_examples(query)
        self.prompt_history.append(current_prompt)

        response_before_current = ""
        response_so_far = ""
        num_requests_made = 0
        max_requests = int(self.client_config["max_tokens"] / TOKENS_PER_REQUEST)
        reply_complete = False

        # As soon as the function is called (and the generator is created), dispatch
        # a concurrent call to co.generate
        future = self._dispatch_concurrent_generate_call(
            model=self.client_config["model"],
            prompt=current_prompt,
            max_tokens=TOKENS_PER_REQUEST,
            temperature=self.client_config["temperature"],
            frequency_penalty=self.client_config["frequency_penalty"],
            presence_penalty=self.client_config["presence_penalty"],
            stop_sequences=self.client_config["stop_sequences"],
        )

        while num_requests_made < max_requests and not reply_complete:
            generated_object = future.result()
            partial_response = generated_object.generations[0].text

            # If the partial response is an empty string, then this iteration is a no-op
            # (we indicate that the reply is completely generated).
            if not partial_response:
                reply_complete = True

            else:

                # Concatenate the candidate response, then fetches the stop sequence if
                # it exists in the candidate response
                candidate_response = response_so_far + partial_response
                stop_seq = self.get_stop_seq(response_so_far + partial_response)

                # Truncate the candidate response if a stop sequence was found
                if stop_seq:
                    candidate_response = candidate_response[
                        : candidate_response.index(stop_seq)
                    ]

                    # If the stop sequence is found across two partial replies,
                    # then the response_so_far has to be truncated. Example:
                    #
                    #   stop_seq: "\nUser"
                    #   response_so_far: "Thank you!\n"
                    #   partial_response: "User: You are welcome"
                    #
                    # Then the candidate response is:
                    #
                    #   candidate_response: "Thank you!"
                    #
                    # In this case, what is yielded at the end of the loop needs to be:
                    #
                    #   response_before_current: "Thank you!"
                    #   response_so_far: "Thank you!"
                    #
                    # So we'll truncate the response_so_far to be candidate_response
                    if len(candidate_response) < len(response_so_far):
                        response_so_far = candidate_response

                    reply_complete = True

                # Save candidate response
                current_prompt += partial_response
                response_before_current = response_so_far
                response_so_far = candidate_response

                # If this is the first partial_reply, append a new element to
                # chat history after removing the leading whitespace
                if num_requests_made == 0:
                    response_so_far = response_so_far.lstrip()
                    self.chat_history.append(
                        self.prompt.create_interaction(query, response_so_far)
                    )
                    self.prompt_size_history.append(
                        self.co.tokenize(
                            self.prompt.create_interaction_string(
                                query, response_so_far
                            )
                        ).length
                    )
                # Otherwise, overwrite the current chat history with the current
                # response so far
                else:
                    self.chat_history[-1] = self.prompt.create_interaction(
                        query, response_so_far
                    )
                    self.prompt_size_history[-1] = self.co.tokenize(
                        self.prompt.create_interaction_string(query, response_so_far)
                    ).length

                num_requests_made += 1

                # This dispatches a concurrent call to co.generate, which can be
                # later accessed on the next iteration of the generator.
                if num_requests_made < max_requests and not reply_complete:
                    future = self._dispatch_concurrent_generate_call(
                        model=self.client_config["model"],
                        prompt=current_prompt,
                        max_tokens=TOKENS_PER_REQUEST,
                        temperature=self.client_config["temperature"],
                        frequency_penalty=self.client_config["frequency_penalty"],
                        presence_penalty=self.client_config["presence_penalty"],
                        stop_sequences=self.client_config["stop_sequences"],
                    )

                yield response_before_current, response_so_far

    def reply(self, query: str) -> Interaction:
        """Replies to a query given a chat history.

        The reply is then generated directly from a call to a LLM.

        Args:
            query (str): A query passed to the prompt chatbot.

        Returns:
            Interaction: Dictionary of query and generated LLM response
        """

        current_prompt = self.generate_prompt_update_examples(query)

        # Make a call to Cohere's co.generate API
        generated_object = self.co.generate(
            model=self.client_config["model"],
            prompt=current_prompt,
            max_tokens=self.client_config["max_tokens"],
            temperature=self.client_config["temperature"],
            frequency_penalty=self.client_config["frequency_penalty"],
            presence_penalty=self.client_config["presence_penalty"],
            stop_sequences=self.client_config["stop_sequences"],
        )
        # If response was cut off by .generate() finding a stop sequence,
        # remove that sequence from the response.
        response = generated_object.generations[0].text
        for stop_seq in self.client_config["stop_sequences"]:
            if response.endswith(stop_seq):
                response = response[: -len(stop_seq)]
        response = response.lstrip()

        # We need to remember the current response in the chat history for future
        # responses.
        self.chat_history.append(self.prompt.create_interaction(query, response))
        self.prompt_size_history.append(
            self.co.tokenize(
                self.prompt.create_interaction_string(query, response)
            ).length
        )
        self.prompt_history.append(current_prompt)

        return response

    def get_current_prompt(self, query: str, max_context_examples: int = None) -> str:
        """Stitches the prompt with a trailing window of the chat.
        Args:
            query (str): The current user query.
            max_context_examples (int): The length of the chat history for
            the chatbot to use in reply.

        Returns:
            str: The current prompt given a query.
        """
        if max_context_examples is None:
            max_context_examples = self.chatbot_config["max_context_examples"]

        # get base prompt
        base_prompt = self.prompt.to_string() + "\n"

        # get context prompt
        context_prompt_lines = []
        trimmed_chat_history = (
            self.chat_history[-max_context_examples:]
            if max_context_examples > 0
            else []
        )
        # TODO when prompt is updated, the history is mutated
        # as it is recreated using the new prompt. A possible fix is to save the old
        # prompt in history and use it when recreating.
        for turn in trimmed_chat_history:
            context_prompt_lines.append(self.prompt.create_interaction_string(**turn))
        context_prompt = self.prompt.example_separator + "".join(context_prompt_lines)

        current_prompt = base_prompt + context_prompt

        # get query prompt
        if query != "":
            query_prompt = self.prompt.create_interaction_string(query)
            current_prompt += query_prompt
        return current_prompt.strip()

    def configure_chatbot(self, chatbot_config: Dict = {}) -> None:
        """Configures chatbot options.

        Args:
            chatbot_config (Dict, optional): Updates self.chatbot_config. Defaults
                to {}.
        """
        # We initialize the chatbot to these default config values.
        if not hasattr(self, "chatbot_config"):
            self.chatbot_config = {"max_context_examples": 10, "avatar": ":robot:"}
        # Override default config values with the config passed in
        if isinstance(chatbot_config, Dict):
            self.chatbot_config.update(chatbot_config)
        else:
            raise TypeError(
                "chatbot_config must be of type Dict, but was passed in as "
                f"{type(chatbot_config)}"
            )

    def configure_client(self, client_config: Dict = {}) -> None:
        """Configures client options.

        Args:
            client_config (Dict, optional): Updates self.client_config. Defaults to {}.
        """
        # We initialize the client to these default config values.
        if not hasattr(self, "client_config"):
            self.client_config = {
                "model": "xlarge",
                "max_tokens": 200,
                "temperature": 0.75,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "stop_sequences": ["\\n", "\n"],
            }
        # Override default config values with the config passed in
        if isinstance(client_config, Dict):
            self.client_config.update(client_config)
        else:
            raise TypeError(
                "client_config must be of type Dict, but was passed in as "
                f"{type(client_config)}"
            )

        # Checks if the parameter is equal or bigger than MAX_GENERATE_TOKENS
        if self.client_config["max_tokens"] >= MAX_GENERATE_TOKENS:
            raise ValueError(
                f"The parameter max_tokens needs to be smaller than "
                f"{MAX_GENERATE_TOKENS}. Try using a smaller value."
            )
        elif self.client_config["max_tokens"] > (MAX_GENERATE_TOKENS * 0.75):
            warnings.warn(
                "The parameter max_tokens has a value "
                f"({self.client_config['max_tokens']}) close to the total allowed"
                f" for prompt and prediction - {MAX_GENERATE_TOKENS} tokens"
            )

    @classmethod
    def from_persona(
        cls,
        persona_name: str,
        client: cohere.Client,
        persona_dir: str = PERSONA_MODEL_DIRECTORY,
    ):
        """Initializes a PromptChatbot using a persona.

        Args:
            persona (str): Name of persona, corresponding to a .json file.
            client (cohere.Client): Cohere client for API
            persona_dir (str): Path to where pre-defined personas are.
        """
        # Load the persona from a local directory
        persona_path = os.path.join(persona_dir, persona_name, "config.json")
        if os.path.isfile(persona_path):
            logging.info(f"loading persona from {persona_path}")
        else:
            raise FileNotFoundError(f"{persona_path} cannot be found.")
        with open(persona_path) as f:
            persona = json.load(f)

        # Validate that the persona follows our predefined schema
        cls._validate_persona_dict(persona, persona_path)
        return cls(
            client=client,
            prompt=ChatPrompt.from_dict(persona["chat_prompt_config"]),
            persona_name=persona_name,
            chatbot_config=persona["chatbot_config"],
            client_config=persona["client_config"],
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes this instance into a Python dictionary.

        Returns:
            Dict[str, Any]: Dictionary of attributes that defines this instance of a
                PromptChatbot.
        """
        attr_dict = {k: v for k, v in vars(self).items()}
        attr_dict["prompt"] = attr_dict["prompt"].to_dict()
        return attr_dict

    def _check_prompt_size(self) -> None:

        self.start_prompt_size = self.co.tokenize(self.prompt.to_string()).length
        if self.start_prompt_size > self.max_prompt_size:
            raise ValueError(
                f"The prompt given to PromptChatbot has {self.start_prompt_size}"
                " tokens. And the value of the parameter max_tokens is"
                f" {self.client_config['max_tokens']}. Adding the two values "
                f"the total cannot exceed {MAX_GENERATE_TOKENS}. "
                "Try using a shorter preamble or less examples."
            )
        elif self.start_prompt_size > (0.75 * self.max_prompt_size):
            warnings.warn(
                "The prompt given to PromptChatbot has "
                f"{self.start_prompt_size} tokens. And the value of the parameter"
                f" max_tokens is {self.client_config['max_tokens']}. "
                "Adding the two together gives a value close to the total allowed"
                f" for prompt and prediction - {MAX_GENERATE_TOKENS} tokens"
            )

    @staticmethod
    def _validate_persona_dict(persona: Dict[str, Any], persona_path: str) -> None:
        """Validates formatting of a persona defined as a dictionary.

        Args:
            persona (Dict[str, Any]): A dictionary containing the persona.
            persona_path: The path from which the persona was loaded.
        """
        try:
            jsonschema.validate(instance=persona, schema=PERSONA_JSON_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            raise jsonschema.exceptions.ValidationError(
                f"Type of values in given dictionary (persona from {persona_path}) do "
                f"not match schema': {e}"
            )
        except KeyError as e:
            raise KeyError(
                f"Invalid key in given dictionary (persona from {persona_path})': {e}"
            )
        except Exception as e:
            raise Exception(
                "Failed to validate persona in given dictionary (persona from "
                f"{persona_path}): {e}"
            )
