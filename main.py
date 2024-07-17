from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


# Set up the webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the webpage
    driver.get('https://hprera.nic.in/PublicDashboard')

    # Wait for the dynamic content to load
    # wait for 20 seconds
    wait = WebDriverWait(driver, 20)

    # Locate the div(Regestered Projects) and iterate inside every elements
    div_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#reg-Projects.tab-pane.fade.show.active")))
    next_1=div_content.find_element(By.CSS_SELECTOR, "div.px-2.pt-2" )
    next_2=next_1.find_element(By.CSS_SELECTOR, "div.form-row")
    next_3=next_2.find_elements(By.CSS_SELECTOR, "div.col-lg-6")

    # As the details of every element varies from row to row 
    #defining the indices to extract details 
    row_indices = [
        {'gstin_no': 12, 'pan_no': 5, 'name': 0, 'permanent_address': 11},
        {'gstin_no': 12, 'pan_no': 5, 'name': 0, 'permanent_address': 11},
        {'gstin_no': 12, 'pan_no': 5, 'name': 0, 'permanent_address': 11},
        {'gstin_no': 6, 'pan_no': 5, 'name': 0, 'permanent_address': 12},
        {'gstin_no': 6, 'pan_no': 5, 'name': 0, 'permanent_address': 12},
        {'gstin_no': 6, 'pan_no': 6, 'name': 0, 'permanent_address': 13}
    ]

    #Iteration for first 6 registered projects
    #Including Opening and closing Form 
    for index, col_div in enumerate(next_3[:6]):
        print(f"Registered Project: {index + 1}...")
        a_tag=col_div.find_element(By.TAG_NAME,"a")
        a_tag.click()

        #thread to iterate till the required content by opening the form 

        table = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.modal-content"))
        )

        t_1=table.find_element(By.CSS_SELECTOR,"div#modal-data-display-tab_project_main-content.modal-body.py-0")
        t_2=t_1.find_element(By.CSS_SELECTOR,"div.row.min-vh-50")
        t_3=t_2.find_element(By.CSS_SELECTOR,"div.col-lg-9.bg-white")
        t_4=t_3.find_element(By.CSS_SELECTOR,"div.row.min-vh-50")
        t_5=t_4.find_element(By.CSS_SELECTOR,"div#project-menu-html.col-12")
        t_6=t_5.find_element(By.CSS_SELECTOR,"div.row.mb-3")
        t_7=t_6.find_element(By.CSS_SELECTOR,"div.col-12")
        t_8=t_7.find_element(By.CSS_SELECTOR,"div.mb-2")
        t_9=t_8.find_element(By.CSS_SELECTOR,"table.table.table-borderless.table-sm.table-responsive-lg.table-striped.font-sm")
        tbody=t_9.find_element(By.CSS_SELECTOR,"tbody.lh-2")
        t_rows=tbody.find_elements(By.CSS_SELECTOR,"tr")

        #function to extract the details from <td> as the 2nd <tr> contains the required details  
        def extract_values(t_rows:list[WebElement] , row_index:int , class_name:str)->str:
            tr=t_rows[row_index]
            tds=tr.find_elements(By.TAG_NAME,"td")
            if len(tds)>1:
                value_span=tds[1].find_element(By.CLASS_NAME,class_name)
                return value_span.text
            return None
        
        indices=row_indices[index]

        gstin_no=extract_values(t_rows,row_index=indices['gstin_no'], class_name='mr-1 fw-600')
        pan_no = extract_values(t_rows, row_index=indices['pan_no'], class_name='mr-1 fw-600') 
        name = extract_values(t_rows, row_index=indices['name'], class_name='fw-600')      
        permanent_address = extract_values(t_rows, row_index=indices['permanent_address'], class_name='fw-600') 

        print(f"GSTIN-No: {gstin_no}")
        print(f"PAN No: {pan_no}")
        print(f"Name: {name}")
        print(f"Permanent Address: {permanent_address}")

        #Closing the opened Form  

        c_1 = table.find_element(By.CSS_SELECTOR, "div.modal-header")
        close_button = c_1.find_element(By.CSS_SELECTOR, "button.close")
        close_button.click()
        

finally:
    # Close the driver
    driver.quit()
