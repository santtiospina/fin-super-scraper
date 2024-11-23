from finance_market_scraping.ProjectImports import *
from finance_market_scraping.ScrapingUtils import rename_files, click_element_with_retry, celebrate

def setup_driver(download_path):
    """Sets up the Selenium WebDriver."""
    options = Options()
    prefs = {"download.default_directory": download_path}
    options.add_argument('--start-maximized')
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(service=Service(), options=options)

def scrape_data(driver, nits, anios, tipos_reporte, periodos, download_path):
    for anio_elegir in anios:
        for tipo_reporte_elegir in tipos_reporte:
            for periodo_elegir in periodos:
                for nit in nits:
                    try: 
                        # region Scraping SIMEV
                        # region Abrir SIMEV
                        link = "https://www.superfinanciera.gov.co/SIMEV2/rnve/informesfinancierosniif/001/000051/0"
                        driver.get(link)
                        time.sleep(0.5)
                        # endregion

                        # region Buscar tarjeta del NIT
                        # Buscar 2 veces porque la página no responde bien a la primera
                        for i in range(2):
                            search_input = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Buscar por nombre de entidad o NIT"]'))
                            )
                            search_input.send_keys(nit)
                            search_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '//span[@class="govco-icon govco-icon-search-cn size-27x text-marine"]'))
                            )
                            click_element_with_retry(driver, search_button)
                            time.sleep(0.5)
                        
                        target_card = driver.execute_script(
                        f'return document.evaluate("//div[@id=\'cardRNVE\' and contains(.//p, \'NIT: {nit}\')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'
                        )
                        if target_card:
                            target_card.click()
                        else:
                            print(f"No se encontró ninguna tarjeta con NIT: {nit}")
                        driver.execute_script("window.scrollTo(0, 1000);")
                        # endregion

                        # region Clic en "Resumen de la entidad"
                        resumen_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@id="dropdownMenuButton" and text()=" Resumen de la entidad "]'))
                        )
                        click_element_with_retry(driver, resumen_button)
                        # endregion

                        # region Información financiera
                        informacion_financiera = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//a[contains(@href, "/SIMEV2/rnve/") and text()=" Información financiera "]'))
                        )

                        ActionChains(driver).move_to_element(informacion_financiera).perform()
                        time.sleep(0.5)

                        # Clic en informes financieros bajo NIIF
                        try:
                            informes_financieros = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//a[contains(@href, "/SIMEV2/rnve/informesfinancierosniif/") and text()="Informes financieros bajo NIIF y anexos"]')
                                )
                            )
                            informes_financieros.click()
                        except Exception as e:
                            logging.error(f"Error al intentar dar clic en 'Informes financieros bajo NIIF y anexos': {e}")
                        
                        time.sleep(0.5)
                        # endregion

                        # region Seleccionar año de consulta
                        anio_consulta_dropdown = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                '//div[label[contains(text(), "Año")]]//button[contains(@class, "dropdown-toggle")]'
                            ))
                        )
                        click_element_with_retry(driver, anio_consulta_dropdown)

                        anio_clic = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                f'//option[contains(@class, "dropdown-item") and contains(text(), {anio_elegir})]'
                            ))
                        )
                        driver.execute_script("arguments[0].click();", anio_clic)
                        # endregion

                        # region Seleccionar tipo de reporte
                        tipo_reporte_dropdown = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                '//div[label[contains(text(), "Tipo de reporte")]]//button[contains(@class, "dropdown-toggle")]'
                            ))
                        )
                        click_element_with_retry(driver, tipo_reporte_dropdown)

                        tipo_reporte_clic = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                f'//option[contains(@class, "dropdown-item") and contains(text(), "{tipo_reporte_elegir}")]'
                            ))
                        )
                        driver.execute_script("arguments[0].click();", tipo_reporte_clic)
                        # endregion

                        # region Seleccionar periodo
                        periodo_dropdown = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((
                                By.XPATH,
                                '//div[label[contains(text(), "Periodo")]]//button[contains(@class, "dropdown-toggle")]'
                            ))
                        )
                        click_element_with_retry(driver, periodo_dropdown)

                        
                        periodo_clic = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                f'//option[contains(@class, "dropdown-item") and contains(text(), "{periodo_elegir}")]'
                            ))
                        )
                        driver.execute_script("arguments[0].click();", periodo_clic)
                        
                        # bajar para que se vean los botones de descarga
                        driver.execute_script("window.scrollTo(0, 1250);")
                        time.sleep(2)
                        # endregion

                        # region Download XBRL

                        try:
                            xbrl_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[contains(@class, "btn btn-low no-padding hasTooltip") and contains(text(), "VER XBRL")]')
                                )
                            )
                            click_element_with_retry(driver, xbrl_button)
                    
                            descargar_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[@id="btnDescargaNiif" and contains(text(), "DESCARGAR")]'))
                            )
                            click_element_with_retry(driver, descargar_button)
                            time.sleep(0.1)

                            boton_cerrar = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[contains(@class, "btn btn-close-modal")]')
                                )
                            )
                            click_element_with_retry(driver, boton_cerrar)
                        except TimeoutException as e:
                            logging.error(f"* XBRL not found: {nit} {periodo_elegir} {anio_elegir}")
                            # print(f"* XBRL not found: {nit} {periodo_elegir} {anio_elegir}")

                        # Download PDF
                        try:
                            pdf_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[contains(@class, "btn btn-low no-padding") and contains(text(), "VER PDF")]'))
                            )
                            time.sleep(0.15)
                            click_element_with_retry(driver, pdf_button)

                            time.sleep(0.5)

                            descargar_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[@id="btnDescargaNiif" and contains(text(), "DESCARGAR")]'))
                            )
                            click_element_with_retry(driver, descargar_button)

                            time.sleep(0.1)

                            boton_cerrar = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//button[contains(@class, "btn btn-close-modal")]')
                                )
                            )
                            click_element_with_retry(driver, boton_cerrar)
                        except TimeoutException as e:
                            logging.error(f"* PDF not found: {nit} {periodo_elegir} {anio_elegir}")
                        
                        try:
                            rename_files(nit, periodo_elegir[0:3].lower(), anio_elegir, download_path)
                        except Exception as e:
                            logging.error(f"Error while renaming files: {e}")
                        
                        time.sleep(2)
                        
                        try:
                            rename_files(nit, periodo_elegir[0:3].lower(), anio_elegir, download_path)
                        except Exception as e:
                            logging.error(f"Error while renaming files: {e}")

                        # endregion

                        # endregion

                    except Exception as e:
                            logging.error(f"Error while processing NIT {nit}: {e}")

        driver.execute_script("window.scrollTo(0, 1600);")
        celebrate(driver, anio_elegir, periodo_elegir, tipo_reporte_elegir)

def main():
    load_dotenv()
    
    # define the path where the files will be downloaded:
    download_path = "/Users/santiospina/Documents/Projects/finance_market_scraping/scraped_files"
    
    driver = setup_driver(download_path)
    logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

    # parameters
    
    '''
    # NITs with both XBRL and PDF (this may vary: written in nov 2024)
    nits = [
    "800167643", "800169499", "800216181", "800226766", "800242106", "800249860", 
    "811000740", "811010754", "811012271", "811019012", "811026226", "811030322", 
    "817000676", "830025448", "830029703", "830095213", "830112317", "830122566", 
    "860002464", "860002541", "860002554", "860003012", "860005223", "860025674", 
    "860028601", "860029995", "860053930", "860063875", "890100251", "890105526", 
    "890205952", "890208395", "890300440", "890300604", "890301884", "890302567", 
    "890302594", "890309496", "890318252", "890321567", "890400869", "890900050", 
    "890900099", "890900259", "890900266", "890900285", "890900308", "890900608", 
    "890901110", "890903474", "890914525", "890922447", "891301592", "891301676", 
    "891900101", "900087414", "900430878", "900591195", "901544345"
    '''

    nits = [ "900430878", "900087414"]
    anios = ["2024"]
    tipos_reporte = ["Intermedios"]
    periodos = ["Septiembre"]

    try:
        scrape_data(driver, nits, anios, tipos_reporte, periodos, download_path)
    finally:
        # to rename the last one, just in case
        try:
            rename_files(nits[-1], periodos[-1][0:3].lower(), anios[-1], download_path)
        except Exception as e:
            logging.error(f"Error while renaming files: {e}")

        driver.quit()

if __name__ == "__main__":
    main()