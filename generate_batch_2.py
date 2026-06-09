import os

TEMPLATES_DIR = "/root/nano/templates/prompts"

pages = {
    "ai-wedding-invitation-maker": {
        "title": "AI Wedding Invitation Maker & Design Prompts | Google Nano Banana",
        "desc": "Create elegant, high-end wedding invitations for free using AI. Copy our exact prompts for floral borders, watercolor accents, and typography backgrounds.",
        "h1": "AI Wedding Invitation Maker Prompts",
        "intro": "Why pay hundreds of dollars to a stationery designer when you can generate bespoke, high-end wedding invitations instantly? We've engineered the perfect AI prompts to output elegant floral borders, watercolor washes, and premium minimalist backgrounds ready for your text.",
        "prompt": "Elegant wedding invitation background, watercolor blush pink floral border, gold foil geometric accents, pure white negative space in the center, soft pastel lighting, high-end stationery design, flat lay --ar 3:4",
        "seo_h2": "How to Generate Flawless Wedding Stationery with AI",
        "seo_p1": "The biggest mistake people make when generating AI wedding invitations is asking the AI to write the text. Image generators are terrible at spelling and formatting text perfectly. Instead, your goal should be to generate the perfect **background and border artwork**, leaving a blank space in the middle so you can add your custom text later in Canva or Photoshop.",
        "seo_p2": "Use phrasing like 'negative space in the center' or 'blank white center' to ensure the AI leaves room for your details. To achieve a premium look, use artistic style keywords like 'watercolor wash', 'letterpress texture', or 'gold foil accents'. By specifying 'flat lay' or 'stationery design', you prevent the AI from generating a 3D object and instead get a flat, printable image perfect for luxury cardstock."
    },
    "ai-logo-generator-for-startups": {
        "title": "AI Logo Generator for Startups & Tech Brands | Google Nano Banana",
        "desc": "Generate clean, modern, and scalable logos for your tech startup or SaaS. Copy our minimalist AI logo prompts.",
        "h1": "AI Startup Logo Generator Prompts",
        "intro": "Startups need clean, memorable branding, not overly complex illustrations. Use these precision-engineered prompts to generate flat, scalable vector-style logos perfect for SaaS, apps, and tech companies.",
        "prompt": "A modern minimalist logo for a tech startup, abstract geometric fox shape, flat vector style, vibrant gradient of electric blue and neon purple, solid white background, clean lines, no text, dribbble style --ar 1:1",
        "seo_h2": "Creating Scalable AI Logos for Tech Brands",
        "seo_p1": "When using an AI logo generator for a business, simplicity is your ultimate goal. If you give a generic prompt, the AI will likely create an intricate emblem with photorealistic shading that looks terrible when scaled down to a tiny website favicon. You must force the AI into a graphic design mindset.",
        "seo_p2": "Always include constraints like 'flat vector style', 'minimalist', and 'clean lines'. It is highly recommended to append 'no text' to your prompt, as you can easily add your exact company name using a crisp web font later. Finally, enforce a 'solid white background' or 'solid black background' so you can easily remove the background with a single click and drop the transparent logo right onto your website."
    },
    "ai-tshirt-design-maker": {
        "title": "AI T-Shirt Design Maker & Merch Prompts | Google Nano Banana",
        "desc": "Design viral merch and graphic tees with AI. Use our specialized prompts for clean vector pop-art, vintage styles, and transparent-ready backgrounds.",
        "h1": "AI T-Shirt Design Prompts",
        "intro": "Building a Print-on-Demand empire? These prompts are formulated specifically for graphic tees. From retro 90s bootleg aesthetics to crisp vector pop-art, generate designs that are perfectly isolated and ready to print.",
        "prompt": "Vintage 90s bootleg rap shirt graphic of a cool cybernetic skeleton playing basketball, bold halftone textures, neon retro colors, pure black background, streetwear aesthetic, high contrast, clean edges --ar 3:4",
        "seo_h2": "Optimizing AI Art for Print-on-Demand Merch",
        "seo_p1": "Designing for t-shirts requires striking visuals with stark, clean edges. If an AI generates a beautiful painting with soft, faded edges, it will print like a messy, unappealing square on a cotton shirt. You need designs that 'pop' and can be easily isolated from their background.",
        "seo_p2": "To achieve this, command the AI to use a 'pure black background' (if printing on dark shirts) or 'pure white background' (if printing on light shirts). This makes background removal an instant, flawless process. Use stylistic keywords favored by the streetwear and merch industry, such as 'halftone textures', 'bold vector pop art', 'vintage distressed graphic', or 'traditional tattoo flash'. These styles translate exceptionally well to direct-to-garment (DTG) printing."
    },
    "ai-sticker-generator": {
        "title": "AI Sticker Generator & Die-Cut Prompts | Google Nano Banana",
        "desc": "Create perfect die-cut stickers for Redbubble, Etsy, or personal use. Copy our AI prompts for thick white borders and bold sticker art.",
        "h1": "AI Sticker Generator Prompts",
        "intro": "Generate flawless, ready-to-print die-cut stickers instantly. These specific prompts force the AI to encapsulate your design in a clean border, making them perfect for Redbubble, Etsy, or your laptop.",
        "prompt": "A cute kawaii ghost drinking iced coffee, thick white die-cut border around the outside, flat 2d vector art style, pure solid blue background, high contrast, bold colors, sticker design --ar 1:1",
        "seo_h2": "The Secret to Perfect AI Sticker Generation",
        "seo_p1": "The difference between a normal image and a great sticker is the edge. A true die-cut sticker needs a defined, continuous border so the cutting machine knows exactly where to slice. Standard AI prompts won't provide this naturally.",
        "seo_p2": "The magic phrase to include in every sticker prompt is 'thick white die-cut border'. You should also prompt for a solid, high-contrast background color (like 'pure solid blue background' or 'neon green background') that directly contrasts with the white border. This ensures that when you drop the image into a background removal tool, it perfectly isolates the sticker with its white border intact, giving you a professional-grade asset ready for immediate printing."
    },
    "ai-anime-background-generator": {
        "title": "AI Anime Background Generator & Scenery Prompts | Google Nano Banana",
        "desc": "Generate breathtaking Studio Ghibli and Makoto Shinkai style anime backgrounds for games, videos, and lo-fi streams.",
        "h1": "AI Anime Background Prompts",
        "intro": "Need gorgeous, cinematic anime backgrounds for a visual novel, Lo-Fi music stream, or YouTube video? We've cracked the prompt structure to perfectly emulate the nostalgic, highly detailed scenery of legendary anime studios.",
        "prompt": "Anime background scenery of a quiet Japanese train crossing at golden hour, fluffy detailed cumulonimbus clouds, warm glowing sunlight, Studio Ghibli style, lush green foliage, highly detailed painted background, cinematic anime aesthetic --ar 16:9",
        "seo_h2": "Emulating Legendary Anime Studios with AI",
        "seo_p1": "Anime backgrounds are famous for their unique blend of hyper-detailed architectural elements and soft, painterly nature scenes. To get this exact aesthetic, you can't just type 'anime style', as the AI will likely try to generate a character instead of a landscape.",
        "seo_p2": "Force the focus onto the environment by starting your prompt with 'Anime background scenery' or 'Anime establishing shot'. Reference specific studios or directors like 'Studio Ghibli style' or 'Makoto Shinkai style' to guide the lighting and texture engine. Focus heavily on atmospheric lighting phrases—'golden hour lighting', 'glowing dust motes', or 'soft rainy atmosphere'—as lighting is the defining characteristic that turns a flat drawing into a cinematic anime masterpiece."
    },
    "ai-comic-book-generator": {
        "title": "AI Comic Book Panel Generator & Prompts | Google Nano Banana",
        "desc": "Generate dramatic, dynamic comic book panels and graphic novel pages. Copy our AI prompts for Marvel, DC, and Noir styles.",
        "h1": "AI Comic Book Panel Prompts",
        "intro": "Creating a graphic novel just got infinitely faster. Use these highly-tuned prompts to generate dramatic, high-action comic panels complete with halftone shading, bold ink lines, and dynamic perspectives.",
        "prompt": "A dramatic comic book panel of a cyberpunk detective looking over a neon city from a gargoyle, extreme low angle perspective, heavy black ink shadows, Frank Miller noir style, halftone dots, vibrant graphic novel coloring --ar 16:9",
        "seo_h2": "Directing AI for Dynamic Graphic Novel Art",
        "seo_p1": "Standard AI images lack the dramatic flair and specific texture techniques used in the comic book industry. To generate panels that actually look like they were pulled from a graphic novel, you need to act as an art director, focusing heavily on ink style and camera angles.",
        "seo_p2": "Incorporate traditional comic techniques into your text, such as 'heavy black ink shadows', 'halftone dot shading', or 'crosshatching'. To create the explosive energy typical of the medium, dictate the camera angle aggressively. Use terms like 'extreme low angle', 'dutch angle', or 'foreshortened perspective'. Finally, referencing eras or specific industry styles—like 'Golden Age comic book style', 'modern Marvel aesthetic', or 'gritty noir graphic novel'—will perfectly tune the coloring and line weight."
    },
    "ai-sneaker-design-generator": {
        "title": "AI Sneaker Design Generator & Concept Art Prompts | Google Nano Banana",
        "desc": "Design the next hypebeast streetwear sneaker using AI. Generate 3D concept art of futuristic kicks with our custom prompts.",
        "h1": "AI Sneaker Concept Design Prompts",
        "intro": "Whether you're a fashion student, a 3D modeler, or just a sneakerhead, our AI prompts will help you conceptualize the next viral streetwear drop. Generate hyper-realistic, futuristic shoe concepts in seconds.",
        "prompt": "Product photography of a futuristic chunky streetwear sneaker, glowing neon orange accents, translucent sole, technical fabric textures, floating in mid-air, dark studio background, cinematic lighting, Nike concept design --ar 16:9",
        "seo_h2": "Rendering High-Fashion Footwear Concepts",
        "seo_p1": "To generate compelling sneaker concepts, the AI needs to understand material science and product photography. If you don't specify the textures, the shoe will look like a solid block of clay rather than a wearable, breathable piece of apparel.",
        "seo_p2": "Always dictate the materials explicitly. Use phrases like 'breathable mesh', 'translucent rubber sole', 'matte leather panels', or 'reflective metallic accents'. Frame the image by treating it as a high-end commercial shoot—using terms like 'dramatic studio lighting', 'product photography', and 'floating in mid-air' ensures the AI focuses entirely on the design of the shoe, eliminating distracting background elements."
    },
    "ai-moodboard-creator": {
        "title": "AI Moodboard Creator & Aesthetic Prompts | Google Nano Banana",
        "desc": "Generate instant aesthetic moodboards and concept collages for brands, fashion shoots, or creative projects.",
        "h1": "AI Aesthetic Moodboard Prompts",
        "intro": "Creative directors and brand managers: instantly generate cohesive aesthetic moodboards to pitch your vision. Our prompts combine textures, color palettes, and photography into perfect inspirational grids.",
        "prompt": "A cohesive visual moodboard for a luxury organic skincare brand, split panel collage, containing soft neutral linen textures, a minimalist glass bottle, abstract beige shapes, and warm morning sunlight, editorial layout --ar 16:9",
        "seo_h2": "Generating Cohesive Visual Collages",
        "seo_p1": "Moodboards are about conveying a 'vibe' rather than a single distinct object. The challenge with AI is getting it to generate multiple distinct concepts within a single frame while maintaining a unified color palette.",
        "seo_p2": "To trick the AI into creating a collage, use formatting keywords like 'split panel collage', 'editorial grid layout', or 'curated moodboard'. Next, list 3 to 4 distinct but related elements separated by commas (e.g., 'a marble texture, a gold ring, a neutral paint swatch'). Finally, wrap the entire prompt in a unifying lighting or aesthetic term, such as 'cohesive earthy color palette' or 'soft film photography style', to ensure the disparate elements look like they belong in the same brand presentation."
    }
}

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="https://googlenanobanana.com/prompts/{slug}">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 0; line-height: 1.6; max-width: 100%; overflow-x: hidden; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        h1 {{ color: #fbbf24; font-size: 2.5rem; margin-bottom: 20px; }}
        .intro-box {{ background: #1e293b; padding: 25px; border-radius: 12px; border-left: 4px solid #fbbf24; margin-bottom: 30px; font-size: 1.1rem; }}
        .prompt-box {{ background: #000; padding: 20px; border-radius: 8px; font-family: monospace; color: #10b981; margin-bottom: 30px; border: 1px solid #334155; }}
        .cta-btn {{ display: inline-block; background: #fbbf24; color: #000; padding: 15px 30px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 1.2rem; transition: transform 0.2s; }}
        .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3); }}
        a {{ color: #fbbf24; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div style="padding: 20px; text-align: center; border-bottom: 1px solid #1e293b;">
        <a href="/" style="font-size: 1.5rem; font-weight: bold; text-decoration: none;">🍌 Google Nano Banana</a>
    </div>
    <div class="container">
        <h1>{h1}</h1>
        
        <div class="intro-box">
            <p>{intro}</p>
        </div>
        
        <h2>The Master Prompt</h2>
        <p>Copy and paste this into our free Google Nano Banana generator:</p>
        
        <div class="prompt-box">
            {prompt}
        </div>
        <div style="text-align: center; margin: 40px 0;">
            <a href="/" class="cta-btn">Generate This Image Now</a>
        </div>
        
        <div style="margin-top: 40px; padding-top: 40px; border-top: 1px solid #334155; text-align: left;">
            <div style="background-color: #0f172a; color: #f8fafc; padding: 40px 20px; line-height: 1.8;">
                <h2 style="font-size: 28px; margin-bottom: 20px; color: #e2e8f0;">{seo_h2}</h2>
                <p style="margin-bottom: 16px;">{seo_p1}</p>
                <p style="margin-bottom: 16px;">{seo_p2}</p>
            </div>
        </div>
    </div>
</body>
</html>"""

os.makedirs(TEMPLATES_DIR, exist_ok=True)

for slug, data in pages.items():
    file_path = os.path.join(TEMPLATES_DIR, f"{slug}.html")
    content = html_template.format(
        title=data["title"],
        desc=data["desc"],
        slug=slug,
        h1=data["h1"],
        intro=data["intro"],
        prompt=data["prompt"],
        seo_h2=data["seo_h2"],
        seo_p1=data["seo_p1"],
        seo_p2=data["seo_p2"]
    )
    with open(file_path, "w") as f:
        f.write(content)
        print(f"Created: {file_path}")

print("Done generating batch 2 HTML files.")
