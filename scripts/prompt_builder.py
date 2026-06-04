#!/usr/bin/env python3
"""
GPT Image 2 Prompt Engineering Engine.
Builds production-grade image prompts by combining:
1. User requirements analysis
2. Matched case patterns from the 1322-case library
3. Category-specific best practices distilled from 3 community projects

Architecture:
  User Requirements + Matched Cases → Strategy Selection → Template Assembly → Quality Injection → Final Prompt
"""

import json, os, re, sys

INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "cases", "index.json")

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

    def build(self, requirements, matched_cases=None, user_lang="zh"):
        """
        Build a production-grade prompt from requirements and matched cases.

        Args:
            requirements: dict with subject, style, purpose, category, ratio, text, constraints, ref_info
            matched_cases: list of case dicts from search_cases()
            user_lang: user's language (zh/en/ja)

        Returns:
            dict with {prompt, explanation, cases_used, methodology_notes}
        """
        analysis = self.analyze_requirements(requirements)
        category = analysis["category"]
        strategy = CATEGORY_STRATEGIES.get(category, CATEGORY_STRATEGIES["Portrait & People"])

        # Extract best patterns from matched cases
        case_patterns = self._extract_case_patterns(matched_cases or [])

        # Build prompt based on approach
        prompt, methodology = self._compose_prompt(
            requirements, strategy, analysis, case_patterns, user_lang
        )

        # Post-process: inject quality keywords from case patterns
        prompt = self._inject_quality(prompt, analysis, case_patterns)

        return {
            "prompt": prompt,
            "methodology_notes": methodology,
            "approach_used": analysis["approach"],
            "cases_referenced": [c["id"] for c in (matched_cases or [])[:3]],
            "quality_injections": self._summarize_injections(analysis, case_patterns),
        }

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

    def _compose_prompt(self, req, strategy, analysis, patterns, lang):
        """Core prompt composition logic."""
        methodology = []

        # Choose language for prompt
        is_chinese = lang == "zh"
        is_japanese = lang == "ja"

        # Strategy selection
        if strategy["approach"] == "json_structured" and req.get("complex_layout"):
            prompt = self._build_json_prompt(req, strategy, patterns)
            methodology.append("Using JSON-structured approach for complex layout control")
        elif strategy["approach"] == "detailed_commercial":
            prompt = self._build_commercial_prompt(req, strategy, patterns)
            methodology.append("Using detailed commercial photography approach with precise parameter control")
        elif strategy["approach"] == "photography_spec":
            prompt = self._build_photography_prompt(req, strategy, patterns)
            methodology.append("Using professional photography specification approach")
        elif strategy["approach"] == "platform_specific":
            prompt = self._build_platform_prompt(req, strategy, patterns)
            methodology.append("Using platform-specific UI/UX prompt structure")
        else:
            prompt = self._build_natural_prompt(req, strategy, patterns)
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

        return prompt, methodology

    def _build_natural_prompt(self, req, strategy, patterns):
        """Build a natural language prompt."""
        parts = []

        # Task definition
        subject = req.get("subject", "")
        style = req.get("style", "")
        purpose = req.get("purpose", "")

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

    def _build_photography_prompt(self, req, strategy, patterns):
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

    def _inject_quality(self, prompt, analysis, patterns):
        """Smoothly integrate quality keywords into the prompt flow."""
        style_key = analysis["style_key"]
        injections = STYLE_INJECTIONS.get(style_key, {})

        # Build a smooth quality suffix that reads naturally
        quality_parts = []

        if "quality" in injections and injections["quality"]:
            quality_parts.append(injections["quality"][0])

        if "camera" in injections and injections["camera"]:
            quality_parts.append(f"shot on {injections['camera'][0]}")

        if "lens" in injections and injections["lens"]:
            quality_parts.append(f"with {injections['lens'][0]}")

        if "lighting" in injections and injections["lighting"]:
            quality_parts.append(f"under {injections['lighting'][0]}")

        if "composition" in injections and injections["composition"]:
            quality_parts.append(f"{injections['composition'][0]} composition")

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

    def _summarize_injections(self, analysis, patterns):
        """Summarize what quality injections were applied."""
        summary = []
        style_key = analysis["style_key"]
        if style_key in STYLE_INJECTIONS:
            for cat, terms in STYLE_INJECTIONS[style_key].items():
                summary.append(f"{cat}: {terms[0]}")
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
    parser.add_argument("--json-output", action="store_true", help="Output as JSON")
    args = parser.parse_args()

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
    result = builder.build(requirements, cases, args.lang)

    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("🎯 GENERATED PROMPT")
        print("=" * 60)
        print(f"\n{result['prompt']}\n")
        print("=" * 60)
        print("📚 REFERENCED CASES")
        print("=" * 60)
        for case in cases:
            print(f"  [{case['id']}] {case['title']}")
            print(f"  Category: {case.get('category', 'N/A')} | Source: {case.get('source', 'N/A')}")
            preview = case.get('prompt', '')[:150]
            print(f"  Preview: {preview}...\n")
        print("=" * 60)
        print("🔬 METHODOLOGY")
        print("=" * 60)
        for note in result['methodology_notes']:
            print(f"  • {note}")
        print(f"\n  Quality injections: {', '.join(result['quality_injections'])}")
        print(f"  Approach: {result['approach_used']}")


if __name__ == "__main__":
    main()
