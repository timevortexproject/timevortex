Feature: Current Cost data collection
    As a end-user,
    I want to see my current cost information about my consumption,
    in order to reduce my energy consumption

    @wip
    Scenario Outline: 1.Problem with current cost connexion
        When I run the 'currentcost' script with '<setting_type>' settings
        Then I should see an error message '<setting_type>' in the 'currentcost' log
        And I should see an error message '<setting_type>' on the screen

    Examples: 1.Problem with current cost connexion
   | setting_type                  | 
   | currentcost_bad_port          |
   | currentcost_no_message        |
   | currentcost_disconnected      |
   | currentcost_incorrect_message |

    @wipa
    Scenario Outline: 2.Nominal case instant consumption       
        When I run the 'currentcost' script with '<setting_type>' settings
        Then I should see '<setting_type>' data update in DB for 'test_site'
        And I should see '<setting_type>' data update in TSV file for 'test_site'

    Examples: 2.Nominal case instant consumption
   | setting_type                       | 
   | incorrect_tmpr_timeseries_0        |
   | incorrect_watts_timeseries_7       |
   | instant_consumption_1_timeseries_0 |
   | instant_consumption_2_timeseries_7 |
   | instant_consumption_1_timeseries_3 |
   | instant_consumption_2_timeseries_3 |
   | instant_consumption_2_timeseries_0 |
   | instant_consumption_3_timeseries_3 |

    @wipa
    Scenario: 2.Problem with USB port
        Given current cost is connected and currentcost script is launched
        When we disconnect USB port
        Then we should receive a message saying that current cost is disconnected
        And we should see currentcost is disconnected in log

    @wipa
    Scenario: 3.Problem with current cost message
        Given current cost is connected and script is launched
        When current cost send incorrect message
        Then we should get informed that current cost send incorrect message
        And we should see incorrect message error in log

    @wipa
    Scenario: 2.Nominal case instant consumption
        Given current cost is connected and script is launched
        When current cost send instant consumption
        Then we should receive instant consumption and 0 ts over the network

    @wipa
    Scenario: 5.Nominal case instant consumption with 7 timeseries
        Given current cost is connected and script is launched with 7 params
        When current cost send instant consumption 2
        Then we should receive instant consumption 2 and 7 ts over the network

    @wipa
    Scenario: 6.Nominal case instant consumption with 3 timeseries
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption
        Then we should receive instant consumption and 3 ts over the network

    @wipa
    Scenario: 7.Nominal case instant consumption with 3 timeseries 2
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption 2
        Then we should receive instant consumption 2 and 3 ts over the network

    @wipa
    Scenario: 8.Nominal case instant consumption with 3 timeseries 3
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption 2
        Then we should receive instant consumption 2 and 0 ts over the network

    @wipa
    Scenario: 9.Nominal case instant consumption with 3 timeseries 4 not sudo
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption 3
        Then we should receive instant consumption 3 and 3 ts over the network

    @wipa
    Scenario: 10.Error case incorrect tmpr instant consumption
        Given current cost is connected and script is launched
        When current cost send incorrect tmpr instant consumption
        Then we should receive an tmpr error and 0 ts on RabbitMQ

    @wipa
    Scenario: 11.Error case incorrect watts instant consumption
        Given current cost is connected and script is launched
        When current cost send incorrect watts instant consumption
        Then we should receive an watts error and 0 ts on RabbitMQ
