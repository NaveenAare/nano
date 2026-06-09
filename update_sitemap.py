import os
import xml.etree.ElementTree as ET

SITEMAP_PATH = "/root/nano/static/sitemap.xml"
TEMPLATES_DIR = "/root/nano/templates/prompts"
BASE_URL = "https://googlenanobanana.com/prompts/"

ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
tree = ET.parse(SITEMAP_PATH)
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Extract existing URLs
existing_urls = set()
for url in root.findall('ns:url', namespace):
    loc = url.find('ns:loc', namespace)
    if loc is not None and loc.text is not None:
        existing_urls.add(loc.text.strip())

added_count = 0

# Check templates/prompts/ for new files
for filename in os.listdir(TEMPLATES_DIR):
    if filename.endswith(".html"):
        slug = filename[:-5] # remove .html
        page_url = BASE_URL + slug
        
        if page_url not in existing_urls:
            # Create new <url> element
            url_el = ET.Element('url')
            
            loc_el = ET.SubElement(url_el, 'loc')
            loc_el.text = page_url
            
            changefreq_el = ET.SubElement(url_el, 'changefreq')
            changefreq_el.text = "weekly"
            
            priority_el = ET.SubElement(url_el, 'priority')
            priority_el.text = "0.8"
            
            root.append(url_el)
            added_count += 1
            print(f"Added {page_url} to sitemap")

if added_count > 0:
    tree.write(SITEMAP_PATH, encoding='UTF-8', xml_declaration=True)
    print(f"Sitemap updated successfully with {added_count} new pages.")
else:
    print("No new pages to add to sitemap.")
