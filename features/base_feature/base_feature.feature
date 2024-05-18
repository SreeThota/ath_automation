Feature: As a admin user, I do have an option to add a new user

  Scenario: Verify admin can add another user with admin permissions
    Given I am on login page
    """
    This is the text to read in spec file
    """
    When  I logged in application as admin
    """
    This is for when case
    """
    And  I map a table here
      |name|desc|
      |Sreeni|Senior QA|
      |Bharathi|Junior QA|