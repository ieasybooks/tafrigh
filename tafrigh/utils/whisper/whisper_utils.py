import faster_whisper
import stable_whisper
import whisper_jax

from tafrigh.config import Config
from tafrigh.types.whisper.type_hints import WhisperModel


def load_model(whisper_config: Config.Whisper) -> WhisperModel:
    if whisper_config.use_whisper_jax:
        return whisper_jax.FlaxWhisperPipline(f'openai/whisper-{whisper_config.model_name_or_path}')
    elif whisper_config.use_faster_whisper:
        return faster_whisper.WhisperModel(
            whisper_config.model_name_or_path,
            compute_type=whisper_config.ct2_compute_type,
        )
    else:
        return stable_whisper.load_model(whisper_config.model_name_or_path)
