Feature: Current Cost data collection
    As a end-user,
    I want to see my current cost information about my consumption,
    in order to reduce my energy consumption

    @wipa
    Scenario Outline: 1.Problem with current cost connexion
        Given I created a testing Site 'test_site'
        When I run the 'currentcost' script with '<setting_type>' settings
        Then I should see an error message '<setting_type>' in the 'currentcost' log
        And I should see an error message '<setting_type>' on the screen
        And I should see an error message '<setting_type>' on 'error' TSV file

    Examples: 1.Problem with current cost connexion
   | setting_type                                | 
   | currentcost_bad_port                        |
   | currentcost_no_message                      |
   | currentcost_disconnected                    |
   | currentcost_incorrect_message               |
   | currentcost_incorrect_message_missing_tmpr  |
   | currentcost_incorrect_message_missing_watts |

    @wipa
    Scenario: 2.Nominal case instant_consumption_1_timeseries_0
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_0' settings
        Then I should see an error message 'instant_consumption_1_timeseries_0' in the 'currentcost' log
        And I should see 'instant_consumption_1_timeseries_0' data update in DB for 'test_site'
        And I should see 'instant_consumption_1_timeseries_0' data update in TSV file for 'test_site'

    @wipa
    Scenario: 3.Nominal case instant_consumption_2_timeseries_7
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_0' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_7' settings
        Then I should see an error message 'instant_consumption_2_timeseries_7' in the 'currentcost' log
        And I should see 'instant_consumption_2_timeseries_7' data update in DB for 'test_site'
        And I should see 'instant_consumption_2_timeseries_7' data update in TSV file for 'test_site'

    @wipa
    Scenario: 4.Nominal case instant_consumption_1_timeseries_3
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_0' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_7' settings
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_3' settings
        Then I should see an error message 'instant_consumption_1_timeseries_3' in the 'currentcost' log
        And I should see 'instant_consumption_1_timeseries_3' data update in DB for 'test_site'
        And I should see 'instant_consumption_1_timeseries_3' data update in TSV file for 'test_site'

    @wipa
    Scenario: 5.Nominal case instant_consumption_2_timeseries_3
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_0' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_7' settings
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_3' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_3' settings
        Then I should see an error message 'instant_consumption_2_timeseries_3' in the 'currentcost' log
        And I should see 'instant_consumption_2_timeseries_3' data update in DB for 'test_site'
        And I should see 'instant_consumption_2_timeseries_3' data update in TSV file for 'test_site'


    @wipa
    Scenario: 6.Nominal case instant_consumption_2_timeseries_0
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_0' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_7' settings
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_3' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_3' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_0' settings
        Then I should see an error message 'instant_consumption_2_timeseries_0' in the 'currentcost' log
        And I should see 'instant_consumption_2_timeseries_0' data update in DB for 'test_site'
        And I should see 'instant_consumption_2_timeseries_0' data update in TSV file for 'test_site'

    @wipa
    Scenario: 7.Nominal case instant_consumption_3_timeseries_3
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_0' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_7' settings
        When I run the 'currentcost' script with 'instant_consumption_1_timeseries_3' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_3' settings
        When I run the 'currentcost' script with 'instant_consumption_2_timeseries_0' settings
        When I run the 'currentcost' script with 'instant_consumption_3_timeseries_3' settings
        Then I should see an error message 'instant_consumption_3_timeseries_3' in the 'currentcost' log
        And I should see 'instant_consumption_3_timeseries_3' data update in DB for 'test_site'
        And I should see 'instant_consumption_3_timeseries_3' data update in TSV file for 'test_site'

    @wipa
    Scenario: 8.Historical case consumption
        Given I created a testing Site 'test_site'  
        When I run the 'currentcost' script with 'currentcost_historical_consumption' settings
        Then I should see an error message 'currentcost_historical_consumption' in the 'currentcost' log
