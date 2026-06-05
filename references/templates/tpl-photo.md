# 摄影与写实

> Template Anchor: `tpl-photo`

### 摄影与写实

**常规模板**

```text
拍摄主题：[人物/物品/街景]，场景为[地点]。
摄影参数风格：[35mm/85mm]，[浅景深/深景深]，[纪实/电影感]。
光线：[自然光/夜景霓虹/逆光]，情绪：[情绪词]。
细节要求：[肤质/材质/颗粒感]。
输出：高写实摄影风格图像。
```

**JSON 进阶模板（推荐给 Agent 调用）**

```json
{
  "type": "Hyper-realistic Photography",
  "subject": {
    "description": "A weary 30-year-old barista wiping a coffee cup",
    "details": "Subtle sweat on forehead, detailed skin pores, wearing a denim apron"
  },
  "setting": "Dimly lit vintage cafe, rain visible through the window behind",
  "camera_specs": {
    "gear": "Shot on Sony A7R IV, 50mm lens",
    "aperture": "f/1.4 (shallow depth of field, background completely blurred)",
    "lighting": "Cinematic lighting, neon sign reflecting on wet window, soft rim light on subject's hair"
  },
  "film_aesthetic": "Kodak Portra 400 emulation, subtle film grain"
}
```

**街头意外瞬间写实摄影模板**

```text
生成一张竖版手机纪实照片，主题是[意外事件/日常瞬间]发生在[街头/室外地点]。
主体：[物品/人物动作/现场痕迹]，必须呈现真实的材质状态，例如[液体扩散/冰块散落/纸张褶皱/灰尘颗粒]。
环境：[地面材质/墙面/街景元素]，保留自然杂乱和生活痕迹。
光线：[正午强光/阴天散射光/夜间路灯]，阴影要符合真实方向，可加入[人物影子/路牌影子/树影]。
镜头：手持手机视角，略微俯拍或低角度，构图自然，像随手拍到的现场。
画面质感：raw unedited photo look，自然色彩，真实纹理，高细节。
负面约束：不要插画、动漫、CGI、棚拍光、过度干净、过度构图、假液体、漂浮物、品牌文字、水印、海报设计感。
输出：一张可信的日常纪实摄影图。
```

**避坑指南**

- **加点瑕疵**：AI 画的人太完美了，反而像假人。加入“皮肤纹理（skin pores）”、“雀斑”、“轻微胶片颗粒（film grain）”，真实感瞬间拉满。
- **用参数说话**：用 `f/1.4` 代替“浅景深”，用 `50mm` 代替“半身照”，大模型吃这套。
- **把“不完美”写具体**：写“粗糙石砖、散落冰块、自然阴影、轻微手持感”，比只写“真实”更稳定。
