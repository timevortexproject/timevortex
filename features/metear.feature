Feature: Retrieve METEAR data
    As a end-user,
    I want to collect my weather information,
    in order to compare it with my other data

    @testing
    Scenario: 1.No site_id
        When I run the metear script
        Then I should see an error message 'metear_no_site_id' in the log
        And I should see an error message 'metear_no_site_id' on the screen
        And I should see an error message 'metear_no_site_id' on system TSV file

    @testing
    Scenario: 2.Bad url
        Given I created a testing Site
        And I add a bad metear url in settings
        When I run the metear script
        Then I should see an error message 'metear_bad_url' in the log
        And I should see an error message 'metear_bad_url' on the screen
        And I should an error message 'metear_no_site_id' on error TSV file

    @testing
    Scenario: 3.Web service down
        Given I created a testing Site
        And I shutdown the metear web service
        When I run the metear script
        Then I should see an error message 'metear_problem_ws' in the log
        And I should see an error message 'metear_problem_ws' on the screen
        And I should an error message 'metear_no_site_id' on error TSV file

    Scenario: 4.Bad content
        Given I created a testing Site
        And I configure metear web service to generate a bad content
        When I run the metear script
        Then I should see an error message 'metear_bad_content' in the log
        And I should see an error message 'metear_bad_content' on the screen
        And I should an error message 'metear_no_site_id' on error TSV file

    Scenario: 5.Retrieve historical data
        Given I created a testing Site
        When I run the metear script
        Then I should see data update on RBMQ (or signal) and in DB and in TSV files

    Scenario: 6.Retrieve other airport data
        Given I created a second testing Site
        When I run the metear script
        Then I should see data update on RBMQ (or signal) and in DB and in TSV files
