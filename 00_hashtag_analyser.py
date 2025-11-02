#!/usr/bin/env python3
"""
Mastodon Archive Hashtag Analyzer
Analysiert ein Mastodon JSON-Archiv und zählt verwendete Hashtags
"""

import json
import csv
from collections import Counter
from pathlib import Path
import argparse
import sys


def extract_hashtags_from_post(post):
    """Extrahiert Hashtags aus einem einzelnen Post"""
    hashtags = []

    # Hashtags können in verschiedenen Strukturen sein
    # 1. Im 'tags' Array (häufigste Struktur)
    if 'tags' in post and isinstance(post['tags'], list):
        for tag in post['tags']:
            if isinstance(tag, dict) and 'name' in tag:
                hashtags.append(tag['name'].lower())
            elif isinstance(tag, str):
                hashtags.append(tag.lower().lstrip('#'))

    # 2. Im 'object' für ältere Archive
    if 'object' in post:
        obj = post['object']
        if isinstance(obj, dict) and 'tag' in obj:
            tags = obj['tag']
            if isinstance(tags, list):
                for tag in tags:
                    if isinstance(tag, dict) and tag.get('type') == 'Hashtag':
                        name = tag.get('name', '').lower().lstrip('#')
                        if name:
                            hashtags.append(name)

    return hashtags


def analyze_archive(archive_path):
    """Analysiert das Mastodon-Archiv und zählt Hashtags"""
    archive_path = Path(archive_path)
    hashtag_counter = Counter()
    posts_processed = 0

    print(f"📂 Lese Archiv: {archive_path}")

    # Prüfe ob es eine Datei oder ein Verzeichnis ist
    if archive_path.is_file():
        # Einzelne JSON-Datei
        files_to_process = [archive_path]
    elif archive_path.is_dir():
        # Verzeichnis - suche nach relevanten JSON-Dateien
        files_to_process = list(archive_path.glob('**/*.json'))
        # Filtere typische Mastodon-Archiv-Dateien
        files_to_process = [
            f for f in files_to_process
            if f.name in ['outbox.json', 'posts.json'] or 'outbox' in f.name.lower()
        ]
        if not files_to_process:
            # Fallback: alle JSON-Dateien
            files_to_process = list(archive_path.glob('**/*.json'))
    else:
        print(f"❌ Fehler: {archive_path} existiert nicht")
        sys.exit(1)

    print(f"📄 Gefundene JSON-Dateien: {len(files_to_process)}")

    for json_file in files_to_process:
        print(f"   Verarbeite: {json_file.name}...", end=' ')
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Verschiedene Strukturen unterstützen
            posts = []
            if isinstance(data, list):
                posts = data
            elif isinstance(data, dict):
                # ActivityPub Format
                if 'orderedItems' in data:
                    posts = data['orderedItems']
                elif 'items' in data:
                    posts = data['items']
                else:
                    posts = [data]  # Einzelner Post

            file_posts = 0
            for post in posts:
                if isinstance(post, dict):
                    hashtags = extract_hashtags_from_post(post)
                    hashtag_counter.update(hashtags)
                    if hashtags:
                        file_posts += 1

            posts_processed += file_posts
            print(f"✓ ({file_posts} Posts mit Hashtags)")

        except json.JSONDecodeError as e:
            print(f"⚠️  Überspringe (kein gültiges JSON): {e}")
        except Exception as e:
            print(f"⚠️  Fehler: {e}")

    print(f"\n✅ Verarbeitet: {posts_processed} Posts mit Hashtags")
    print(f"📊 Gefunden: {len(hashtag_counter)} unterschiedliche Hashtags")

    return hashtag_counter


def export_to_csv(hashtag_counter, output_path, encoding='utf-8-sig', delimiter=','):
    """Exportiert die Hashtag-Statistik in eine CSV-Datei"""
    print(f"\n💾 Exportiere nach: {output_path}")
    print(f"   Encoding: {encoding}, Trennzeichen: '{delimiter}'")

    try:
        with open(output_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(['Hashtag', 'Anzahl'])

            # Sortiert nach Häufigkeit (absteigend)
            for hashtag, count in hashtag_counter.most_common():
                writer.writerow([hashtag, count])

        print(f"✅ Export abgeschlossen!")
    except UnicodeEncodeError as e:
        print(f"⚠️  Encoding-Fehler mit {encoding}: {e}")
        print(f"   Versuche es mit: --encoding windows-1252 oder --encoding iso-8859-15")


def print_top_hashtags(hashtag_counter, n=20):
    """Zeigt die Top N Hashtags in der Konsole"""
    print(f"\n🏆 Top {n} Hashtags:")
    print("-" * 50)
    for i, (hashtag, count) in enumerate(hashtag_counter.most_common(n), 1):
        print(f"{i:2d}. #{hashtag:<30} {count:>6}x")


def main():
    parser = argparse.ArgumentParser(
        description='Analysiert Mastodon-Archive und zählt Hashtag-Verwendung',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s archive.json
  %(prog)s /pfad/zum/mastodon-archiv/
  %(prog)s archive.json -o meine-hashtags.csv
  %(prog)s archive.json --top 50
  %(prog)s archive.json --encoding windows-1252 --delimiter ";"
        """
    )

    parser.add_argument(
        'archive',
        help='Pfad zur Mastodon-Archiv JSON-Datei oder zum Archiv-Verzeichnis'
    )
    parser.add_argument(
        '-o', '--output',
        default='mastodon_hashtags.csv',
        help='Output CSV-Datei (Standard: mastodon_hashtags.csv)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=20,
        help='Anzahl der Top-Hashtags zur Anzeige (Standard: 20)'
    )
    parser.add_argument(
        '--encoding',
        choices=['utf-8-sig', 'utf-8', 'iso-8859-15', 'windows-1252'],
        default='utf-8-sig',
        help='Encoding für die CSV-Datei (Standard: utf-8-sig für Excel-Kompatibilität)'
    )
    parser.add_argument(
        '--delimiter',
        default=',',
        help='CSV-Trennzeichen (Standard: ,) - verwende ";" für deutsche Excel-Version'
    )

    args = parser.parse_args()

    # Analysiere das Archiv
    hashtag_counter = analyze_archive(args.archive)

    if not hashtag_counter:
        print("\n⚠️  Keine Hashtags gefunden!")
        sys.exit(1)

    # Zeige Top-Hashtags
    print_top_hashtags(hashtag_counter, args.top)

    # Exportiere zu CSV
    export_to_csv(hashtag_counter, args.output, args.encoding, args.delimiter)

    print(f"\n📈 Statistik:")
    print(f"   Gesamt verschiedene Hashtags: {len(hashtag_counter)}")
    print(f"   Gesamt Hashtag-Verwendungen: {sum(hashtag_counter.values())}")


if __name__ == '__main__':
    main()