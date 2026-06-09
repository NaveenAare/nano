import os

TEMPLATES_DIR = "/root/nano/templates/prompts"

pages = {
    "ai-tattoo-stencil-maker": {
        "title": "AI Tattoo Stencil Maker & Generator Prompts | Google Nano Banana",
        "desc": "Generate custom AI tattoo designs and printable line-art stencils instantly. Copy our tested prompts for clean, perfect ink.",
        "h1": "AI Tattoo Stencil Maker Prompts",
        "intro": "Finding the perfect tattoo design shouldn't mean scrolling Pinterest for hours. We've crafted specific prompts that force the AI to output clean, high-contrast, printable tattoo stencils that your artist can actually use.",
        "prompt": "A minimalist fine-line geometric wolf tattoo, pure white background, solid black ink, high contrast, clean vector line art stencil style, printable tattoo flash --ar 1:1",
        "seo_h2": "Advanced Parameters for AI Tattoo Stencil Generation",
        "seo_p1": "Creating usable AI tattoo designs requires a completely different approach than standard image generation. Most AI models default to photorealistic shading and blended colors, which are notoriously difficult for tattoo artists to translate into a stencil. To fix this, your prompts must explicitly command the AI to focus on line weight, contrast, and negative space.",
        "seo_p2": "The golden rule for AI tattoo prompts is commanding a 'pure white background' and 'solid black ink'. Adding terms like 'vector line art', 'tattoo flash sheet', and 'unshaded stencil' strips away the unnecessary complexity. Whether you want a traditional American style piece, fine-line minimalism, or heavy blackwork, guiding the AI to focus on stark contrasts ensures the final image can be easily run through a thermal printer at your local studio."
    },
    "ai-hairstyle-try-on": {
        "title": "AI Hairstyle Try-On & Haircut Generator Prompts | Google Nano Banana",
        "desc": "Visualize your next haircut before going to the salon. Use our AI hairstyle try-on prompts to generate realistic new looks.",
        "h1": "AI Hairstyle Try-On Prompts",
        "intro": "Terrified of getting a bad haircut? Don't guess—visualize it. We've optimized prompts that seamlessly blend trendy hairstyles and hair colors onto a reference image, so you know exactly what it looks like before the scissors come out.",
        "prompt": "Portrait of a person with a textured messy fringe fade haircut, matte lighting, high fashion photography, ultra-realistic hair texture, barbershop lighting --ar 3:4",
        "seo_h2": "How to Guide AI for Realistic Hairstyle Previews",
        "seo_p1": "The biggest challenge with AI hairstyle generation is maintaining the structural integrity of the face while fully replacing the hair physics. Standard prompts often result in 'helmet hair' or unnatural blending at the roots. To achieve a realistic preview that you can confidently show your barber or stylist, your text prompts need to include lighting and texture instructions.",
        "seo_p2": "When generating new hair colors, specify the exact tone (e.g., 'ash blonde balayage' rather than just 'blonde') to prevent the AI from defaulting to cartoonish yellows. For haircuts, use precise industry terminology like 'curtain bangs', 'taper fade', or 'layered wolf cut'. Adding terms like 'editorial photography' and 'natural hair texture' forces the AI to render individual strands rather than a block of color, giving you a true-to-life try-on experience."
    },
    "ai-room-remodel": {
        "title": "AI Room Remodel & Interior Design Prompts | Google Nano Banana",
        "desc": "Redesign your living room, kitchen, or exterior instantly. Copy our interior design AI prompts for photorealistic room remodeling.",
        "h1": "AI Room Remodel Prompts",
        "intro": "Renovating a house is expensive; visualizing it should be free. Use these specific architectural prompts to transform photos of empty or outdated rooms into stunning, magazine-ready interior designs.",
        "prompt": "Interior design of a modern farmhouse kitchen, natural warm light, sage green cabinets, white quartz countertops, exposed wood beams, architectural digest photography --ar 16:9",
        "seo_h2": "Mastering Architectural and Interior AI Prompts",
        "seo_p1": "When using AI for a room remodel, lighting and spatial consistency are everything. If you simply ask for 'a nice kitchen', the AI might generate an impossible floor plan or warped perspectives. To get accurate interior design mockups, you need to use architectural photography keywords.",
        "seo_p2": "Start by defining the exact style: Mid-Century Modern, Japandi, Industrial, or Coastal. Then, dictate the lighting sources using phrases like 'natural sunlight streaming through large windows' or 'warm ambient recessed lighting'. Finally, mentioning specific materials ('matte black fixtures', 'herringbone wood floors', 'terrazzo tiles') grounds the AI in reality, producing an image that your contractor can actually use as a reference point."
    },
    "ai-pet-portrait-maker": {
        "title": "AI Pet Portrait Maker Prompts (Pixar Style) | Google Nano Banana",
        "desc": "Turn photos of your dog or cat into stunning 3D Pixar-style movie posters. Use our viral AI pet portrait generator prompts.",
        "h1": "AI Pet Portrait Maker Prompts",
        "intro": "Ready to make your pet the star of their own animated movie? These prompts are engineered to perfectly recreate the iconic, highly-rendered 3D animation style for your dogs, cats, and exotic pets.",
        "prompt": "A 3D animated movie poster of a golden retriever wearing a tiny red bandana, Pixar style animation, highly detailed fur, vibrant studio lighting, cinematic, 8k resolution --ar 3:4",
        "seo_h2": "Nailing the 3D Animated Style for Pet Portraits",
        "seo_p1": "The viral trend of turning pets into animated movie posters relies heavily on specific render engine keywords. The AI needs to know it shouldn't produce a real photograph or a flat 2D cartoon, but rather a volumetric, 3D CGI masterpiece. This requires prompting for lighting and texture simultaneously.",
        "seo_p2": "To get the best results, use phrases like 'Octane Render', 'Unreal Engine 5', and 'Pixar style'. When describing the pet, focus on exaggerating their cutest features (e.g., 'big expressive eyes', 'fluffy detailed fur'). Setting the environment is also crucial—putting them in a 'magical glowing forest' or a 'cozy warmly lit bedroom' adds the narrative depth required to make the image look like a genuine movie poster."
    },
    "ai-coloring-page-generator": {
        "title": "AI Coloring Page Generator Prompts | Google Nano Banana",
        "desc": "Create endless printable coloring book pages for kids and adults. Copy our AI prompts for clean, crisp black and white line art.",
        "h1": "AI Coloring Page Generator Prompts",
        "intro": "Teachers, parents, and artists: stop buying coloring books. With these precise prompts, you can force the AI to generate flawless, unshaded black-and-white line art of any subject you can imagine.",
        "prompt": "A cute baby dinosaur drinking tea on the moon, clean vector line art, coloring book page for kids, pure white background, crisp black outlines, no shading, simple shapes --ar 3:4",
        "seo_h2": "Optimizing AI Prompts for Printable Coloring Pages",
        "seo_p1": "Generating a coloring page seems simple, but AI naturally wants to add shading, grayscale tones, and complex textures. If these are present, the image becomes muddy when printed and frustrating to color. The secret to a perfect coloring page prompt is exclusion.",
        "seo_p2": "You must explicitly use negative constraints or highly specific styles like 'pure line art', 'unshaded', and 'monochrome vector'. For children's pages, add 'simple shapes' and 'thick outlines' to ensure the designs are approachable. For adult coloring books, you can swap those for 'intricate mandala patterns' and 'detailed zentangle style'. Regardless of the audience, always enforce a pure white background to save printer ink."
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

print("Done generating HTML files.")
