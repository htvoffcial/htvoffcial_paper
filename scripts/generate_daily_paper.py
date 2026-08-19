import csv
import json
import random
import os
import urllib.parse
from collections import defaultdict
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
    "N declare that they have no competing financial interests .",

        # --- 追加: 要旨・概要 ---
    "This paper presents a A N for N .",
    "In this paper , we propose a A N to V N .",
    "This study investigates the effect of N on N .",
    "We introduce a A framework for V-ing N .",
    "We show that N V N under A conditions .",
    "Our results demonstrate that N V N .",
    "Our approach achieves A performance on N .",
    "The proposed method outperforms N by A margins .",
    "We provide evidence that N V N .",
    "This article reports on a A study of N .",

    # --- 追加: 研究の位置づけ・新規性 ---
    "To the best of our knowledge , this is the first study to V N .",
    "This work bridges the gap between N and N .",
    "Our study sits at the intersection of N and N .",
    "The novelty of this work lies in N .",
    "What distinguishes this study is the use of N .",
    "Unlike existing approaches , our method explicitly accounts for N .",
    "Our approach differs from prior work in that it V N .",
    "This paper offers a new perspective on N .",
    "This study extends the literature by considering N .",
    "The main contribution of this paper is threefold .",

    # --- 追加: 問題の重大さ・動機 ---
    "N poses a serious challenge to N .",
    "Addressing N is critical for V-ing N .",
    "The lack of N remains a major obstacle to N .",
    "Understanding N is of fundamental importance to N .",
    "N has become an increasingly pressing issue in N .",
    "The rapid growth of N has created new challenges for N .",
    "Failure to account for N may lead to A consequences .",
    "Improving N is essential for the development of N .",
    "Current approaches are insufficient to address N .",
    "This gap motivates the present study .",

    # --- 追加: 研究デザイン ---
    "We adopted a A research design .",
    "The study employed a A methodology .",
    "We combined A and A methods to examine N .",
    "A mixed-methods approach was used to investigate N .",
    "The analysis is based on a A design .",
    "The study was designed to capture both N and N .",
    "We used a longitudinal design to examine changes in N .",
    "A cross-sectional design was used to assess N .",
    "We conducted a randomized controlled trial to evaluate N .",
    "The experiment followed a A design .",

    # --- 追加: データ前処理 ---
    "We preprocessed N by V-ing N .",
    "All N were normalized using N .",
    "Missing values were imputed using N .",
    "Outliers were removed based on N .",
    "We removed N that did not meet the inclusion criteria .",
    "The data were cleaned and standardized prior to analysis .",
    "We applied N to reduce the effects of N .",
    "Texts were tokenized and lowercased before analysis .",
    "We transformed N using N .",
    "The final dataset was constructed by merging N with N .",

    # --- 追加: データセット記述 ---
    "The dataset consists of N samples .",
    "Each instance in the dataset contains N .",
    "The corpus comprises N documents collected from N .",
    "The dataset was annotated by N .",
    "Annotations were performed by A annotators .",
    "Inter-annotator agreement was A .",
    "The dataset is balanced with respect to N .",
    "The distribution of N is shown in Figure N .",
    "The training set contains N examples .",
    "The test set was manually curated .",

    # --- 追加: 実装・学習設定 ---
    "The proposed model was implemented in N .",
    "All experiments were conducted using N .",
    "The model was trained for N epochs .",
    "We used N as the optimizer .",
    "The learning rate was set to N .",
    "The learning rate was scheduled using N .",
    "We used a batch size of N .",
    "Hyperparameters were selected on the validation set .",
    "The model was initialized with pretrained weights .",
    "Early stopping was applied based on validation performance .",

    # --- 追加: 評価設定 ---
    "We evaluated the proposed method on N .",
    "Performance was evaluated using N .",
    "We report accuracy , precision , recall , and F1 score .",
    "We used N-fold cross-validation to evaluate N .",
    "The model was evaluated on a held-out test set .",
    "We compared our approach with N baselines .",
    "All baselines were trained under the same conditions .",
    "We report results in terms of N .",
    "Higher scores indicate better N .",
    "The evaluation protocol follows N .",

    # --- 追加: ベースライン比較 ---
    "We compared our method against N .",
    "N served as the primary baseline .",
    "Our method consistently outperformed N across all datasets .",
    "The proposed approach achieved a A improvement over the strongest baseline .",
    "Compared with N , our method reduced N by N .",
    "The improvement over N was modest but consistent .",
    "Although N achieved higher N , our method was more A .",
    "The baseline methods performed poorly when N was A .",
    "Our approach was particularly effective when N was limited .",
    "These gains suggest that N V N .",

    # --- 追加: アブレーション ---
    "To assess the contribution of each component , we conducted an ablation study .",
    "Removing N resulted in a A drop in N .",
    "The performance decreased when N was replaced by N .",
    "The largest drop in performance was observed when N was removed .",
    "These ablation results confirm the importance of N .",
    "The results suggest that N is essential for A performance .",
    "Each component contributes to the overall performance of N .",
    "The benefit of N was most pronounced in A settings .",
    "Ablation results are reported in Table N .",
    "We further analyzed the effect of varying N .",

    # --- 追加: 定性分析・事例 ---
    "Qualitative analysis reveals that N V N .",
    "Figure N shows representative examples of N .",
    "In this example , N V N .",
    "The model correctly predicts N in this case .",
    "This example illustrates how N V N .",
    "These cases suggest that N V N .",
    "Manual inspection of the outputs revealed A patterns .",
    "We examined several cases where N failed to V N .",
    "Such examples highlight the difficulty of N .",
    "A detailed case study is provided in Appendix N .",

    # --- 追加: エラー分析 ---
    "Errors were primarily caused by N .",
    "The most frequent error type was N .",
    "Failure cases often occur when N V N .",
    "The model tends to confuse N with N .",
    "These errors may be attributed to N .",
    "This error pattern suggests that N V N .",
    "Reducing N may help mitigate these errors .",
    "Error analysis reveals limitations of the current approach .",
    "Some errors arise from ambiguity in N .",
    "Future work should address these failure cases .",

    # --- 追加: 図表参照 ---
    "Figure N shows the relationship between N and N .",
    "Table N summarizes the main results .",
    "As shown in Figure N , N V N .",
    "As can be seen from Table N , N V N .",
    "The results are reported in Table N .",
    "Appendix N provides additional details on N .",
    "The distribution of N is plotted in Figure N .",
    "We visualize N in Figure N .",
    "A comparison of N is presented in Table N .",
    "Further results are provided in the supplementary material .",

    # --- 追加: 節の案内 ---
    "Section N presents the related work .",
    "Section N describes the proposed method .",
    "Section N reports the experimental setup .",
    "Section N presents the results .",
    "Section N discusses the implications of the findings .",
    "Section N concludes the paper .",
    "The following section provides an overview of N .",
    "In the next section , we review the relevant literature .",
    "In Section N , we present our methodology .",
    "Finally , we discuss limitations and future work .",

    # --- 追加: 記号・定式化 ---
    "Let N denote the set of N .",
    "We denote N by N .",
    "The input is represented as N .",
    "The output is defined as N .",
    "The objective function can be written as N .",
    "We formulate the problem as N .",
    "The model parameters are estimated by maximizing N .",
    "The loss function is defined as N .",
    "We assume that N follows a A distribution .",
    "The probability of N is modeled as N .",

    # --- 追加: 仮定・適用条件 ---
    "Under the assumption that N V N , we show that N V N .",
    "This result holds under A conditions .",
    "The proposed approach is applicable when N V N .",
    "Our analysis relies on the assumption that N V N .",
    "If this assumption does not hold , N may V N .",
    "The validity of this approach depends on N .",
    "This formulation assumes that N is A .",
    "In practice , this assumption is often reasonable .",
    "We relax this assumption in Section N .",
    "The method can be extended to cases where N V N .",

    # --- 追加: 反論・譲歩 ---
    "One might argue that N V N .",
    "It could be objected that N V N .",
    "While this concern is valid , N V N .",
    "Although alternative explanations are possible , N V N .",
    "We acknowledge that N may V N .",
    "Admittedly , N is not without limitations .",
    "This does not , however , undermine the main conclusion .",
    "Even if N V N , the overall pattern remains A .",
    "Despite this caveat , the results are robust .",
    "It is nevertheless important to consider N .",

    # --- 追加: 改善度・定量差 ---
    "Our method improved N by N percentage points .",
    "The proposed model achieved a A improvement over the baseline .",
    "The accuracy increased from N to N .",
    "The error rate decreased from N to N .",
    "The proposed approach reduced N by N percent .",
    "The gain was larger when N was A .",
    "The difference corresponds to a relative improvement of N .",
    "This represents an improvement of N over N .",
    "The effect size was A .",
    "The observed difference was both statistically and practically significant .",

    # --- 追加: 信頼区間・検定補足 ---
    "The estimated effect was N , with a confidence interval of N .",
    "The 95% confidence interval did not include N .",
    "The p-value was less than N .",
    "We used bootstrap resampling to estimate uncertainty .",
    "Standard errors are reported in parentheses .",
    "All tests were two-sided .",
    "We corrected for multiple comparisons using N .",
    "The estimated standard error was N .",
    "The effect remained significant after adjusting for N .",
    "The results were robust to different choices of N .",

    # --- 追加: 質的研究・調査 ---
    "A questionnaire was administered to N .",
    "The survey consisted of N items .",
    "Responses were collected on a A scale .",
    "Participants were asked to rate N on a scale from N to N .",
    "Semi-structured interviews were conducted with N .",
    "Interviews lasted an average of N minutes .",
    "Interviews were transcribed and coded using N .",
    "Thematic analysis revealed several recurring patterns .",
    "Participants described N as A and A .",
    "The most frequently cited reason was N .",

    # --- 追加: 実験タスク・手順 ---
    "Participants completed N tasks .",
    "Each trial began with N .",
    "Participants were instructed to V N .",
    "The task was designed to elicit N .",
    "Reaction times were recorded using N .",
    "The experiment consisted of N blocks .",
    "The order of conditions was randomized .",
    "The session lasted approximately N minutes .",
    "Before the experiment , participants provided informed consent .",
    "The experiment was conducted in a controlled environment .",

    # --- 追加: 深層学習・モデル ---
    "The model consists of N layers .",
    "The architecture is based on N .",
    "We fine-tuned the model on N .",
    "The model was trained end-to-end .",
    "Dropout was applied to prevent overfitting .",
    "We used N to regularize the model .",
    "The hidden state was initialized with N .",
    "We used pretrained embeddings for N .",
    "The output layer was designed to predict N .",
    "The model size was varied to examine scalability .",

    # --- 追加: 倫理・再現性 ---
    "The study was approved by N .",
    "Informed consent was obtained from all participants .",
    "All procedures were conducted in accordance with N .",
    "Participant data were anonymized prior to analysis .",
    "The study complies with the ethical guidelines of N .",
    "The code and data are publicly available at N .",
    "Detailed instructions for reproducing the experiments are provided in Appendix N .",
    "We report all experimental settings to facilitate reproducibility .",
    "The authors declare no competing interests .",
    "The replication package is available at N .",

    # --- 追加: 実務・政策含意 ---
    "From a policy perspective , these findings suggest that N V N .",
    "Practitioners may use N to improve N .",
    "These results have direct implications for the design of N .",
    "Organizations seeking to V N may benefit from N .",
    "The findings can inform the development of N .",
    "Policymakers should consider N when designing N .",
    "This approach may be useful in A settings .",
    "The proposed framework can support decision-making in N .",
    "In practice , N can be used to V N .",
    "These insights may help practitioners mitigate N .",

    # --- 追加: 一般化・適用範囲 ---
    "These findings may generalize to other domains of N .",
    "The proposed framework can be adapted to a variety of N .",
    "It is plausible that similar results would be obtained for N .",
    "Further validation is needed to confirm the applicability of N to N .",
    "The approach is applicable to a wide range of N .",
    "The results suggest that N is robust across N .",
    "The method can be extended to A settings .",
    "This framework is not limited to N .",
    "Similar patterns were observed in N and N .",
    "The generalizability of the findings warrants further investigation .",

    # --- 追加: 今後の作業の具体化 ---
    "In future work , we plan to extend N to N .",
    "A natural extension of this work is to V N .",
    "It would be valuable to investigate whether N V N in other domains .",
    "We intend to explore the use of N for N .",
    "Future work could examine the effect of N on N .",
    "We plan to evaluate our approach on A datasets .",
    "A promising direction is to incorporate N into N .",
    "Future studies could compare N with N in A contexts .",
    "We hope to release a larger dataset for N .",
    "Developing A measures of N is left for future work .",

    # --- 追加: 例示・分類 ---
    "Examples of N include N and N .",
    "N can be divided into several categories .",
    "There are three main types of N .",
    "We consider three alternative measures of N .",
    "N can be broadly classified into N and N .",
    "A typical example of N is N .",
    "We distinguish between two forms of N .",
    "The most common form of N is N .",
    "This category includes N such as N .",
    "Each type of N exhibits A characteristics .",

    # --- 追加: 重要性の強調 ---
    "A key finding of this study is that N V N .",
    "The central contribution of this work is N .",
    "The most important insight from our analysis is that N V N .",
    "Of particular interest is the relationship between N and N .",
    "The crucial role of N in N should not be overlooked .",
    "This result underscores the value of N .",
    "These observations highlight the potential of N .",
    "The finding that N V N is especially noteworthy .",
    "This study provides compelling evidence for N .",
    "The implications of this result are far-reaching .",

    # --- 追加: 限定的貢献・予備性 ---
    "While modest , this improvement is consistent across settings .",
    "Although preliminary , these results point to N .",
    "This study offers a first step toward V-ing N .",
    "These findings provide a proof of concept for N .",
    "Our results are suggestive , but further validation is required .",
    "This work should be viewed as an initial exploration of N .",
    "The evidence is promising , but not yet conclusive .",
    "Further work is needed to confirm these early findings .",
    "The current study is exploratory in nature .",
    "These observations warrant further investigation .",

    # --- 追加: よく使われる方法・技術 ---
    "N has been widely used in N .",
    "N is commonly employed to V N .",
    "N has long been recognized as A .",
    "N remains a popular choice for N .",
    "N is often used as a baseline in N .",
    "N is well suited to V-ing N .",
    "N has been shown to be effective for N .",
    "N is particularly useful when N is limited .",
    "This technique is widely adopted in the literature .",
    "The use of N has become standard in this field .",

    # --- 追加: 引用・文献参照表現 ---
    "According to N , N V N .",
    "As noted by N , N V N .",
    "As discussed in N , N V N .",
    "Several authors have emphasized the role of N .",
    "N has argued that N V N .",
    "This view is supported by N .",
    "Similar findings have been reported in N .",
    "This account is consistent with N .",
    "The claim that N V N has been widely discussed .",
    "For a comprehensive review , see N .",

    # --- 追加: 文献の分類・整理 ---
    "The literature on N can be grouped into three broad categories .",
    "Existing approaches to N fall into two main families .",
    "One strand of literature focuses on N .",
    "Another line of research examines N .",
    "A third body of work is concerned with N .",
    "Our work is most closely related to N .",
    "This study complements research on N .",
    "We build on this line of work by examining N .",
    "The present paper differs from this literature in several ways .",
    "This literature provides the starting point for our analysis .",

    # --- 追加: 用語・略語 ---
    "We refer to this phenomenon as N .",
    "This process is commonly referred to as N .",
    "Hereafter , we use N to denote N .",
    "The term N is used throughout this paper .",
    "We adopt the terminology of N .",
    "For brevity , we refer to N as N .",
    "The acronym N stands for N .",
    "We use N and N interchangeably .",
    "The label N is used for convenience .",
    "This concept has been referred to by several names .",

    # --- 追加: 慎重な主張の補強 ---
    "We do not claim that N V N .",
    "Our results do not imply that N V N .",
    "This finding does not rule out the possibility that N V N .",
    "The absence of evidence is not evidence of absence .",
    "No firm conclusion can be drawn from this observation alone .",
    "This result should be regarded as suggestive rather than definitive .",
    "We therefore avoid making strong causal claims .",
    "These observations are correlational in nature .",
    "This should not be taken as evidence that N V N .",
    "The evidence is compatible with multiple explanations .",

    # --- 追加: 研究の全体像・データ戦略 ---
    "The analysis combines N and N .",
    "We draw on data from N sources .",
    "The study integrates evidence from N and N .",
    "The paper brings together insights from N and N .",
    "The study leverages a unique dataset of N .",
    "The research design exploits variation in N .",
    "The empirical strategy relies on N .",
    "The identification strategy is based on N .",
    "The approach exploits differences in N across N .",
    "We triangulate findings across multiple N .",

    # --- 追加: 実験の妥当性・バイアス ---
    "These checks help to rule out alternative explanations .",
    "The findings are unlikely to be driven by N .",
    "We find no evidence that N explains the results .",
    "The design reduces concerns about N .",
    "This strategy helps mitigate concerns related to N .",
    "The main threat to validity is N .",
    "We address this concern by V-ing N .",
    "The use of N strengthens the internal validity of the study .",
    "The external validity of the findings is supported by N .",
    "Potential sources of bias include N .",

    # --- 追加: 応用分野・実装価値 ---
    "The proposed approach has applications in N .",
    "This method may be useful for N .",
    "The framework can be applied to tasks such as N .",
    "Our results are relevant to researchers working on N .",
    "The findings may benefit practitioners in N .",
    "This technique is particularly promising for N .",
    "The approach can support A decision-making in N .",
    "The results are applicable to a range of A scenarios .",
    "This work has potential implications for N .",
    "The method could be deployed in real-world N .",

    # --- 追加: データ可用性・補足資料 ---
    "The dataset used in this study is available from the authors upon request .",
    "Additional material is available in the supplementary appendix .",
    "Further details are provided in the online supplementary material .",
    "The full list of N is provided in Appendix N .",
    "All tables and figures are available in the supplementary material .",
    "The questionnaire is reproduced in Appendix N .",
    "Additional experiments are reported in the appendix .",
    "The code used for analysis is available upon request .",
    "The replication package is available at N .",
    "Supplementary analyses are available online .",

    # --- 追加: アルゴリズム・最適化 ---
    "The procedure is summarized in Algorithm N .",
    "Algorithm N describes the proposed method .",
    "The model is trained by minimizing N .",
    "The parameters are updated using N .",
    "At each step , the algorithm computes N .",
    "The output of the algorithm is N .",
    "The complexity of the algorithm is N .",
    "The optimization problem can be solved using N .",
    "The update rule is given by N .",
    "The inference procedure is outlined below .",

    # --- 追加: 具体例・シナリオ ---
    "Consider a setting in which N V N .",
    "Suppose that N V N .",
    "In a typical scenario , N V N .",
    "For example , N may V N .",
    "To illustrate , consider the case of N .",
    "Imagine a situation where N is A .",
    "In such cases , N tends to V N .",
    "This situation is common in N .",
    "This example highlights the relevance of N .",
    "A similar pattern can be observed in N .",

    # --- 追加: 比較研究の位置づけ ---
    "Our work complements previous studies by focusing on N .",
    "Whereas prior work has examined N , we focus on N .",
    "Unlike earlier studies , we use N to measure N .",
    "This paper extends previous research in two important ways .",
    "First , we consider N . Second , we analyze N .",
    "This study differs from previous work by using A data .",
    "Our analysis goes beyond N by incorporating N .",
    "We improve upon previous approaches by V-ing N .",
    "The present study addresses a limitation of previous work .",
    "Our findings confirm and extend earlier results .",

    # --- 追加: 主張・論点の提示 ---
    "We make three main claims .",
    "The central argument of this paper is that N V N .",
    "Our analysis yields two key insights .",
    "The first insight is that N V N .",
    "The second insight is that N V N .",
    "This paper argues that N V N .",
    "We contend that N V N .",
    "The evidence supports the view that N V N .",
    "Our position is that N V N .",
    "This claim is supported by N .",

    # --- 追加: 結果の提示順序 ---
    "We first present the results for N .",
    "We then turn to the analysis of N .",
    "Next , we examine the relationship between N and N .",
    "Finally , we report the results of the robustness checks .",
    "We begin by describing N .",
    "Before presenting the results , we describe N .",
    "The analysis is organized around three questions .",
    "We address each question in turn .",
    "The results are presented in the order of the hypotheses .",
    "We proceed as follows .",

    # --- 追加: 研究の焦点 ---
    "Our analysis focuses on N .",
    "We concentrate on N because N V N .",
    "The central focus of this paper is N .",
    "We pay particular attention to N .",
    "Special attention is given to N .",
    "We devote particular attention to N .",
    "The emphasis is on N .",
    "We are primarily interested in N .",
    "The key variable of interest is N .",
    "Our main interest lies in the relationship between N and N .",

    # --- 追加: 数値結果の記述 ---
    "The mean value of N was N .",
    "The standard deviation was N .",
    "N ranged from N to N .",
    "The median value was N .",
    "The maximum value of N was N .",
    "The minimum value of N was N .",
    "The proportion of N was N percent .",
    "The prevalence of N was N percent .",
    "The incidence of N increased from N to N .",
    "The average score on N was N .",
]
# --- ここから差分: 既存のTEMPLATESリストの末尾に追加 ---
TEMPLATES += [

    # --- 0. 超頻出の掴み・問題提起 (Introduction Opener) ---
    "The role of N in N has been extensively studied in recent years .",
    "Understanding the relationship between N and N is crucial for N .",
    "N is a fundamental component of N .",
    "The ability to V N is essential for A N .",
    "Despite its importance , N remains a challenging problem in the field of N .",
    "N has been recognized as a major bottleneck for N .",
    "Recent advances in N have enabled the development of A N .",
    "The emergence of N has opened up new opportunities for V-ing N .",
    "There is an urgent need for A methods to V N .",
    "N is characterized by A N and A N .",

    # --- 1. 先行研究の批判的レビュー (Critical Review) ---
    "However , most existing studies on N fail to consider N .",
    "A major drawback of previous approaches is their inability to V N .",
    "Existing methods for N suffer from A N .",
    "The majority of prior work has overlooked the importance of N .",
    "While N has been widely adopted , its effectiveness in A N remains questionable .",
    "A critical limitation of N is that it does not account for N .",
    "Previous approaches typically assume that N is A , which may not hold in practice .",
    "Despite promising results , N is computationally expensive and difficult to scale .",
    "The applicability of N to A N is limited by N .",
    "Most prior work treats N as A , ignoring its A nature .",

    # --- 2. 本研究の貢献・差別化 (Contribution / Novelty) ---
    "In contrast to previous studies , this study focuses on N .",
    "The key contribution of this work is to introduce a novel N for V-ing N .",
    "Unlike previous methods , our approach does not require A N .",
    "Our work provides the first comprehensive analysis of N .",
    "We present a new perspective on N by considering N .",
    "This paper presents a unified framework for V-ing N .",
    "The novelty of our approach lies in its ability to V N and V N simultaneously .",
    "Our method is distinguished by its use of A N to V N .",
    "We propose a simple yet effective N that significantly improves N .",
    "This study is the first to demonstrate that N can V N .",
    "Our approach bridges the gap between A N and A N .",
    "We introduce the concept of A N to better capture N .",
    "A central contribution of this paper is the introduction of N .",
    "Our work sheds new light on the role of N in N .",

    # --- 3. 方法の概要・直感 (Method Overview) ---
    "The core idea behind our approach is to V N using N .",
    "Our method consists of two main components: N and N .",
    "At a high level , our N works by V-ing N to V N .",
    "The proposed N is built upon the observation that N V N .",
    "We formulate the problem of N as a A N problem .",
    "The key insight is that N can be V-ed as N .",
    "Our approach leverages A N to effectively V N .",
    "We design a novel N that explicitly models N .",
    "The architecture of our N is illustrated in Figure N .",
    "We decompose N into a set of A subproblems .",
    "The intuition behind N is that A N tends to V N .",
    "Our framework jointly learns to V N and V N .",

    # --- 4. 実装・詳細・数式導入 (Implementation Details) ---
    "We denote the set of N as N .",
    "Let N be a A N that V N .",
    "Formally , the objective is to minimize N with respect to N .",
    "The loss function is composed of two terms: N and N .",
    "We use N to represent the A N of N .",
    "The parameter N controls the trade-off between N and N.",
    "We initialize N with A N .",
    "The training procedure is summarized in Algorithm N .",
    "We adopt a A N to model the relationship between N and N .",
    "Each N is encoded into a A representation using N .",
    "We apply A normalization to ensure that N is A .",
    "The final N is obtained by aggregating N across A N .",

    # --- 5. 実験設定の厳密化 (Experimental Setup) ---
    "We evaluate our method on a wide range of A benchmarks .",
    "All experiments were conducted on N with A N .",
    "We follow the standard evaluation protocol used in N .",
    "For fair comparison , all N were implemented using A N .",
    "We use N as the primary evaluation metric .",
    "The dataset is split into N , N , and N for training , validation, and testing, respectively .",
    "We report the average performance over N independent runs .",
    "To ensure reproducibility , we fix the random seed to N .",
    "We tune hyperparameters via grid search on the validation set .",
    "The computational cost is measured in terms of N and N .",
    "We compare against N state-of-the-art baselines , including N and N .",

    # --- 6. 結果の客観的報告 (Results Reporting) ---
    "Our method achieves state-of-the-art performance on N .",
    "As shown in Table N , our N outperforms N by a large margin .",
    "The proposed method yields a consistent improvement across all N .",
    "We observe a significant improvement in N when using A N .",
    "The performance gap between N and N widens as N increases .",
    "Our model achieves comparable performance with significantly fewer N .",
    "The results demonstrate the effectiveness of our approach in V-ing N .",
    "We find that N is highly effective for V-ing N .",
    "The benefit of N is particularly evident when N is A .",
    "Our approach achieves a new state-of-the-art result of N on N .",

    # --- 7. 詳細分析・アブレーション (Ablation / Analysis) ---
    "To better understand the effect of N , we conduct an in-depth analysis of N .",
    "We investigate the impact of varying N on N .",
    "As expected, increasing N leads to A N in N .",
    "The results suggest that N is a crucial factor for A N .",
    "We find that removing N causes a substantial performance degradation .",
    "Interestingly, replacing N with N has little effect on N .",
    "The analysis reveals that A N contributes most to the overall performance .",
    "We observe a trade-off between N and N .",
    "The performance saturates when N exceeds N .",
    "This confirms that our N effectively captures N .",
    "We further break down the results by N to examine A differences .",

    # --- 8. 考察・示唆・一般化 (Discussion) ---
    "This finding is consistent with the notion that N V N .",
    "One plausible explanation for this phenomenon is that N V N .",
    "This suggests that N plays a more important role than previously thought .",
    "The observed trend can be attributed to the fact that N is A .",
    "These results imply that N should be taken into account when V-ing N .",
    "Our findings challenge the conventional assumption that N is A .",
    "This highlights the importance of N in achieving A N .",
    "We attribute the success of N to its ability to V N .",
    "This observation is in agreement with findings reported in N .",
    "A deeper understanding of N may lead to more A N .",
    "This indicates that N and N are complementary to each other .",

    # --- 9. 限界の丁寧な言い方 (Limitations - polite) ---
    "It is worth noting that our analysis is limited to A N .",
    "Our current implementation does not explicitly handle N .",
    "The effectiveness of N may depend on the quality of N .",
    "A limitation of this study is the lack of experiments on A N .",
    "We leave the exploration of N for future work .",
    "Due to computational constraints , we were unable to evaluate N on A N.",
    "Our method assumes that N is available, which may not always be the case .",
    "The interpretation of N is subject to A N .",
    "While our approach is effective , it may not generalize to A settings .",

    # --- 10. 結論の強い言い回し・将来展望 (Conclusion / Future Work) ---
    "In this paper , we have presented a novel approach to V-ing N .",
    "We have shown that N can be effectively V-ed by leveraging N .",
    "Our work opens up several avenues for future research on N .",
    "We believe that our findings will inspire further research into N .",
    "We hope that this work will serve as a basis for future studies on N .",
    "A promising direction for future research is to extend N to A N .",
    "In the future , we plan to investigate the application of N to N .",
    "To conclude , this study demonstrates the potential of N for V-ing N .",
    "Overall , this work provides valuable insights into N .",
    "We envision that N will become a standard component of A N .",

    # --- 11. 引用・位置づけの便利フレーズ (Citation Phrases) ---
    "Following N , we define N as N .",
    "Inspired by recent work on N , we propose to V N .",
    "Our work is closely related to N , which also focuses on N .",
    "Similar to N, we adopt a A N approach .",
    "Building upon the work of N , we extend N to A N .",
    "In line with N , we hypothesize that N V N .",
    "As argued by N , N is crucial for V-ing N .",
    "For a thorough survey of N , we refer readers to N .",
    "The idea of V-ing N has been previously explored in N .",
    "Our formulation generalizes that of N by incorporating N .",

    # --- 12. 図表・付録への言及 (Figure / Appendix) ---
    "We provide a detailed illustration of N in Figure N .",
    "The overall pipeline of our approach is depicted in Figure N .",
    "Table N presents a comparison of different N in terms of N.",
    "The statistics of the N are summarized in Table N .",
    "We include additional qualitative results in Appendix N .",
    "For implementation details , please refer to Appendix N .",
    "A detailed proof of N is provided in Appendix N .",
    "We refer to the supplementary material for more examples of N .",
    "An overview of the notation used in this paper is provided in Table N .",
    "The pseudo-code for V-ing N is given in Algorithm N .",
]

STATE_FILE = "data/state.json"
README_FILE = "README.md"

# 論文らしい大見出しのリスト
SECTIONS = [
    "## Introduction",
    "## Literature Review",
    "## Methodology",
    "## Results",
    "## Discussion",
    "## Conclusion",
    "## Future Work"
]


def modify_word(word, form):
    """
    テンプレート側の指定 (ing, ed, s など) に合わせて、英単語を簡易的に活用させる
    """
    if not word:
        return word
        
    # 小文字化して判定（出力時に大文字化されることは呼び出し元で制御）
    lower_word = word.lower()
    
    if form == 'ing':
        # 例: make -> making
        if lower_word.endswith('e') and not lower_word.endswith(('ee', 'oe', 'ye')):
            return word[:-1] + 'ing'
        # 例: stop -> stopping, run -> running (短母音＋子音の簡易判定)
        elif len(lower_word) >= 3 and lower_word[-1] not in 'aeiouwxy' and lower_word[-2] in 'aeiou' and lower_word[-3] not in 'aeiou':
            return word + word[-1] + 'ing'
        return word + 'ing'
        
    elif form == 'ed':
        # 例: analyze -> analyzed
        if lower_word.endswith('e'):
            return word + 'd'
        # 例: apply -> applied
        elif lower_word.endswith('y') and len(lower_word) >= 2 and lower_word[-2] not in 'aeiou':
            return word[:-1] + 'ied'
        # 例: stop -> stopped
        elif len(lower_word) >= 3 and lower_word[-1] not in 'aeiouwxy' and lower_word[-2] in 'aeiou' and lower_word[-3] not in 'aeiou':
            return word + word[-1] + 'ed'
        return word + 'ed'
        
    elif form in ['s', 'es']:
        # 例: focus -> focuses, catch -> catches
        if lower_word.endswith(('s', 'x', 'z', 'ch', 'sh', 'o')):
            return word + 'es'
        # 例: study -> studies
        elif lower_word.endswith('y') and len(lower_word) >= 2 and lower_word[-2] not in 'aeiou':
            return word[:-1] + 'ies'
        return word + 's'
        
    # 未知の接尾辞の場合はハイフンをつけてそのまま結合
    return word + "-" + form

def load_words(csv_path):
    # どんな品詞タグが来ても対応できるように defaultdict を使用
    words = defaultdict(list)
    
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Using dummy data.")
        return {
            'N': ['system', 'model', 'data'], 
            'V': ['analyze', 'process', 'stop', 'apply'], 
            'A': ['novel', 'robust'], 
            'ADV': ['rapidly', 'accurately']
        }
        
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # words.csv 内に 'pos' キーと 'word' キーがあることを前提
            if 'pos' in row and 'word' in row:
                words[row['pos']].append(row['word'])
    return words

def generate_sentence(words_dict):
    template = random.choice(TEMPLATES)
    tokens = template.split()
    sentence_tokens = []
    
    for token in tokens:
        # 1. 完全に一致する品詞タグ (N, V, A など) の場合
        if token in words_dict and words_dict[token]:
            sentence_tokens.append(random.choice(words_dict[token]))
            
        # 2. V-ing や N-s など、ハイフンで活用が指定されている場合
        elif '-' in token:
            base_pos, form = token.split('-', 1)
            # base_pos (例: V) が辞書に存在すれば、その単語を取得して活用させる
            if base_pos in words_dict and words_dict[base_pos]:
                base_word = random.choice(words_dict[base_pos])
                conjugated_word = modify_word(base_word, form)
                sentence_tokens.append(conjugated_word)
            else:
                sentence_tokens.append(token)
                
        # 3. それ以外 (The, by, ピリオドなど)
        else:
            sentence_tokens.append(token)
            
    return sentence_tokens

def generate_subsection_title(words_dict):
    """
    words.csvの単語を使って、論文らしいサブセクションを生成する
    例: ### Robust Model
    """
    adj = random.choice(words_dict['A']).capitalize() if 'A' in words_dict and words_dict['A'] else "Advanced"
    noun = random.choice(words_dict['N']).capitalize() if 'N' in words_dict and words_dict['N'] else "Method"
    return f"### {adj} {noun}"

def main():
    words_dict = load_words("data/words.csv")
    
    buffer = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            buffer = json.load(f)
            
    # 一度に生成する文の量を増やして、内容を素早く濃くする
    while len(buffer) < 90:
        buffer.extend(generate_sentence(words_dict))
        
    output_tokens = buffer:90]
    buffer = buffer[90:]
    
    # READMEを読み込む（なければ新規作成）
    if os.path.exists(README_FILE):
        with open(README_FILE, "r", encoding="utf-8") as f:
            readme_content = f.read()
    else:
        readme_content = "# Abstract\n\n"

    total_sentence_count = readme_content.count('.')
    capitalize_next = True # 文頭の単語を大文字にするためのフラグ
    
    # 【追加】現在進行中の「章のタイトル」を保持。最初は Abstract に設定。
    current_section_title = "Abstract"

    for token in output_tokens:
        if token in [".", ",", ";", ":"]:
            # 記号の前のスペースを削除して結合
            readme_content = readme_content.rstrip() + token
            
            # ピリオド（文末）の場合の処理
            if token == ".":
                total_sentence_count += 1
                capitalize_next = True # 次の単語は大文字にする
                
                # 現在の段落に含まれる文の数を計算
                last_paragraph = readme_content.split("\n\n")[-1]
                sentences_in_current_para = last_paragraph.count('.')
                
                # 1. 大セクション区切り
                if total_sentence_count > 0 and total_sentence_count % 700 == 0:
                    section_idx = (total_sentence_count // 700) % len(SECTIONS)
                    section_text = SECTIONS[section_idx]
                    readme_content += f"\n\n{section_text}\n\n"
                    
                    # 【追加】大セクションのタイトルに更新（#や前後の空白を除外）
                    current_section_title = section_text.replace('#', '').strip()
                
                # 2. 段落の区切り（3〜5文に達したらアクションを起こす）
                elif sentences_in_current_para >= random.randint(3, 5):
                    rand_action = random.random()
                    
                    # 【追加】段落の区切りで、5%の確率で画像を挿入する
                    if random.random() < 0.05:
                        # スペースなどをURLセーフな形にエンコード
                        safe_title = urllib.parse.quote(current_section_title)
                        readme_content += f"![{current_section_title}](https://usercontent.haruharutv.jp/gen/IMG_{safe_title}.png)\n\n"
                    
                    # 9%の確率で「箇条書き」を生成
                    if rand_action < 0.09:
                        readme_content += "\n\n"
                        bullet_count = random.randint(3, 5)
                        for _ in range(bullet_count):
                            bullet_tokens = generate_sentence(words_dict)
                            bullet_text = " ".join(bullet_tokens).replace(" ,", ",").replace(" .", ".")
                            readme_content += f"- {bullet_text.capitalize()}\n"
                        readme_content += "\n"
                        
                    # 20%の確率で「サブセクション」を生やす
                    elif rand_action < 0.50:
                        subsection_title = generate_subsection_title(words_dict)
                        readme_content += f"\n\n{subsection_title}\n\n"
                        
                        # 【追加】サブセクションが生成されたら、現在の章タイトルを更新する
                        current_section_title = subsection_title.replace('#', '').strip()
                        
                    # それ以外は通常の段落区切り
                    else:
                        readme_content += "\n\n"
        else:
            # 単語の追加
            if capitalize_next:
                readme_content += token.capitalize() + " "
                capitalize_next = False
            else:
                readme_content += token + " "
                
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    # dataディレクトリがない場合のエラー防止
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(buffer, f)

if __name__ == "__main__":
    main()
