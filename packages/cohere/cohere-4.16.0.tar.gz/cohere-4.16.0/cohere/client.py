import json as jsonlib
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from functools import partial
from typing import Any, Dict, Iterable, List, Optional, Union

try:
    from typing import Literal, TypedDict
except ImportError:
    from typing_extensions import Literal, TypedDict

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import cohere
from cohere.custom_model_dataset import CustomModelDataset
from cohere.error import CohereAPIError, CohereConnectionError, CohereError
from cohere.logging import logger
from cohere.responses import (
    Classification,
    Classifications,
    Codebook,
    Detokenization,
    Generations,
    StreamingGenerations,
    Tokens,
)
from cohere.responses.bulk_embed import BulkEmbedJob, CreateBulkEmbedJobResponse
from cohere.responses.chat import Chat, Mode, StreamingChat
from cohere.responses.classify import Example as ClassifyExample
from cohere.responses.classify import LabelPrediction
from cohere.responses.cluster import ClusterJobResult, CreateClusterJobResponse
from cohere.responses.custom_model import (
    CUSTOM_MODEL_PRODUCT_MAPPING,
    CUSTOM_MODEL_STATUS,
    CUSTOM_MODEL_TYPE,
    INTERNAL_CUSTOM_MODEL_TYPE,
    CustomModel,
    HyperParametersInput,
)
from cohere.responses.detectlang import DetectLanguageResponse, Language
from cohere.responses.embeddings import Embeddings
from cohere.responses.feedback import (
    GenerateFeedbackResponse,
    GeneratePreferenceFeedbackResponse,
    PreferenceRating,
)
from cohere.responses.rerank import Reranking
from cohere.responses.summarize import SummarizeResponse
from cohere.utils import is_api_key_valid, threadpool_map, wait_for_job


class Client:
    """Cohere Client

    Args:
        api_key (str): Your API key.
        num_workers (int): Maximal number of threads for parallelized calls.
        request_dict (dict): Additional parameters for calls with the requests library. Currently ignored in AsyncClient
        check_api_key (bool): Whether to check the api key for validity on initialization.
        client_name (str): A string to identify your application for internal analytics purposes.
        max_retries (int): maximal number of retries for requests.
        timeout (int): request timeout in seconds.
        api_url (str): override the default api url from the default cohere.COHERE_API_URL
    """

    def __init__(
        self,
        api_key: str = None,
        num_workers: int = 64,
        request_dict: dict = {},
        check_api_key: bool = True,
        client_name: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 120,
        api_url: str = None,
    ) -> None:
        self.api_key = api_key or os.getenv("CO_API_KEY")
        self.api_url = api_url or os.getenv("CO_API_URL", cohere.COHERE_API_URL)
        self.batch_size = cohere.COHERE_EMBED_BATCH_SIZE
        self._executor = ThreadPoolExecutor(num_workers)
        self.num_workers = num_workers
        self.request_dict = request_dict
        self.request_source = "python-sdk-" + cohere.SDK_VERSION
        self.max_retries = max_retries
        self.timeout = timeout
        self.api_version = f"v{cohere.API_VERSION}"
        if client_name:
            self.request_source += ":" + client_name

        if check_api_key:
            self.check_api_key()

    def check_api_key(self) -> Dict[str, bool]:
        """
        Checks the api key, which happens automatically during Client initialization, but not in AsyncClient.
        check_api_key raises an exception when the key is invalid, but the return value for valid keys is kept for
        backwards compatibility.
        """
        return {"valid": is_api_key_valid(self.api_key)}

    def batch_generate(
        self, prompts: List[str], return_exceptions=False, **kwargs
    ) -> List[Union[Generations, Exception]]:
        """A batched version of generate with multiple prompts.

        Args:
            prompts: list of prompts
            return_exceptions (bool): Return exceptions as list items rather than raise them. Ensures your entire batch is not lost on one of the items failing.
            kwargs: other arguments to `generate`
        """
        return threadpool_map(
            self.generate,
            [dict(prompt=prompt, **kwargs) for prompt in prompts],
            num_workers=self.num_workers,
            return_exceptions=return_exceptions,
        )

    def generate(
        self,
        prompt: Optional[str] = None,
        prompt_vars: object = {},
        model: Optional[str] = None,
        preset: Optional[str] = None,
        num_generations: Optional[int] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        k: Optional[int] = None,
        p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        end_sequences: Optional[List[str]] = None,
        stop_sequences: Optional[List[str]] = None,
        return_likelihoods: Optional[str] = None,
        truncate: Optional[str] = None,
        logit_bias: Dict[int, float] = {},
        stream: bool = False,
    ) -> Union[Generations, StreamingGenerations]:
        """Generate endpoint.
        See https://docs.cohere.ai/reference/generate for advanced arguments

        Args:
            prompt (str): Represents the prompt or text to be completed. Trailing whitespaces will be trimmed.
            model (str): (Optional) The model ID to use for generating the next reply.
            return_likelihoods (str): (Optional) One of GENERATION|ALL|NONE to specify how and if the token (log) likelihoods are returned with the response.
            preset (str): (Optional) The ID of a custom playground preset.
            num_generations (int): (Optional) The number of generations that will be returned, defaults to 1.
            max_tokens (int): (Optional) The number of tokens to predict per generation, defaults to 20.
            temperature (float): (Optional) The degree of randomness in generations from 0.0 to 5.0, lower is less random.
            truncate (str): (Optional) One of NONE|START|END, defaults to END. How the API handles text longer than the maximum token length.\
            stream (bool): Return streaming tokens.
        Returns:
            if stream=False: a Generations object
            if stream=True: a StreamingGenerations object including:
                id (str): The id of the whole generation call
                generations (Generations): same as the response when stream=False
                finish_reason (string) possible values:
                    COMPLETE: when the stream successfully completed
                    ERROR: when an error occurred during streaming
                    ERROR_TOXIC: when the stream was halted due to toxic output.
                    ERROR_LIMIT: when the context is too big to generate.
                    USER_CANCEL: when the user has closed the stream / cancelled the request
                    MAX_TOKENS: when the max tokens limit was reached.
                texts (List[str]): list of segments of text streamed back from the API

        Examples:
            A simple generate message:
                >>> res = co.generate(prompt="Hey! How are you doing today?")
                >>> print(res.text)
            Streaming generate:
                >>> res = co.generate(
                >>>     prompt="Hey! How are you doing today?",
                >>>     stream=True)
                >>> for token in res:
                >>>     print(token)
        """
        json_body = {
            "model": model,
            "prompt": prompt,
            "prompt_vars": prompt_vars,
            "preset": preset,
            "num_generations": num_generations,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "k": k,
            "p": p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "end_sequences": end_sequences,
            "stop_sequences": stop_sequences,
            "return_likelihoods": return_likelihoods,
            "truncate": truncate,
            "logit_bias": logit_bias,
            "stream": stream,
        }
        response = self._request(cohere.GENERATE_URL, json=json_body, stream=stream)
        if stream:
            return StreamingGenerations(response)
        else:
            return Generations.from_dict(response=response, return_likelihoods=return_likelihoods)

    def chat(
        self,
        message: Optional[str] = None,
        query: Optional[str] = None,
        conversation_id: Optional[str] = "",
        model: Optional[str] = None,
        return_chatlog: Optional[bool] = False,
        return_prompt: Optional[bool] = False,
        return_preamble: Optional[bool] = False,
        chat_history: Optional[List[Dict[str, str]]] = None,
        preamble_override: Optional[str] = None,
        user_name: Optional[str] = None,
        temperature: Optional[float] = 0.8,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = False,
        p: Optional[float] = None,
        k: Optional[float] = None,
        logit_bias: Optional[Dict[int, float]] = None,
        mode: Optional[Mode] = None,
        documents: Optional[List[Dict[str, str]]] = None,
    ) -> Union[Chat, StreamingChat]:
        """Returns a Chat object with the query reply.

        Args:
            query (str): Deprecated. Use message instead.
            message (str): The message to send to the chatbot.
            conversation_id (str): (Optional) The conversation id to continue the conversation.
            model (str): (Optional) The model to use for generating the next reply.
            return_chatlog (bool): (Optional) Whether to return the chatlog.
            return_prompt (bool): (Optional) Whether to return the prompt.
            return_preamble (bool): (Optional) Whether to return the preamble.
            chat_history (List[Dict[str, str]]): (Optional) A list of entries used to construct the conversation. If provided, these messages will be used to build the prompt and the conversation_id will be ignored so no data will be stored to maintain state.
            preamble_override (str): (Optional) A string to override the preamble.
            user_name (str): (Optional) A string to override the username.
            temperature (float): (Optional) The temperature to use for the next reply. The higher the temperature, the more random the reply.
            max_tokens (int): (Optional) The max tokens generated for the next reply.
            stream (bool): Return streaming tokens.
            p (float): (Optional) The nucleus sampling probability.
            k (float): (Optional) The top-k sampling probability.
            logit_bias (Dict[int, float]): (Optional) A dictionary of logit bias values to use for the next reply.
            mode Mode: (Optional) This property determines which functionality of retrieval augmented generation to use.
                                    chat mode doesn't use any retrieval augmented generation functionality.
                                    search_query_generation uses the provided query to produce search terms that you can use to search for documents.
                                    augmented_generation uses the provided documents and query to produce citations
            document Document: (Optional) The documents to use in augmented_generation mode. Shape: ("title", str), ("snippet", str), ("url", str)
        Returns:
            a Chat object if stream=False, or a StreamingChat object if stream=True

        Examples:
            A simple chat message:
                >>> res = co.chat(message="Hey! How are you doing today?")
                >>> print(res.text)
                >>> print(res.conversation_id)
            Continuing a session using a specific model:
                >>> res = co.chat(
                >>>     message="Hey! How are you doing today?",
                >>>     conversation_id="1234",
                >>>     model="command",
                >>>     return_chatlog=True)
                >>> print(res.text)
                >>> print(res.chatlog)
            Streaming chat:
                >>> res = co.chat(
                >>>     message="Hey! How are you doing today?",
                >>>     stream=True)
                >>> for token in res:
                >>>     print(token)
            Stateless chat with chat history:
                >>> res = co.chat(
                >>>     message="Tell me a joke!",
                >>>     chat_history=[
                >>>         {'user_name': 'User', message': 'Hey! How are you doing today?'},
                >>>         {'user_name': 'Bot', message': 'I am doing great! How can I help you?'},
                >>>     ],
                >>>     return_prompt=True)
                >>> print(res.text)
                >>> print(res.prompt)
            Query generation example:
                >>> res = co.chat(query="What are the tallest penguins?", mode="search_query_generation")
                >>> print(res.queries)
                >>> print(res.is_search_required)
            Augmented generation example:
                >>> res = co.chat(query="What are the tallest penguins?",
                                  mode="augmented_generation",
                                  documents = [{"title":"Tall penguins", "snippet":"Emperor penguins are the tallest", "url":"http://example.com/foo"}])
                >>> print(res.text)
                >>> print(res.citations)
        """
        if chat_history is not None:
            should_warn = True
            for entry in chat_history:
                if "text" in entry:
                    entry["message"] = entry["text"]

                if "text" in entry and should_warn:
                    logger.warning(
                        "The 'text' parameter is deprecated and will be removed in a future version of this function. "
                        + "Use 'message' instead.",
                    )
                    should_warn = False

        if query is not None:
            logger.warning(
                "The chat_history 'text' key is deprecated and will be removed in a future version of this function. "
                + "Use 'message' instead.",
            )
            message = query

        json_body = {
            "message": message,
            "conversation_id": conversation_id,
            "model": model,
            "return_chatlog": return_chatlog,
            "return_prompt": return_prompt,
            "return_preamble": return_preamble,
            "chat_history": chat_history,
            "preamble_override": preamble_override,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            "user_name": user_name,
            "p": p,
            "k": k,
            "logit_bias": logit_bias,
            "mode": mode,
            "documents": documents,
        }
        response = self._request(cohere.CHAT_URL, json=json_body, stream=stream)

        if stream:
            return StreamingChat(response)
        else:
            return Chat.from_dict(response, message=message, client=self)

    def embed(
        self,
        texts: List[str],
        model: Optional[str] = None,
        truncate: Optional[str] = None,
        compress: Optional[bool] = False,
        compression_codebook: Optional[str] = "default",
    ) -> Embeddings:
        """Returns an Embeddings object for the provided texts. Visit https://cohere.ai/embed to learn about embeddings.

        Args:
            text (List[str]): A list of strings to embed.
            model (str): (Optional) The model ID to use for embedding the text.
            truncate (str): (Optional) One of NONE|START|END, defaults to END. How the API handles text longer than the maximum token length.
            compress (bool): (Optional) Whether to compress the embeddings. When True, the compressed_embeddings will be returned as integers in the range [0, 255].
            compression_codebook (str): (Optional) The compression codebook to use for compressed embeddings. Defaults to "default".
        """
        responses = {
            "embeddings": [],
            "compressed_embeddings": [],
        }
        json_bodys = []

        for i in range(0, len(texts), self.batch_size):
            texts_batch = texts[i : i + self.batch_size]
            json_bodys.append(
                {
                    "model": model,
                    "texts": texts_batch,
                    "truncate": truncate,
                    "compress": compress,
                    "compression_codebook": compression_codebook,
                }
            )

        meta = None
        for result in self._executor.map(lambda json_body: self._request(cohere.EMBED_URL, json=json_body), json_bodys):
            responses["embeddings"].extend(result["embeddings"])
            responses["compressed_embeddings"].extend(result.get("compressed_embeddings", []))
            meta = result["meta"] if not meta else meta

        return Embeddings(
            embeddings=responses["embeddings"],
            compressed_embeddings=responses["compressed_embeddings"],
            meta=meta,
        )

    def codebook(
        self,
        model: Optional[str] = None,
        compression_codebook: Optional[str] = "default",
    ) -> Codebook:
        """Returns a codebook object for the provided model. Visit https://cohere.ai/embed to learn about compressed embeddings and codebooks.

        Args:
            model (str): (Optional) The model ID to use for embedding the text.
            compression_codebook (str): (Optional) The compression codebook to use for compressed embeddings. Defaults to "default".
        """
        json_body = {
            "model": model,
            "compression_codebook": compression_codebook,
        }
        response = self._request(cohere.CODEBOOK_URL, json=json_body)
        return Codebook(response["codebook"], response["meta"])

    def classify(
        self,
        inputs: List[str] = [],
        model: Optional[str] = None,
        preset: Optional[str] = None,
        examples: List[ClassifyExample] = [],
        truncate: Optional[str] = None,
    ) -> Classifications:
        """Returns a Classifications object of the inputs provided, see https://docs.cohere.ai/reference/classify for advances usage.

        Args:
            inputs (List[str]): A list of texts to classify.
            model (str): (Optional) The model ID to use for classifing the inputs.
            examples (List[ClassifyExample]): A list of ClassifyExample objects containing a text and its associated label.
            truncate (str): (Optional) One of NONE|START|END, defaults to END. How the API handles text longer than the maximum token length.
        """
        examples_dicts = [{"text": example.text, "label": example.label} for example in examples]

        json_body = {
            "model": model,
            "preset": preset,
            "inputs": inputs,
            "examples": examples_dicts,
            "truncate": truncate,
        }
        response = self._request(cohere.CLASSIFY_URL, json=json_body)

        classifications = []
        for res in response["classifications"]:
            labelObj = {}
            for label, prediction in res["labels"].items():
                labelObj[label] = LabelPrediction(prediction["confidence"])
            classifications.append(
                Classification(res["input"], res["prediction"], res["confidence"], labelObj, id=res["id"])
            )

        return Classifications(classifications, response.get("meta"))

    def summarize(
        self,
        text: str,
        model: Optional[str] = None,
        length: Optional[str] = None,
        format: Optional[str] = None,
        temperature: Optional[float] = None,
        additional_command: Optional[str] = None,
        extractiveness: Optional[str] = None,
    ) -> SummarizeResponse:
        """Returns a generated summary of the specified length for the provided text.

        Args:
            text (str): Text to summarize.
            model (str): (Optional) ID of the model.
            length (str): (Optional) One of {"short", "medium", "long"}, defaults to "medium". \
                Controls the length of the summary.
            format (str): (Optional) One of {"paragraph", "bullets"}, defaults to "paragraph". \
                Controls the format of the summary.
            extractiveness (str) One of {"high", "medium", "low"}, defaults to "high". \
                Controls how close to the original text the summary is. "High" extractiveness \
                summaries will lean towards reusing sentences verbatim, while "low" extractiveness \
                summaries will tend to paraphrase more.
            temperature (float): Ranges from 0 to 5. Controls the randomness of the output. \
                Lower values tend to generate more “predictable” output, while higher values \
                tend to generate more “creative” output. The sweet spot is typically between 0 and 1.
            additional_command (str): (Optional) Modifier for the underlying prompt, must \
                complete the sentence "Generate a summary _".

        Examples:
            Summarize a text:
                >>> res = co.summarize(text="Stock market report for today...")
                >>> print(res.summary)

            Summarize a text with a specific model and prompt:
                >>> res = co.summarize(
                >>>     text="Stock market report for today...",
                >>>     model="summarize-xlarge",
                >>>     length="long",
                >>>     format="bullets",
                >>>     temperature=0.3,
                >>>     additional_command="focusing on the highest performing stocks")
                >>> print(res.summary)
        """
        json_body = {
            "model": model,
            "text": text,
            "length": length,
            "format": format,
            "temperature": temperature,
            "additional_command": additional_command,
            "extractiveness": extractiveness,
        }
        # remove None values from the dict
        json_body = {k: v for k, v in json_body.items() if v is not None}
        response = self._request(cohere.SUMMARIZE_URL, json=json_body)

        return SummarizeResponse(id=response["id"], summary=response["summary"], meta=response["meta"])

    def batch_tokenize(self, texts: List[str], return_exceptions=False, **kwargs) -> List[Union[Tokens, Exception]]:
        """A batched version of tokenize.

        Args:
            texts: list of texts
            return_exceptions (bool): Return exceptions as list items rather than raise them. Ensures your entire batch is not lost on one of the items failing.
            kwargs: other arguments to `tokenize`
        """
        return threadpool_map(
            self.tokenize,
            [dict(text=text, **kwargs) for text in texts],
            num_workers=self.num_workers,
            return_exceptions=return_exceptions,
        )

    def tokenize(self, text: str, model: Optional[str] = None) -> Tokens:
        """Returns a Tokens object of the provided text, see https://docs.cohere.ai/reference/tokenize for advanced usage.

        Args:
            text (str): Text to summarize.
            model (str): An optional model name that will ensure that the tokenization uses the tokenizer used by that model, which can be critical for counting tokens properly.
        """
        json_body = {"text": text, "model": model}
        res = self._request(cohere.TOKENIZE_URL, json=json_body)
        return Tokens(tokens=res["tokens"], token_strings=res["token_strings"], meta=res.get("meta"))

    def batch_detokenize(
        self, list_of_tokens: List[List[int]], return_exceptions=False, **kwargs
    ) -> List[Union[Detokenization, Exception]]:
        """A batched version of detokenize.

        Args:
            list_of_tokens: list of list of tokens
            return_exceptions (bool): Return exceptions as list items rather than raise them. Ensures your entire batch is not lost on one of the items failing.
            kwargs: other arguments to `detokenize`
        """
        return threadpool_map(
            self.detokenize,
            [dict(tokens=tokens, **kwargs) for tokens in list_of_tokens],
            num_workers=self.num_workers,
            return_exceptions=return_exceptions,
        )

    def detokenize(self, tokens: List[int], model: Optional[str] = None) -> Detokenization:
        """Returns a Detokenization object of the provided tokens, see https://docs.cohere.ai/reference/detokenize for advanced usage.

        Args:
            tokens (List[int]): A list of tokens to convert to strings
            model (str): An optional model name. This will ensure that the detokenization is done by the tokenizer used by that model.
        """
        json_body = {"tokens": tokens, "model": model}
        res = self._request(cohere.DETOKENIZE_URL, json=json_body)
        return Detokenization(text=res["text"], meta=res.get("meta"))

    def detect_language(self, texts: List[str]) -> DetectLanguageResponse:
        """Returns a DetectLanguageResponse object of the provided texts, see https://docs.cohere.ai/reference/detect-language-1 for advanced usage.

        Args:
            texts (List[str]): A list of texts to identify language for
        """
        json_body = {
            "texts": texts,
        }
        response = self._request(cohere.DETECT_LANG_URL, json=json_body)
        results = []
        for result in response["results"]:
            results.append(Language(result["language_code"], result["language_name"]))
        return DetectLanguageResponse(results, response["meta"])

    def generate_feedback(
        self,
        request_id: str,
        good_response: bool,
        model=None,
        desired_response: str = None,
        flagged_response: bool = None,
        flagged_reason: str = None,
        prompt: str = None,
        annotator_id: str = None,
    ) -> GenerateFeedbackResponse:
        """Give feedback on a response from the Cohere Generate API to improve the model.

        Args:
            request_id (str): The request_id of the generation request to give feedback on.
            good_response (bool): Whether the response was good or not.
            model (str): (Optional) ID of the model.
            desired_response (str): (Optional) The desired response.
            flagged_response (bool): (Optional) Whether the response was flagged or not.
            flagged_reason (str): (Optional) The reason the response was flagged.
            prompt (str): (Optional) The prompt used to generate the response.
            annotator_id (str): (Optional) The ID of the annotator.

        Examples:
            A user accepts a model's suggestion in an assisted writing setting:
                >>> generations = co.generate(f"Write me a polite email responding to the one below: {email}. Response:")
                >>> if user_accepted_suggestion:
                >>>     co.generate_feedback(request_id=generations[0].id, good_response=True)

            The user edits the model's suggestion:
                >>> generations = co.generate(f"Write me a polite email responding to the one below: {email}. Response:")
                >>> if user_edits_suggestion:
                >>>     co.generate_feedback(request_id=generations[0].id, good_response=False, desired_response=user_edited_suggestion)

        """

        json_body = {
            "request_id": request_id,
            "good_response": good_response,
            "desired_response": desired_response,
            "flagged_response": flagged_response,
            "flagged_reason": flagged_reason,
            "prompt": prompt,
            "annotator_id": annotator_id,
            "model": model,
        }
        response = self._request(cohere.GENERATE_FEEDBACK_URL, json_body)
        return GenerateFeedbackResponse(id=response["id"])

    def generate_preference_feedback(
        self,
        ratings: List[PreferenceRating],
        model=None,
        prompt: str = None,
        annotator_id: str = None,
    ) -> GeneratePreferenceFeedbackResponse:
        """Give preference feedback on a response from the Cohere Generate API to improve the model.

        Args:
            ratings (List[PreferenceRating]): A list of PreferenceRating objects.
            model (str): (Optional) ID of the model.
            prompt (str): (Optional) The prompt used to generate the response.
            annotator_id (str): (Optional) The ID of the annotator.

        Examples:
            A user accepts a model's suggestion in an assisted writing setting, and prefers it to a second suggestion:
            >>> generations = co.generate(f"Write me a polite email responding to the one below: {email}. Response:", num_generations=2)
            >>> if user_accepted_idx: // prompt user for which generation they prefer
            >>>    ratings = []
            >>>    if user_accepted_idx == 0:
            >>>        ratings.append(PreferenceRating(request_id=0, rating=1))
            >>>        ratings.append(PreferenceRating(request_id=1, rating=0))
            >>>    else:
            >>>        ratings.append(PreferenceRating(request_id=0, rating=0))
            >>>        ratings.append(PreferenceRating(request_id=1, rating=1))
            >>>    co.generate_preference_feedback(ratings=ratings)
        """
        ratings_dicts = []
        for rating in ratings:
            ratings_dicts.append(asdict(rating))

        json_body = {
            "ratings": ratings_dicts,
            "prompt": prompt,
            "annotator_id": annotator_id,
            "model": model,
        }
        response = self._request(cohere.GENERATE_PREFERENCE_FEEDBACK_URL, json_body)
        return GenerateFeedbackResponse(id=response["id"])

    def rerank(
        self,
        query: str,
        documents: Union[List[str], List[Dict[str, Any]]],
        model: str,
        top_n: Optional[int] = None,
        max_chunks_per_doc: Optional[int] = None,
    ) -> Reranking:
        """Returns an ordered list of documents ordered by their relevance to the provided query

        Args:
            query (str): The search query
            documents (list[str], list[dict]): The documents to rerank
            model (str): The model to use for re-ranking
            top_n (int): (optional) The number of results to return, defaults to returning all results
            max_chunks_per_doc (int): (optional) The maximum number of chunks derived from a document
        """
        parsed_docs = []
        for doc in documents:
            if isinstance(doc, str):
                parsed_docs.append({"text": doc})
            elif isinstance(doc, dict) and "text" in doc:
                parsed_docs.append(doc)
            else:
                raise CohereError(
                    message='invalid format for documents, must be a list of strings or dicts with a "text" key'
                )

        json_body = {
            "query": query,
            "documents": parsed_docs,
            "model": model,
            "top_n": top_n,
            "return_documents": False,
            "max_chunks_per_doc": max_chunks_per_doc,
        }

        reranking = Reranking(self._request(cohere.RERANK_URL, json=json_body))
        for rank in reranking.results:
            rank.document = parsed_docs[rank.index]
        return reranking

    def _check_response(self, json_response: Dict, headers: Dict, status_code: int):
        if "X-API-Warning" in headers:
            logger.warning(headers["X-API-Warning"])
        if "message" in json_response:  # has errors
            raise CohereAPIError(
                message=json_response["message"],
                http_status=status_code,
                headers=headers,
            )
        if 400 <= status_code < 500:
            raise CohereAPIError(
                message=f"Unexpected client error (status {status_code}): {json_response}",
                http_status=status_code,
                headers=headers,
            )
        if status_code >= 500:
            raise CohereError(message=f"Unexpected server error (status {status_code}): {json_response}")

    def _request(self, endpoint, json=None, method="POST", stream=False) -> Any:
        headers = {
            "Authorization": "BEARER {}".format(self.api_key),
            "Content-Type": "application/json",
            "Request-Source": self.request_source,
        }

        url = f"{self.api_url}/{self.api_version}/{endpoint}"
        with requests.Session() as session:
            retries = Retry(
                total=self.max_retries,
                backoff_factor=0.5,
                allowed_methods=["POST", "GET"],
                status_forcelist=cohere.RETRY_STATUS_CODES,
                raise_on_status=False,
            )
            session.mount("https://", HTTPAdapter(max_retries=retries))
            session.mount("http://", HTTPAdapter(max_retries=retries))

            if stream:
                return session.request(method, url, headers=headers, json=json, **self.request_dict, stream=True)

            try:
                response = session.request(
                    method, url, headers=headers, json=json, timeout=self.timeout, **self.request_dict
                )
            except requests.exceptions.ConnectionError as e:
                raise CohereConnectionError(str(e)) from e
            except requests.exceptions.RequestException as e:
                raise CohereError(f"Unexpected exception ({e.__class__.__name__}): {e}") from e

            try:
                json_response = response.json()
            except jsonlib.decoder.JSONDecodeError:  # CohereAPIError will capture status
                raise CohereAPIError.from_response(response, message=f"Failed to decode json body: {response.text}")

            self._check_response(json_response, response.headers, response.status_code)
        return json_response

    def create_cluster_job(
        self,
        embeddings_url: str,
        min_cluster_size: Optional[int] = None,
        n_neighbors: Optional[int] = None,
        is_deterministic: Optional[bool] = None,
        generate_descriptions: Optional[bool] = None,
    ) -> CreateClusterJobResponse:
        """Create clustering job.

        Args:
            embeddings_url (str): File with embeddings to cluster.
            min_cluster_size (Optional[int], optional): Minimum number of elements in a cluster. Defaults to 10.
            n_neighbors (Optional[int], optional): Number of nearest neighbors used by UMAP to establish the
                local structure of the data. Defaults to 15. For more information, please refer to
                https://umap-learn.readthedocs.io/en/latest/parameters.html#n-neighbors
            is_deterministic (Optional[bool], optional): Determines whether the output of the cluster job is
                deterministic. Defaults to True.
            generate_descriptions (Optional[bool], optional): Determines whether to generate cluster descriptions. Defaults to False.

        Returns:
            CreateClusterJobResponse: Created clustering job handler
        """

        json_body = {
            "embeddings_url": embeddings_url,
            "min_cluster_size": min_cluster_size,
            "n_neighbors": n_neighbors,
            "is_deterministic": is_deterministic,
            "generate_descriptions": generate_descriptions,
        }

        response = self._request(cohere.CLUSTER_JOBS_URL, json=json_body)
        return CreateClusterJobResponse.from_dict(
            response,
            wait_fn=self.wait_for_cluster_job,
        )

    def get_cluster_job(
        self,
        job_id: str,
    ) -> ClusterJobResult:
        """Get clustering job results.

        Args:
            job_id (str): Clustering job id.

        Raises:
            ValueError: "job_id" is empty

        Returns:
            ClusterJobResult: Clustering job result.
        """

        if not job_id.strip():
            raise ValueError('"job_id" is empty')

        response = self._request(f"{cohere.CLUSTER_JOBS_URL}/{job_id}", method="GET")

        return ClusterJobResult.from_dict(response)

    def list_cluster_jobs(self) -> List[ClusterJobResult]:
        """List clustering jobs.

        Returns:
            List[ClusterJobResult]: Clustering jobs created.
        """

        response = self._request(cohere.CLUSTER_JOBS_URL, method="GET")
        return [ClusterJobResult.from_dict({"meta": response.get("meta"), **r}) for r in response["jobs"]]

    def wait_for_cluster_job(
        self,
        job_id: str,
        timeout: Optional[float] = None,
        interval: float = 10,
    ) -> ClusterJobResult:
        """Wait for clustering job result.

        Args:
            job_id (str): Clustering job id.
            timeout (Optional[float], optional): Wait timeout in seconds, if None - there is no limit to the wait time.
                Defaults to None.
            interval (float, optional): Wait poll interval in seconds. Defaults to 10.

        Raises:
            TimeoutError: wait timed out

        Returns:
            ClusterJobResult: Clustering job result.
        """

        return wait_for_job(
            get_job=partial(self.get_cluster_job, job_id),
            timeout=timeout,
            interval=interval,
        )

    def create_bulk_embed_job(
        self,
        input_file_url: str,
        model: Optional[str] = None,
        truncate: Optional[str] = None,
        compress: Optional[bool] = None,
        compression_codebook: Optional[str] = None,
        text_field: Optional[str] = None,
        output_format: Optional[str] = None,
    ) -> CreateBulkEmbedJobResponse:
        """Create bulk embed job.

        Args:
            input_file_url (str): File with texts to embed.
            model (Optional[str], optional): The model ID to use for embedding the text. Defaults to None.
            truncate (Optional[str], optional): How the API handles text longer than the maximum token length. Defaults to None.
            compress (Optional[bool], optional): Use embedding compression. Defaults to None.
            compression_codebook (Optional[str], optional): Embedding compression codebook. Defaults to None.
            text_field (Optional[str], optional): Name of the column containing text to embed. Defaults to None.
            output_format (Optional[str], optional): Output format and file extension. Defaults to None.

        Returns:
            CreateBulkEmbedJobResponse: Created bulk embed job handler
        """

        json_body = {
            "input_file_url": input_file_url,
            "model": model,
            "truncate": truncate,
            "compress": compress,
            "compression_codebook": compression_codebook,
            "text_field": text_field,
            "output_format": output_format,
        }

        response = self._request(cohere.BULK_EMBED_JOBS_URL, json=json_body)

        return CreateBulkEmbedJobResponse.from_dict(
            response,
            wait_fn=self.wait_for_bulk_embed_job,
        )

    def list_bulk_embed_jobs(self) -> List[BulkEmbedJob]:
        """List bulk embed jobs.

        Returns:
            List[BulkEmbedJob]: Bulk embed jobs.
        """

        response = self._request(f"{cohere.BULK_EMBED_JOBS_URL}/list", method="GET")
        return [BulkEmbedJob.from_dict({"meta": response.get("meta"), **r}) for r in response["bulk_embed_jobs"]]

    def get_bulk_embed_job(self, job_id: str) -> BulkEmbedJob:
        """Get bulk embed job.

        Args:
            job_id (str): Bulk embed job id.

        Raises:
            ValueError: "job_id" is empty

        Returns:
            BulkEmbedJob: Bulk embed job.
        """

        if not job_id.strip():
            raise ValueError('"job_id" is empty')

        response = self._request(f"{cohere.BULK_EMBED_JOBS_URL}/{job_id}", method="GET")
        return BulkEmbedJob.from_dict(response)

    def cancel_bulk_embed_job(self, job_id: str) -> None:
        """Cancel bulk embed job.

        Args:
            job_id (str): Bulk embed job id.

        Raises:
            ValueError: "job_id" is empty
        """

        if not job_id.strip():
            raise ValueError('"job_id" is empty')

        self._request(f"{cohere.BULK_EMBED_JOBS_URL}/{job_id}/cancel", method="POST", json={})

    def wait_for_bulk_embed_job(
        self,
        job_id: str,
        timeout: Optional[float] = None,
        interval: float = 10,
    ) -> BulkEmbedJob:
        """Wait for bulk embed job completion.

        Args:
            job_id (str): Bulk embed job id.
            timeout (Optional[float], optional): Wait timeout in seconds, if None - there is no limit to the wait time.
                Defaults to None.
            interval (float, optional): Wait poll interval in seconds. Defaults to 10.

        Raises:
            TimeoutError: wait timed out

        Returns:
            BulkEmbedJob: Bulk embed job.
        """

        return wait_for_job(
            get_job=partial(self.get_bulk_embed_job, job_id),
            timeout=timeout,
            interval=interval,
        )

    def create_custom_model(
        self,
        name: str,
        model_type: CUSTOM_MODEL_TYPE,
        dataset: CustomModelDataset,
        hyperparameters: Optional[HyperParametersInput] = None,
    ) -> CustomModel:
        """Create a new custom model

        Args:
            name (str): name of your custom model, has to be unique across your organization
            model_type (GENERATIVE, CLASSIFY, RERANK): type of custom model
            dataset (InMemoryDataset, CsvDataset, JsonlDataset, TextDataset): A dataset for your training. Consists of a train and optional eval file.
            hyperparameters (HyperParametersInput): adjust hyperparameters for your custom model. Only for generative custom models.
        Returns:
            str: the id of the custom model that was created

        Examples:
            prompt completion custom model with csv file
                >>> from cohere.custom_model_dataset import CsvDataset
                >>> co = cohere.Client("YOUR_API_KEY")
                >>> dataset = CsvDataset(train_file="/path/to/your/file.csv", delimiter=",")
                >>> finetune = co.create_custom_model("prompt-completion-ft", dataset=dataset, model_type="GENERATIVE")

            prompt completion custom model with in-memory dataset
                >>> from cohere.custom_model_dataset import InMemoryDataset
                >>> co = cohere.Client("YOUR_API_KEY")
                >>> dataset = InMemoryDataset(training_data=[
                >>>     ("this is the prompt", "and this is the completion"),
                >>>     ("another prompt", "and another completion")
                >>> ])
                >>> finetune = co.create_custom_model("prompt-completion-ft", dataset=dataset, model_type="GENERATIVE")

        """
        internal_custom_model_type = CUSTOM_MODEL_PRODUCT_MAPPING[model_type]
        json = {
            "name": name,
            "settings": {
                "trainFiles": [],
                "evalFiles": [],
                "baseModel": "medium",
                "finetuneType": internal_custom_model_type,
            },
        }
        if hyperparameters:
            json["settings"]["hyperparameters"] = {
                "earlyStoppingPatience": hyperparameters.get("early_stopping_patience"),
                "earlyStoppingThreshold": hyperparameters.get("early_stopping_threshold"),
                "trainBatchSize": hyperparameters.get("train_batch_size"),
                "trainSteps": hyperparameters.get("train_steps"),
                "learningRate": hyperparameters.get("learning_rate"),
            }

        remote_path = self._upload_dataset(
            dataset.get_train_data(), name, dataset.train_file_name(), internal_custom_model_type
        )
        json["settings"]["trainFiles"].append({"path": remote_path, **dataset.file_config()})
        if dataset.has_eval_file():
            remote_path = self._upload_dataset(
                dataset.get_eval_data(), name, dataset.eval_file_name(), internal_custom_model_type
            )
            json["settings"]["evalFiles"].append({"path": remote_path, **dataset.file_config()})

        response = self._request(f"{cohere.CUSTOM_MODEL_URL}/CreateFinetune", method="POST", json=json)
        return CustomModel.from_dict(response["finetune"])

    def _upload_dataset(
        self, content: Iterable[bytes], custom_model_name: str, file_name: str, type: INTERNAL_CUSTOM_MODEL_TYPE
    ) -> str:
        gcs = self._create_signed_url(custom_model_name, file_name, type)
        response = requests.put(gcs["url"], data=content, headers={"content-type": "text/plain"})
        if response.status_code != 200:
            raise CohereError(message=f"Unexpected server error (status {response.status_code}): {response.text}")
        return gcs["gcspath"]

    def _create_signed_url(
        self, custom_model_name: str, file_name: str, type: INTERNAL_CUSTOM_MODEL_TYPE
    ) -> TypedDict("gcsData", {"url": str, "gcspath": str}):
        json = {"finetuneName": custom_model_name, "fileName": file_name, "finetuneType": type}
        return self._request(f"{cohere.CUSTOM_MODEL_URL}/GetFinetuneUploadSignedURL", method="POST", json=json)

    def get_custom_model(self, custom_model_id: str) -> CustomModel:
        """Get a custom model by id.

        Args:
            custom_model_id (str): custom model id
        Returns:
            CustomModel: the custom model
        """
        json = {"finetuneID": custom_model_id}
        response = self._request(f"{cohere.CUSTOM_MODEL_URL}/GetFinetune", method="POST", json=json)
        return CustomModel.from_dict(response["finetune"])

    def get_custom_model_by_name(self, name: str) -> CustomModel:
        """Get a custom model by name.

        Args:
            name (str): custom model name
        Returns:
            CustomModel: the custom model
        """
        json = {"name": name}
        response = self._request(f"{cohere.CUSTOM_MODEL_URL}/GetFinetuneByName", method="POST", json=json)
        return CustomModel.from_dict(response["finetune"])

    def list_custom_models(
        self,
        statuses: Optional[List[CUSTOM_MODEL_STATUS]] = None,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
        order_by: Optional[Literal["asc", "desc"]] = None,
    ) -> List[CustomModel]:
        """List custom models of your organization. Limit is 50.

        Args:
            statuses (CUSTOM_MODEL_STATUS, optional): search for fintunes which are in one of these states
            before (datetime, optional): search for custom models that were created before this timestamp
            after (datetime, optional): search for custom models that were created after this timestamp
            order_by (Literal["asc", "desc"], optional): sort custom models by created at, either asc or desc
        Returns:
            List[CustomModel]: a list of custom models.
        """
        if before:
            before = before.replace(tzinfo=before.tzinfo or timezone.utc)
        if after:
            after = after.replace(tzinfo=after.tzinfo or timezone.utc)

        json = {
            "query": {
                "statuses": statuses,
                "before": before.isoformat(timespec="seconds") if before else None,
                "after": after.isoformat(timespec="seconds") if after else None,
                "orderBy": order_by,
            }
        }

        response = self._request(f"{cohere.CUSTOM_MODEL_URL}/ListFinetunes", method="POST", json=json)
        return [CustomModel.from_dict(r) for r in response["finetunes"]]
