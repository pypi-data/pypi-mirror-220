import os
from typing import List, Tuple
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner
from llm import Prompt, Response, get_model
from llm.cli import cli

from llm_claude import Claude
from llm_claude.vendored_anthropic import AI_PROMPT, HUMAN_PROMPT


@patch("llm_claude.Anthropic")
def test_claude_response(mock_anthropic):
    mock_response = MagicMock()
    mock_response.completion = "hello"
    mock_anthropic.return_value.completions.create.return_value.__iter__.return_value = [
        mock_response
    ]
    prompt = Prompt("hello", "")
    model = Claude("claude-2")
    model.key = "key"
    items = list(model.response(prompt))

    mock_anthropic.return_value.completions.create.assert_called_with(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt="\n\nHuman: hello\n\nAssistant:",
        stream=True,
    )

    assert items == ["hello"]


@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "X"})
@patch("llm_claude.Anthropic")
def test_claude_prompt(mock_anthropic):
    mock_response = Mock()
    mock_response.completion = "🐶🐶"
    mock_anthropic.return_value.completions.create.return_value = mock_response
    runner = CliRunner()
    result = runner.invoke(cli, ["two dog emoji", "-m", "claude", "--no-stream"])
    assert result.exit_code == 0, result.output
    assert result.output == "🐶🐶\n"


@pytest.mark.parametrize(
    "prompt, conversation_messages, expected",
    (
        ("hello", [], [f"{HUMAN_PROMPT} hello{AI_PROMPT}"]),
        (
            "hello 2",
            [("user 1", "response 1")],
            [
                f"{HUMAN_PROMPT} user 1{AI_PROMPT}response 1",
                f"{HUMAN_PROMPT} hello 2{AI_PROMPT}",
            ],
        ),
        (
            "hello 3",
            [("user 1", "response 1"), ("user 2", "response 2")],
            [
                "\n\nHuman: user 1\n\nAssistant:response 1",
                "\n\nHuman: user 2\n\nAssistant:response 2",
                "\n\nHuman: hello 3\n\nAssistant:",
            ],
        ),
    ),
)
def test_generate_prompt_messages(
    prompt: str, conversation_messages: List[Tuple[str, str]], expected: List[str]
):
    model = get_model("claude")
    conversation = None
    if conversation_messages:
        conversation = model.conversation()
        for prev_prompt, prev_response in conversation_messages:
            conversation.responses.append(
                Response.fake(
                    prompt=prev_prompt,
                    model=model,
                    system=None,
                    response=prev_response,
                )
            )

    messages = model.generate_prompt_messages(prompt, conversation)
    assert list(messages) == expected
