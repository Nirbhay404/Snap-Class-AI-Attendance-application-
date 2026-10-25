import sys

# Ensure pkg_resources is available for webrtcvad on Python 3.13+
try:
    import pkg_resources
except ModuleNotFoundError:
    import importlib.metadata as _im

    class _PkgResourcesStub:
        @staticmethod
        def get_distribution(dist_name):
            class _Dist:
                try:
                    version = _im.version(dist_name)
                except Exception:
                    version = "2.0.10"
            return _Dist()

    sys.modules["pkg_resources"] = _PkgResourcesStub()

import io
import librosa
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import streamlit as st


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        print(f"Voice recognition error: {e}")
        st.error("Voice recog error")
        return None


def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    new_emb_arr = np.array(new_embedding, dtype=np.float32)

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            try:
                stored_emb_arr = np.array(stored_embedding, dtype=np.float32)
                similarity = float(np.dot(new_emb_arr, stored_emb_arr))
                if similarity > best_score:
                    best_score = similarity
                    best_sid = sid
            except Exception:
                continue

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(embedding, candidates_dict, threshold)
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        print(f"Bulk audio processing error: {e}")
        st.error("Bulk process error")
        return {}
