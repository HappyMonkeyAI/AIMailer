import importlib
import pytest
import re

def test_clean_thought_blocks():
    summarizer = importlib.import_module('aimailer.summarizer')
    
    # Test <thought> tags
    input_text = "<thought>I should summarize this.</thought>This is the summary."
    assert summarizer.clean_thought_blocks(input_text) == "This is the summary."
    
    # Test <think> tags (DeepSeek style)
    input_text = "<think>Reasoning here...</think>Final answer."
    assert summarizer.clean_thought_blocks(input_text) == "Final answer."
    
    # Test multiple blocks and mixed case
    input_text = "<THOUGHT>First block</thought> Content <think>Second block</THINK>"
    assert summarizer.clean_thought_blocks(input_text) == "Content"
    
    # Test nested-ish or multiple brackets
    input_text = "[[[thought]]]Hidden[[[/thought]]]Visible"
    assert summarizer.clean_thought_blocks(input_text) == "Visible"

def test_summarizer_with_thought_clutter():
    summarizer = importlib.import_module('aimailer.summarizer')
    
    # Mocking call_ollama would be better, but we can test the internal logic 
    # if we refactor or just test the cleaning directly as above.
    # For now, let's verify that summarize_text handles a response with thoughts if we could inject it.
    pass

def test_summarizer_stub():
    summarizer = importlib.import_module('aimailer.summarizer')
    out = summarizer.summarize_text('This is a test article about AI tooling and agents.')
    assert 'summary' in out
    assert out['summary']
