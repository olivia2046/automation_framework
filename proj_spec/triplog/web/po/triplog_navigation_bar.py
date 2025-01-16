# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/9 12:26
# @Author : Olivia
# Desc:
# **************************************
import logging

from selenium.webdriver.common.by import By


from proj_spec.triplog.web.po.triplog_base_page import TriplogWebBasePage


class TriplogNavigationBar(TriplogWebBasePage):
    _product_box_loc = (By.CSS_SELECTOR,".n_product-box.n_box")

    def navigate(self, first_level_menu, second_level_menu=""):
        """

        :return:
        """
        try:
            first_level_menu_loc = (By.XPATH,'//span[@class="n_nav-main-menu-text" and text()="%s"]'%first_level_menu)
            # second_level_menu_loc = (By.XPATH,"//li[@class='n_submenu-item n_submenu-selected']/a[contains(text(),'%s')]"%second_level_menu) # the class of the li element is changing each visitation?
            second_level_menu_loc = (By.XPATH, "//li[contains(@class,'n_submenu-item')]/a[contains(text(),'%s')]"%second_level_menu)

            first_level_menu_element = self.find_element(first_level_menu_loc,condition="presence_of_element_located")
            if not first_level_menu_element.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", first_level_menu_element)


            self.hover_over_element(first_level_menu_loc)
            if second_level_menu!="":
                #self.find_element_and_click((By.XPATH,"//li[@class='n_submenu-item n_submenu-selected']/a[contains(text(),'%s')]"%second_level_menu))
                self.find_element_and_click(second_level_menu_loc)
            from proj_spec.triplog.web.po.triplog_navigable_page import TriplogNavigablePage
            return TriplogNavigablePage(self.driver)
        except Exception as e:
            logging.error(e)
            return None


    def goto_trips(self):
        from proj_spec.triplog.web.po.mileage.trips_page import TripsPage
        self.find_element(self._product_box_loc)
        self.navigate("Mileage","Trips")
        return TripsPage(self.driver)



