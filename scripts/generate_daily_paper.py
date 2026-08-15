import csv
import json
import random
import os

# 論文によくある文型テンプレート
# N: 名詞, V: 動詞, A: 形容詞, ADV: 副詞

TEMPLATES = [
    # --- 元の8個 ---
    "It is widely recognized that the N V a A N .",
    "Recent studies on N have shown that N V ADV .",
    "The primary objective of this N is to V the N of N .",
    "Furthermore , the A N V the A N .",
    "In this context , N V a crucial role in A N .",
    "We hypothesize that A N V due to A N .",
    "The experimental N V that N is A .",
    "As a result , N V A N in the N .",

    # --- 追加: 背景・先行研究 ---
    "There is a growing body of literature that recognizes the importance of N .",
    "Despite extensive research on N , the role of N remains poorly understood .",
    "Previous studies have predominantly focused on A N .",
    "A considerable amount of literature has been published on N .",
    "Recent developments in the field of N have led to a renewed interest in N .",
    "The N of N has been a subject of considerable debate .",
    "An important question associated with N is whether N V N .",
    "To date , there has been little agreement on what N V .",
    "Prior studies have noted the importance of N .",

    # --- 追加: 目的・貢献・構成 ---
    "The purpose of this N is to investigate the N of N .",
    "This N aims to contribute to this growing area of research by exploring N .",
    "To address this gap , we propose a novel N that V N .",
    "This N is structured as follows .",
    "The remainder of this N is organized as follows .",
    "This N contributes to the existing literature on N by V N .",
    "We argue that A N highlights the need for A N .",

    # --- 追加: 手法 ---
    "The N was V to measure the A N .",
    "N were randomly V from A N .",
    "We conducted a series of N to V the N of N .",
    "The data were collected via A N over a period of N .",
    "In order to V N , we employed a A N approach .",
    "For the purpose of N , A N were V .",
    "All N were V prior to N .",
    "Prior to N , it is necessary to V N .",

    # --- 追加: 結果 ---
    "As shown in N , the A N V significantly .",
    "The results indicate that N V more A than N .",
    "A statistically significant difference was observed between A N and A N .",
    "Interestingly , N was found to V ADV when N was A .",
    "The most striking result to emerge from the data is that N V ADV .",
    "On average , A N were shown to have A N than A N .",
    "Compared with A N , the N V a significantly more A N .",
    "Notably , the A N V more ADV than the A N .",

    # --- 追加: 考察・議論 ---
    "These findings suggest that N plays a A role in V N .",
    "This result can be explained by the fact that N V N .",
    "Contrary to expectations , this N did not find a significant difference between N and N .",
    "The present findings are consistent with those of N , who found that N V N .",
    "In line with previous literature , our N V that N is A .",
    "There are several possible explanations for this N .",
    "One possible implication of this finding is that N V N .",
    "However , this result has not previously been described .",
    "While A N V N , A N V N .",
    "It is important to note that N V only when N is A .",
    "The analysis of N reveals that N is A and A .",

    # --- 追加: 結論・限界・今後の課題 ---
    "Taken together , these results suggest that N V N .",
    "In conclusion , this N has demonstrated that N V N .",
    "The insights gained from this N may be of assistance to N .",
    "Ultimately , N V the importance of A N in A N .",
    "This N has several limitations that should be acknowledged .",
    "Our results may be limited by the A N of N .",
    "The generalizability of these results is subject to certain limitations .",
    "Despite its limitations , this N adds to our understanding of N .",
    "Future research should focus on V N in more detail .",
    "Further studies regarding the role of N would be worthwhile .",
]

STATE_FILE = "data/state.json"
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
    words_dict = load_words("data/words.csv")
    
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
