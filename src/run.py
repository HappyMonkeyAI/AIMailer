import argparse
import importlib


def main(dry_run=True):
    # Import modules dynamically to avoid static analysis import errors
    fetchers = importlib.import_module('aimailer.fetchers')
    extractor = importlib.import_module('aimailer.extractor')
    summarizer = importlib.import_module('aimailer.summarizer')
    composer = importlib.import_module('aimailer.composer')
    sender = importlib.import_module('aimailer.sender')
    config = importlib.import_module('aimailer.config')

    print('Running AIMailer pipeline (dry_run=%s)' % dry_run)
    example_url = 'https://example.com'
    html = fetchers.fetch_http(example_url) or ''
    text = extractor.extract_text(html)
    s = summarizer.summarize_text(text or 'Example placeholder article about AI tooling.')
    item = {'title': 'Example article', 'summary': s['summary'], 'url': example_url}
    html_email = composer.compose_html('Weekly AI Tooling Roundup', [item])
    sender.send_email('Weekly AI Tooling Roundup', html_email, config.RECIPIENT, dry_run=dry_run)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', dest='dry_run', default=True, help='Do not actually send email')
    args = p.parse_args()
    main(dry_run=args.dry_run)
