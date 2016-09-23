Feature: Backup command
    As a end-user,
    I want to backup my data,
    in order to save data

    @wip
    Scenario: 1.No backup
        Given I have data to backup
        And I deactivate backup script
        When I run the backup command
        Then nothing should be backuped
        And I should see an error message 'error_backup_deactivated' in the 'timevortex' log

    @wip
    Scenario: 2.Backup
        Given I have data to backup
        When I run the backup command
        Then I should see backuped data

    @wip
    Scenario: 3.Backup more data
        Given I add more data
        When I run the backup command
        Then I should see new backuped data
