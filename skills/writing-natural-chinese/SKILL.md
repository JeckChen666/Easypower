---
name: writing-natural-chinese
description: Use whenever producing Chinese user-facing explanations, progress updates, reviews, specifications, plans, or technical and business documents. Keep established professional or project-specific terms in English, add a concise contextual Chinese gloss on first occurrence as English（中文）, and avoid literal translation or unnatural mixed-language phrasing.
---

# 自然技术中文

使用自然中文组织句子，保留行业和项目中已经稳定使用的英文术语。不要把英文流程名逐字翻译成生硬中文。

## 术语规则

- 专业术语、协议名、状态名或项目约定词用英文更准确时，保留英文。
- 首次出现写成 `English（中文意译）`，例如 `Schema（数据结构）`、`Agent Brief（任务说明）`。中文说明应解释当前语境，不追求字典直译。
- 后文固定使用同一个英文词或已约定的中文简称，不重复加括号，不混用多套译名。
- API、JSON、HTML 等通用缩写在含义清楚时无需补译；代码标识、命令、路径、字段名和原文引用保持原样。
- 状态名保留英文原值，并在定义处补中文，例如 `Blocked（受阻）`。

## 表达规则

- 普通动作和判断使用日常中文。把“计算 Frontier”写成“根据依赖关系更新 Frontier（当前可执行任务）”，把“网络接缝”写成“网络边界”。
- 保留必要英文，不堆叠英文。普通词有清楚中文说法时直接用中文。
- 使用具体主语、动作和结果，删除讲义腔、空泛总结和为了显得专业而增加的术语。
- 优先沿用用户用词和项目术语表；用户指定语言或格式时，以用户要求为准。

输出前检查首次释义、术语一致性和直译句式。只调整表达，不改变事实、业务规则、代码语义或批准状态。
