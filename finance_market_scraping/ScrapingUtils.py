from finance_market_scraping.ProjectImports import *

def rename_files(nit, periodo, anio, download_path, verbose=False):
    """
    Renames recently downloaded files based on provided parameters.

    Args:
        nit (str): NIT of the entity.
        periodo (str): Period of the report.
        anio (str): Year of the report.
        download_path (str): Path to the downloads directory.
        verbose (bool): Whether to print process details.

    Returns:
        None
    """
    files = os.listdir(download_path)

    for file in files:
        if file.startswith("00") and (file.endswith(".xbrl") or file.endswith(".pdf")):
            new_name = f"{nit}_{periodo}_{anio}{os.path.splitext(file)[1]}"
            os.rename(os.path.join(download_path, file), os.path.join(download_path, new_name))
            if verbose:
                print(f"Renamed: {file} -> {new_name}")

def click_element_with_retry(driver, element, retries=30, wait_time=1):
    """
    Attempts to click an element with retries.

    Args:
        driver: Selenium WebDriver instance.
        element: WebElement to be clicked.
        retries (int): Number of attempts.
        wait_time (int): Wait time between retries in seconds.

    Returns:
        bool: True if the click succeeds, False otherwise.
    """
    for attempt in range(retries):
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            time.sleep(wait_time)
            driver.execute_script("arguments[0].scrollIntoView();", element)
    return False

def celebrate(driver, anio_elegir, periodo_elegir, tipo_reporte_elegir):
    """
    Celébralo curramba.

    Adds celebratory effects to the webpage (just for fun).

    Args:
        driver: Selenium WebDriver instance.
        anio_elegir (str): Year of selection.
        periodo_elegir (str): Selected period.
        tipo_reporte_elegir (str): Selected report type.

    Returns:
        None
    """

    driver.execute_script(f"document.body.style.backgroundColor = 'darkblue';")
    
    messages = [
        f"Data scraped by Ospi B)",
        f"{anio_elegir} - {periodo_elegir} - {tipo_reporte_elegir}"
    ]
    for selector, message, color, size in [
        ('h2[style*="text-align: center"]', messages[0], 'white', '5em'),
        ('h4[style*="text-align: left"]', messages[1], 'orange', '2.5em')
    ]:
        driver.execute_script(f"""
            const el = document.querySelector('{selector}');
            if (el) {{
                el.innerText = '{message}';
                el.style.color = '{color}';
                el.style.fontSize = '{size}';
            }}
        """)
    time.sleep(1)

    # cool color transition effect B)
    for i in range(1_500):
        color = f'hsl({i}, 100%, 50%)'
        driver.execute_script(f"document.body.style.backgroundColor = '{color}';")