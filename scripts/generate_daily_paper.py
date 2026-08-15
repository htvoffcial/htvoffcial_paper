import csv
import json
import random
import os

# 論文によくある文型テンプレート
# N: 名詞, V: 動詞, A: 形容詞, ADV: 副詞
TEMPLATES = [
    "It is widely recognized that the N V a A N .",
    "Recent studies on N have shown that N V ADV .",
    "The primary objective of this N is to V the N of N .",
    "Furthermore , the A N V the A N .",
    "In this context , N V a crucial role in A N .",
    "We hypothesize that A N V due to A N .",
    "The experimental N V that N is A .",
    "As a result , N V A N in the N ."
]

STATE_FILE = "state.json"
README_FILE = "README.md"

def load_words(csv_path):
    words = {'N': [], 'V': [], 'A': [], 'ADV': []}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['pos'] in words:
                words[row['pos']].append(row['word'])
    return words

def generate_sentence(words_dict):
    template = random.choice(TEMPLATES)
    tokens = template.split()
    sentence_tokens = []
    for token in tokens:
        if token in words_dict:
            sentence_tokens.append(random.choice(words_dict[token]))
        else:
            sentence_tokens.append(token)
    return sentence_tokens

def main():
    words_dict = load_words("words.csv")
    
    # 未出力の単語バッファを読み込む
    buffer = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            buffer = json.load(f)
            
    # バッファが10単語未満なら、新しい文を生成して補充する
    while len(buffer) < 10:
        buffer.extend(generate_sentence(words_dict))
        
    # 今日の出力分として10単語を取り出す
    output_tokens = buffer[:10]
    buffer = buffer[10:]
    
    # READMEを読み込む（なければ新規作成）
    if os.path.exists(README_FILE):
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_content = f.read()
    else:
        readme_content = "# Abstract\n\n"

    # READMEに単語を追記（ピリオドなどの前の不要なスペースを処理）
    for token in output_tokens:
        if token in [".", ",", ";", ":"]:
            readme_content = readme_content.rstrip() + token + " "
        else:
            readme_content += token + " "
            
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    # 残りのバッファを保存して翌日に引き継ぐ
    with open(STATE_FILE, "w") as f:
        json.dump(buffer, f)

if __name__ == "__main__":
    main()
