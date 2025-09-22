"""Tests for the Phase 1 tokenizer/codec implementation."""

from __future__ import annotations

import pytest

from refactor import TelemetryExporter, TokenizationResult, TokenizationStats, Tokenizer


def test_encode_decode_roundtrip_with_special_tokens() -> None:
    exporter = TelemetryExporter()
    tokenizer = Tokenizer(telemetry=exporter)

    text = "Hello <|system|> 👋"
    result = tokenizer.encode(text, add_bos=True, add_eos=True)

    assert tokenizer.decode(result.ids) == text
    assert result.stats.characters == len(text)
    assert result.stats.total_tokens == len(result.ids)
    assert result.stats.special_tokens >= 3  # BOS, EOS, and <|system|>
    assert result.stats.byte_tokens > 0  # emoji uses byte fallbacks

    heartbeat = exporter.latest("tokenizer.codec")
    assert heartbeat is not None
    assert heartbeat.metadata["total_tokens"] == str(result.stats.total_tokens)


def test_registering_custom_protocol_token() -> None:
    tokenizer = Tokenizer()
    custom_id = tokenizer.register_special_token("<|custom:tool|>")

    text = "invoke <|custom:tool|>"
    result = tokenizer.encode(text)

    assert custom_id in result.ids
    assert tokenizer.decode(result.ids) == text


def test_image_stub_invocation() -> None:
    tokenizer = Tokenizer()
    marker_id = tokenizer.token_to_id("<|image|>")

    def stub(payload: bytes) -> TokenizationResult:
        stats = TokenizationStats(
            characters=len(payload),
            total_tokens=1,
            special_tokens=1,
            byte_tokens=0,
            segment_lengths=(len(payload),),
        )
        return TokenizationResult(ids=(marker_id,), stats=stats)

    tokenizer.register_image_codec("dummy", stub)
    payload = b"raw-image"
    result = tokenizer.encode_image(payload, codec="dummy")

    assert result.ids == (marker_id,)
    assert result.stats.characters == len(payload)


def test_missing_codec_registration_errors() -> None:
    tokenizer = Tokenizer()

    with pytest.raises(KeyError):
        tokenizer.encode_image(b"data", codec="unknown")

    with pytest.raises(KeyError):
        tokenizer.encode_audio(b"data", codec="unknown")
