import seleniumbase
from seleniumbase import SB
import time
from selenium.webdriver.common.by import By
from random import uniform
from tkinter import  messagebox
from DatabaseModel import *

EMAIL = 'npltariklthu04@mailsac.com'
PASSWORD = '@T147852a#@'
URLS_DICT = {"Thailand": "https://visa.vfsglobal.com/tha/en/ltp/login",
             "Dubai": "https://visa.vfsglobal.com/are/en/ltp/login",
             "Malaysia": "https://visa.vfsglobal.com/mys/en/ltp/login",
             "Baku": "https://visa.vfsglobal.com/aze/en/ltp/login"}

def WaitForLoadingToComplete(driver : seleniumbase.BaseCase):
    loading_path = '//div[@class="ngx-overlay loading-foreground"]'
    i = 1
    while True:
        if driver.is_element_present(loading_path):
            print(f"Loading appears: {i}")
            time.sleep(5)
            i += 1

        else:
            print("Loading Completed")
            break

def ExecuteBot(client_details : dict):
    URL = URLS_DICT.get(client_details['Country'])

    with SB(uc=True, test = True, incognito = True) as driver:
        driver : seleniumbase.BaseCase

        #-------------------- LOGGING SECTION STARTED!! : 0 --------------------
        try:
            # Initializing VFS Global website
            print(f"User Agent: '{driver.get_user_agent()}'")
            driver.maximize_window()
            driver.uc_open_with_reconnect(URL, 25)

            # Accepting all cookies in VFS Global website
            acceptcookies_xpath = '//button[@id="onetrust-accept-btn-handler"]'
            WaitForLoadingToComplete(driver)
            driver.click(acceptcookies_xpath,timeout=20)
            driver.sleep(0.5)

            # Getting and updating latest cookies to avoid getting spam/blocked
            driver.get_cookies()
            cook = driver.get_cookies()
            driver.add_cookies(cook)

        except Exception as error:
            print(f"Fail to login due to unexpected issue -> '{error}'")
            messagebox.showerror("Login Issue", message= 'Fail to login due to unexpected issue!')

        #Filling the email
        print("Filling Username")
        email_input = driver.find_element(By.ID, 'email')
        for email_key in EMAIL:
            email_input.send_keys(email_key)
            time.sleep(uniform(0,0.5))

        #Filling the password
        print("Filling Password")
        password_input = driver.find_element(By.ID, 'password')
        for pass_key in PASSWORD:
            password_input.send_keys(pass_key)
            time.sleep(uniform(0,0.5))

        #Handling captcha (if not solved automatically)
        print("Handling Captcha")
        driver.uc_gui_handle_captcha()

        #Logging in!
        submitbutton_xpath = "//button[contains(@class,'mat-btn-lg')]"
        signin_button = driver.find_element(By.XPATH,submitbutton_xpath)
        signin_button.click()
        WaitForLoadingToComplete(driver)
        print("Clicked Sign In!!!")
        #-------------------- LOGGING SECTION ENDED!!: 0 --------------------

        #-------------------- POST LOGIN SECTION STARTED!!: 1 --------------------
        newbooking_xpath = "//span[contains(.,'Start New Booking')]/parent::button[contains(@class,'d-lg-inline-block')]"
        try:
            WaitForLoadingToComplete(driver)
            driver.wait_for_element_clickable(newbooking_xpath)
            print("Login Successful!")
            Book_Appointment(driver = driver,client_details = client_details)
        except Exception as error:
            print(f"Fail to login due to unexpected issue -> '{error}'")
            messagebox.showerror("Login Issue", message= 'Fail to login due to unexpected issue!')

def Book_Appointment(driver : seleniumbase.BaseCase, client_details : dict):

    try:
        #Clicking Start New Booking Button!!!
        newbooking_xpath = "//span[contains(.,'Start New Booking')]/parent::button[contains(@class,'d-lg-inline-block')]"
        driver.wait_for_element_clickable(newbooking_xpath)
        driver.click(newbooking_xpath)
        print("Clicked Start New Booking Button!!!")
        WaitForLoadingToComplete(driver)
        #-------------------- POST LOGIN SECTION ENDED!! : 1 --------------------

        #-------------------- APPLICATION DETAILS SECTION STARTED!! : 2 --------------------
        #Select 'Lithuania Temporary Residence Permit' Booking slot
        appointmentcategory_xpath = '//mat-select[@formcontrolname="selectedSubvisaCategory"]'
        selectcategory_xpath = "//span[contains(.,'Lithuania Temporary Residence Permit')]/parent::*"

        try:
            driver.assert_element_present(appointmentcategory_xpath)
        except Exception as err:
            print(f"Error in Lithuania Temporary Residence Permit dropdown option not appeared -> '{err}'")
            messagebox.showerror("BOT ERROR",'Did not find the "Lithuania Temporary Residence Permit" dropdown option, Session closed!')
            return

        driver.wait_for_element_clickable(appointmentcategory_xpath)
        driver.click(appointmentcategory_xpath)
        if not driver.is_element_present(selectcategory_xpath):
            driver.sleep(2)
            driver.click(appointmentcategory_xpath)
        driver.click(selectcategory_xpath)
        WaitForLoadingToComplete(driver)

        nobookings_xpath = "//div[contains(@class,'alert-info') and contains(.,'We are sorry')]"
        yesbookgins_xpath = "//div[contains(@class,'alert-info') and not(contains(.,'We are sorry'))]"
        try:
            # If booking available, Bot processes will continue
            driver.assert_element_present(yesbookgins_xpath,timeout=15)
            # -------------------- APPLICATION DETAILS SECTION ENDED!! : 2 --------------------

            # -------------------- YOUR DETAILS SECTION STARTED!! : 3 --------------------
            #Clicking Continue button when booking available!
            continueenabledbtn_xpath = "//span[@class='mat-button-wrapper' and contains(.,'Continue')]/parent::button[not(@disabled = 'true')]"
            driver.click(continueenabledbtn_xpath)
            WaitForLoadingToComplete(driver)

            #Fill the Appointment fields
            applicantwindow_xpath = "//h2[contains(text(),'Applicant')]"
            migris_xpath = "//input[contains(@placeholder,'MIGRIS')]"
            firstname_xpath = "//input[contains(@placeholder,'first name')]"
            lastname_xpath = "//input[contains(@placeholder,'last name')]"
            passportnum_xpath = "//input[contains(@placeholder,'passport')]"
            phonecode_xpath = "//input[@id='mat-input-9']"
            phonenum_xpath = "//input[@id='mat-input-10']"
            email_xpath = "//input[contains(@placeholder,'Email')]"
            passportexpire_xpath = "//input[contains(@placeholder,'date') and starts-with(@id,'passportExpir')]" #20122022 no slashes
            dob_xpath = "//input[contains(@placeholder,'date') and @id='dateOfBirth']"  #20122022 no slashes
            gender_xpath = "//mat-select[@id='mat-select-6']"
            nationality_xpath = "//mat-select[@id='mat-select-8']"
            savebtn_xpath = '//span[@class="mat-button-wrapper" and contains(text(),"Save")]/parent::button'
            invaliddetails_xpath = "//mat-dialog-container//p[contains(text(),'enter valid detail')]"
            continuebtn_xpath = '//span[@class="mat-button-wrapper" and contains(text(),"Continue")]/parent::button'
            firstbookingdate_xpath = "//td[contains(@class,'date-availiable')][1]"
            firstbookingtime_xpath = '//input[@name="SlotRadio"][1]/parent::*'
            acceptterms_xpath = '//input[@id="mat-checkbox-1-input"]'
            confirmbtn_xpath = '//span[@class="mat-button-wrapper" and contains(text(),"Confirm")]/parent::button'

            try:
                driver.assert_element_present(applicantwindow_xpath)

                print("Filling all the fields")
                driver.send_keys(migris_xpath, client_details['Migris'])
                driver.send_keys(firstname_xpath, client_details['First Name'])
                driver.send_keys(lastname_xpath, client_details['Last Name'])
                driver.send_keys(dob_xpath, client_details['DOB'].replace('/', ''))
                driver.send_keys(passportnum_xpath, client_details['Passport Num'])
                driver.send_keys(passportexpire_xpath, client_details['Passport Expiry'].replace('/', ''))
                driver.send_keys(phonecode_xpath, client_details['Ph. Code'])
                driver.send_keys(phonenum_xpath, client_details['Phone'])
                driver.send_keys(email_xpath, client_details['Email'])
                driver.send_keys(gender_xpath, client_details['Gender'])
                driver.send_keys(nationality_xpath, client_details['Nationality'])

                driver.sleep(1)
                driver.click(savebtn_xpath)
                print("Clicking the Save Button and now wait for 20 seconds")
                driver.sleep(20)

                try:
                    driver.assert_element_present(invaliddetails_xpath, timeout = 4)
                    print("Invalid Details")
                    messagebox.showerror("BOT ERROR",'Please enter the valid Applicant Details')
                    return False

                except:
                    print("All details are valid!")

                if driver.is_element_present(savebtn_xpath):
                    print("Save button still presents, Trying clicking again!")
                    driver.click(savebtn_xpath)
                    driver.sleep(2)

                if driver.is_element_present(savebtn_xpath):
                    print("Save button still presents, Trying clicking again second time!")
                    driver.click(savebtn_xpath)
                # -------------------- YOUR DETAILS SECTION ENDED!! : 3 --------------------

                # -------------------- BOOK APPOINTMENT SECTION STARTED!! : 4 --------------------
                WaitForLoadingToComplete(driver)
                driver.wait_for_element_clickable(continuebtn_xpath)
                if driver.is_element_clickable(continuebtn_xpath):
                    driver.click(continuebtn_xpath)
                    print("Now clicking the Continue Button!")
                    WaitForLoadingToComplete(driver)

                    try:
                        driver.assert_element_present(firstbookingdate_xpath)
                        print("Dates Available!")

                    except:
                        print("Unable to reach to Book Appointment Section")
                        messagebox.showerror("BOT ERROR",'Unable to Book the dates/time due to unexpected Error!')
                        return False

                    driver.click(firstbookingdate_xpath)
                    print("Now clicking the First Available booking date")
                    WaitForLoadingToComplete(driver)

                    driver.click(firstbookingtime_xpath)
                    print("Now clicking the First Available booking time")
                    WaitForLoadingToComplete(driver)

                    driver.wait_for_element_clickable(continuebtn_xpath)
                    driver.click(continuebtn_xpath)
                    print("Now clicking the Continue Button")
                    WaitForLoadingToComplete(driver)
                    # -------------------- BOOK APPOINTMENT SECTION ENDED!! : 4 --------------------

                    # -------------------- REVIEW SECTION STARTED!! : 5 --------------------

                    try:
                        driver.assert_element_present(acceptterms_xpath)
                        print("Reached at Review Section")

                    except:
                        print('Unable to move to the REVIEW section due to unexpected Error!')
                        messagebox.showerror("BOT ERROR",'Unable to move to the REVIEW section due to unexpected Error!')

                    driver.click(acceptterms_xpath)
                    print("Now clicking the Accept Terms Checkbox")
                    driver.sleep(1)


                    driver.click(confirmbtn_xpath)
                    print("Now clicking the Confirm Button")
                    driver.wait_for_ready_state_complete()
                    driver.sleep(3)

                    thankyou_xpath = "//h2[contains(text(),' Thank you for booking an appointment with us!')]"
                    try:
                        driver.assert_element_present(thankyou_xpath)
                        client_details["Status"] = "Booked"
                        Update_Single_Client_Field(client_details)
                        messagebox.showinfo("BOOKING SUCCESS",'Appointment Booked')
                    except:
                        print("Unable to book the appointment due to some error after Submission!")
                        messagebox.showerror("BOT ERROR","Unable to book the appointment due to some error after Submission!")

                    print("BOT PROCESS COMPLETED!!!")
                    # -------------------- REVIEW SECTION ENDED!! : 5 --------------------

            except:
                print("Unable to move to the Applicant Window")
                messagebox.showerror("BOT ERROR",'Did not find the "Applicant" Window or something is wrong while filling the fields, Session closed!')
                return False

        except:
            # If No booking available, Warning message will be given
            print("Getting alert text")
            message = str(driver.get_text(nobookings_xpath)).strip()
            messagebox.showwarning("No Booking", message)
            return False

    except Exception as error:
        print(f"Error in Booking Appointment due to -> '{error}' ")
        messagebox.showerror("BOT ERROR",'Error in Booking Appointment due to Unexpected Error!')
