"""
A text generation model with stream decoding.
"""
import os
import gc
import copy
import pynvml
import torch
from sentencepiece import SentencePieceProcessor
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    LogitsProcessorList,
    MinNewTokensLengthLogitsProcessor,
    TemperatureLogitsWarper,
    TopPLogitsWarper,
)
from loguru import logger
from .choice import map_choice
from .tokenizer import StreamTokenizer


class StreamModel:
    """StreamModel wraps around a language model to provide stream decoding."""

    def __init__(self, model, tokenizer,**kwargs):
        super().__init__()
        self.model = model
        self.tokenizer = tokenizer
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.path=kwargs.get('path',None)
        if self.path:
            self.s_tokenizer =SentencePieceProcessor(model_file=f"{self.path}/tokenizer.model")

    def __call__(
        self,
        prompt,
        min_tokens=0,
        max_tokens=16,
        temperature=1.0,
        top_p=1.0,
        n=1,
        logprobs=0,
        echo=False,
    ):
        
        """Create a completion stream for the provided prompt."""
        if isinstance(prompt, str):
            input_ids = self.tokenize(prompt)
        elif isinstance(prompt, torch.Tensor) and prompt.dim() == 1:
            input_ids = prompt
        else:
            raise TypeError("prompt must be a string or a 1-d tensor")

        # Ensure arguments are non-negative.
        min_tokens = max(min_tokens, 0)
        max_tokens = max(max_tokens, 1)
        n = max(n, 1)
        logprobs = max(logprobs, 0)

        # Keep track of the finish reason of each sequence.
        finish_reasons = [None] * n

        # Create stateful detokenizer for each sequence.
        detokenizers = []
        for i in range(n):
            detokenizers.append(StreamTokenizer(self.tokenizer))

        # Echo prompt tokens if required.
        for token in input_ids:
            samples = self._sample(token, 0, [], []) if logprobs > 0 else {}
            for i in range(n):
                text = detokenizers[i].decode(token)
                offset = detokenizers[i].start
                if echo:
                    yield map_choice(text, i, text_offset=offset, **samples)

        # Generate completion tokens.
        for (
            tokens,
            token_logprobs,
            top_tokens,
            top_logprobs,
            status,
        ) in self.generate(
            input_ids[None, :].repeat(n, 1),
            logprobs=logprobs,
            min_new_tokens=min_tokens,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        ):
            for i in range(n):
                # Check and update the finish status of the sequence.
                if finish_reasons[i]:
                    continue
                if status[i] == 0:
                    finish_reasons[i] = "stop"
                elif status[i] == -1:
                    finish_reasons[i] = "length"

                # Collect samples of the most likely tokens if required.
                samples = (
                    self._sample(
                        token=tokens[i],
                        token_logprob=token_logprobs[i],
                        top_tokens=top_tokens[i],
                        top_logprobs=top_logprobs[i],
                    )
                    if logprobs > 0
                    else {}
                )

                # Yield predicted tokens.
                text = detokenizers[i].decode(tokens[i])
                offset = detokenizers[i].start
                # print(f"word:{text}, token:{tokens[i]}")
                yield map_choice(
                    text,
                    i,
                    text_offset=offset,
                    finish_reason=finish_reasons[i],
                    **samples,
                )

    def _sample(self, token, token_logprob, top_tokens, top_logprobs):
        """Sample log probabilities of the most likely tokens."""
        token = self.tokenizer.decode(token)
        top_tokens = self.tokenizer.batch_decode(top_tokens)

        # Do not use tensor operations as arguments may be of list type.
        token_logprob = round(float(token_logprob), 8)
        top_logprobs = [round(float(p), 8) for p in top_logprobs]

        # Always include the log probability of the selected token.
        top_logprobs = dict(zip(top_tokens, top_logprobs))
        top_logprobs[token] = token_logprob

        return {
            "token": token,
            "token_logprob": token_logprob,
            "top_logprobs": top_logprobs,
        }

    def _logits_processor(self, config, input_length):
        """Set up logits processor based on the generation config."""
        processor = LogitsProcessorList()

        # Add processor for enforcing a min-length of new tokens.
        if (
            config.min_new_tokens is not None
            and config.min_new_tokens > 0
            and config.eos_token_id is not None
        ):
            processor.append(
                MinNewTokensLengthLogitsProcessor(
                    prompt_length_to_skip=input_length,
                    min_new_tokens=config.min_new_tokens,
                    eos_token_id=config.eos_token_id,
                )
            )

        # Add processor for scaling output probability distribution.
        if (
            config.temperature is not None
            and config.temperature > 0
            and config.temperature != 1.0
        ):
            processor.append(TemperatureLogitsWarper(config.temperature))

        # Add processor for nucleus sampling.
        if config.top_p is not None and config.top_p > 0 and config.top_p < 1:
            processor.append(TopPLogitsWarper(config.top_p))

        return processor

    def tokenize(self, text,trim_to=2048):
        """Tokenize a string into a tensor of token IDs."""
        num_tokens = self.get_tokens_count(text)            
        if num_tokens>trim_to:
            raise ValueError(f"Tokenized original text:{num_tokens} tokens, trimed:{trim_to} tokens. Some tokens are lost, please try to reduce the length of the input text.")
        self.wait_and_clear_gpu()
        with torch.inference_mode():
            batch = self.tokenizer.encode(text,truncation=True,max_length=trim_to,return_tensors="pt")
            logger.debug(f"Sending tokenized text to device {self.device}")
            res=batch[0].to(self.device)
        logger.debug(f"Tokenized original text:{num_tokens} tokens, trimed:{batch.shape[-1]} tokens")
        
        return res

    def generate(self, input_ids, logprobs=0, **kwargs):
        """Generate a stream of predicted tokens using the language model."""

        # Store the original batch size and input length.
        batch_size = input_ids.shape[0]
        input_length = input_ids.shape[-1]

        # Separate model arguments from generation config.
        config = self.model.generation_config
        config = copy.deepcopy(config)
        kwargs = config.update(**kwargs)
        kwargs["output_attentions"] = False
        kwargs["output_hidden_states"] = False
        kwargs["use_cache"] = config.use_cache

        # Collect special token IDs.
        pad_token_id = config.pad_token_id
        bos_token_id = config.bos_token_id
        eos_token_id = config.eos_token_id
        if isinstance(eos_token_id, int):
            eos_token_id = [eos_token_id]
        if pad_token_id is None and eos_token_id is not None:
            pad_token_id = eos_token_id[0]

        # Generate from eos if no input is specified.
        if input_length == 0:
            input_ids = input_ids.new_ones((batch_size, 1)).long()
            if eos_token_id is not None:
                input_ids = input_ids * eos_token_id[0]
            input_length = 1

        # Prepare inputs for encoder-decoder models.
        if self.model.config.is_encoder_decoder:
            # Get outputs from the encoder.
            encoder = self.model.get_encoder()
            
            with torch.inference_mode():
                encoder_kwargs = kwargs.copy()
                encoder_kwargs.pop("use_cache", None)
                encoder_kwargs["input_ids"] = input_ids
                encoder_kwargs["return_dict"] = True
                kwargs["encoder_outputs"] = encoder(**encoder_kwargs)

            # Reinitialize inputs for the decoder.
            decoder_start_token_id = config.decoder_start_token_id
            if decoder_start_token_id is None:
                decoder_start_token_id = bos_token_id
            input_ids = input_ids.new_ones((batch_size, 1))
            input_ids = input_ids * decoder_start_token_id
            input_length = 1

        # Set up logits processor.
        processor = self._logits_processor(config, input_length)

        # Keep track of which sequences are already finished.
        unfinished = input_ids.new_ones(batch_size)

        # Repeated tokens tracking
        last_token_count=[0,0]
        limit_repetitions = 20

        # Start auto-regressive generation.
        while True:
            # Over repeated tokens limit
            if last_token_count[1] > limit_repetitions:
                logger.debug(f"Generation stoped, over repeated tokens limit, Token:{last_token_count[0]}, Count:{last_token_count[1]}")
                break

            inputs = self.model.prepare_inputs_for_generation(
                input_ids, **kwargs
            )  # noqa: E501
            with torch.inference_mode():
                outputs = self.model(
                    **inputs,
                    return_dict=True,
                    output_attentions=False,
                    output_hidden_states=False,
                )

            # Pre-process the probability distribution of the next tokens.
            logits = outputs.logits[:, -1, :]
            with torch.inference_mode():
                logits = processor(input_ids, logits)
            probs = torch.nn.functional.softmax(logits, dim=-1)

            # Select deterministic or stochastic decoding strategy.
            if (config.top_p is not None and config.top_p <= 0) or (
                config.temperature is not None and config.temperature <= 0
            ):
                tokens = torch.argmax(probs, dim=-1)[:, None]
            else:
                tokens = torch.multinomial(probs, num_samples=1)

            # Collect log probabilities of the selected tokens.
            token_logprobs = torch.gather(probs, 1, tokens)
            token_logprobs = torch.log(token_logprobs + 1e-7).squeeze(1)
            tokens = tokens.squeeze(1)

            # Collect log probabilities of the most likely tokens.
            top_logprobs, top_tokens = probs.topk(logprobs)
            top_logprobs = torch.log(top_logprobs + 1e-7)

            # Finished sequences should have their next token be a padding.
            if pad_token_id is not None:
                tokens = tokens * unfinished + pad_token_id * (1 - unfinished)

            # Append selected tokens to the inputs.
            input_ids = torch.cat([input_ids, tokens[:, None]], dim=-1)
            if tokens[-1]==last_token_count[0]:
                last_token_count[1]+=1
            else:
                last_token_count[0]=tokens[-1]
                last_token_count[1]=0
            
            # Extract past key values from model outputs.
            if "past_key_values" in outputs:
                kwargs["past_key_values"] = outputs.past_key_values
            elif "mems" in outputs:
                kwargs["past_key_values"] = outputs.mems
            elif "past_buckets_states" in outputs:
                kwargs["past_key_values"] = outputs.past_buckets_states

            # Mark sequences with eos tokens as finished.
            if eos_token_id is not None:
                not_eos = sum(tokens != i for i in eos_token_id)
                unfinished = unfinished.mul(not_eos.long())

            # Set status to -1 if exceeded the max length.
            status = unfinished.clone()
            if input_ids.shape[-1] - input_length >= config.max_new_tokens:
                status = 0 - status
            # print(f"(g)status:{status}")
            # print(f"(g)tokens:{tokens}")
            # print(f"(g)last_token_count:{last_token_count}")
            # Yield predictions and status.
            yield tokens, token_logprobs, top_tokens, top_logprobs, status

            # Stop when finished or exceeded the max length.
            if status.max() <= 0:
                break
    
    def get_tokens_count(self, prompt):
        """Tokenize a string into a tensor of token IDs."""
        if isinstance(prompt, str):
            if len(prompt) == 0:
                return 0
            if self.s_tokenizer:
                return len(self.s_tokenizer.EncodeAsIds(prompt))+1#+1 for eos
            batch = self.tokenizer.encode(prompt, return_tensors="pt")
            return batch.shape[-1]
        elif isinstance(prompt, torch.Tensor) and prompt.dim() == 1:
            return prompt.shape[-1]
        raise TypeError("prompt must be a string or a 1-d tensor")

    def wait_and_clear_gpu(self):
        """Wait for GPU memory to be released and clear the cache."""
        # torch.cuda.empty_cache()
        logger.debug("Waiting for GPU memory to be released")
        
        pynvml.nvmlInit()
        gpus_count = pynvml.nvmlDeviceGetCount()
        logger.debug(f"Found {gpus_count} GPUs")
        handles = []
        for index in range(gpus_count):
            try:
                handles.append(pynvml.nvmlDeviceGetHandleByIndex(index))
                logger.debug(f"Got handle for GPU {index}")
            except Exception as e:
                logger.error(f"Failed to get handle for GPU {index}: {e}")
        
        for i,handle in enumerate(handles):
            info=pynvml.nvmlDeviceGetMemoryInfo(handle)
            logger.debug(f"GPU {i} memory info: {gpu_sum(info)}") 
        
        # logger.debug(torch.cuda.memory_stats())
        
        logger.debug("Clearing GPU cache")
        gc.collect()
        torch.cuda.empty_cache()
        gc.collect()

        for i,handle in enumerate(handles):
            info=pynvml.nvmlDeviceGetMemoryInfo(handle)
            logger.debug(f"GPU {i} memory info: {gpu_sum(info)}") 

        # logger.debug(torch.cuda.memory_stats())
        
        pynvml.nvmlShutdown()
        

def load_model(
    name_or_path,
    revision=None,
    cache_dir=None,
    load_in_8bit=False,
    load_in_4bit=False,
    local_files_only=False,
    trust_remote_code=False,
    half_precision=False,
):
    """Load a text generation model and make it stream-able."""
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Loading tokenizer from {name_or_path}")
    kwargs = {
        "local_files_only": local_files_only,
        "trust_remote_code": trust_remote_code,
    }
    if revision:
        kwargs["revision"] = revision
    if cache_dir:
        kwargs["cache_dir"] = cache_dir
    tokenizer = AutoTokenizer.from_pretrained(name_or_path, **kwargs)
    logger.info(f"Tokenizer loaded")
    logger.info(f"Loading model from {name_or_path}")
    # Set device mapping and quantization options if CUDA is available.
    if torch.cuda.is_available():
        kwargs = kwargs.copy()
        kwargs["device_map"] = "auto"
        kwargs["load_in_8bit"] = load_in_8bit
        # kwargs["load_in_4bit"] = load_in_4bit

        # Cast all parameters to float16 if quantization is enabled.
        if half_precision or load_in_8bit or load_in_4bit:
            kwargs["torch_dtype"] = torch.float16

    # Support both decoder-only and encoder-decoder models.
    try:
        model = AutoModelForCausalLM.from_pretrained(name_or_path, **kwargs)
    except ValueError:
        model = AutoModelForSeq2SeqLM.from_pretrained(name_or_path, **kwargs)

    # Check if the model has text generation capabilities.
    if not model.can_generate():
        logger.error(f"{name_or_path} is not a text generation model")
        raise TypeError(f"{name_or_path} is not a text generation model")

    return StreamModel(model, tokenizer,path=name_or_path)

def gpu_sum(info):
    bytes_gib = 1024.0 ** 3
    s=""        
    s+='used:'+f"{int(info.used / bytes_gib)} GiB | "
    s+='free:'+ f"{int(info.free / bytes_gib)} GiB | "
    s+='total:'+f"{int(info.total / bytes_gib)} GiB"
    return s