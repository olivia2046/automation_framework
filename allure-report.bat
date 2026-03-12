rem Used after test execution to generate single file allure report with history trend
xcopy testreport\allure-report\history testreport\allure-results\history /E /I /Y
rem start allure generate testreport\allure-results --clean -o testreport\allure-report
rem start cmd /k allure serve testreport\allure-results
start allure generate --single-file testreport\allure-results --clean -o testreport\allure-report

