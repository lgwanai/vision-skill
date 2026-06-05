# 海报与排版

> Template Anchor: `tpl-poster`

### 海报与排版

**常规模板**

```text
设计一张[活动/产品/电影]海报，主题为[主题词]。
主视觉：[主体元素]，标题文案：[标题]，副标题：[副标题]。
版式：[居中/左对齐/对角构图]，风格：[复古/未来/极简]。
色彩：[主色 + 辅色]，氛围：[情绪关键词]。
输出：可用于社媒传播的高分辨率海报。
```

**运动商业 Campaign 模板**

```text
设计一张[运动项目/健身品类]商业 Campaign 海报。
主体：[运动员/模特/产品道具]，姿态：[坐姿/冲刺/挥拍/力量动作]。
核心道具：[球拍/哑铃/球鞋/球衣]，以夸张比例或对角构图成为视觉锚点。
版式：[单张强主视觉/三联画/数据涂鸦海报]。
大字标题："[主标题]"，辅助文案："[短句/数据/精神口号]"。
视觉风格：高端运动品牌广告，强光影，反光地面，干净构图，品牌化配色[主色+辅助色]。
约束：主体清晰，文字可读，色调统一，不要杂乱拼贴，不要生成错误运动器材。
输出：1:1 或 4:5，适合社媒传播的运动商业视觉。
```

**概念字体海报模板**

```text
Create ONE finished premium conceptual typography poster for the exact title:

"[标题/词语/短句]"

Single poster only. No moodboard, grid, presentation board, mockup, captions, prompt text, process sheet, or sample labels.

The title must be the dominant visual structure of the poster: huge, readable, powerful, and spelled exactly. Do not translate, shorten, replace, or misspell it. Do not add other large readable text.

Silently interpret the title's meaning, mood, cultural aura, symbolic associations, psychological tension, and visual rhythm. Turn that interpretation into one strong visual metaphor.

Typography is the hero. Design custom-looking letterforms whose weight, width, contrast, spacing, rhythm, distortion, negative space, edge quality, and ink texture express the temperament of the title. The type should feel intentionally designed, not like a default font.

If the title refers to a widely known person, make a large editorial portrait or half-body figure a major visual presence, occupying roughly 40%-70% of the composition. The figure should interact with the typography: overlapping the letters, emerging from them, being framed by them, casting shadows on them, breaking through them, or being partially hidden behind them.

For abstract or non-person titles, use a human figure, landscape, object, or atmospheric setting only when it strengthens the meaning. It must interact with the typography and deepen the concept, not decorate it.

Use a restrained 4-6 color system matched to the theme: dominant background color, primary typography color, figure / landscape tone, emotional accent color, muted support color, and subtle paper / ink texture tone.

Composition style: high-end editorial poster, museum-quality graphic design, dramatic scale, strong hierarchy, few elements, intelligent whitespace, bold flat color areas, sharp cropping, silkscreen / lithograph / risograph grain, paper fibers, subtle ink imperfections, refined visual tension.

Avoid generic word art, glossy 3D lettering, random icons, stock-photo realism, cluttered collage, excessive grunge, tourist clichés, official logos, copied slogans, copied campaign aesthetics, unrelated text, and misspelled typography.
```

**多风格签名选择海报模板**

> 来源参考：[signature-image-prompts-gpt-image-2.md](https://github.com/zaizhi-1112/ai-image-extension-playbook/blob/main/signature-image-prompts-gpt-image-2.md) / [@liyue_ai](https://x.com/liyue_ai)

```text
你是一个高端签名设计系统 + 风格人格视觉系统。

输入：
姓名：[姓名/昵称]

任务：
基于姓名自动生成一张 9:16 竖版「多风格签名选择海报」。
目标是把姓名转译成 6 种具有笔势、气质和力量感的签名方案。

隐藏分析：
1. 分析姓名字形：疏密、横竖比例、重心、连笔空间、草写空间。
2. 推断气质：清冷、张扬、克制、商业、文艺、松弛、锋利、高级。
3. 为每个签名先设定书写行为：起笔、连笔、节奏、结构变形、收笔。

版式：
- 纯白或极浅灰渐变背景，留白不少于 40%
- 顶部大标题：[姓名] · 签名风格选择
- 副标题：不同笔势，不同气场
- 中部使用 2 列 × 3 行卡片网格
- 底部小字：选一个，作为你的专属签名。

卡片规范：
- 每张卡片统一尺寸、统一间距、整体对齐
- 轻微圆角 8-16px
- 极细描边或无边框
- 极轻阴影
- 纯白微差、极浅灰、宣纸或磨砂质感
- 视觉目标接近高级杂志排版，避免强 UI 感

6 种签名：
1. 极简理性：接近品牌签名，笔画克制，留白清晰
2. 狂放张力：强连笔，速度感强，尾笔拉伸
3. 松弛随性：手写感明显，自然舒展，亲和轻松
4. 东方行草：飞白、墨感、节奏起伏明显
5. 锋利结构：几何切角，断裂感，冷静克制
6. 实验风格：部分不可读，结构重塑，先锋个性

每张卡片必须包含：
- 编号
- 风格名称
- 大尺寸签名
- 一句短气质说明
- 一个极轻微点缀色

光影与质感：
高级棚拍光、柔光环境、细腻阴影、干净空气感。
整体以黑、灰、白为主，点缀色克制。

禁止项：
不要字体拼贴，不要普通书法字，不要颜色杂乱，不要签名太小，不要排版松散，不要缺乏笔势，不要模板拼接感。
```

**单款签名提取模板**

```text
从输入图中的[位置/编号/风格名]签名里，提取该签名的核心笔势，生成一张纯签名图。

要求：
- 只保留签名主体，不生成海报卡片、标题、副标题或说明文字
- 保留原签名的起笔、连笔、结构倾斜、飞白和收笔节奏
- 背景为纯白或极浅米白
- 签名居中，尺寸充足，边缘留白干净
- 墨色为深黑或墨黑，带自然笔锋、轻微墨痕和真实手写压力变化
- 输出适合继续临摹、收藏或二次设计的高清纯签名图

避免：
不要新增多种签名，不要变成字体展示，不要加边框，不要加装饰元素，不要弱化原有笔势。
```

**签名练习拆解图模板**

```text
基于输入的[签名图/签名风格]，生成一张签名练习拆解图。

目标：
帮助用户用黑笔在纸上练好这个签名，拆解每一笔的书写路径、顺序、力度和节奏。

画面结构：
- 竖版教学图或横版练习板
- 顶部放最终签名小样
- 中部用 8-12 个步骤拆解关键笔画
- 每个步骤展示当前笔画、运动方向箭头、起笔点、停顿点、收笔点
- 下方展示完整连写路径和 3-5 行练习建议

拆解要求：
- 每一笔都要对应签名主体中的真实笔势
- 标出快写、慢写、重压、轻提、转折、回钩、飞白、长甩尾
- 展示从基础骨架到完整签名的渐进过程
- 说明字间连接逻辑和整体重心变化

视觉风格：
白纸背景、黑色手写线条、红色或蓝色教学箭头、清晰编号、练习册质感。

避免：
不要只给成品图，不要省略关键笔画，不要把步骤画成随机涂鸦，不要生成无关书法字帖。

**中文版：概念字体海报模板**

```text
为以下标题生成一张完成度极高的高级概念字体海报，只需要一张。

标题：「[标题/词语/短句]」

只需要一张海报。不要 moodboard、不要网格排版、不要展示板、不要样机、不要说明文字、不要过程稿、不要样张标签。

标题必须是海报的主视觉结构：巨大、可读、有力量、拼写完全正确。不要翻译、缩短、替换或拼错标题。不要添加其他大段可读文字。

深入理解标题的含义、情绪、文化氛围、符号关联、心理张力和视觉节奏。把这种理解转化成一个强有力的视觉隐喻。

字体是主角。设计定制的字形，其字重、字宽、对比度、间距、节奏、变形、负空间、边缘质感和墨迹纹理必须表达标题的气质。字体应该看起来经过精心设计，而不是一个默认字体。

如果标题指向一个广为人知的人物，让一个大型编辑肖像或半身人物成为主要的视觉存在，占据构图的 40%-70%。人物必须与字体互动：重叠字母、从字母中浮现、被字母框住、在字母上投下阴影、打破字母、或部分隐藏在字母后面。

对于抽象或非人物标题，只有当人像、风景、物体或氛围场景能强化意义时才使用。它必须与字体互动并深化概念，而不是装饰它。

使用受限制的 4-6 色调色板来匹配主题：主背景色、主字体色、人物/风景色调、情感强调色、柔和辅助色、微妙的纸张/墨迹纹理色。

构图风格：高端编辑海报、博物馆级平面设计、戏剧性尺度、强层级、少元素、聪明留白、大胆平色区域、锐利裁切、丝网/平版/孔版印刷颗粒、纸纤维、微妙油墨瑕疵、精炼视觉张力。

避免：通用字效、光泽 3D 字体、随机图标、素材库写实、杂乱拼贴、过度脏旧、旅游明信片陈词滥调、官方标志、抄袭标语、抄袭 Campaign 美学、无关文字和拼写错误的字体。

```

**水墨双重曝光人物海报模板**

```text
生成一张[人物/角色/品牌主理人/运动员]的水墨双重曝光人物海报。
画幅：9:16 竖版，高级电影海报构图。
主体结构：
- 上半区：放大的人物头部、面部轮廓或半身剪影，形成最强识别锚点。
- 中下区：同一人物的全身或半身主体，姿态为[站姿/动作姿态/凝视镜头]。
- 剪影内部：融合[关键场景]、[象征物]、[叙事片段]、[环境纹理]，形成双重曝光叙事。
视觉连接：用云雾、水墨扩散、飞白边缘、负空间和柔和明暗过渡，把上方剪影、内部拼贴和下方主体连成一条从上到下的视觉动线。
风格：东方水墨美学 + 写实电影感，克制、高级、留白充足，层次丰富但不杂乱。
文字：可加入[标题/姓名/短句]，必须少量、可读、像海报题签而不是信息图说明。
约束：不要硬拼贴，不要把背景塞满，不要廉价武侠特效，不要复制真实海报版式，不要让剪影和主体互相抢焦点。
输出：海报级完成图，主体清晰，水墨边缘自然，叙事元素与人物身份强相关。
```

**自然科普海报模板**

```text
你是一个高端自然科普海报生成系统，目标是为稀有动物、昆虫、爬行动物、哺乳动物或其他小众生物生成 Apple keynote 风格的高级科普视觉海报。

整体视觉方向：
生成一张 9:16 竖版高级科普海报，画面采用极简、纯白、干净、现代、Apple 式产品发布海报语言。背景应为纯白或极浅灰白渐变，保持大量留白。整体设计应具备高级感、克制感、视觉冲击力和科学展示感。

核心设计原则：
1. 主体动物必须被极度放大，成为画面最强视觉中心。
2. 主体应具有强烈立体感、真实质感、高清细节和柔和棚拍光影。
3. 海报信息要少而准，避免拥挤。
4. 不使用传统信息图的卡片、圆角框、复杂底纹、淡黄色纸张质感或装饰性边框。
5. 底部信息区只使用四列极简 icon + 标题 + 短说明，通过细竖线分隔。
6. 文字排版要像高端发布会视觉，标题巨大，副标题克制，正文小而清晰。
7. 风格关键词：Apple-inspired, premium editorial, pure white background, hero subject, clean typography, minimal infographic, high-end science poster.

画面结构：
顶部左侧为标题区：
中文大标题：{中文物种名}
中文副标题：{一句有吸引力的物种定位}
细短横线
英文名：{英文物种名}
分布信息：主要分布：{分布区域}

中部与下中部为主体视觉：
生成一个超高清、真实、具有强烈立体感的 {中文物种名}。
主体应占据画面 50% 到 70% 的视觉面积。
主体姿态应具有展示性、力量感或识别度。
保持白色背景，不添加复杂自然环境。
可以保留少量必要承托物，例如树枝、岩石、雪地、沙土或木皮，但必须简洁。
主体要有真实阴影，使其像高级产品摄影一样立在画面中。

底部信息区：
用四个极简信息栏目展示科普信息。
每个栏目包含：
一个细线 icon
一个彩色小标题
一段 1 到 3 行短文字
栏目之间用极细浅灰竖线分隔。
不使用卡片框，不使用圆角背景，不使用大面积色块。

四个信息栏目：
栏目 1：
标题：{重点特征1标题}
说明：{重点特征1短说明}

栏目 2：
标题：{重点特征2标题}
说明：{重点特征2短说明}

栏目 3：
标题：{重点特征3标题}
说明：{重点特征3短说明}

栏目 4：
标题：{重点特征4标题}
说明：{重点特征4短说明}

底部总结句：
在最底部居中放置一句灰色小字总结：
{一句高级、克制、有记忆点的科普总结}

字体与排版：
中文标题使用大号黑色、高级、稳重、有力量感的字体。
副标题使用灰色，中等字号，字距略宽。
英文名使用小号灰色，简洁现代。
正文使用清晰现代中文字体，保持可读。
所有文字必须留有足够呼吸感。

色彩规范：
背景：纯白、极浅灰、轻微柔光渐变。
主标题：黑色或深石墨色。
副标题与正文：中性灰。
底部四个信息标题可使用低饱和强调色：
暖棕、冷蓝、松石绿、紫色、橙色。
颜色只用于 icon 和小标题，不要大面积铺色。

图像质量：
2K 高清质感，细节清晰，主体锐利，光影真实。
主体纹理必须可信，例如毛发、鳞片、甲壳、皮肤褶皱、羽毛或斑纹。
避免变形、错误肢体、错误解剖结构、模糊主体、低质贴图、塑料感、卡通感。

禁止项：
不要使用淡黄色旧纸背景。
不要使用复杂信息图网格。
不要使用圆角卡片。
不要使用厚边框。
不要使用大面积装饰图形。
不要添加无关 logo。
不要添加多余小字。
不要让主体太小。
不要让文字压住主体。
不要让底部信息区过度拥挤。
不要出现儿童科普风、卡通风、低端展板风。

最终输出：
生成一张 9:16 竖版、高级、干净、强视觉冲击的 Apple 风自然科普海报。
```

**JSON 进阶模板（推荐给 Agent 调用）**

```json
{
  "type": "Movie Poster",
  "theme": "Interstellar Journey",
  "typography": {
    "headline": "BEYOND STARS",
    "subheading": "A New Era Begins",
    "layout": "Centered, bold cinematic font, bottom heavy"
  },
  "visuals": {
    "subject": "Silhouette of an astronaut looking at a glowing nebula",
    "style": "Cinematic lighting, high contrast, dramatic shadows",
    "color_palette": "Deep space blue, glowing orange accents"
  },
  "vibe": "Epic, mysterious, vast"
}
```

**避坑指南**

- **不要偷懒**：写清“主视觉到底是什么玩意儿”，不要只丢一句“做一张海报”就指望出神图。
- **文案硬编码**：主标题与副标题都要写死，否则模型会给你疯狂加戏，自动瞎编不知所云的文字。
- **运动海报先定结构**：运动 Campaign 最容易变成杂乱拼贴，先锁定“单主视觉 / 三联画 / 数据涂鸦”再写主体和文案。
- **道具要当构图骨架**：球拍、哑铃、球鞋这类道具最好指定角度、比例和位置，否则模型容易把它们画成普通背景装饰。
- **字体海报先锁标题**：概念字体海报必须明确“标题必须拼写完全正确且成为主视觉”，否则很容易变成漂亮但不可读的字效图。
- **图像要和字互动**：人物、物体或场景必须嵌入、遮挡、穿过或托起字形，只摆在旁边会像装饰素材。
- **禁止 moodboard 化**：明确要求 single poster only，避免模型生成多方案展示板、过程稿或样张拼贴。
- **主体放大**：自然科普海报中，主体动物必须被极度放大，占据画面 50%-70% 的视觉面积，确保成为最强视觉中心。
- **信息克制**：遵循“少而准”原则，底部信息区只使用四列极简布局，避免信息拥挤和视觉混乱。
- **风格统一**：严格遵循 Apple 式极简风格，使用纯白背景、干净排版和柔和棚拍光影，避免传统信息图的卡片、圆角框等元素。
