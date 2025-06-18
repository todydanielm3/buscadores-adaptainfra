from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://adaptainfra.streamlit.app/")

    # Aguarda o botão com texto visível
    page.wait_for_selector("button:has-text('Artículos Publicaciones')")

    # Clica no botão exato
    page.click("button:has-text('Artículos Publicaciones')")

    # Espera para visualizar o resultado
    page.wait_for_timeout(5000)
    browser.close()
