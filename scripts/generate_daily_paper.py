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

        # --- 追加: 導入・問題設定 ---
    "In recent years , increasing attention has been paid to N .",
    "N has attracted considerable attention in recent years .",
    "The importance of N has been increasingly recognized in the literature .",
    "N has emerged as a key issue in the study of N .",
    "A growing number of studies have examined the relationship between N and N .",
    "The relationship between N and N remains an open question .",
    "Little is known about how N affects N .",
    "It remains unclear whether N V N .",
    "Despite growing interest in N , relatively little is known about N .",
    "Although N has been extensively studied , N remains largely unexplored .",
    "The extent to which N V N remains unclear .",
    "Understanding N is essential for advancing our knowledge of N .",
    "N represents a significant challenge for researchers seeking to V N .",
    "One of the central issues in this area is whether N V N .",
    "A key challenge is to determine whether N V N .",

    # --- 追加: 先行研究・文献レビュー ---
    "Previous research has demonstrated that N V N .",
    "Previous studies have consistently reported that N V N .",
    "Several studies have investigated whether N V N .",
    "A number of researchers have argued that N V N .",
    "The existing literature provides evidence that N V N .",
    "The literature on N can be broadly divided into A N .",
    "Studies of N have yielded mixed results .",
    "Previous findings regarding N have been inconsistent .",
    "The findings reported in the literature vary considerably across studies .",
    "Several explanations have been proposed to account for N .",
    "Prior research has identified several factors that may influence N .",
    "Previous work has primarily examined N in the context of N .",
    "Much of the existing research has focused on N rather than N .",
    "Few studies have considered the possibility that N V N .",
    "To the best of our knowledge , no previous study has examined N .",
    "The present study builds on previous research by examining N .",
    "Our approach differs from previous studies in several important respects .",
    "Unlike previous studies , we examine N using A N .",

    # --- 追加: ギャップ・研究課題 ---
    "However , several important questions remain unanswered .",
    "However , this issue has received relatively little attention .",
    "This leaves an important gap in the existing literature .",
    "A major limitation of previous research is that N has not been adequately considered .",
    "One limitation of the existing literature is the lack of N .",
    "The existing literature has yet to provide a satisfactory explanation for N .",
    "There is therefore a need for further research on N .",
    "Further investigation is required to determine whether N V N .",
    "These observations raise the question of whether N V N .",
    "This raises an important question regarding the extent to which N V N .",
    "To fill this gap , the present study examines N .",
    "To address this issue , we investigate the relationship between N and N .",
    "The present study seeks to address this gap by V-ing N .",
    "This study extends previous research by taking into account N .",

    # --- 追加: 研究目的・研究質問 ---
    "The present study aims to determine whether N V N .",
    "The primary aim of this study is to examine N .",
    "A secondary aim is to investigate whether N V N .",
    "Specifically , we examine how N affects N .",
    "This study addresses the following research question : whether N V N .",
    "We seek to determine the extent to which N V N .",
    "Our objective is to assess whether N V N .",
    "The study is designed to answer two related questions .",
    "We focus specifically on the relationship between N and N .",
    "The analysis presented here is intended to clarify N .",

    # --- 追加: 仮説・予測 ---
    "We hypothesize that N V N .",
    "We hypothesize that N is positively associated with N .",
    "We hypothesize that N is negatively associated with N .",
    "It is expected that N V N .",
    "We expect N to V N .",
    "Based on previous research , we predict that N V N .",
    "Our hypothesis is that N V N .",
    "This leads us to hypothesize that N V N .",
    "If N V N , then N should V N .",
    "We further hypothesize that N V N under A N .",

    # --- 追加: 理論・概念枠組み ---
    "The present analysis is based on the assumption that N V N .",
    "Our theoretical framework assumes that N V N .",
    "From a theoretical perspective , N may be understood as N .",
    "Theoretically , N can be interpreted as N .",
    "This perspective provides a useful framework for understanding N .",
    "The concept of N refers to the extent to which N V N .",
    "In the present study , N is defined as N .",
    "For the purposes of this study , N is defined as N .",
    "The relationship between N and N can be conceptualized in terms of N .",
    "This framework suggests that N should V N .",

    # --- 追加: データ・対象 ---
    "The study was conducted using data obtained from N .",
    "The dataset consists of N observations collected from N .",
    "The sample consisted of N N selected from N .",
    "Participants were recruited from N .",
    "The sample was restricted to N that met the following criteria .",
    "Only N satisfying the following criteria were included in the analysis .",
    "Data from N were excluded from the analysis because N .",
    "The final sample included N observations .",
    "The data cover the period from N to N .",
    "The analysis was based on a sample of N .",

    # --- 追加: 変数・測定 ---
    "N was measured using a A N scale .",
    "N was operationalized as N .",
    "The dependent variable was measured as N .",
    "The independent variable was defined as N .",
    "We used N as a proxy for N .",
    "To assess N , we used N .",
    "The measurement of N was based on N .",
    "All variables were standardized prior to the analysis .",
    "The reliability of the measure was assessed using N .",
    "Higher values of N indicate greater levels of N .",

    # --- 追加: 方法・分析手順 ---
    "We employed a A N method to examine N .",
    "The analysis was performed using A N .",
    "We used N to estimate the effect of N on N .",
    "To examine this relationship , we estimated a A N model .",
    "The model was estimated using N .",
    "The analysis proceeded in two stages .",
    "First , we examined whether N V N .",
    "Second , we assessed the extent to which N V N .",
    "We controlled for N in all analyses .",
    "The analysis was conducted separately for N and N .",
    "To ensure the robustness of our findings , we performed several additional analyses .",
    "We conducted a series of robustness checks to assess N .",
    "Several alternative specifications were considered .",
    "We repeated the analysis using an alternative measure of N .",
    "To minimize the potential influence of N , we V-ed N .",

    # --- 追加: 比較・対照 ---
    "In contrast , N V N .",
    "By contrast , N V N .",
    "In comparison with N , N V N .",
    "N differs substantially from N with respect to N .",
    "The results for N are broadly similar to those for N .",
    "There is a marked difference between N and N .",
    "Compared with N , N is substantially more A .",
    "N was considerably higher among N than among N .",
    "The difference between N and N was particularly pronounced in N .",
    "This pattern was observed across all N .",

    # --- 追加: 因果・関連 ---
    "N is strongly associated with N .",
    "N is positively associated with N .",
    "N is negatively associated with N .",
    "The results provide evidence of a relationship between N and N .",
    "The findings indicate a significant association between N and N .",
    "N appears to influence N through N .",
    "N may contribute to the development of N .",
    "One possible mechanism underlying this relationship is N .",
    "This association may be attributable to N .",
    "The observed relationship is likely to reflect N .",
    "These results provide support for the view that N V N .",
    "The evidence suggests that N may play a role in determining N .",

    # --- 追加: 結果の詳細 ---
    "The results reveal a clear relationship between N and N .",
    "The analysis yielded several important findings .",
    "The results provide strong evidence that N V N .",
    "The results provide limited evidence that N V N .",
    "No significant association was found between N and N .",
    "No statistically significant difference was detected between N and N .",
    "The effect of N on N was statistically significant .",
    "The effect remained significant after controlling for N .",
    "The estimated effect was substantially larger for N than for N .",
    "The magnitude of the effect increased with N .",
    "The effect was particularly strong among N .",
    "The observed effect was robust across alternative specifications .",
    "The results remained unchanged when N was included in the model .",
    "Taken together , the results provide evidence in favor of N .",
    "These findings are broadly consistent with our initial hypothesis .",

    # --- 追加: 不確実性・慎重な主張 ---
    "These findings should be interpreted with caution .",
    "The results should not necessarily be interpreted as evidence that N V N .",
    "Although the results are suggestive , they do not establish that N V N .",
    "The findings provide some evidence that N V N .",
    "The available evidence is insufficient to determine whether N V N .",
    "It remains possible that N V N .",
    "One interpretation of these findings is that N V N .",
    "These results may reflect differences in N .",
    "The extent to which N contributes to N remains uncertain .",
    "Further evidence is needed before a definitive conclusion can be drawn .",

    # --- 追加: 考察・解釈 ---
    "A possible explanation for this finding is that N V N .",
    "This finding may be attributable to differences in N .",
    "One interpretation is that N V N .",
    "This pattern is consistent with the hypothesis that N V N .",
    "The findings can be interpreted in several ways .",
    "The results are particularly noteworthy because N V N .",
    "This finding is important because it suggests that N V N .",
    "The observed pattern may reflect the influence of N .",
    "These findings highlight the importance of considering N when examining N .",
    "The results underscore the need to account for N .",
    "This may explain why N V N .",
    "Taken together , these findings provide a possible explanation for N .",

    # --- 追加: 意外な結果・例外 ---
    "Unexpectedly , N V N .",
    "Contrary to our expectations , N V N .",
    "Surprisingly , N did not V N .",
    "An unexpected finding was that N V N .",
    "This result differs from the pattern observed in previous studies .",
    "This finding contrasts with the results reported by N .",
    "Although we expected N to V N , the results indicate that N V N .",
    "The absence of a significant effect is particularly noteworthy .",
    "This exception suggests that the relationship between N and N may depend on N .",

    # --- 追加: 限界 ---
    "Several limitations of the present study should be considered .",
    "First , the study is limited by N .",
    "A further limitation concerns the measurement of N .",
    "The relatively small sample size may limit the generalizability of the findings .",
    "The observational nature of the data limits our ability to draw causal conclusions .",
    "The results should be interpreted in light of several limitations .",
    "Another potential limitation is the use of N as a proxy for N .",
    "The findings may not generalize beyond N .",
    "The possibility of unobserved confounding cannot be ruled out .",
    "These limitations suggest that caution is warranted when interpreting the results .",

    # --- 追加: 頑健性・追加分析 ---
    "The main findings were robust to a range of alternative specifications .",
    "The results remained qualitatively unchanged across different models .",
    "Additional analyses yielded similar results .",
    "The main conclusion was unaffected by the inclusion of N .",
    "We obtained similar results when using an alternative measure of N .",
    "The findings were robust to the exclusion of N .",
    "Sensitivity analyses produced results consistent with the main analysis .",
    "These additional tests provide further support for our main findings .",

    # --- 追加: 因果推論・条件 ---
    "If N is held constant , N V N .",
    "Holding N constant , we find that N V N .",
    "After accounting for N , the relationship between N and N remains significant .",
    "Once N is taken into account , N V N .",
    "The observed association persists even after controlling for N .",
    "This suggests that the relationship cannot be fully explained by N alone .",
    "The results are consistent with a causal effect of N on N , although further evidence is required .",

    # --- 追加: 時系列・変化 ---
    "Over time , N has become increasingly A .",
    "The prevalence of N increased substantially over the study period .",
    "N has changed considerably over the past N years .",
    "The rate of N remained relatively stable throughout the study period .",
    "A gradual increase in N was observed over time .",
    "The trend was particularly pronounced during N .",
    "Following N , the level of N increased significantly .",
    "Since N , there has been a substantial change in N .",

    # --- 追加: 空間・集団差 ---
    "The effect of N varied across different groups .",
    "The relationship between N and N differed substantially across N .",
    "The strongest effect was observed among N .",
    "The effect was weaker among N than among N .",
    "Substantial heterogeneity was observed across N .",
    "These differences may be attributable to variation in N .",
    "The results suggest that the effect of N is context-dependent .",

    # --- 追加: 定義・言い換え・明確化 ---
    "In other words , N V N .",
    "More specifically , N refers to N .",
    "In the present context , N can be understood as N .",
    "Here , we use the term N to refer to N .",
    "For clarity , we distinguish between N and N .",
    "It should be emphasized that N does not necessarily imply N .",
    "This distinction is important because N V N .",

    # --- 追加: 論文らしい接続表現 ---
    "Taken together , the evidence suggests that N V N .",
    "Collectively , these findings indicate that N V N .",
    "More importantly , N V N .",
    "Of particular importance is the finding that N V N .",
    "It is worth noting that N V N .",
    "Of note , N V N .",
    "At the same time , N V N .",
    "Nevertheless , N V N .",
    "Nonetheless , N V N .",
    "In particular , N V N .",
    "In contrast to N , N V N .",
    "Accordingly , N V N .",
    "Consequently , N V N .",
    "Thus , N V N .",
    "Hence , N V N .",

    # --- 追加: 受動態 ---
    "N was considered to be A .",
    "N was assumed to be A .",
    "N was identified as a A N .",
    "N was classified as A .",
    "N was included in the analysis .",
    "N was excluded from the final analysis .",
    "N was estimated using A N .",
    "N was calculated based on N .",
    "N was obtained from N .",
    "N was subsequently analyzed using N .",

    # --- 追加: 名詞節・形式主語 ---
    "It is possible that N V N .",
    "It is likely that N V N .",
    "It is unlikely that N V N .",
    "It is important to recognize that N V N .",
    "It is important to consider whether N V N .",
    "It should be noted that N V N .",
    "It can be argued that N V N .",
    "It has been suggested that N V N .",
    "It has been proposed that N V N .",
    "It remains to be determined whether N V N .",

    # --- 追加: 不定詞・動名詞・分詞構文 ---
    "To better understand N , we examined N .",
    "To determine whether N V N , we conducted N .",
    "To further investigate this issue , we V-ed N .",
    "By examining N , we can better understand N .",
    "By controlling for N , we were able to V N .",
    "Using N , we estimated N .",
    "Based on N , we conclude that N V N .",
    "Given N , it is reasonable to assume that N V N .",
    "Considering N , N may V N .",
    "Having controlled for N , we found that N V N .",

    # --- 追加: 複文・従属節 ---
    "Although N V N , N V N .",
    "While N V N , N V N .",
    "Whereas N V N , N V N .",
    "Even though N V N , N V N .",
    "If N V N , N may V N .",
    "Unless N V N , N is unlikely to V N .",
    "Because N V N , N V N .",
    "Since N V N , N V N .",
    "As N V N , N V N .",
    "Once N V N , N V N .",
    "When N V N , N tends to V N .",

    # --- 追加: 相関・予測モデル ---
    "N was significantly correlated with N .",
    "N was positively correlated with N .",
    "N was negatively correlated with N .",
    "The correlation between N and N was statistically significant .",
    "N was found to be a significant predictor of N .",
    "N significantly predicted N after controlling for N .",
    "The model explained a substantial proportion of the variance in N .",
    "The predictive power of the model was substantially improved by including N .",

    # --- 追加: 統計結果 ---
    "The difference was statistically significant at the A level .",
    "The effect of N reached statistical significance .",
    "No statistically significant effect of N was observed .",
    "The estimated coefficient for N was positive and statistically significant .",
    "The estimated coefficient was negative but not statistically significant .",
    "The confidence interval indicates that N V N .",
    "The results remained significant after adjustment for multiple comparisons .",
    "The statistical analysis revealed a significant effect of N on N .",

    # --- 追加: 研究の意義・応用 ---
    "These findings have important implications for both theory and practice .",
    "The present findings have several important implications .",
    "From a practical perspective , these findings suggest that N V N .",
    "From a theoretical perspective , the findings contribute to our understanding of N .",
    "These results may have implications for the design of N .",
    "The findings provide useful insights into how N can be improved .",
    "The present study provides a basis for further investigation of N .",
    "This approach may be applicable to a broader range of N .",
    "The findings may inform future research on N .",
    "These results offer a potential explanation for N .",

    # --- 追加: 結論の強化 ---
    "Overall , the findings provide evidence that N V N .",
    "Overall , our results indicate that N V N .",
    "In summary , N V N .",
    "The evidence presented in this study supports the conclusion that N V N .",
    "The present findings demonstrate the importance of N in understanding N .",
    "The results highlight the need for further investigation into N .",
    "These findings contribute to a more comprehensive understanding of N .",
    "The present study provides new evidence regarding the relationship between N and N .",
    "Future research may benefit from examining N across different contexts .",
    "Future studies should investigate whether these findings hold in other settings .",
    "Further work is needed to determine the mechanisms underlying N .",
    "A promising direction for future research is to examine N .",
    "Future research could extend the present analysis by considering N .",
    "Additional research is needed to establish the generalizability of these findings .",

    # --- 追加: 図表の説明・参照 ---
    "Figure N illustrates the relationship between N and N .",
    "Table N summarizes the descriptive statistics for N .",
    "As can be seen in Figure N , there is a clear trend toward A N .",
    "The data in Table N reveal that N V ADV .",
    "Figure N provides a schematic representation of N .",
    "A closer inspection of Table N shows that N V N .",

    # --- 追加: 手法の正当化・選択理由 ---
    "The rationale for using N is that N V N .",
    "N was chosen because it allows for A N .",
    "One of the main advantages of N is that it V N .",
    "The primary benefit of this N is its ability to V N .",
    "This approach is particularly useful when N is A .",
    "We opted for A N in order to minimize A N .",

    # --- 追加: 新規性・独自性の強調 ---
    "To the authors' knowledge , this is the first N to systematically V N .",
    "A key strength of the present N is its use of A N .",
    "This N provides a novel perspective on the complex interplay between N and N .",
    "Our approach offers several distinct advantages over traditional N .",
    "This N represents a significant step forward in understanding N .",

    # --- 追加: データ前処理・クリーニング ---
    "Outliers were V from the N to ensure A N .",
    "Missing values were imputed using a A N method .",
    "The raw data were transformed to V a normal N .",
    "To reduce noise , the A N was filtered using N .",
    "Data were aggregated at the A level to facilitate N .",

    # --- 追加: 矛盾する先行研究の整理 ---
    "While some researchers argue that N V N , others claim that N V N .",
    "The debate over N has produced highly contradictory findings .",
    "Attempts to resolve this contradiction have largely relied on A N .",
    "These conflicting results may be due to differences in A N .",

    # --- 追加: 研究範囲と除外 (Scope & Exclusions) ---
    "The scope of this N is limited to A N .",
    "This N does not attempt to V N .",
    "Issues related to N are beyond the scope of this N .",
    "We restrict our focus to N , leaving N for future research .",
    "It is not the purpose of this N to V N .",

    # --- 追加: 政策・実務への含意 (Policy & Practical Implications) ---
    "Policymakers should consider N when designing A N .",
    "These findings highlight the need for targeted N in N .",
    "The implementation of N could significantly V A N .",
    "Practitioners can utilize these findings to V A N .",
    "The successful adoption of N relies heavily on A N .",

    # --- 追加: 謝辞・資金提供 (Acknowledgments & Funding) ---
    "This N was supported by a grant from N .",
    "We thank N for their helpful comments on earlier drafts of this N .",
    "Financial support for this N was provided by N .",
    "The authors gratefully acknowledge the assistance of N in V-ing N .",
    "N declare that they have no competing financial interests ."
]

STATE_FILE = "data/state.json"
README_FILE = "README.md"

# 論文らしい小見出しのリスト
SECTIONS = [
    "## Introduction",
    "## Literature Review",
    "## Methodology",
    "## Results",
    "## Discussion",
    "## Conclusion",
    "## Future Work"
]

def load_words(csv_path):
    words = {'N': [], 'V': [], 'A': [], 'ADV': []}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['pos'] in words:
                words[row['pos']].append(row['word'])
    return words

def generate_sentence(words_dict):
    # TEMPLATESは既存のものを使用
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
    # --- 省略: words_dictの読み込みとバッファの補充 ---
    words_dict = load_words("data/words.csv")
    
    buffer = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            buffer = json.load(f)
            
    while len(buffer) < 10:
        buffer.extend(generate_sentence(words_dict))
        
    output_tokens = buffer[:10]
    buffer = buffer[10:]
    
    # READMEを読み込む（なければ新規作成）
    if os.path.exists(README_FILE):
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_content = f.read()
    else:
        readme_content = "# Abstract\n\n"

    # 現在の文数（ピリオドの数）をカウント
    sentence_count = readme_content.count('.')

    # READMEに単語を追記
    for token in output_tokens:
        if token in [".", ",", ";", ":"]:
            # 記号の前のスペースを削除して結合
            readme_content = readme_content.rstrip() + token
            
            # ピリオド（文末）の場合の処理
            if token == ".":
                sentence_count += 1
                
                # 例: 10文ごとに小見出しを挿入
                if sentence_count % 10 == 0:
                    # インデックスがSECTIONSの長さを超えないように調整
                    section_idx = (sentence_count // 10) % len(SECTIONS)
                    readme_content += f"\n\n{SECTIONS[section_idx]}\n\n"
                
                # 例: 3文ごとに段落を分ける（小見出しが入るタイミング以外）
                elif sentence_count % 3 == 0:
                    readme_content += "\n\n"
                
                # 通常の文と文の間
                else:
                    readme_content += " "
            else:
                # , や ; の後は通常のスペース
                readme_content += " "
        else:
            # 通常の単語
            readme_content += token + " "
            
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    with open(STATE_FILE, "w") as f:
        json.dump(buffer, f)

if __name__ == "__main__":
    main()
