from pathlib import Path

DEFAULT_HOOKS_CONFIG = {
    'train.hooks': [{
        'type': 'CheckpointHook',
        'interval': 1
    }, {
        'type': 'TextLoggerHook',
        'interval': 10
    }, {
        'type': 'IterTimerHook'
    }]
}


HOOK_KEY_CHAIN_MAP = {
    'TextLoggerHook': 'train.logging',
    'CheckpointHook': 'train.checkpoint.period',
    'BestCkptSaverHook': 'train.checkpoint.best',
    'EvaluationHook': 'evaluation.period',
}



DEFAULT_CACHE_DIR = Path.home().joinpath('.cache', 'weathon')

BARK_WEBHOOK_URL = 'https://notify.omycloud.site/webhook/39fcacdb578a4259ab6d7b87c2ec9f1d'


# openai 
OPENAI_API_KEY = "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"
OPENAI_API_BASE = "https://openai.omycloud.site/v1"
OPENAI_API_COMPLETIONS = "https://openai/omycloud.site/v1/chat/completions" 


# google search
SERPAPI_API_KEY = '2448ba6361437353026c6cc15fe4a30d2328fd6ae6008dfdfb0b5d1bc32013d8'


