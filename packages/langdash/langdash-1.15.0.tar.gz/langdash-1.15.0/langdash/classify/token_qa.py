from typing import Union, List, Tuple, Dict, Optional
from langdash.chains import LDChainCached, LDResult, LDNodeArgs
from langdash.llm_session import LLMGenerationSession


class TokenQA:
  """
  Helper class for performing text classification through generative
  language models.
  """

  _classes_tok: Dict[str, List[int]]

  def __init__(
    self,
    prompt_chain: LDChainCached,
    classes: Dict[str, Union[str, List[str]]],
  ):
    """
    Args:
      prompt_chain (LDChainCached):
        Cached chain used for inference.
      classes (Dict[str, Union[str, List[str]]]):
        A dictionary of class to one or more tokens to be classified.
    """
    self._prompt_chain = prompt_chain

    if self._prompt_chain.argtype("query") != str:
      raise ValueError("prompt must have query argument")

    self._classes = classes
    self._classes_tok = {}
    self._token_list_set = False

  @staticmethod
  def _strs_to_token_list(
    session: LLMGenerationSession, str_or_list: Union[str, List[str]]
  ) -> List[int]:
    str_list = str_or_list if isinstance(str_or_list, list) else [str_or_list]
    token_list = []
    for str_ in str_list:
      token = session.tokenize(str_)
      assert len(token) == 1
      token_list.append(token[0])
    return token_list

  def query(self,
            query: str,
            additional_args: Optional[LDNodeArgs] = None,
            return_result: bool = False) \
    -> Union[Dict[str, float], Tuple[Dict[str, float], LDResult]]:
    """
    Perform a query using the language model.
    
    Args:
      query (str):
        The query.
      additional_args (Optional[LDNodeArgs]):
        Optional additional arguments to be submitted for inference.
        Defaults to `None`.
      return_result (bool):
        Whether or not to return the full result of inference.
    
    Returns:
      A dictionary of class to probability floats.
      If `return_result` is true, then a tuple with that dictionary and
      an `LDResult` object is returned.
    """
    args = {"query": query}
    if additional_args is not None:
      args.update(additional_args)
    result, session = self._prompt_chain.call(args=args, return_session=True)
    if not self._token_list_set:
      self._classes_tok = {}
      for k, v in self._classes.items():
        self._classes_tok[k] = TokenQA._strs_to_token_list(session, v)
      self._token_list_set = True

    tok_probs = session.next_token_probs()

    prob: Dict[str, float] = {}
    for k, toks in self._classes_tok.items():
      prob[k] = sum(map(lambda tok: float(tok_probs[tok]), toks))
    prob_sum = sum(prob.values())
    # FIXME: mypy gives wrong type inference for k and v
    for k, v in prob.items():  # type: ignore
      prob[k] = v / prob_sum  # type: ignore

    if return_result:
      return prob, result
    return prob
