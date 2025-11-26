import importlib

def test_summarizer_stub():
    summarizer = importlib.import_module('aimailer.summarizer')
    out = summarizer.summarize_text('This is a test article about AI tooling and agents.')
    assert 'summary' in out
    assert out['summary']
