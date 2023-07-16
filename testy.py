from app.bezkolejki.drivers import selenium_driver as sd

driver = sd.SeleniumBaseFields(base_link=sd.BASE_LINK, driver_name='edge')

# driver.close()