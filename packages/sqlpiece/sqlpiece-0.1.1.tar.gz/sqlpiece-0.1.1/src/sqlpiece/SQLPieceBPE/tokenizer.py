# coding=utf-8
# Copyright 2018 The Open AI Team Authors and The HuggingFace Inc. team.
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
"""Tokenization class for MorphPieceBPE"""

import pickle
from typing import List, Optional
import regex as re
from transformers import GPT2Tokenizer
from transformers.utils import logging
from pathlib import Path

logger = logging.get_logger(__name__)
path = Path(__file__).parent

class SQLPieceBPE(GPT2Tokenizer):
    r""" Construct a SQLPieceBPE tokenizer. Based on BPE, but uses a split vocabulary paradigm to tokenize SQL statements. For more information, please refer to the `MorphPiece paper <https://arxiv.org/abs/xxx.xxx>`.

    This tokenizer inherits from [`GPT2Tokenizer`] which contains all the methods, except _tokenize() function, which implements the MorphPiece tokenization for WordPiece. Users should refer to this superclass for more information regarding those methods.

    Attention : Please do NOT use .from_pretrained() method as it will override the custom vocabularies. Instead instentiate the class without any arguments to load the default vocabularies.

    Args:
        All arguments are the same as GPT2Tokenizer except for the following additional argument:
        morpheme_file (`Path`):
            Path to a pickled file which has both the morpheme vocabulary and lookup table.
        
        The original 'vocab_file' and 'merges_file' arguments now point to a custom vocabulary and merges which takes into account the morpheme vocabulary.

    Example:
    ```
    >>> from sqlpiece import SQLPieceBPE
    >>> tokenizer = SQLPieceBPE()
    >>> tokenizer.tokenize("SELECT name FROM students WHERE age > 10")
    ['SELECT', 'name', 'FROM', 'stud', 'ents', 'WHERE', 'age', '>', '10']
    ```

    """
    def __init__(
        self,
        vocab_file=None,
        merges_file=None,
        sql_vocab_file=None,
        ver=1.0,
        errors="replace",
        unk_token="<UNK>",
        bos_token="<BOS>",
        eos_token="<EOS>",
        pad_token="<PAD>",
        add_prefix_space=False,
        add_bos_token=False,
        **kwargs
    ):
        if sql_vocab_file is None:
            if ver==1.0:
                sql_vocab_file = path/'vocab/sql_vocab.pkl'
                vocab_file = path/'vocab/vocab.json'
                merges_file = path/'vocab/merges.txt'
        super().__init__(
        vocab_file,
        merges_file,
        errors,
        unk_token,
        bos_token,
        eos_token,
        pad_token,
        add_prefix_space,
        add_bos_token,
        **kwargs
        )
        
        self.sql_vocab = pickle.load(open(sql_vocab_file,'rb'))
        self.counter_sql = dict.fromkeys(self.sql_vocab,0)   
        self.counter_bpe = dict()   
        self.counter_token = dict()

        special_tokens_dict = {
                               "cls_token": "<CLS>",
                               "sep_token": "<SEP>",
                               "mask_token": "<MASK>",
                            #    "pad_token": "<PAD>",
                            #    "unk_token": "<UNK>",
                            #    "bos_token": "<BOS>",
                            #    "eos_token": "<EOS>",
                               }

        self.add_special_tokens(special_tokens_dict)   

    def get_byte_encoding(self,token):
        return "".join(
            self.byte_encoder[b] for b in token.encode("utf-8")
        )  # Maps all our bytes to unicode strings, avoiding control tokens of the BPE (spaces in our case)
        
    def _get_bpe(self,token):
        byte_encoded_token = self.get_byte_encoding(token)
        return [bpe_token for bpe_token in self.bpe(byte_encoded_token).split(" ")]
        
    def reset_counters(self):
        self.counter_sql = dict.fromkeys(self.sql_vocab,0)
        self.counter_bpe = dict()
        self.counter_token = dict()

    def increment_counter(self,counter,token):
        if token in counter:
            counter[token]+=1
        else:
            counter[token]=1
    
    def _tokenize(self, text):
        """Tokenize a string."""
        all_tokens = []
        self.token_type_ids = []
        pretokens = text.split() # SQL statements are first split by space.
        
        for token in pretokens:
            self.increment_counter(self.counter_token,token)
            if token.upper() in self.sql_vocab:
                self.increment_counter(self.counter_sql,token.upper())
                all_tokens.append(token)
                self.token_type_ids.append(0)
            else:
                bpe_pretokens = re.findall(self.pat, token) # and then split by bpe regex

                for token in bpe_pretokens:
                    self.increment_counter(self.counter_bpe,token)
                    bpe_tokens = self._get_bpe(token)
                    all_tokens.extend(bpe_tokens)
                    self.token_type_ids.extend([1]*len(bpe_tokens))
        
        return all_tokens
    
    def _convert_bpe_tokens_to_string(self, tokens):
        """Converts a sequence of BPE tokens (string) in a single string."""
        text = "".join(tokens)
        text = bytearray([self.byte_decoder[c] for c in text]).decode("utf-8", errors=self.errors)
        return text

    def from_pretrained(self,x):
        raise NotImplementedError("Please do not use from_pretrained() method for MorphPieceBPE. Instead, instantiate the class without any arguments to load the default vocabularies.")
    
    def _encode_plus(self, *args, **kwargs):
        kwargs['return_token_type_ids'] = True
        return super()._encode_plus(*args, **kwargs)
    
    def _batch_encode_plus(self, *args, **kwargs):
        kwargs['return_token_type_ids'] = True
        return super()._batch_encode_plus(*args, **kwargs)
    
    def create_token_type_ids_from_sequences(
        self, token_ids_0: List[int], token_ids_1: Optional[List[int]] = None
    ) -> List[int]:

        if token_ids_1 is not None:
            return NotImplemented("This tokenizer determines token_type_ids for only 1 sequence.")
        return self.token_type_ids
        # return [1] * self.token_type_ids + [2] * self.token_type_ids
