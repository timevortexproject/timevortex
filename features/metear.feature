Feature: Retrieve METEAR data
    As a end-user,
    I want to collect my weather information,
    in order to compare it with my other data

    @wipa
    Scenario: 1.No site_id
        When I run the 'metear' script with 'correct' settings
        Then I should see an error message 'metear_no_site_id' in the 'weather' log
        And I should see an error message 'metear_no_site_id' on the screen

    @wipa
    Scenario: 2.Bad url
        Given I created a testing Site 'LFMN'
        And I add a bad metear url in settings
        When I run the 'metear' script with 'correct' settings
        Then I should see an error message 'metear_bad_url' in the 'weather' log
        And I should see an error message 'metear_bad_url' on the screen
        And I should see an error message 'metear_bad_url' on 'error' TSV file

    @wipa
    Scenario: 3.Web service down
        Given I created a testing Site 'LFMN'
        And I shutdown the metear web service
        When I run the 'metear' script with 'correct' settings
        Then I should see an error message 'metear_problem_ws' in the 'weather' log
        And I should see an error message 'metear_problem_ws' on the screen
        And I should see an error message 'metear_problem_ws' on 'error' TSV file

    @wipa
    Scenario: 4.Bad content
        Given I created a testing Site 'LFMN'
        And I configure metear web service to generate bad content
        When I run the 'metear' script with 'correct' settings
        Then I should see an error message 'metear_bad_content' in the 'weather' log
        And I should see an error message 'metear_bad_content' on the screen
        And I should see an error message 'metear_bad_content' on 'error' TSV file

    @wip
    Scenario: 5.Retrieve historical data
        Given I created a testing Site 'LFMN'
        When I run the 'metear' script with 'correct' settings
        Then I should see 'historical' data update in DB for 'LFMN'
        And I should see 'historical' data update in TSV file for 'LFMN'

    @wip
    Scenario: 6.Retrieve new data
        Given I created a testing Site 'LFMN'
        And I run for the first time the metear script
        And new data are available
        When I run the 'metear' script with 'correct' settings
        Then I should see 'new' data update in DB for 'LFMN'
        And I should see 'new' data update in TSV file for 'LFMN'

    @wip
    Scenario: 7.Retrieve other airport data
        Given I created a testing Site 'LFBP'
        When I run the 'metear' script with 'correct' settings
        Then I should see 'historical' data update in DB for 'LFBP'
        And I should see 'historical' data update in TSV file for 'LFBP'
