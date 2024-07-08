Feature: There are several tables which will be requiring few set of sanity checks on it.
  1. Count validation
  2. PK matching validation
  3. Duplicated PK validation
  4. Data in each Column validation based on PK joins
  5. Mandatory fields validation - all FK columns are neither empty or null
  6. PK/FK relationship validation

  @db_sanity
  Scenario Outline: Performing sanity tests on table <schema>.<table>
    Given Schema <schema> name
    And   Table <table> name
    When  I query all records of table
    And   I insert 3 entry into the table
    And   I query all records of the table after insertion
    Then  I verify record count matched
    When  I query duplicate records in table
    Then  I verify no duplicates found in table
    And   I verify content of the table matched
    And   I verify none of the mandatory columns holding either empty or null
    And   I verify no foreign key reference issue exists
    Examples:
    |schema|table|
    | sakila | payment |
#    | sakila | address |
#    | sakila | city |
