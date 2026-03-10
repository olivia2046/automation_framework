xcopy testreport\allure-report\history testreport\allure-results\history /E /I /Y
start allure generate testreport\allure-results --clean -o testreport\allure-report
start cmd /k allure serve testreport\allure-results
