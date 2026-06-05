#!/usr/bin/env python3
"""
GPT Image 2 Prompt Engineering Engine.
Builds production-grade image prompts by combining:
1. User requirements analysis
2. Matched case patterns from the 832-case library
3. Category-specific best practices distilled from 3 community projects

Architecture:
  User Requirements + Matched Cases → Strategy Selection → Template Assembly → Quality Injection → Final Prompt

v2.1 Features:
  - Bilingual output (zh/en) for ChatGPT + Doubao compatibility
  - Fidelity modes: strict (exact text) / normal (case-referenced) / creative (max artistic freedom)
"""

import json, os, re, sys

INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "cases", "index.json")

# ═══════════════════════════════════════════════════════════════
# FIDELITY MODES
# ═══════════════════════════════════════════════════════════════

FIDELITY_MODES = {
    "strict": {
        "label": "严格模式",
        "label_en": "Strict",
        "description": "严格遵循用户指定的文字内容，AI不可自行发挥修改文字。光影、构图、画质等视觉效果正常优化。适用于品牌文案、UI界面、海报文字等需要精确文字的场合。",
        "description_en": "Faithfully reproduce user-specified text/copy exactly. Visual quality (lighting, composition, effects) is still optimized. For brand copy, UI text, posters where text accuracy is critical.",
        "case_weight": 1.0,      # Reference cases for visual patterns
        "injection_level": 1,     # Normal quality injections (lighting, camera, etc.)
        "creativity": 0.3,        # Low on TEXT creativity, normal on visuals
    },
    "normal": {
        "label": "普通模式",
        "label_en": "Normal",
        "description": "重点参考高质量案例，在用户需求基础上合理增强。适用于大多数图像生成场景。",
        "description_en": "Heavily reference quality cases, enhance user requirements reasonably. For most image generation scenarios.",
        "case_weight": 1.0,       # Full case reference
        "injection_level": 1,     # Standard quality injections
        "creativity": 0.5,        # Balanced creativity
    },
    "creative": {
        "label": "创意模式",
        "label_en": "Creative",
        "description": "尽最大可能联想，充分发挥AI艺术创作能力。适用于艺术插画、概念设计、抽象表达等创意场景。",
        "description_en": "Maximum association and AI artistic freedom. For art illustrations, concept design, abstract expression.",
        "case_weight": 0.3,       # Light case reference (just for inspiration)
        "injection_level": 2,     # Maximum quality injections
        "creativity": 1.0,        # Full creativity
    },
}

# ============================================================
# CATEGORY-SPECIFIC BEST PRACTICES (distilled from 1322 cases)
# ============================================================

CATEGORY_STRATEGIES = {
    "Portrait & People": {
        "approach": "natural_language",
        "template": """Generate a {style} portrait of {subject}. {pose_and_expression}. The subject is {clothing_and_styling}. {lighting_setup}. The background shows {background_scene}. Camera: {camera_specs}. Composition: {composition}. Color palette: {colors}. {atmosphere}.
{text_requirements}
{negative_constraints}""",
        "key_params": [
            "lighting_setup (studio/natural/golden hour/ring light/soft diffused)",
            "camera_specs (35mm/85mm/DSLR/medium format, f/stop, depth of field)",
            "pose_and_expression (candid/posed/candid laughter/looking away/direct gaze)",
            "composition (close-up/medium shot/full body/environmental portrait)",
            "skin texture detail, eye catchlights, hair detail",
        ],
        "photo_injection": True,
        "neg_defaults": ["avoid watermarks", "avoid distorted facial features", "avoid unnatural skin texture"],
        "ratio_common": ["3:4", "1:1", "9:16"],
    },

    "Poster & Typography": {
        "approach": "json_or_natural",
        "template": """Design a {purpose} poster for {subject}.
Main visual: {hero_element}.
Title typography: "{title_text}" in {typography_style}.
Subtitle: "{subtitle_text}".
Layout: {layout_style}.
Color system: {color_palette} (4-6 colors max).
Background: {background}.
Atmosphere: {mood}.
{additional_elements}
Output: high-resolution poster, {ratio}, {style} aesthetic.
{negative_constraints}""",
        "json_template": """{{
  "type": "poster",
  "purpose": "{purpose}",
  "subject": "{subject}",
  "hero_visual": "{hero_element}",
  "typography": {{
    "title": "{title_text}",
    "title_style": "{typography_style}",
    "subtitle": "{subtitle_text}"
  }},
  "layout": "{layout_style}",
  "colors": "{color_palette}",
  "background": "{background}",
  "style": "{style}",
  "constraints": "{negative_constraints}"
}}""",
        "key_params": [
            "typography_style (bold/serif/hand-lettered/minimal/experimental)",
            "layout_style (centered/diagonal/asymmetric/grid/swiss)",
            "color_palette (4-6 color system with dominant+accent+support)",
            "hero_element as visual anchor (product/person/abstract/typography itself)",
        ],
        "photo_injection": False,
        "neg_defaults": ["no generic word art", "no default fonts", "no cluttered composition", "no unreadable text", "no mismatched typography"],
        "ratio_common": ["2:3", "3:4", "4:5", "1:1"],
    },

    "Social Media & UI": {
        "approach": "structured_natural",
        "template": """Create a {platform} {content_type} screenshot/mockup for {purpose}.
Platform: {platform} ({mode} mode, {ratio}).
Account/Profile: {profile_info}.
Content: {content_description}.
UI Elements: {ui_elements}.
Engagement data: {engagement}.
Style: {style}.
Constraints: All text must be clearly readable, accurate platform UI elements, no gibberish placeholder text.
{negative_constraints}""",
        "key_params": [
            "platform (iOS/Android/X/TikTok/Instagram/WeChat/Xiaohongshu)",
            "mode (dark/light)",
            "ratio (9:16 for stories, 1:1 for feed, 16:9 for video)",
            "accurate platform-specific UI elements (tab bars, status bars, buttons)",
        ],
        "photo_injection": False,
        "neg_defaults": ["no gibberish text", "no mixed platform UI elements", "no placeholder text", "accurate Chinese/Japanese/Korean text rendering"],
        "ratio_common": ["9:16", "1:1", "16:9"],
    },

    "Product & E-commerce": {
        "approach": "detailed_natural",
        "template": """Create a {style} product {shot_type} for {product_name}.
Product details: {product_description}.
The product is positioned {product_position}.
Lighting: {lighting_setup}.
Background: {background_setup}.
Camera: {camera_specs}, {composition}.
Additional elements: {props_and_context}.
Color palette: {colors}.
{text_requirements}
{negative_constraints}""",
        "key_params": [
            "shot_type (hero shot/detail close-up/lifestyle/exploded view/group shot)",
            "lighting_setup (studio softbox/rim lighting/dramatic/product tent/natural window light)",
            "camera_specs (macro lens/commercial photography/8K resolution/tilt-shift)",
            "background (pure white/clean studio/lifestyle context/dark moody)",
            "product_position (centered hero/three-quarter angle/floating/on surface)",
        ],
        "photo_injection": True,
        "neg_defaults": ["no distorted product proportions", "no incorrect branding/logos", "no cluttered background", "accurate product colors"],
        "ratio_common": ["1:1", "4:5", "3:4"],
    },

    "Illustration & Storytelling": {
        "approach": "natural_language",
        "template": """Create an illustration in {art_style} style depicting {scene_description}.
Subject: {subject}.
Composition: {composition}.
Color palette: {color_scheme}.
Line work: {line_style}.
Rendering: {rendering_style}.
Atmosphere: {mood_and_tone}.
{panel_structure}
{text_requirements}
{negative_constraints}""",
        "key_params": [
            "art_style (anime/manga/watercolor/oil painting/vector/comic/children's book)",
            "composition (dynamic/balanced/asymmetric/panoramic/close-up)",
            "line_style (clean ink/rough sketch/painterly/no lines/brush stroke)",
            "rendering (cel-shaded/flat color/gradient/textured/hatched)",
        ],
        "photo_injection": False,
        "neg_defaults": ["no inconsistent character design", "no clashing art styles", "no stiff poses"],
        "ratio_common": ["16:9", "2:3", "3:4"],
    },

    "Photography & Realism": {
        "approach": "detailed_natural",
        "template": """{shot_type} photograph of {subject}. {scene_description}.
Camera: {camera_specs}. Lens: {lens_specs}.
Lighting: {lighting_setup}. {time_of_day}.
Composition: {composition_style}. Depth of field: {dof}.
Color grading: {color_treatment}. Film stock: {film_reference}.
{atmosphere_details}.
{technical_specs}.
{negative_constraints}""",
        "key_params": [
            "camera (Hasselblad/Leica/Canon/Sony/film/DSLR/medium format/35mm)",
            "lens (85mm f/1.4/50mm f/1.8/24-70mm f/2.8/tilt-shift/macro)",
            "lighting (Rembrandt/butterfly/split/rim/golden hour/overcast/studio strobe)",
            "film (Kodak Portra 400/Fuji Pro 400H/Cinestill 800T/Ilford HP5)",
            "composition (rule of thirds/centered/leading lines/frame within frame/dutch angle)",
        ],
        "photo_injection": True,
        "neg_defaults": ["no CGI-looking render", "no over-processed HDR", "no artificial bokeh", "natural skin texture"],
        "ratio_common": ["2:3", "3:4", "1:1", "16:9"],
    },

    "Infographic & Charts": {
        "approach": "json_or_natural",
        "template": """Create an infographic about {topic} for {audience}.
Structure: {structure_description} ({module_count} modules).
Chart types: {chart_types}.
Visual style: {visual_style}.
Color system: {colors} (color-coded by category).
Typography: {typography_style}, readable at infographic scale.
Layout: {layout_type}.
{text_requirements}
{negative_constraints}""",
        "key_params": [
            "structure (title area + 3-5 modules with icons + short descriptions + logical flow arrows)",
            "chart_types (flowchart/comparison/timeline/relationship diagram/process)",
            "visual_style (professional report/children's education/scientific atlas/minimal)",
            "3-5 modules max to avoid information overload",
        ],
        "photo_injection": False,
        "neg_defaults": ["no long paragraphs", "no generic clipart icons", "no information overload", "no cyberpunk aesthetic for serious topics", "keep text short and readable"],
        "ratio_common": ["16:9", "4:3", "2:3", "1:1"],
    },

    "Brand & Identity": {
        "approach": "structured_natural",
        "template": """Design a brand identity system for {brand_name}.
Brand personality: {personality}.
Logo concept: {logo_description}.
Color palette: {color_system}.
Typography: {typography_system}.
Applications shown: {applications}.
Style: {visual_style}.
{negative_constraints}""",
        "key_params": [
            "brand personality (luxury/playful/minimal/tech-forward/heritage/craft)",
            "color_system (primary + secondary + accent + neutral palette)",
            "applications (business card/letterhead/packaging/social media/digital)",
            "logo style (wordmark/symbol/combination/lettermark/emblem)",
        ],
        "photo_injection": False,
        "neg_defaults": ["no generic template look", "no stock logo elements", "no inconsistent brand application"],
        "ratio_common": ["16:9", "1:1"],
    },

    "Architecture & Scenes": {
        "approach": "detailed_natural",
        "template": """{view_type} of {subject}. {architectural_style}.
Materials: {materials}.
Lighting: {lighting_conditions}, {time_of_day}.
Atmosphere: {atmosphere}.
Camera: {camera_specs}, {composition}.
Environment: {surroundings}.
{technical_details}
{negative_constraints}""",
        "key_params": [
            "view_type (exterior/interior/aerial/isometric/cutaway/elevation)",
            "architectural_style (modernist/brutalist/Japanese zen/Art Deco/parametric)",
            "materials (concrete/wood/glass/steel/stone/bamboo)",
            "atmosphere (fog/mist/golden hour/night/rain/clear day)",
        ],
        "photo_injection": False,
        "neg_defaults": ["no unrealistic lighting", "no incorrect scale", "no generic 3D render look"],
        "ratio_common": ["16:9", "3:2", "1:1"],
    },
}

# ============================================================
# STYLE-SPECIFIC QUALITY INJECTIONS
# ============================================================

STYLE_INJECTIONS = {
    "photography": {
        "camera": ["professional DSLR", "medium format camera", "35mm film", "Hasselblad", "Leica"],
        "lighting": ["studio softbox lighting", "golden hour natural light", "Rembrandt lighting", "soft diffused window light", "dramatic rim lighting"],
        "quality": ["8K resolution", "hyper-realistic", "commercial photography", "editorial quality", "award-winning photograph"],
        "lens": ["85mm f/1.4 prime lens", "50mm f/1.8", "24-70mm f/2.8", "macro lens", "tilt-shift lens"],
        "composition": ["rule of thirds", "shallow depth of field", "bokeh background", "sharp focus on subject", "cinematic composition"],
    },
    "cinematic": {
        "camera": ["ARRI Alexa", "RED cinema camera", "anamorphic lens", "35mm film stock"],
        "lighting": ["cinematic volumetric lighting", "atmospheric haze", "practical lights in frame", "motivated lighting"],
        "quality": ["film still quality", "cinematic color grading", "widescreen aspect ratio", "Oscar-winning cinematography"],
        "film": ["Kodak Vision3 500T", "Fuji Eterna Vivid 160", "Technicolor", "CineStill 800T"],
    },
    "anime": {
        "style": ["Studio Ghibli aesthetic", "Makoto Shinkai cinematic lighting", "90s cel animation style", "modern anime cleanup"],
        "quality": ["sakuga-quality animation frame", "detailed background art", "expressive character design", "clean linework"],
        "color": ["vibrant cel-shaded colors", "soft watercolor background", "dramatic lighting with lens flares"],
    },
    "illustration": {
        "style": ["award-winning illustration", "professional editorial illustration", "children's book quality", "gallery-quality artwork"],
        "technique": ["watercolor and ink", "digital painting", "gouache", "colored pencil", "vector art", "mixed media"],
        "quality": ["highly detailed", "masterful composition", "expressive brushwork", "rich texture"],
    },
    "3d": {
        "style": ["photorealistic 3D render", "isometric 3D", "claymation style", "voxel art", "low poly"],
        "quality": ["8K render", "global illumination", "subsurface scattering", "ambient occlusion", "ray tracing"],
        "software": ["Octane Render", "Blender Cycles", "Cinema 4D", "Unreal Engine 5"],
    },
    "poster": {
        "style": ["Swiss design", "Japanese graphic design", " Bauhaus", "minimalist poster", "brutalist poster", "vintage travel poster"],
        "technique": ["silkscreen print texture", "letterpress impression", "risograph grain", "offset lithography", "foil stamping"],
        "quality": ["museum-quality graphic design", "award-winning poster", "bold typographic hierarchy", "intelligent whitespace"],
    },
    "ui": {
        "platform": ["iOS 18", "Android Material Design 3", "visionOS", "Figma prototype", "high-fidelity mockup"],
        "quality": ["pixel-perfect", "readable text at all sizes", "consistent spacing", "proper component hierarchy"],
        "mode": ["dark mode", "light mode", "OLED black", "frosted glass effect"],
    },
}

# ============================================================
# NEGATIVE CONSTRAINT LIBRARY
# ============================================================

NEGATIVE_CONSTRAINTS = {
    "universal": [
        "no watermarks or signatures",
        "no distorted or unreadable text",
        "no low-resolution artifacts",
    ],
    "photography": [
        "no CGI or 3D render look",
        "no over-processed HDR effect",
        "no artificial bokeh",
        "no plastic skin texture",
    ],
    "poster": [
        "no generic word art",
        "no default system fonts",
        "no cluttered composition",
        "no mismatched typography styles",
    ],
    "ui": [
        "no gibberish placeholder text",
        "no mixed platform UI elements",
        "no unreadable small text",
        "no broken layout at screen edges",
    ],
    "product": [
        "no distorted product proportions",
        "no incorrect colors on branded items",
        "no cluttered background distracting from product",
    ],
    "illustration": [
        "no inconsistent art styles in same image",
        "no stiff or unnatural poses",
        "no muddy or desaturated colors unless intentional",
    ],
    "infographic": [
        "no long paragraphs of body text",
        "no generic clipart icons",
        "no information overload (>5 modules)",
    ],
}

# ============================================================
# MAIN PROMPT BUILDER
# ============================================================

class PromptBuilder:
    def __init__(self):
        self.case_library = self._load_cases()

    def _load_cases(self):
        if os.path.exists(INDEX_PATH):
            with open(INDEX_PATH) as f:
                return json.load(f)
        return {"cases": []}

    def search_cases(self, keywords, category=None, limit=3):
        """Search for relevant cases."""
        cases = self.case_library.get("cases", [])
        scored = []
        for c in cases:
            score = 0
            text = (c.get("title","") + " " + c.get("prompt","") + " " + c.get("original_category","")).lower()
            for kw in keywords:
                if kw.lower() in text:
                    score += 10
                for part in kw.lower().split():
                    if part in text:
                        score += 3
            if category and c.get("category","") == category:
                score += 5
            if c.get("featured"):
                score += 5
            if score > 0:
                scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:limit]]

    def analyze_requirements(self, requirements):
        """Analyze user requirements to determine strategy."""
        subject = requirements.get("subject", "")
        style = requirements.get("style", "").lower()
        purpose = requirements.get("purpose", "").lower()
        category = requirements.get("category", "Other")

        # Determine approach
        if category in ["Poster & Typography", "Infographic & Charts"] and requirements.get("complex_layout"):
            approach = "json_structured"
        elif category == "Product & E-commerce" and "photography" in style:
            approach = "detailed_commercial"
        elif category == "Photography & Realism":
            approach = "photography_spec"
        elif category == "Social Media & UI":
            approach = "platform_specific"
        else:
            approach = "natural_language"

        # Determine if photo params needed
        needs_photo_params = any(kw in style for kw in [
            "photo", "photography", "realistic", "cinematic", "film", "editorial", "commercial"
        ]) or category in ["Photography & Realism", "Portrait & People", "Product & E-commerce"]

        # Style quality injection key
        style_key = "photography"
        for key in STYLE_INJECTIONS:
            if key in style:
                style_key = key
                break

        return {
            "approach": approach,
            "needs_photo_params": needs_photo_params,
            "style_key": style_key,
            "category": category,
        }

    def build(self, requirements, matched_cases=None, user_lang="zh", fidelity="normal", bilingual=True):
        """
        Build prompts from requirements and matched cases.

        Args:
            requirements: dict with subject, style, purpose, category, ratio, text, constraints, ref_info
            matched_cases: list of case dicts from search_cases()
            user_lang: user's language (zh/en/ja)
            fidelity: "strict" / "normal" / "creative"
            bilingual: if True, output both zh and en versions

        Returns:
            dict with {prompt, prompt_en, explanation, cases_used, methodology_notes, fidelity_mode}
        """
        analysis = self.analyze_requirements(requirements)
        category = analysis["category"]
        strategy = CATEGORY_STRATEGIES.get(category, CATEGORY_STRATEGIES["Portrait & People"])
        fidelity_config = FIDELITY_MODES.get(fidelity, FIDELITY_MODES["normal"])

        # Adjust case usage based on fidelity
        effective_cases = matched_cases or []
        if fidelity == "creative":
            effective_cases = (matched_cases or [])[:1]  # Light reference for creative

        # Extract best patterns from matched cases (all modes benefit)
        case_patterns = self._extract_case_patterns(effective_cases)

        # Build Chinese prompt
        prompt_zh, methodology = self._compose_prompt(
            requirements, strategy, analysis, case_patterns, "zh", fidelity_config
        )

        # Build English prompt
        prompt_en = ""
        if bilingual or user_lang == "en":
            prompt_en, _ = self._compose_prompt(
                requirements, strategy, analysis, case_patterns, "en", fidelity_config
            )

        # Post-process: inject quality keywords (all modes get quality injections)
        prompt_zh = self._inject_quality(prompt_zh, analysis, case_patterns, fidelity_config)
        if prompt_en:
            prompt_en = self._inject_quality(prompt_en, analysis, case_patterns, fidelity_config)

        result = {
            "prompt": prompt_zh if user_lang == "zh" else prompt_en,
            "prompt_zh": prompt_zh if bilingual else "",
            "prompt_en": prompt_en if bilingual else "",
            "methodology_notes": methodology,
            "approach_used": analysis["approach"],
            "cases_referenced": [c["id"] for c in effective_cases[:3]],
            "quality_injections": self._summarize_injections(analysis, case_patterns, fidelity_config),
            "fidelity_mode": fidelity,
            "fidelity_label": fidelity_config["label"],
        }

        return result

    def _extract_case_patterns(self, cases):
        """Extract reusable patterns from matched cases."""
        patterns = {
            "lighting_terms": [],
            "camera_terms": [],
            "composition_terms": [],
            "style_descriptors": [],
            "structure_patterns": [],
            "neg_constraints": [],
        }
        for c in cases[:5]:
            prompt = c.get("prompt", "")
            # Extract common high-quality descriptors
            for term in ["studio lighting", "golden hour", "soft light", "dramatic lighting", "Rembrandt", "cinematic lighting"]:
                if term.lower() in prompt.lower() and term not in patterns["lighting_terms"]:
                    patterns["lighting_terms"].append(term)
            for term in ["8K", "4K", "photorealistic", "hyper-realistic", "high resolution", "detailed"]:
                if term.lower() in prompt.lower() and term not in patterns["style_descriptors"]:
                    patterns["style_descriptors"].append(term)
            # Extract negative constraints
            for line in prompt.lower().split("\n"):
                if any(kw in line for kw in ["avoid", "no ", "do not", "without", "禁止", "不要"]):
                    patterns["neg_constraints"].append(line.strip())
        return patterns

    def _compose_prompt(self, req, strategy, analysis, patterns, lang, fidelity_config=None):
        """Core prompt composition logic with fidelity control."""
        if fidelity_config is None:
            fidelity_config = FIDELITY_MODES["normal"]
        methodology = []

        # Choose language for prompt
        is_chinese = lang == "zh"
        is_japanese = lang == "ja"

        # All modes use the same strategy branches — fidelity only affects
        # how text content is handled (strict: verbatim, creative: free interpretation)

        # Strategy selection
        if strategy["approach"] == "json_structured" and req.get("complex_layout"):
            prompt = self._build_json_prompt(req, strategy, patterns, lang)
            methodology.append("Using JSON-structured approach for complex layout control")
        elif strategy["approach"] == "detailed_commercial":
            prompt = self._build_commercial_prompt(req, strategy, patterns, lang)
            methodology.append("Using detailed commercial photography approach with precise parameter control")
        elif strategy["approach"] == "photography_spec":
            prompt = self._build_photography_prompt(req, strategy, patterns, lang)
            methodology.append("Using professional photography specification approach")
        elif strategy["approach"] == "platform_specific":
            prompt = self._build_platform_prompt(req, strategy, patterns, lang)
            methodology.append("Using platform-specific UI/UX prompt structure")
        else:
            prompt = self._build_natural_prompt(req, strategy, patterns, lang)
            methodology.append("Using natural language approach with quality injections")

        # Reference image handling
        if req.get("ref_info"):
            ref = req["ref_info"]
            keep = ref.get("keep", "composition and subject structure")
            change = ref.get("change", req.get("style", "style"))
            ref_instruction = f"\nBased on the reference image: maintain {keep}, transform {change}."
            prompt = ref_instruction + "\n" + prompt
            methodology.append(f"Image-to-image mode: keep [{keep}], change [{change}]")

        # Raycast parameterization
        if req.get("raycast"):
            methodology.append("Raycast dynamic parameters enabled for flexible iteration")

        methodology.append(f"Category strategy: {req.get('category', 'General')}")
        methodology.append(f"Approach: {analysis['approach']}")

        # Apply fidelity wrapper (strict text accuracy / creative freedom / normal = as-is)
        if fidelity_config:
            prompt = self._apply_fidelity_wrapper(prompt, fidelity_config, lang)
            if fidelity_config["creativity"] <= 0.3:
                methodology.append(f"[{fidelity_config['label']}] 文字严格遵循原文，视觉效果正常优化")
            elif fidelity_config["creativity"] >= 1.0:
                methodology.append(f"[{fidelity_config['label']}] 最大化艺术创作自由度")

        return prompt, methodology

    def _apply_fidelity_wrapper(self, prompt, fidelity_config, lang):
        """Wrap prompt with fidelity-specific instructions.

        Strict: enforce text accuracy, visual quality still optimized.
        Creative: encourage artistic freedom and exploration.
        Normal: no additional wrapper (prompt as-is).
        """
        is_chinese = lang == "zh"

        if fidelity_config["creativity"] <= 0.3:  # strict
            if is_chinese:
                return prompt + "\n\n【重要】上述指定的所有文字内容必须原样呈现，不得修改、改写或编造任何文字。光影、构图、画质等视觉效果请充分优化。"
            else:
                return prompt + "\n\nIMPORTANT: All text/copy specified above must appear exactly as written. Do not modify, paraphrase, or invent any text content. Visual quality (lighting, composition, effects) should be fully optimized."

        if fidelity_config["creativity"] >= 1.0:  # creative
            if is_chinese:
                return prompt + "\n\n请充分发挥艺术创造力，大胆运用戏剧性光影、非常规构图和大胆配色。可以自由联想和增强视觉元素，突破常规，追求独特的艺术表达。"
            else:
                return prompt + "\n\nFeel free to creatively interpret and enhance all visual elements. Push artistic boundaries with dramatic lighting, unexpected compositions, and bold color choices. Prioritize unique artistic expression over literal accuracy."

        return prompt  # normal: no wrapper

    def _build_natural_prompt(self, req, strategy, patterns, lang="en"):
        """Build a natural language prompt."""
        is_chinese = lang == "zh"
        parts = []

        # Task definition
        subject = req.get("subject", "")
        style = req.get("style", "")
        purpose = req.get("purpose", "")

        if is_chinese:
            if purpose:
                parts.append(f"生成一张{style}风格的{purpose}，主题为{subject}。")
            else:
                parts.append(f"生成一张{style}风格的{subject}图像。")

            if req.get("mood"):
                parts.append(f"氛围：{req['mood']}。")

            if strategy.get("photo_injection"):
                parts.append("灯光：专业摄影棚灯光，柔和散射照明。")
                parts.append("相机：高分辨率商业摄影，清晰对焦，适当浅景深。")

            if req.get("ratio"):
                parts.append(f"画幅比例：{req['ratio']}。")
            if req.get("composition"):
                parts.append(f"构图：{req['composition']}。")

            if req.get("text_content"):
                parts.append(f"需要包含的文字（务必清晰可读）：{req['text_content']}。")

            if req.get("colors"):
                parts.append(f"色彩方案：{req['colors']}。")

            if req.get("special_elements"):
                parts.append(f"附加元素：{req['special_elements']}。")

            negs = list(strategy.get("neg_defaults", []))
            if req.get("constraints"):
                negs.extend(req["constraints"].split(","))
            if negs:
                parts.append("避免：" + "、".join(negs[:5]) + "。")
        else:
            if purpose:
                parts.append(f"Create a {style} {purpose} featuring {subject}.")
            else:
                parts.append(f"Create a {style} image of {subject}.")

            # Style specifics
            parts.append(f"Visual style: {style}.")
            if req.get("mood"):
                parts.append(f"Atmosphere: {req['mood']}.")

            # Technical details
            if strategy.get("photo_injection"):
                parts.append("Lighting: professional studio lighting with soft diffused illumination.")
                parts.append("Camera: high-resolution commercial photography, sharp focus, shallow depth of field where appropriate.")

            # Composition
            if req.get("ratio"):
                parts.append(f"Aspect ratio: {req['ratio']}.")
            if req.get("composition"):
                parts.append(f"Composition: {req['composition']}.")

            # Text requirements
            if req.get("text_content"):
                parts.append(f"Text to include (must be clearly readable): {req['text_content']}.")

            # Color
            if req.get("colors"):
                parts.append(f"Color palette: {req['colors']}.")

            # Special elements
            if req.get("special_elements"):
                parts.append(f"Additional elements: {req['special_elements']}.")

            # Negative constraints
            negs = list(strategy.get("neg_defaults", []))
            if req.get("constraints"):
                negs.extend(req["constraints"].split(","))
            if negs:
                parts.append("Avoid: " + ", ".join(negs[:5]) + ".")

        return " ".join(parts)

    def _build_photography_prompt(self, req, strategy, patterns, lang="en"):
        """Build a professional photography prompt."""
        subject = req.get("subject", "")
        style = req.get("style", "editorial photography")
        parts = []

        # Shot type
        shot = req.get("shot_type", "editorial portrait" if "portrait" in req.get("category","").lower() else "commercial photograph")
        parts.append(f"{shot.capitalize()} of {subject}.")

        # Scene
        if req.get("scene"):
            parts.append(f"Scene: {req['scene']}.")
        if req.get("mood"):
            parts.append(f"Mood: {req['mood']}.")

        # Camera specs (critical for photography quality)
        camera = req.get("camera", "professional DSLR")
        lens = req.get("lens", "85mm f/1.4 prime lens")
        parts.append(f"Shot on {camera} with {lens}.")

        # Lighting
        lighting = req.get("lighting", "soft natural window light with subtle fill")
        parts.append(f"Lighting: {lighting}.")

        # Composition
        comp = req.get("composition", "rule of thirds composition with shallow depth of field")
        parts.append(f"Composition: {comp}.")

        # Quality
        parts.append("Hyper-realistic, 8K resolution, commercial photography quality, natural skin texture, cinematic color grading.")

        # Color
        if req.get("colors"):
            parts.append(f"Color palette: {req['colors']}.")

        # Format
        if req.get("ratio"):
            parts.append(f"Aspect ratio: {req['ratio']}.")

        # Negative
        negs = ["no CGI render look", "no plastic skin", "no over-processed HDR", "no artificial bokeh"]
        if req.get("constraints"):
            negs.extend(req["constraints"].split(","))
        parts.append("Avoid: " + ", ".join(negs[:4]) + ".")

        return " ".join(parts)

    def _build_commercial_prompt(self, req, strategy, patterns):
        """Build a commercial/e-commerce product prompt."""
        product = req.get("subject", "")
        style = req.get("style", "commercial product photography")
        parts = []

        parts.append(f"Create a {style} hero shot for {product}.")
        if req.get("product_details"):
            parts.append(f"Product details: {req['product_details']}.")

        parts.append("Studio lighting: professional softbox with rim light for product definition, pure white seamless background.")
        parts.append("Camera: macro commercial lens, 8K resolution, shallow depth of field on product, sharp focus throughout.")
        if req.get("ratio"):
            parts.append(f"Format: {req['ratio']}.")
        if req.get("scene"):
            parts.append(f"Context: {req['scene']}.")

        negs = strategy.get("neg_defaults", [])
        if req.get("constraints"):
            negs.extend(req["constraints"].split(","))
        parts.append("Avoid: " + ", ".join(negs[:4]) + ".")

        return " ".join(parts)

    def _build_json_prompt(self, req, strategy, patterns):
        """Build a JSON-structured prompt for complex layouts."""
        json_str = strategy.get("json_template", "")
        if not json_str:
            return self._build_natural_prompt(req, strategy, patterns)

        # Fill template
        for key, val in req.items():
            json_str = json_str.replace("{" + key + "}", str(val))

        # Fill defaults
        defaults = {
            "purpose": req.get("purpose", "promotional"),
            "subject": req.get("subject", ""),
            "hero_element": req.get("hero_element", req.get("subject", "")),
            "title_text": req.get("text_content", "Title"),
            "subtitle_text": req.get("subtitle", ""),
            "typography_style": req.get("typography", "bold editorial"),
            "layout_style": req.get("composition", "centered with asymmetric elements"),
            "color_palette": req.get("colors", "4-color system: dominant + accent + neutral + highlight"),
            "background": req.get("background", "clean gradient with subtle texture"),
            "style": req.get("style", "editorial"),
            "negative_constraints": ", ".join(strategy.get("neg_defaults", [])[:3]),
        }

        for key, val in defaults.items():
            json_str = json_str.replace("{" + key + "}", str(val))

        return json_str.strip()

    def _build_platform_prompt(self, req, strategy, patterns):
        """Build a platform-specific UI/social media prompt."""
        platform = req.get("platform", "iOS")
        mode = req.get("mode", "light")
        ratio = req.get("ratio", "9:16")
        parts = []

        parts.append(f"Generate a {platform} {req.get('content_type', 'app')} screenshot in {mode} mode, {ratio} aspect ratio.")
        if req.get("subject"):
            parts.append(f"Content: {req['subject']}.")
        if req.get("ui_elements"):
            parts.append(f"UI elements: {req['ui_elements']}.")

        parts.append("High-fidelity mockup, all text clearly readable, accurate platform UI components.")
        if req.get("text_content"):
            parts.append(f"Display text: \"{req['text_content']}\" (must be pixel-perfect).")

        negs = ["no gibberish placeholder text", "no mixed-platform UI elements", "no unreadable small text"]
        if req.get("constraints"):
            negs.extend(req["constraints"].split(","))
        parts.append("Avoid: " + ", ".join(negs[:3]) + ".")

        return " ".join(parts)

    def _inject_quality(self, prompt, analysis, patterns, fidelity_config=None):
        """Smoothly integrate quality keywords into the prompt flow."""
        if fidelity_config is None:
            fidelity_config = FIDELITY_MODES["normal"]

        # Strict mode: no quality injections
        if fidelity_config["injection_level"] == 0:
            return prompt

        style_key = analysis["style_key"]
        injections = STYLE_INJECTIONS.get(style_key, {})

        # Creative mode: use max injections
        max_terms = 3 if fidelity_config["injection_level"] >= 2 else 1

        # Build quality suffix respecting fidelity level
        quality_parts = []

        if "quality" in injections and injections["quality"]:
            quality_parts.extend(injections["quality"][:max_terms])

        if fidelity_config["injection_level"] >= 2:
            if "camera" in injections and injections["camera"]:
                quality_parts.append(f"shot on {injections['camera'][0]}")
            if "lens" in injections and injections["lens"]:
                quality_parts.append(f"with {injections['lens'][0]}")
            if "lighting" in injections and injections["lighting"]:
                quality_parts.append(f"under {injections['lighting'][0]}")
            if "composition" in injections and injections["composition"]:
                quality_parts.append(f"{injections['composition'][0]} composition")

        if fidelity_config["injection_level"] == 1:
            if "camera" in injections and injections["camera"]:
                quality_parts.append(injections["camera"][0])

        if quality_parts:
            # Integrate smoothly: add before negative constraints
            suffix = ". ".join(quality_parts) + "."
            # Insert before "Avoid:" if present
            if "Avoid:" in prompt:
                prompt = prompt.replace("Avoid:", f"{suffix}\n\nAvoid:")
            elif "不要" in prompt:
                prompt = prompt.replace("不要", f"{suffix}\n\n不要")
            else:
                prompt += f" {suffix}"

        return prompt.strip()

    def _summarize_injections(self, analysis, patterns, fidelity_config=None):
        """Summarize what quality injections were applied."""
        if fidelity_config is None:
            fidelity_config = FIDELITY_MODES["normal"]
        summary = []
        if fidelity_config["injection_level"] == 0:
            return ["[严格模式] 无质量注入，使用用户原文" if True else "[Strict] No quality injections"]
        style_key = analysis["style_key"]
        if style_key in STYLE_INJECTIONS:
            max_terms = 3 if fidelity_config["injection_level"] >= 2 else 1
            for cat, terms in STYLE_INJECTIONS[style_key].items():
                for t in terms[:max_terms]:
                    summary.append(f"{cat}: {t}")
        return summary


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="GPT Image 2 Intelligent Prompt Builder")
    parser.add_argument("--subject", required=True, help="What to generate (subject/scene)")
    parser.add_argument("--style", default="photography", help="Visual style")
    parser.add_argument("--purpose", default="", help="Use case / purpose")
    parser.add_argument("--category", default="Portrait & People", help="Unified category")
    parser.add_argument("--ratio", default="", help="Aspect ratio (1:1, 9:16, 16:9, etc.)")
    parser.add_argument("--text", default="", help="Text content to include")
    parser.add_argument("--colors", default="", help="Color palette")
    parser.add_argument("--mood", default="", help="Atmosphere / mood")
    parser.add_argument("--composition", default="", help="Composition style")
    parser.add_argument("--constraints", default="", help="Negative constraints (comma-separated)")
    parser.add_argument("--ref-keep", default="", help="(Image-to-image) What to keep from reference")
    parser.add_argument("--ref-change", default="", help="(Image-to-image) What to change")
    parser.add_argument("--raycast", action="store_true", help="Enable Raycast dynamic parameters")
    parser.add_argument("--complex", action="store_true", help="Use JSON-structured approach")
    parser.add_argument("--search-limit", type=int, default=3, help="Number of cases to reference")
    parser.add_argument("--lang", default="zh", help="User language (zh/en/ja)")
    parser.add_argument("--fidelity", default="normal", choices=["strict", "normal", "creative"],
                        help="Fidelity mode: strict (exact text), normal (case-referenced), creative (max artistic freedom)")
    parser.add_argument("--bilingual", action="store_true", default=True,
                        help="Output both Chinese and English versions (default: true)")
    parser.add_argument("--no-bilingual", action="store_true", help="Disable bilingual output")
    parser.add_argument("--json-output", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    bilingual = not args.no_bilingual

    builder = PromptBuilder()

    # Search relevant cases
    keywords = args.subject.split() + args.style.split()
    if args.purpose:
        keywords.extend(args.purpose.split())
    cases = builder.search_cases(keywords, category=args.category, limit=args.search_limit)

    # Build requirements
    requirements = {
        "subject": args.subject,
        "style": args.style,
        "purpose": args.purpose,
        "category": args.category,
        "ratio": args.ratio,
        "text_content": args.text,
        "colors": args.colors,
        "mood": args.mood,
        "composition": args.composition,
        "constraints": args.constraints,
        "complex_layout": args.complex,
        "raycast": args.raycast,
    }

    if args.ref_keep or args.ref_change:
        requirements["ref_info"] = {
            "keep": args.ref_keep or "composition and subject",
            "change": args.ref_change or args.style,
        }

    # Build prompt
    result = builder.build(requirements, cases, args.lang, fidelity=args.fidelity, bilingual=bilingual)

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        fidelity_emoji = {"strict": "🔒", "normal": "📋", "creative": "🎨"}
        print("=" * 60)
        print(f"{fidelity_emoji.get(args.fidelity, '📋')} GENERATED PROMPT [{result['fidelity_label']}]")
        print("=" * 60)

        if result.get("prompt_zh") and result.get("prompt_en"):
            print(f"\n--- 🇨🇳 中文版 (for 豆包/国内模型) ---")
            print(f"{result['prompt_zh']}\n")
            print(f"--- 🇺🇸 English (for ChatGPT/GPT Image) ---")
            print(f"{result['prompt_en']}\n")
        else:
            print(f"\n{result['prompt']}\n")

        if cases:
            print("=" * 60)
            print("📚 REFERENCED CASES")
            print("=" * 60)
            for case in cases[:3]:
                print(f"  [{case['id']}] {case['title']}")
                print(f"  Category: {case.get('category', 'N/A')} | Source: {case.get('source', 'N/A')}")
                preview = case.get('prompt', '')[:150]
                print(f"  Preview: {preview}...\n")

        print("=" * 60)
        print("🔬 METHODOLOGY")
        print("=" * 60)
        for note in result['methodology_notes']:
            print(f"  • {note}")
        print(f"\n  Fidelity: {result['fidelity_mode']} ({result['fidelity_label']})")
        print(f"  Quality injections: {', '.join(result['quality_injections'])}")
        print(f"  Approach: {result['approach_used']}")


if __name__ == "__main__":
    main()
