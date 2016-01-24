Feature: Current Cost data collection
    As a end-user,
    I want to see my current cost information about my consumption,
    in order to reduce my energy consumption

    @wip
    Scenario Outline: 1.No settings
        Given I created according settings for 'currentcost' to test '<error_type>'
        When I run the 'currentcost' script
        Then I should see an error message '<error_type>' in the 'currentcost' log
        And I should see an error message '<error_type>' on the screen

    Examples: 1.No settings
   | error_type                  | 
   | currentcost_no_site_id      |
   | currentcost_no_variable_id  |

    @wipa
    Scenario: 2.Problem with current cost connexion with RabbitMQ activated
        When we start currentcost with bad port with rabbitmq
        Then we should receive a message saying that current cost is unreachable
        And we should see currentcost is unreachable in log

    @wipa
    Scenario: 3.Current cost disconnected
        Given current cost does not send any message
        When we launch currentcost script and reach the timeout limit
        Then we should get informed that current cost does not send messages
        And we should see current cost does not send any message in log

    @wipa
    Scenario: 4.Problem with USB port
        Given current cost is connected and currentcost script is launched
        When we disconnect USB port
        Then we should receive a message saying that current cost is disconnected
        And we should see currentcost is disconnected in log

    @wipa
    Scenario: 5.Problem with current cost message
        Given current cost is connected and script is launched
        When current cost send incorrect message
        Then we should get informed that current cost send incorrect message
        And we should see incorrect message error in log

    @wipa
    Scenario: 6.Nominal case instant consumption
        Given current cost is connected and script is launched
        When current cost send instant consumption
        Then we should receive instant consumption and 0 ts over the network

    @wipa
    Scenario: 7.Nominal case instant consumption with 7 timeseries
        Given current cost is connected and script is launched with 7 params
        When current cost send instant consumption 2
        Then we should receive instant consumption 2 and 7 ts over the network

    @wipa
    Scenario: 8.Nominal case instant consumption with 3 timeseries
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption
        Then we should receive instant consumption and 3 ts over the network

    @wipa
    Scenario: 9.Nominal case instant consumption with 3 timeseries 2
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption 2
        Then we should receive instant consumption 2 and 3 ts over the network

    @wipa
    Scenario: 10.Nominal case instant consumption with 3 timeseries 3
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption 2
        Then we should receive instant consumption 2 and 0 ts over the network

    @wipa
    Scenario: 11.Nominal case instant consumption with 3 timeseries 4 not sudo
        Given current cost is connected and script is launched with 3 params
        When current cost send instant consumption 3
        Then we should receive instant consumption 3 and 3 ts over the network

    @wipa
    Scenario: 12.Error case incorrect tmpr instant consumption
        Given current cost is connected and script is launched
        When current cost send incorrect tmpr instant consumption
        Then we should receive an tmpr error and 0 ts on RabbitMQ

    @wipa
    Scenario: 13.Error case incorrect watts instant consumption
        Given current cost is connected and script is launched
        When current cost send incorrect watts instant consumption
        Then we should receive an watts error and 0 ts on RabbitMQ
