#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# ===========================================================================
#
# This file is adapted from
# https://github.com/abetlen/llama-cpp-python/blob/main/llama_cpp/llama.py
#
# MIT License
#
# Copyright (c) 2023 Andrei Betlen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This would makes sure Python is aware there is more than one sub-package within bigdl,
# physically located elsewhere.
# Otherwise there would be module not found error in non-pip's setting as Python would
# only search the first bigdl package and end up finding only one sub-package.

import os
import sys
import uuid
import time
import math
import multiprocessing
from typing import List, Optional, Union, Generator, Sequence, Iterator, Deque, Tuple
from collections import deque, OrderedDict
from bigdl.llm.utils.common import invalidInputError
from bigdl.llm.ggml.model.generation import GenerationMixin
from . import llama_cpp
from .llama_types import *


class LlamaCache:
    """Cache for a llama.cpp model."""

    def __init__(self, capacity_bytes: int = (2 << 30)):
        self.cache_state: OrderedDict[Tuple[int, ...], "LlamaState"] = OrderedDict()
        self.capacity_bytes = capacity_bytes

    @property
    def cache_size(self):
        return sum([state.llama_state_size for state in self.cache_state.values()])

    def _find_longest_prefix_key(
        self,
        key: Tuple[int, ...],
    ) -> Optional[Tuple[int, ...]]:
        min_len = 0
        min_key = None
        keys = (
            (k, Llama.longest_token_prefix(k, key)) for k in self.cache_state.keys()
        )
        for k, prefix_len in keys:
            if prefix_len > min_len:
                min_len = prefix_len
                min_key = k
        return min_key

    def __getitem__(self, key: Sequence[int]) -> "LlamaState":
        key = tuple(key)
        _key = self._find_longest_prefix_key(key)
        invalidInputError(_key is not None, "Key not found.")
        value = self.cache_state[_key]
        self.cache_state.move_to_end(_key)
        return value

    def __contains__(self, key: Sequence[int]) -> bool:
        return self._find_longest_prefix_key(tuple(key)) is not None

    def __setitem__(self, key: Sequence[int], value: "LlamaState"):
        key = tuple(key)
        if key in self.cache_state:
            del self.cache_state[key]
        self.cache_state[key] = value
        while self.cache_size > self.capacity_bytes:
            self.cache_state.popitem(last=False)


class LlamaState:
    def __init__(
        self,
        eval_tokens: Deque[int],
        eval_logits: Deque[List[float]],
        llama_state,  # type: llama_cpp.Array[llama_cpp.c_uint8]
        llama_state_size: int,
    ):
        self.eval_tokens = eval_tokens
        self.eval_logits = eval_logits
        self.llama_state = llama_state
        self.llama_state_size = llama_state_size


class Llama(GenerationMixin):
    """High-level Python wrapper for a llama.cpp model."""

    def __init__(
        self,
        model_path: str,
        # NOTE: These parameters are likely to change in the future.
        n_ctx: int = 512,
        n_parts: int = -1,
        n_gpu_layers: int = 0,
        seed: int = -1,
        f16_kv: bool = True,
        logits_all: bool = False,
        vocab_only: bool = False,
        use_mmap: bool = False,
        use_mlock: bool = False,
        embedding: bool = False,
        n_threads: Optional[int] = 2,
        n_batch: int = 512,
        last_n_tokens_size: int = 64,
        lora_base: Optional[str] = None,
        lora_path: Optional[str] = None,
        verbose: bool = True,
    ):
        """Load a llama.cpp model from `model_path`.

        Args:
            model_path: Path to the model.
            n_ctx: Maximum context size.
            n_parts: Number of parts to split the model into. If -1, the number of parts
            is automatically determined.
            seed: Random seed. For default value -1, current timestamp is used as seed.
            f16_kv: Use half-precision for key/value cache.
            logits_all: Return logits for all tokens, not just the last token.
            vocab_only: Only load the vocabulary no weights.
            use_mmap: Use mmap if possible.
            use_mlock: Force the system to keep the model in RAM.
            embedding: Embedding mode only.
            n_threads: Number of threads to use. Default to be 2.
            n_batch: Maximum number of prompt tokens to batch together when calling llama_eval.
            last_n_tokens_size: Maximum number of tokens to keep in the last_n_tokens deque.
            lora_base: Optional path to base model, useful if using a quantized base model and
            you want to apply LoRA to an f16 model.
            lora_path: Path to a LoRA file to apply to the model.
            verbose: Print verbose output to stderr.

        Raises:
            ValueError: If the model path does not exist.

        Returns:
            A Llama instance.
        """
        self.verbose = verbose
        self.model_path = model_path

        self.params = llama_cpp.llama_context_default_params()
        self.params.n_ctx = n_ctx
        self.params.n_gpu_layers = n_gpu_layers
        self.params.seed = seed
        self.params.f16_kv = f16_kv
        self.params.logits_all = logits_all
        self.params.vocab_only = vocab_only
        self.params.use_mmap = use_mmap if lora_path is None else False
        self.params.use_mlock = use_mlock
        self.params.embedding = embedding

        self.last_n_tokens_size = last_n_tokens_size
        self.n_batch = min(n_ctx, n_batch)
        self.eval_tokens: Deque[int] = deque(maxlen=n_ctx)
        self.eval_logits: Deque[List[float]] = deque(maxlen=n_ctx if logits_all else 1)

        self.cache: Optional[LlamaCache] = None

        self.n_threads = n_threads

        self.lora_base = lora_base
        self.lora_path = lora_path

        # DEPRECATED
        self.n_parts = n_parts
        # DEPRECATED

        invalidInputError(os.path.exists(model_path), f"Model path does not exist: {model_path}.")

        self.ctx = llama_cpp.llama_init_from_file(
            self.model_path.encode("utf-8"), self.params
        )

        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")

        if self.lora_path:
            if llama_cpp.llama_apply_lora_from_file(
                self.ctx,
                llama_cpp.c_char_p(self.lora_path.encode("utf-8")),
                llama_cpp.c_char_p(self.lora_base.encode("utf-8"))
                if self.lora_base is not None
                else llama_cpp.c_char_p(0),
                llama_cpp.c_int(self.n_threads),
            ):
                invalidInputError(False,
                                  "Failed to apply LoRA from lora path: "
                                  f"{self.lora_path} to base path: {self.lora_base}")

        if self.verbose:
            print(llama_cpp.llama_print_system_info().decode("utf-8"), file=sys.stderr)

        n_vocab = self.n_vocab()
        n_ctx = self.n_ctx()
        data = (llama_cpp.llama_token_data * n_vocab)(
            *[
                llama_cpp.llama_token_data(
                    id=llama_cpp.llama_token(i),
                    logit=llama_cpp.c_float(0.0),
                    p=llama_cpp.c_float(0.0),
                )
                for i in range(n_vocab)
            ]
        )
        size = llama_cpp.c_size_t(n_vocab)
        sorted = False
        candidates = llama_cpp.llama_token_data_array(
            data=data,
            size=size,
            sorted=sorted,
        )
        self._candidates = candidates
        self._token_nl = Llama.token_nl()
        self._token_eos = Llama.token_eos()

    def _tokenize(self, text: bytes, add_bos: bool = True) -> List[int]:
        """Tokenize a string.

        Args:
            text: The utf-8 encoded string to tokenize.

        Raises:
            RuntimeError: If the tokenization failed.

        Returns:
            A list of tokens.
        """
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        n_ctx = llama_cpp.llama_n_ctx(self.ctx)
        tokens = (llama_cpp.llama_token * int(n_ctx))()
        n_tokens = llama_cpp.llama_tokenize(
            self.ctx,
            text,
            tokens,
            llama_cpp.c_int(n_ctx),
            llama_cpp.c_bool(add_bos),
        )
        if int(n_tokens) < 0:
            n_tokens = abs(n_tokens)
            tokens = (llama_cpp.llama_token * int(n_tokens))()
            n_tokens = llama_cpp.llama_tokenize(
                self.ctx,
                text,
                tokens,
                llama_cpp.c_int(n_tokens),
                llama_cpp.c_bool(add_bos),
            )
            invalidInputError(n_tokens >= 0,
                              f'Failed to tokenize: text="{text}" n_tokens={n_tokens}')
        return list(tokens[:n_tokens])

    def detokenize(self, tokens: List[int]) -> bytes:
        """Detokenize a list of tokens.

        Args:
            tokens: The list of tokens to detokenize.

        Returns:
            The detokenized string.
        """
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        output = b""
        for token in tokens:
            output += llama_cpp.llama_token_to_str(
                self.ctx, llama_cpp.llama_token(token)
            )
        return output

    def set_cache(self, cache: Optional[LlamaCache]):
        """Set the cache.

        Args:
            cache: The cache to set.
        """
        self.cache = cache

    def reset(self):
        """Reset the model state."""
        self.eval_tokens.clear()
        self.eval_logits.clear()

    def eval(self, tokens: Sequence[int]):
        """Evaluate a list of tokens.

        Args:
            tokens: The list of tokens to evaluate.
        """
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        n_ctx = int(llama_cpp.llama_n_ctx(self.ctx))
        for i in range(0, len(tokens), self.n_batch):
            batch = tokens[i: min(len(tokens), i + self.n_batch)]
            n_past = min(n_ctx - len(batch), len(self.eval_tokens))
            n_tokens = len(batch)
            return_code = llama_cpp.llama_eval(
                ctx=self.ctx,
                tokens=(llama_cpp.llama_token * len(batch))(*batch),
                n_tokens=llama_cpp.c_int(n_tokens),
                n_past=llama_cpp.c_int(n_past),
                n_threads=llama_cpp.c_int(self.n_threads),
            )
            invalidInputError(int(return_code) == 0, f"llama_eval returned {return_code}.")
            # Save tokens
            self.eval_tokens.extend(batch)
            # Save logits
            rows = n_tokens if self.params.logits_all else 1
            n_vocab = llama_cpp.llama_n_vocab(self.ctx)
            cols = int(n_vocab)
            logits_view = llama_cpp.llama_get_logits(self.ctx)
            logits: List[List[float]] = [
                [logits_view[i * cols + j] for j in range(cols)] for i in range(rows)
            ]
            self.eval_logits.extend(logits)

    def _sample(
        self,
        last_n_tokens_data,  # type: llama_cpp.Array[llama_cpp.llama_token]
        last_n_tokens_size: llama_cpp.c_int,
        top_k: llama_cpp.c_int,
        top_p: llama_cpp.c_float,
        temp: llama_cpp.c_float,
        tfs_z: llama_cpp.c_float,
        repeat_penalty: llama_cpp.c_float,
        frequency_penalty: llama_cpp.c_float,
        presence_penalty: llama_cpp.c_float,
        mirostat_mode: llama_cpp.c_int,
        mirostat_tau: llama_cpp.c_float,
        mirostat_eta: llama_cpp.c_float,
        penalize_nl: bool = True,
    ):
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        invalidInputError(len(self.eval_logits) > 0,
                          "The attribute `eval_logits` of `Llama` object is None.")
        n_vocab = self.n_vocab()
        n_ctx = self.n_ctx()
        top_k = llama_cpp.c_int(n_vocab) if top_k.value <= 0 else top_k
        last_n_tokens_size = (
            llama_cpp.c_int(n_ctx)
            if last_n_tokens_size.value < 0
            else last_n_tokens_size
        )
        logits = self.eval_logits[-1]
        nl_logit = logits[self._token_nl]
        candidates = self._candidates
        llama_cpp.llama_init_candidates(
            ctx=self.ctx,
            candidates=llama_cpp.ctypes.byref(candidates),
        )
        llama_cpp.llama_sample_repetition_penalty(
            ctx=self.ctx,
            last_tokens_data=last_n_tokens_data,
            last_tokens_size=last_n_tokens_size,
            candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
            penalty=repeat_penalty,
        )
        llama_cpp.llama_sample_frequency_and_presence_penalties(
            ctx=self.ctx,
            candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
            last_tokens_data=last_n_tokens_data,
            last_tokens_size=last_n_tokens_size,
            alpha_frequency=frequency_penalty,
            alpha_presence=presence_penalty,
        )
        if not penalize_nl:
            candidates.data[self._token_nl].logit = llama_cpp.c_float(nl_logit)
        if temp.value == 0.0:
            return llama_cpp.llama_sample_token_greedy(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
            )
        elif mirostat_mode.value == 1:
            mirostat_mu = llama_cpp.c_float(2.0 * mirostat_tau.value)
            mirostat_m = llama_cpp.c_int(100)
            llama_cpp.llama_sample_temperature(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                temp=temp,
            )
            return llama_cpp.llama_sample_token_mirostat(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                tau=mirostat_tau,
                eta=mirostat_eta,
                mu=llama_cpp.ctypes.byref(mirostat_mu),  # type: ignore
                m=mirostat_m,
            )
        elif mirostat_mode.value == 2:
            mirostat_mu = llama_cpp.c_float(2.0 * mirostat_tau.value)
            llama_cpp.llama_sample_temperature(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.pointer(candidates),
                temp=temp,
            )
            return llama_cpp.llama_sample_token_mirostat_v2(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                tau=mirostat_tau,
                eta=mirostat_eta,
                mu=llama_cpp.ctypes.byref(mirostat_mu),  # type: ignore
            )
        else:
            llama_cpp.llama_sample_top_k(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                k=top_k,
                min_keep=llama_cpp.c_size_t(1),
            )
            llama_cpp.llama_sample_tail_free(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                z=tfs_z,
                min_keep=llama_cpp.c_size_t(1),
            )
            llama_cpp.llama_sample_typical(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                p=llama_cpp.c_float(1.0),
                min_keep=llama_cpp.c_size_t(1),
            )
            llama_cpp.llama_sample_top_p(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                p=top_p,
                min_keep=llama_cpp.c_size_t(1),
            )
            llama_cpp.llama_sample_temperature(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
                temp=temp,
            )
            return llama_cpp.llama_sample_token(
                ctx=self.ctx,
                candidates=llama_cpp.ctypes.byref(candidates),  # type: ignore
            )

    def sample(
        self,
        top_k: int = 40,
        top_p: float = 0.95,
        temp: float = 0.80,
        repeat_penalty: float = 1.1,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_eta: float = 0.1,
        mirostat_tau: float = 5.0,
        penalize_nl: bool = True,
    ):
        """Sample a token from the model.

        Args:
            top_k: The top-k sampling parameter.
            top_p: The top-p sampling parameter.
            temp: The temperature parameter.
            repeat_penalty: The repeat penalty parameter.

        Returns:
            The sampled token.
        """
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        last_n_tokens_data = [llama_cpp.llama_token(0)] * max(
            0, self.last_n_tokens_size - len(self.eval_tokens)
        ) + list(self.eval_tokens)[-self.last_n_tokens_size:]
        return self._sample(
            last_n_tokens_data=(llama_cpp.llama_token * self.last_n_tokens_size)(
                *last_n_tokens_data
            ),
            last_n_tokens_size=llama_cpp.c_int(self.last_n_tokens_size),
            top_k=llama_cpp.c_int(top_k),
            top_p=llama_cpp.c_float(top_p),
            temp=llama_cpp.c_float(temp),
            tfs_z=llama_cpp.c_float(tfs_z),
            repeat_penalty=llama_cpp.c_float(repeat_penalty),
            frequency_penalty=llama_cpp.c_float(frequency_penalty),
            presence_penalty=llama_cpp.c_float(presence_penalty),
            mirostat_mode=llama_cpp.c_int(mirostat_mode),
            mirostat_tau=llama_cpp.c_float(mirostat_tau),
            mirostat_eta=llama_cpp.c_float(mirostat_eta),
            penalize_nl=penalize_nl,
        )

    def _generate(
        self,
        tokens: Sequence[int],
        top_k: int = 40,
        top_p: float = 0.95,
        temp: float = 0.80,
        repeat_penalty: float = 1.1,
        reset: bool = True,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
    ) -> Generator[int, Optional[Sequence[int]], None]:
        """Create a generator of tokens from a prompt.

        Examples:
            >>> llama = Llama("models/ggml-7b.bin")
            >>> tokens = llama.tokenize(b"Hello, world!")
            >>> for token in llama.generate(tokens, top_k=40, top_p=0.95,
            >>>                             temp=1.0, repeat_penalty=1.1):
            ...     print(llama.detokenize([token]))

        Args:
            tokens: The prompt tokens.
            top_k: The top-k sampling parameter.
            top_p: The top-p sampling parameter.
            temp: The temperature parameter.
            repeat_penalty: The repeat penalty parameter.
            reset: Whether to reset the model state.

        Yields:
            The generated tokens.
        """
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")

        if reset and len(self.eval_tokens) > 0:
            longest_prefix = 0
            for a, b in zip(self.eval_tokens, tokens[:-1]):
                if a == b:
                    longest_prefix += 1
                else:
                    break
            if longest_prefix > 0:
                if self.verbose:
                    print("Llama.generate: prefix-match hit", file=sys.stderr)
                reset = False
                tokens = tokens[longest_prefix:]
                for _ in range(len(self.eval_tokens) - longest_prefix):
                    self.eval_tokens.pop()
                    try:
                        self.eval_logits.pop()
                    except IndexError:
                        pass

        if reset:
            self.reset()

        while True:
            self.eval(tokens)
            token = self.sample(
                top_k=top_k,
                top_p=top_p,
                temp=temp,
                repeat_penalty=repeat_penalty,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                tfs_z=tfs_z,
                mirostat_mode=mirostat_mode,
                mirostat_tau=mirostat_tau,
                mirostat_eta=mirostat_eta,
            )
            tokens_or_none = yield token
            tokens = [token]
            if tokens_or_none is not None:
                tokens.extend(tokens_or_none)

    def create_embedding(
        self, input: Union[str, List[str]], model: Optional[str] = None
    ) -> Embedding:
        """Embed a string.

        Args:
            input: The utf-8 encoded string to embed.

        Returns:
            An embedding object.
        """
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        model_name: str = model if model is not None else self.model_path

        invalidInputError(self.params.embedding,
                          "Llama model must be created with embedding=True to call this method.")

        if self.verbose:
            llama_cpp.llama_reset_timings(self.ctx)

        if isinstance(input, str):
            inputs = [input]
        else:
            inputs = input

        data: List[EmbeddingData] = []
        total_tokens = 0
        for index, input in enumerate(inputs):
            tokens = self.tokenize(input.encode("utf-8"))
            self.reset()
            self.eval(tokens)
            n_tokens = len(tokens)
            total_tokens += n_tokens
            embedding = llama_cpp.llama_get_embeddings(self.ctx)[
                : llama_cpp.llama_n_embd(self.ctx)
            ]

            data.append(
                {
                    "object": "embedding",
                    "embedding": embedding,
                    "index": index,
                }
            )
        if self.verbose:
            llama_cpp.llama_print_timings(self.ctx)

        return {
            "object": "list",
            "data": data,
            "model": model_name,
            "usage": {
                "prompt_tokens": total_tokens,
                "total_tokens": total_tokens,
            },
        }

    def embed(self, input: str) -> List[float]:
        """Embed a string.

        Args:
            input: The utf-8 encoded string to embed.

        Returns:
            A list of embeddings
        """
        return list(map(float, self.create_embedding(input)["data"][0]["embedding"]))

    def _create_completion(
        self,
        prompt: str,
        suffix: Optional[str] = None,
        max_tokens: int = 16,
        temperature: float = 0.8,
        top_p: float = 0.95,
        logprobs: Optional[int] = None,
        echo: bool = False,
        stop: Optional[Union[str, List[str]]]=[],
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        repeat_penalty: float = 1.1,
        top_k: int = 40,
        stream: bool = False,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
        model: Optional[str] = None,
    ) -> Union[Iterator[Completion], Iterator[CompletionChunk]]:
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        completion_id: str = f"cmpl-{str(uuid.uuid4())}"
        created: int = int(time.time())
        completion_tokens: List[int] = []
        # Add blank space to start of prompt to match OG llama tokenizer
        prompt_tokens: List[int] = self.tokenize(b" " + prompt.encode("utf-8"))
        text: bytes = b""
        returned_tokens: int = 0
        stop = (
            stop if isinstance(stop, list) else [stop] if isinstance(stop, str) else []
        )
        model_name: str = model if model is not None else self.model_path

        if self.verbose:
            llama_cpp.llama_reset_timings(self.ctx)

        invalidInputError(len(prompt_tokens) + max_tokens <= int(llama_cpp.llama_n_ctx(self.ctx)),
                          "Requested tokens exceed context window of "
                          f"{llama_cpp.llama_n_ctx(self.ctx)}.")

        if stop != []:
            stop_sequences = [s.encode("utf-8") for s in stop]
        else:
            stop_sequences = []

        if logprobs is not None and self.params.logits_all is False:
            invalidInputError(False,
                              "logprobs is not supported for models created with logits_all=False")

        if self.cache:
            try:
                cache_item = self.cache[prompt_tokens]
                cache_prefix_len = Llama.longest_token_prefix(
                    cache_item.eval_tokens, prompt_tokens
                )
                eval_prefix_len = Llama.longest_token_prefix(
                    self.eval_tokens, prompt_tokens
                )
                if cache_prefix_len > eval_prefix_len:
                    self.load_state(cache_item)
                    if self.verbose:
                        print("Llama._create_completion: cache hit", file=sys.stderr)
            except KeyError:
                if self.verbose:
                    print("Llama._create_completion: cache miss", file=sys.stderr)

        finish_reason = "length"
        multibyte_fix = 0
        for token in self._generate(
            prompt_tokens,
            top_k=top_k,
            top_p=top_p,
            temp=temperature,
            tfs_z=tfs_z,
            mirostat_mode=mirostat_mode,
            mirostat_tau=mirostat_tau,
            mirostat_eta=mirostat_eta,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repeat_penalty=repeat_penalty,
        ):
            if token == self._token_eos:
                text = self.detokenize(completion_tokens)
                finish_reason = "stop"
                break

            completion_tokens.append(token)

            all_text = self.detokenize(completion_tokens)

            # Contains multi-byte UTF8
            for k, char in enumerate(all_text[-3:]):
                k = 3 - k
                for num, pattern in [(2, 192), (3, 224), (4, 240)]:
                    # Bitwise AND check
                    if num > k and pattern & char == pattern:
                        multibyte_fix = num - k

            # Stop incomplete bytes from passing
            if multibyte_fix > 0:
                multibyte_fix -= 1
                continue

            any_stop = [s for s in stop_sequences if s in all_text]
            if len(any_stop) > 0:
                first_stop = any_stop[0]
                text = all_text[: all_text.index(first_stop)]
                finish_reason = "stop"
                break

            if stream:
                # We want to avoid yielding any characters from
                # the generated text if they are part of a stop
                # sequence.
                first_stop_position = 0
                for s in stop_sequences:
                    for i in range(len(s), 0, -1):
                        if all_text.endswith(s[:i]):
                            if i > first_stop_position:
                                first_stop_position = i
                            break

                token_end_position = 0
                remaining_tokens = completion_tokens[returned_tokens:]
                remaining_length = len(self.detokenize(remaining_tokens))
                for token in remaining_tokens:
                    token_end_position += len(self.detokenize([token]))
                    # Check if stop sequence is in the token
                    if token_end_position >= (
                        remaining_length - first_stop_position - 1
                    ):
                        break
                    logprobs_or_none: Optional[CompletionLogprobs] = None
                    if logprobs is not None:
                        token_str = self.detokenize([token]).decode(
                            "utf-8", errors="ignore"
                        )
                        text_offset = len(prompt) + len(
                            self.detokenize(completion_tokens[:returned_tokens])
                        )
                        token_offset = len(prompt_tokens) + returned_tokens
                        logits = self.eval_logits[token_offset - 1]
                        current_logprobs = Llama.logits_to_logprobs(logits)
                        sorted_logprobs = list(
                            sorted(
                                zip(current_logprobs, range(len(current_logprobs))),
                                reverse=True,
                            )
                        )
                        top_logprob = {
                            self.detokenize([i]).decode(
                                "utf-8", errors="ignore"
                            ): logprob
                            for logprob, i in sorted_logprobs[:logprobs]
                        }
                        top_logprob.update({token_str: current_logprobs[int(token)]})
                        logprobs_or_none = {
                            "tokens": [
                                self.detokenize([token]).decode(
                                    "utf-8", errors="ignore"
                                )
                            ],
                            "text_offset": [text_offset],
                            "token_logprobs": [sorted_logprobs[int(token)][0]],
                            "top_logprobs": [top_logprob],
                        }
                    returned_tokens += 1
                    yield {
                        "id": completion_id,
                        "object": "text_completion",
                        "created": created,
                        "model": model_name,
                        "choices": [
                            {
                                "text": self.detokenize([token]).decode(
                                    "utf-8", errors="ignore"
                                ),
                                "index": 0,
                                "logprobs": logprobs_or_none,
                                "finish_reason": None,
                            }
                        ],
                        "usage": {
                            "prompt_tokens": len(prompt_tokens),
                        },
                    }

            if len(completion_tokens) >= max_tokens:
                text = self.detokenize(completion_tokens)
                finish_reason = "length"
                break

        if self.cache:
            if self.verbose:
                print("Llama._create_completion: cache save", file=sys.stderr)
            self.cache[prompt_tokens + completion_tokens] = self.save_state()

        if self.verbose:
            llama_cpp.llama_print_timings(self.ctx)

        if stream:
            remaining_tokens = completion_tokens[returned_tokens:]
            all_text = self.detokenize(remaining_tokens)
            any_stop = [s for s in stop_sequences if s in all_text]
            if len(any_stop) > 0:
                end = min(all_text.index(stop) for stop in any_stop)
            else:
                end = len(all_text)

            token_end_position = 0
            for token in remaining_tokens:
                token_end_position += len(self.detokenize([token]))

                logprobs_or_none: Optional[CompletionLogprobs] = None
                if logprobs is not None:
                    token_str = self.detokenize([token]).decode(
                        "utf-8", errors="ignore"
                    )
                    text_offset = len(prompt) + len(
                        self.detokenize(completion_tokens[:returned_tokens])
                    )
                    token_offset = len(prompt_tokens) + returned_tokens - 1
                    logits = self.eval_logits[token_offset]
                    current_logprobs = Llama.logits_to_logprobs(logits)
                    sorted_logprobs = list(
                        sorted(
                            zip(current_logprobs, range(len(current_logprobs))),
                            reverse=True,
                        )
                    )
                    top_logprob = {
                        self.detokenize([i]).decode("utf-8", errors="ignore"): logprob
                        for logprob, i in sorted_logprobs[:logprobs]
                    }
                    top_logprob.update({token_str: current_logprobs[int(token)]})
                    logprobs_or_none = {
                        "tokens": [
                            self.detokenize([token]).decode("utf-8", errors="ignore")
                        ],
                        "text_offset": [text_offset],
                        "token_logprobs": [sorted_logprobs[int(token)][0]],
                        "top_logprobs": [top_logprob],
                    }

                if token_end_position >= end:
                    last_text = self.detokenize([token])
                    if token_end_position == end - 1:
                        break
                    returned_tokens += 1
                    yield {
                        "id": completion_id,
                        "object": "text_completion",
                        "created": created,
                        "model": model_name,
                        "choices": [
                            {
                                "text": last_text[
                                    : len(last_text) - (token_end_position - end)
                                ].decode("utf-8", errors="ignore"),
                                "index": 0,
                                "logprobs": logprobs_or_none,
                                "finish_reason": finish_reason,
                            }
                        ],
                        "usage": {
                            "prompt_tokens": len(prompt_tokens),
                        },
                    }
                    break
                returned_tokens += 1
                yield {
                    "id": completion_id,
                    "object": "text_completion",
                    "created": created,
                    "model": model_name,
                    "choices": [
                        {
                            "text": self.detokenize([token]).decode(
                                "utf-8", errors="ignore"
                            ),
                            "index": 0,
                            "logprobs": logprobs_or_none,
                            "finish_reason": finish_reason
                            if returned_tokens == len(completion_tokens)
                            else None,
                        }
                    ],
                    "usage": {
                        "prompt_tokens": len(prompt_tokens),
                    },
                }
            return

        text_str = text.decode("utf-8", errors="ignore")

        if echo:
            text_str = prompt + text_str

        if suffix is not None:
            text_str = text_str + suffix

        logprobs_or_none: Optional[CompletionLogprobs] = None
        if logprobs is not None:
            text_offset = 0 if echo else len(prompt)
            token_offset = 0 if echo else len(prompt_tokens[1:])
            text_offsets: List[int] = []
            token_logprobs: List[Optional[float]] = []
            tokens: List[str] = []
            top_logprobs: List[Optional[Dict[str, float]]] = []

            if echo:
                # Remove leading BOS token
                all_tokens = prompt_tokens[1:] + completion_tokens
            else:
                all_tokens = completion_tokens

            all_token_strs = [
                self.detokenize([token]).decode("utf-8", errors="ignore")
                for token in all_tokens
            ]
            all_logprobs = [
                Llama.logits_to_logprobs(list(map(float, row)))
                for row in self.eval_logits
            ][token_offset:]
            for token, token_str, logprobs_token in zip(
                all_tokens, all_token_strs, all_logprobs
            ):
                text_offsets.append(text_offset)
                text_offset += len(token_str)
                tokens.append(token_str)
                sorted_logprobs = list(
                    sorted(
                        zip(logprobs_token, range(len(logprobs_token))), reverse=True
                    )
                )
                token_logprobs.append(sorted_logprobs[int(token)][0])
                top_logprob: Optional[Dict[str, float]] = {
                    self.detokenize([i]).decode("utf-8", errors="ignore"): logprob
                    for logprob, i in sorted_logprobs[:logprobs]
                }
                top_logprob.update({token_str: logprobs_token[int(token)]})
                top_logprobs.append(top_logprob)
            # Weird idosincracy of the OpenAI API where
            # token_logprobs and top_logprobs are null for
            # the first token.
            if echo and len(all_tokens) > 0:
                token_logprobs[0] = None
                top_logprobs[0] = None
            logprobs_or_none = {
                "tokens": tokens,
                "text_offset": text_offsets,
                "token_logprobs": token_logprobs,
                "top_logprobs": top_logprobs,
            }

        yield {
            "id": completion_id,
            "object": "text_completion",
            "created": created,
            "model": model_name,
            "choices": [
                {
                    "text": text_str,
                    "index": 0,
                    "logprobs": logprobs_or_none,
                    "finish_reason": finish_reason,
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt_tokens),
                "completion_tokens": len(completion_tokens),
                "total_tokens": len(prompt_tokens) + len(completion_tokens),
            },
        }

    def create_completion(
        self,
        prompt: str,
        suffix: Optional[str] = None,
        max_tokens: int = 128,
        temperature: float = 0.8,
        top_p: float = 0.95,
        logprobs: Optional[int] = None,
        echo: bool = False,
        stop: Optional[Union[str, List[str]]]=[],
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        repeat_penalty: float = 1.1,
        top_k: int = 40,
        stream: bool = False,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
        model: Optional[str] = None,
    ) -> Union[Completion, Iterator[CompletionChunk]]:
        """Generate text from a prompt.

        Args:
            prompt: The prompt to generate text from.
            suffix: A suffix to append to the generated text. If None, no suffix is appended.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature to use for sampling.
            top_p: The top-p value to use for sampling.
            logprobs: The number of logprobs to return. If None, no logprobs are returned.
            echo: Whether to echo the prompt.
            stop: A list of strings to stop generation when encountered.
            repeat_penalty: The penalty to apply to repeated tokens.
            top_k: The top-k value to use for sampling.
            stream: Whether to stream the results.

        Raises:
            ValueError: If the requested tokens exceed the context window.
            RuntimeError: If the prompt fails to tokenize or the model fails to evaluate the prompt.

        Returns:
            Response object containing the generated text.
        """
        completion_or_chunks = self._create_completion(
            prompt=prompt,
            suffix=suffix,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            logprobs=logprobs,
            echo=echo,
            stop=stop,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repeat_penalty=repeat_penalty,
            top_k=top_k,
            stream=stream,
            tfs_z=tfs_z,
            mirostat_mode=mirostat_mode,
            mirostat_tau=mirostat_tau,
            mirostat_eta=mirostat_eta,
            model=model,
        )
        if stream:
            chunks: Iterator[CompletionChunk] = completion_or_chunks
            return chunks
        completion: Completion = next(completion_or_chunks)  # type: ignore
        return completion

    def __call__(
        self,
        prompt: str,
        suffix: Optional[str] = None,
        max_tokens: int = 128,
        temperature: float = 0.8,
        top_p: float = 0.95,
        logprobs: Optional[int] = None,
        echo: bool = False,
        stop: Optional[Union[str, List[str]]]=[],
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        repeat_penalty: float = 1.1,
        top_k: int = 40,
        stream: bool = False,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
        model: Optional[str] = None,
    ) -> Union[Completion, Iterator[CompletionChunk]]:
        """Generate text from a prompt.

        Args:
            prompt: The prompt to generate text from.
            suffix: A suffix to append to the generated text. If None, no suffix is appended.
            max_tokens: The maximum number of tokens to generate.
            temperature: The temperature to use for sampling.
            top_p: The top-p value to use for sampling.
            logprobs: The number of logprobs to return. If None, no logprobs are returned.
            echo: Whether to echo the prompt.
            stop: A list of strings to stop generation when encountered.
            repeat_penalty: The penalty to apply to repeated tokens.
            top_k: The top-k value to use for sampling.
            stream: Whether to stream the results.

        Raises:
            ValueError: If the requested tokens exceed the context window.
            RuntimeError: If the prompt fails to tokenize or the model fails to evaluate the prompt.

        Returns:
            Response object containing the generated text.
        """
        return self.create_completion(
            prompt=prompt,
            suffix=suffix,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            logprobs=logprobs,
            echo=echo,
            stop=stop,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            repeat_penalty=repeat_penalty,
            top_k=top_k,
            stream=stream,
            tfs_z=tfs_z,
            mirostat_mode=mirostat_mode,
            mirostat_tau=mirostat_tau,
            mirostat_eta=mirostat_eta,
            model=model,
        )

    def _convert_text_completion_to_chat(
        self, completion: Completion
    ) -> ChatCompletion:
        return {
            "id": "chat" + completion["id"],
            "object": "chat.completion",
            "created": completion["created"],
            "model": completion["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": completion["choices"][0]["text"],
                    },
                    "finish_reason": completion["choices"][0]["finish_reason"],
                }
            ],
            "usage": completion["usage"],
        }

    def _convert_text_completion_chunks_to_chat(
        self,
        chunks: Iterator[CompletionChunk],
    ) -> Iterator[ChatCompletionChunk]:
        for i, chunk in enumerate(chunks):
            if i == 0:
                yield {
                    "id": "chat" + chunk["id"],
                    "model": chunk["model"],
                    "created": chunk["created"],
                    "object": "chat.completion.chunk",
                    "choices": [
                        {
                            "index": 0,
                            "delta": {
                                "role": "assistant",
                            },
                            "finish_reason": None,
                        }
                    ],
                }
            yield {
                "id": "chat" + chunk["id"],
                "model": chunk["model"],
                "created": chunk["created"],
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "content": chunk["choices"][0]["text"],
                        },
                        "finish_reason": chunk["choices"][0]["finish_reason"],
                    }
                ],
            }

    def create_chat_completion(
        self,
        messages: List[ChatCompletionMessage],
        temperature: float = 0.2,
        top_p: float = 0.95,
        top_k: int = 40,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]]=[],
        max_tokens: int = 256,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        repeat_penalty: float = 1.1,
        tfs_z: float = 1.0,
        mirostat_mode: int = 0,
        mirostat_tau: float = 5.0,
        mirostat_eta: float = 0.1,
        model: Optional[str] = None,
    ) -> Union[ChatCompletion, Iterator[ChatCompletionChunk]]:
        """Generate a chat completion from a list of messages.

        Args:
            messages: A list of messages to generate a response for.
            temperature: The temperature to use for sampling.
            top_p: The top-p value to use for sampling.
            top_k: The top-k value to use for sampling.
            stream: Whether to stream the results.
            stop: A list of strings to stop generation when encountered.
            max_tokens: The maximum number of tokens to generate.
            repeat_penalty: The penalty to apply to repeated tokens.

        Returns:
            Generated chat completion or a stream of chat completion chunks.
        """
        stop = (
            stop if isinstance(stop, list) else [stop] if isinstance(stop, str) else []
        )
        chat_history = "".join(
            f'### {"Human" if message["role"] == "user" else "Assistant"}:{message["content"]}'
            for message in messages
        )
        PROMPT = chat_history + "### Assistant:"
        PROMPT_STOP = ["### Assistant:", "### Human:"]
        completion_or_chunks = self(
            prompt=PROMPT,
            stop=PROMPT_STOP + stop,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stream=stream,
            max_tokens=max_tokens,
            repeat_penalty=repeat_penalty,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            tfs_z=tfs_z,
            mirostat_mode=mirostat_mode,
            mirostat_tau=mirostat_tau,
            mirostat_eta=mirostat_eta,
            model=model,
        )
        if stream:
            chunks: Iterator[CompletionChunk] = completion_or_chunks  # type: ignore
            return self._convert_text_completion_chunks_to_chat(chunks)
        else:
            completion: Completion = completion_or_chunks  # type: ignore
            return self._convert_text_completion_to_chat(completion)

    def __del__(self):
        if self.ctx is not None:
            llama_cpp.llama_free(self.ctx)
            self.ctx = None

    def __getstate__(self):
        return dict(
            verbose=self.verbose,
            model_path=self.model_path,
            n_ctx=self.params.n_ctx,
            n_gpu_layers=self.params.n_gpu_layers,
            seed=self.params.seed,
            f16_kv=self.params.f16_kv,
            logits_all=self.params.logits_all,
            vocab_only=self.params.vocab_only,
            use_mmap=self.params.use_mmap,
            use_mlock=self.params.use_mlock,
            embedding=self.params.embedding,
            last_n_tokens_size=self.last_n_tokens_size,
            n_batch=self.n_batch,
            n_threads=self.n_threads,
            lora_base=self.lora_base,
            lora_path=self.lora_path,
            # DEPRECATED
            n_parts=self.n_parts,
            # DEPRECATED
        )

    def __setstate__(self, state):
        self.__init__(
            model_path=state["model_path"],
            n_ctx=state["n_ctx"],
            n_parts=state["n_parts"],
            n_gpu_layers=state["n_gpu_layers"],
            seed=state["seed"],
            f16_kv=state["f16_kv"],
            logits_all=state["logits_all"],
            vocab_only=state["vocab_only"],
            use_mmap=state["use_mmap"],
            use_mlock=state["use_mlock"],
            embedding=state["embedding"],
            n_threads=state["n_threads"],
            n_batch=state["n_batch"],
            last_n_tokens_size=state["last_n_tokens_size"],
            lora_base=state["lora_base"],
            lora_path=state["lora_path"],
            verbose=state["verbose"],
        )

    def save_state(self) -> LlamaState:
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        state_size = llama_cpp.llama_get_state_size(self.ctx)
        llama_state = (llama_cpp.c_uint8 * int(state_size))()
        n_bytes = llama_cpp.llama_copy_state_data(self.ctx, llama_state)
        invalidInputError(int(n_bytes) <= int(state_size), "Failed to copy llama state data.")
        llama_state_compact = (llama_cpp.c_uint8 * int(n_bytes))()
        llama_cpp.ctypes.memmove(llama_state_compact, llama_state, int(n_bytes))
        if self.verbose:
            print(
                f"Llama.save_state: saving {n_bytes} bytes of llama state",
                file=sys.stderr,
            )
        return LlamaState(
            eval_tokens=self.eval_tokens.copy(),
            eval_logits=self.eval_logits.copy(),
            llama_state=llama_state_compact,
            llama_state_size=n_bytes,
        )

    def load_state(self, state: LlamaState) -> None:
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        self.eval_tokens = state.eval_tokens.copy()
        self.eval_logits = state.eval_logits.copy()
        state_size = state.llama_state_size
        invalidInputError(llama_cpp.llama_set_state_data(self.ctx,
                                                         state.llama_state) == state_size,
                          "Failed to set llama state data.")

    def n_ctx(self) -> int:
        """Return the context window size."""
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        return llama_cpp.llama_n_ctx(self.ctx)

    def n_embd(self) -> int:
        """Return the embedding size."""
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        return llama_cpp.llama_n_embd(self.ctx)

    def n_vocab(self) -> int:
        """Return the vocabulary size."""
        invalidInputError(self.ctx is not None, "The attribute `ctx` of `Llama` object is None.")
        return llama_cpp.llama_n_vocab(self.ctx)

    @staticmethod
    def token_eos() -> int:
        """Return the end-of-sequence token."""
        return llama_cpp.llama_token_eos()

    @staticmethod
    def token_bos() -> int:
        """Return the beginning-of-sequence token."""
        return llama_cpp.llama_token_bos()

    @staticmethod
    def token_nl() -> int:
        """Return the newline token."""
        return llama_cpp.llama_token_nl()

    @staticmethod
    def logits_to_logprobs(logits: List[float]) -> List[float]:
        exps = [math.exp(float(x)) for x in logits]
        sum_exps = sum(exps)
        return [math.log(x / sum_exps) for x in exps]

    @staticmethod
    def longest_token_prefix(a: Sequence[int], b: Sequence[int]):
        longest_prefix = 0
        for _a, _b in zip(a, b):
            if _a == _b:
                longest_prefix += 1
            else:
                break
        return longest_prefix
