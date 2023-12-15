from playwright.sync_api import sync_playwright
import json

def extract_actual_selectors():
    """
    Extract real selectors from BitSight website
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("\nExtracting actual DOM selectors from bitsight.com...")
        print("="*60)
        
        page.goto('https://www.bitsight.com', wait_until='domcontentloaded', timeout=60000)
        
        # Extract all the actual selectors we need
        selectors = page.evaluate('''() => {
            const result = {
                navigation: {},
                buttons: {},
                forms: {},
                links: {},
                structure: {}
            };
            
            // 1. Navigation structure
            const nav = document.querySelector('nav, [role="navigation"], header');
            if (nav) {
                result.navigation.mainNav = {
                    tagName: nav.tagName,
                    className: nav.className,
                    id: nav.id
                };
            }
            
            // 2. Find actual menu items
            const menuItems = [];
            document.querySelectorAll('a, button').forEach(el => {
                const text = el.textContent.trim().toLowerCase();
                if (text.includes('solution') || text.includes('product') || 
                    text.includes('resource') || text.includes('company')) {
                    menuItems.push({
                        text: el.textContent.trim(),
                        tagName: el.tagName,
                        className: el.className,
                        href: el.href || '',
                        hasDropdown: el.getAttribute('aria-expanded') !== null
                    });
                }
            });
            result.navigation.menuItems = menuItems;
            
            // 3. CTA Buttons
            const ctaButtons = [];
            ['demo', 'login', 'sign', 'get started', 'contact'].forEach(keyword => {
                const elements = Array.from(document.querySelectorAll('a, button')).filter(
                    el => el.textContent.toLowerCase().includes(keyword)
                );
                elements.forEach(el => {
                    ctaButtons.push({
                        text: el.textContent.trim(),
                        tagName: el.tagName,
                        className: el.className,
                        href: el.href || ''
                    });
                });
            });
            result.buttons.cta = ctaButtons;
            
            // 4. Hero section
            const h1 = document.querySelector('h1');
            if (h1) {
                result.structure.hero = {
                    h1Text: h1.textContent.trim(),
                    h1Class: h1.className,
                    parentClass: h1.parentElement.className
                };
            }
            
            // 5. Forms
            const forms = document.querySelectorAll('form');
            result.forms.count = forms.length;
            result.forms.details = Array.from(forms).map(form => ({
                id: form.id,
                className: form.className,
                action: form.action,
                method: form.method
            }));
            
            // 6. Footer
            const footer = document.querySelector('footer');
            if (footer) {
                result.structure.footer = {
                    className: footer.className,
                    linkCount: footer.querySelectorAll('a').length
                };
            }
            
            // 7. Images
            const images = document.querySelectorAll('img');
            result.structure.imageCount = images.length;
            result.structure.firstImages = Array.from(images).slice(0, 3).map(img => ({
                src: img.src,
                alt: img.alt,
                className: img.className
            }));
            
            return result;
        }''')
        
        # Print the results
        print("\n1. NAVIGATION STRUCTURE:")
        print("-"*40)
        if selectors['navigation']['mainNav']:
            nav = selectors['navigation']['mainNav']
            print(f"Main Nav Tag: {nav['tagName']}")
            print(f"Main Nav Class: {nav['className']}")
            print(f"Main Nav ID: {nav['id']}")
        
        print("\n2. MENU ITEMS FOUND:")
        print("-"*40)
        for item in selectors['navigation']['menuItems']:
            print(f"- {item['text']}")
            print(f"  Tag: {item['tagName']}, Class: {item['className'][:50]}")
            if item['hasDropdown']:
                print(f"  Has Dropdown: Yes")
        
        print("\n3. CTA BUTTONS:")
        print("-"*40)
        for button in selectors['buttons']['cta'][:5]:
            print(f"- {button['text']}")
            print(f"  Tag: {button['tagName']}, Class: {button['className'][:50]}")
        
        print("\n4. HERO SECTION:")
        print("-"*40)
        if selectors['structure'].get('hero'):
            hero = selectors['structure']['hero']
            print(f"H1 Text: {hero['h1Text']}")
            print(f"H1 Class: {hero['h1Class']}")
        
        print("\n5. FORMS:")
        print("-"*40)
        print(f"Forms found: {selectors['forms']['count']}")
        for form in selectors['forms']['details']:
            print(f"- Form ID: {form['id']}, Class: {form['className'][:50]}")
        
        print("\n6. FOOTER:")
        print("-"*40)
        if selectors['structure'].get('footer'):
            footer = selectors['structure']['footer']
            print(f"Footer Class: {footer['className']}")
            print(f"Footer Links: {footer['linkCount']}")
        
        # Save to file for reference
        with open('actual_selectors.json', 'w') as f:
            json.dump(selectors, f, indent=2)
        print("\n✅ Actual selectors saved to actual_selectors.json")
        
        browser.close()
        return selectors

if __name__ == "__main__":
    extract_actual_selectors()
