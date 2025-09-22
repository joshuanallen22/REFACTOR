"""Tokenizer and codec utilities for REFRACTOR Phase 1.

The module implements a reversible UTF-8 aware tokenizer with explicit
support for protocol/special tokens used across the ingestion pipeline.
The design focuses on predictability and observability rather than raw
compression efficiency; byte-aligned fallback tokens guarantee lossless
round-trips.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from ..telemetry.heartbeat import TelemetryExporter

_SPECIAL_DEFAULTS: Tuple[str, ...] = (
    "<|pad|>",
    "<|bos|>",
    "<|eos|>",
    "<|system|>",
    "<|user|>",
    "<|assistant|>",
    "<|tool|>",
    "<|code|>",
    "<|data|>",
    "<|image|>",
    "<|audio|>",
)


def _default_segmenter(text: str) -> Sequence[str]:
    """Naive segmentation heuristic.

    The default implementation treats the entire payload as a single segment
    unless the text is empty, in which case no segments are reported. The
    interface mirrors richer segmentation logic that will land in later
    phases, enabling downstream telemetry hooks to remain stable.
    """

    return (text,) if text else ()


@dataclass(frozen=True)
class TokenizationStats:
    """Lightweight summary describing an encoding invocation."""

    characters: int
    total_tokens: int
    special_tokens: int
    byte_tokens: int
    segment_lengths: Tuple[int, ...] = field(default_factory=tuple)

    def as_metadata(self) -> Mapping[str, str]:
        """Return metadata strings suitable for telemetry emission."""

        return {
            "characters": str(self.characters),
            "total_tokens": str(self.total_tokens),
            "special_tokens": str(self.special_tokens),
            "byte_tokens": str(self.byte_tokens),
            "segments": ",".join(str(length) for length in self.segment_lengths) or "0",
        }


@dataclass(frozen=True)
class TokenizationResult:
    """Container for encoded token IDs and associated statistics."""

    ids: Tuple[int, ...]
    stats: TokenizationStats


@dataclass(frozen=True)
class TokenizerConfig:
    """Configuration controlling tokenizer vocabulary and behavior."""

    special_tokens: Tuple[str, ...] = _SPECIAL_DEFAULTS
    segmenter: Callable[[str], Sequence[str]] = _default_segmenter
    emit_bos: bool = False
    emit_eos: bool = False

    def unique_special_tokens(self) -> Tuple[str, ...]:
        """Return a stable tuple of de-duplicated special tokens."""

        seen: Dict[str, None] = {}
        for token in self.special_tokens:
            seen[token] = None
        return tuple(seen.keys())


@dataclass(frozen=True)
class _VocabularyEntry:
    token: str
    is_special: bool
    byte_value: Optional[int] = None


class Tokenizer:
    """Implements reversible UTF-8 tokenization with telemetry integration."""

    def __init__(
        self,
        config: Optional[TokenizerConfig] = None,
        *,
        telemetry: Optional[TelemetryExporter] = None,
    ) -> None:
        self._config = config or TokenizerConfig()
        self._telemetry = telemetry
        self._segmenter = self._config.segmenter
        self._token_to_id: Dict[str, int] = {}
        self._id_to_entry: List[_VocabularyEntry] = []
        self._special_token_order: List[str] = []
        self._image_codecs: MutableMapping[str, Callable[[bytes], TokenizationResult]] = {}
        self._audio_codecs: MutableMapping[str, Callable[[bytes], TokenizationResult]] = {}

        for token in self._config.unique_special_tokens():
            self._add_special_token(token)
        self._byte_prefix = "<|byte:"
        for value in range(256):
            self._add_byte_token(value)
        self._update_special_matcher()

    # ------------------------------------------------------------------
    # Vocabulary helpers
    # ------------------------------------------------------------------
    def _add_special_token(self, token: str) -> int:
        if token in self._token_to_id:
            return self._token_to_id[token]
        token_id = len(self._id_to_entry)
        self._token_to_id[token] = token_id
        self._id_to_entry.append(_VocabularyEntry(token=token, is_special=True, byte_value=None))
        self._special_token_order.append(token)
        return token_id

    def _add_byte_token(self, value: int) -> None:
        token = f"{self._byte_prefix}{value:03d}|>"
        token_id = len(self._id_to_entry)
        self._token_to_id[token] = token_id
        self._id_to_entry.append(_VocabularyEntry(token=token, is_special=False, byte_value=value))

    def _update_special_matcher(self) -> None:
        self._special_token_order.sort(key=len, reverse=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def vocabulary_size(self) -> int:
        return len(self._id_to_entry)

    def register_special_token(self, token: str) -> int:
        token_id = self._add_special_token(token)
        self._update_special_matcher()
        return token_id

    def token_to_id(self, token: str) -> int:
        return self._token_to_id[token]

    def id_to_token(self, token_id: int) -> str:
        return self._id_to_entry[token_id].token

    def encode(
        self,
        text: str,
        *,
        add_bos: Optional[bool] = None,
        add_eos: Optional[bool] = None,
        emit_stats: bool = True,
    ) -> TokenizationResult:
        """Encode ``text`` into token IDs."""

        add_bos = self._config.emit_bos if add_bos is None else add_bos
        add_eos = self._config.emit_eos if add_eos is None else add_eos

        ids: List[int] = []
        if add_bos:
            ids.append(self._token_to_id["<|bos|>"])

        special_tokens = 1 if add_bos else 0
        byte_tokens = 0

        index = 0
        while index < len(text):
            matched = False
            for token in self._special_token_order:
                if text.startswith(token, index):
                    ids.append(self._token_to_id[token])
                    index += len(token)
                    special_tokens += 1
                    matched = True
                    break
            if matched:
                continue

            char = text[index]
            char_bytes = char.encode("utf-8")
            for value in char_bytes:
                byte_token = f"{self._byte_prefix}{value:03d}|>"
                ids.append(self._token_to_id[byte_token])
                byte_tokens += 1
            index += 1

        if add_eos:
            ids.append(self._token_to_id["<|eos|>"])
            special_tokens += 1

        stats = TokenizationStats(
            characters=len(text),
            total_tokens=len(ids),
            special_tokens=special_tokens,
            byte_tokens=byte_tokens,
            segment_lengths=tuple(len(segment) for segment in self._segmenter(text)),
        )

        if emit_stats and self._telemetry is not None:
            self._telemetry.emit_heartbeat("tokenizer.codec", **stats.as_metadata())

        return TokenizationResult(ids=tuple(ids), stats=stats)

    def decode(self, ids: Sequence[int]) -> str:
        """Decode a sequence of token IDs back into a string."""

        pieces: List[str] = []
        buffer = bytearray()

        def flush_buffer() -> None:
            if buffer:
                pieces.append(buffer.decode("utf-8", errors="strict"))
                buffer.clear()

        skip_in_decode = {"<|bos|>", "<|eos|>"}

        for token_id in ids:
            entry = self._id_to_entry[token_id]
            if entry.byte_value is not None:
                buffer.append(entry.byte_value)
                continue
            if entry.token in skip_in_decode:
                flush_buffer()
                continue
            flush_buffer()
            pieces.append(entry.token)

        flush_buffer()
        return "".join(pieces)

    # ------------------------------------------------------------------
    # Image/audio stubs
    # ------------------------------------------------------------------
    def register_image_codec(
        self, name: str, handler: Callable[[bytes], TokenizationResult]
    ) -> None:
        self._image_codecs[name] = handler

    def register_audio_codec(
        self, name: str, handler: Callable[[bytes], TokenizationResult]
    ) -> None:
        self._audio_codecs[name] = handler

    def encode_image(self, payload: bytes, *, codec: str) -> TokenizationResult:
        handler = self._image_codecs.get(codec)
        if handler is None:
            raise KeyError(f"No image codec registered for '{codec}'")
        return handler(payload)

    def encode_audio(self, payload: bytes, *, codec: str) -> TokenizationResult:
        handler = self._audio_codecs.get(codec)
        if handler is None:
            raise KeyError(f"No audio codec registered for '{codec}'")
        return handler(payload)


__all__ = [
    "TokenizationResult",
    "TokenizationStats",
    "Tokenizer",
    "TokenizerConfig",
]
