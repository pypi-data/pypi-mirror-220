from enum import Enum, auto
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
  from langdash.chains import LDChain
  from langdash.llm_session import LLMGenerationSession


class Role(Enum):
  System = auto()
  User = auto()
  Bot = auto()


class ChatCompletion:

  def __init__(
    self,
    init_session: "LLMGenerationSession",
    chain_by_role: Dict[Role, "LDChain"],
  ):
    self._init_session = init_session
    self._chain_by_role = chain_by_role

  def session(self) -> "ChatCompletionSession":
    return ChatCompletionSession(self)


class ChatCompletionSession:

  def __init__(self, cc: ChatCompletion):
    self._cc = cc
    self._session = self._cc._init_session.clone()

  def _get_call_args(self, role, content: Optional[str]):
    chain = self._cc._chain_by_role[role]
    args = None
    if content is not None:
      args = {"content": content}
    return chain, args

  def stream(
    self,
    role: Role,
    content: Optional[str] = None,
  ):
    chain, args = self._get_call_args(role, content)
    return chain.stream(self._session, args=args)

  def call(
    self,
    role: Role,
    content: Optional[str] = None,
  ):
    chain, args = self._get_call_args(role, content)
    return chain.call(self._session, args=args)
