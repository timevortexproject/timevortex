Feature: Time series data logging
    As a end-user,
    I want to store all time series providing by my sensor,
    in order to uniformize input of more complex module.

    @wipa
    Scenario: 1.Send message without TS
        When I send JSON message 'ts_without_json_message'
        Then I should see an error message 'ts_without_json_message' in the 'default' log

    @wipa
    Scenario Outline: 2.Bad JSON message
        When I send JSON message '<error_type>'
        Then I should see an error message '<error_type>' in the 'default' log
        And I should see an error message '<error_type>' on 'system' TSV file        

    Examples: 2.Bad JSON message
   | error_type                  | 
   | ts_without_site_id          |
   | ts_without_variable_id      |
   | ts_without_message          |
   | ts_without_date             |
   | ts_without_dst_timezone     |
   | ts_without_non_dst_timezone |  

    @wipa
    Scenario Outline: 3.Correct message
        When I send JSON message '<message>'
        Then I should see '<message>' data update in TSV file for 'TEST_site'

    Examples: 3.Correct message
   | message               | 
   | ts_error_message      |
   | ts_first_watts        |
   | ts_first_kwh          |
   | ts_first_temperature  |
   | ts_second_watts       |
   | ts_second_kwh         |
   | ts_second_temperature |
